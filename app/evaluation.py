from typing import Any, TypedDict
import os
import subprocess
try:
    from .format import message_format
    from .dynamic_import import module_import
except ImportError:
    # run it on the local machine
    from format import message_format


class Params(TypedDict):
    is_unique_answer: bool
    is_multiple_answers: bool
    is_ai_feedback: bool
    has_output: bool


class Result(TypedDict):
    is_correct: bool
    feedback: str


def evaluation_function(response: Any, answer: Any, params: Params) -> Result:
    """
    Function used to evaluate a student response.
    ---
    The handler function passes three arguments to evaluation_function():
    - `response` which are the answers provided by the student.
    - `answer` which are the correct answers to compare against.
    - `params` which are any extra parameters that may be useful,
        e.g., error tolerances.
    The output of this function is what is returned as the API response
    and therefore must be JSON-encodable. It must also conform to the
    response schema.
    Any standard python library may be used, as well as any package
    available on pip (provided it is added to requirements.txt).
    The way you wish to structure you code (all in this function, or
    split into many) is entirely up to you. All that matters are the
    return types and that evaluation_function() is the main function used
    to output the evaluation response.
    """
    general_feedback = general_check(response)
    if general_feedback != "General check passed!":
        return Result(is_correct=False, feedback=general_feedback)
    if params['has_output'] and params['is_unique_answer']:
        if not check_answer_with_output(response, answer):
            return Result(is_correct=False, feedback=general_feedback)
        return Result(is_correct=True, feedback=general_feedback)


def check_indents(code_string: str) -> bool:
    """
    This function checks the indentation correctness of the given Python code.
    Notice that indentation depends on student preference: (2 spaces or 4 spaces are acceptable)
    :param code_string: str, the Python code to be checked.
    :return: bool, True if the indentation is correct, otherwise False.
    """
    indent_levels = []
    lines = code_string.strip().split('\n')
    for line in lines:
        indent_level = len(line) - len(line.lstrip(' '))
        indent_levels.append(indent_level)

    # first line should not have any indents
    if indent_levels[0] != 0:
        return False

    # find the correctness indent: 2 or 4 spaces
    indent_difference = 0
    for indent_level in indent_levels:
        if indent_level > 0:
            indent_difference = indent_level
            break

    # zero indent only occur when they are no any syntax like (if, for)
    if indent_difference == 0:
        return all(indent_level == 0 for indent_level in indent_levels)

    # correct indents
    if indent_difference != 2 and indent_difference != 4:
        return False

    return all(indent_level % indent_difference == 0 for indent_level in indent_levels)


def general_check(code_string) -> str:
    if not check_indents(code_string):
        return f"Indent error, the indent should only be multiple of 2 or 4"
    # import necessary modules dynamically
    module_import(code_string)
    is_syntax_correct, msg = check_syntax(code_string)
    if not is_syntax_correct:
        return f"Error occurs, please check the details below: <br>{message_format(msg)}"

    return "General check passed!"


def check_syntax(code_string):
    try:
        result = subprocess.run(['python', '-c', code_string], capture_output=True)
        if result.returncode != 0:
            try:
                stderr = result.stderr.decode('utf-8')
            except UnicodeDecodeError:
                stderr = result.stderr.decode('utf-8', errors='replace')
            return False, f"Error: {stderr}"
        else:
            return True, result.stdout.decode('utf-8')
    except Exception as e:
        return False, f"Exception occurred: {str(e)}"


def check_answer_with_output(response, answer):
    """
    The function is called iff the answer is unique. i.e. aList = [1,2,3,4,5] is the unique answer
    Notice that styles (at least they can pass general check) are NOT sensitive
    """
    try:
        res_result = subprocess.run(['python', '-c', response], capture_output=True, text=True)
        if res_result.returncode != 0:
            res_feedback = f"Error: {res_result.stderr.strip()}"
        else:
            res_feedback = res_result.stdout.strip()
    except Exception as e:
        res_feedback = f"Exception occurred: {str(e)}"
    try:
        ans_result = subprocess.run(['python', '-c', answer], capture_output=True, text=True)
        if ans_result.returncode != 0:
            ans_feedback = f"Error: {ans_result.stderr.strip()}"
        else:
            ans_feedback = ans_result.stdout.strip()
    except Exception as e:
        ans_feedback = f"Exception occurred: {str(e)}"

    return res_feedback == ans_feedback


def check_each_letter(response, answer):
    """
    The function is called iff the answer and the response are unique. i.e. aList = [1,2,3,4,5] is the unique answer and response
    Notice that styles (at least they can pass general check) are NOT sensitive
    """
    return answer.replace(" ", "").replace("\t", "").replace("\n", "") == response.replace(" ", "").replace("\t",
                                                                                                            "").replace(
        "\n", "")


