import subprocess
import sys
import json
import os
#import pyseccomp as seccomp
from pathlib import Path
import random

from .general_check import check_style, validate_answer
from .func_check import check_func
from .structure_check import check_structure
from .output_check import check_answer_with_output
from .global_variable_check import check_global_variable_content
from .check_result import CheckResult
from ..format.output_traceback_format import output_diffs
from ..format.general_format import markdown_format

def run_checks(response: str, answer: str, params: dict, sandbox: bool = True) -> CheckResult:
    if sandbox:
        # Set up the sandbox, and run this script in a new process
        # First create a new process that can then be isolated
        proc = subprocess.Popen(
            [sys.executable, "-m", "evaluation_function.checks.run_checks"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True,
        )

        # Send the response and answer code over stdin
        proc.communicate(json.dumps({
            "response": response,
            "answer": answer,
            "params": params,
        }))

        # The process will return zero if successful
        exit_code = proc.wait()
        if exit_code == 0:
            # A JSON object should have been written to stdout
            result = json.loads(proc.communicate()[0])
            return (
                CheckResult(result["is_correct"])
                .add_message(result["message"])
                .add_payload("ai", result["ai"])
            )
        else:
            # If sandbox.py exited prematurely, return stderr
            return CheckResult(False).add_message(proc.communicate())
    else:
        # Run the checks in this process.
        # SHOULD ONLY BE USED FOR TESTING!!!
        return run_checks_internal(response, answer, params)

def restrict_process():
    # Change the root directory to isolate the filesystem
    # This directory is empty, so no commands can be used by this process.
    # Might not be necessary with seccomp removing access to any file other
    # than stdout, stderr and stdin, but let's do it anyway

    print(f"euid: {os.geteuid()}", file=sys.stderr)

    Path("/tmp/py_chroot").mkdir(exist_ok=True)
    os.chroot("/tmp/py_chroot")
    os.chdir("/")

    # Clear the environment variables
    os.environ.clear()

    # Remove any privileges this process has by changing the group to nogroup
    # This should prevent malicious code from using "sudo" etc. even if they break
    # out of the chroot jail.
    os.setgid(65534)
    # Set the user to nobody
    os.setuid(65534)

    # Uses seccomp to restrict access to potentially harmful syscalls
    #filter = seccomp.SyscallFilter(seccomp.ERRNO(seccomp.errno.EPERM))
    # Allow writing to stdout and stderr
    #filter.add_rule(seccomp.ALLOW, "write", seccomp.Arg(0, seccomp.EQ, sys.stdout.fileno()))
    #filter.add_rule(seccomp.ALLOW, "write", seccomp.Arg(0, seccomp.EQ, sys.stderr.fileno()))
    # Allow seeking
    #filter.add_rule(seccomp.ALLOW, "lseek")
    # Allow reading from stdout
    #filter.add_rule(seccomp.ALLOW, "read", seccomp.Arg(0, seccomp.EQ, sys.stdin.fileno()))
    # Allow the process to exit cleanly
    #filter.add_rule(seccomp.ALLOW, "exit")
    # Allow allocation of additional memory
    #filter.add_rule(seccomp.ALLOW, "brk")

    # Load the filters
    #filter.load()

def run_checks_internal(response: str, answer: str, params: dict) -> CheckResult:
    # Ensure that the answer is valid
    # The result includes the answer's stdout as a payload, and its parsed AST
    answer_feedback = validate_answer(answer)
    if not answer_feedback.passed():
        return answer_feedback
    answer_ast = answer_feedback.get_payload("ast", None)
    correct_output = answer_feedback.get_payload("correct_output", None)

    # Check the student response's code style, and return an incorrect response if 
    # any egregious mistakes were made.
    # The result returned includes the AST as a payload, so it can be reused later.
    general_feedback = check_style(response)
    if not general_feedback.passed():
        return general_feedback
    response_ast = general_feedback.get_payload("ast", None)

    # If a function test is desired, run tests to ensure that a particular function returns the 
    # correct values
    check_func_name = params.get('check_func', None)
    if check_func_name:
        return check_func(response_ast, answer_ast, check_func_name)
    
    # Analyse the structure of the response, and ensure that it has the same function/class
    # heirarchy as the correct answer.
    structure_feedback = check_structure(
        response_ast,
        answer_ast,
        check_names=params.get('check_names', False)
    )
    if not structure_feedback.passed():
        return structure_feedback

    # Did the answer print anything to stdout?
    # Check that first if it did
    if correct_output:
        is_output_inexact = params.get('output_inexact', True)
        is_correct, res_msg = check_answer_with_output(response, correct_output, is_output_inexact)
        if not is_correct:
            error_feedback = "The output is different to given answer: \n"

            diff = output_diffs(res_msg, correct_output)
            return CheckResult(False).add_message(markdown_format(error_feedback + diff))
        else:
            return CheckResult(True)
    elif check_each_letter(response, answer):
        return CheckResult(True)

    # Check global variables if a check list was given
    check_list = params.get('global_variable_check_list', {})
    if check_list != {}:
        if isinstance(check_list, str):
            # check list is a set as repeated variable names are not meaningful
            check_list = {var.strip() for var in check_list.split(',') if len(var.strip()) > 0}
        else:
            check_list = set(check_list)

        check_result = check_global_variable_content(response_ast, answer_ast, check_list)
        if not check_result.passed():
            return CheckResult(False).add_message(markdown_format(check_result.message()))
        else:
            return CheckResult(True)
    
    # If none of the tests were run, return an indeterminate result and defer to AI
    return CheckResult(False).add_payload("ai", True)

def check_each_letter(response, answer):
    """
    The function is called iff the answer and the response are unique. i.e. aList = [1,2,3,4,5] is the unique answer and response
    Notice that styles (at least they can pass general check) are NOT sensitive
    """
    return answer.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "") == response.replace(
        " ", "").replace("\t", "").replace("\n", "").replace("\r", "")

if __name__ == "__main__":
    # Isolate this process
    restrict_process()

    # Get the input from stdin
    params_str = sys.stdin.read()
    sys.stdout.flush()
    params = json.loads(params_str)

    result = run_checks_internal(params["response"], params["answer"], params["params"])
    ai = result.get_payload("ai", False)
    sys.stdout.flush()
    print(json.dumps({"is_correct": result.passed(), "message": result.message(), "ai": ai}))
