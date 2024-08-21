import random
from typing import Any, TypedDict

from .format.output_traceback_format import output_diffs
from .format.variable_compare_format import variables_content_compare
from .format.general_format import ai_content_format, markdown_format
from .checks.ai_prompt_check import ai_check
from .checks.global_variable_check import check_global_variable_content, get_err_vars, variable_content
from .checks.local_variable_check import check_local_variable_content, extract_modules
from .checks.general_check import check_style, validate_answer
from .checks.structure_check import check_structure
import subprocess


class Params(TypedDict):
    # TODO it will be list after the website updates
    check_list: Any
    check_names: bool


class Result(TypedDict):
    is_correct: bool
    feedback: str


def evaluation_function(response: Any, answer: Any, params: Params) -> Result:
    check_list = params.get('check_list', [])
    if isinstance(check_list, str):
        check_list = [var.strip() for var in check_list.split(',') if len(var.strip()) > 0]
        
    check_list_defined = len(check_list) != 0
    
    correct_feedback = random.choice(["Good Job!", "Well Done!", "Awesome"])

    # Ensure that the answer is valid
    # The result includes the answer's stdout as a payload, and its parsed AST
    answer_feedback = validate_answer(answer)
    if not answer_feedback.passed():
        return Result(is_correct=False, feedback=answer_feedback.message())
    answer_ast = answer_feedback.get_payload("ast", None)
    correct_output = answer_feedback.get_payload("correct_output", None)

    # Check the student response's code style, and return an incorrect response if 
    # any egregious mistakes were made.
    # The result returned includes the AST as a payload, so it can be reused later.
    general_feedback = check_style(response)
    if not general_feedback.passed():
        return Result(is_correct=False, feedback=general_feedback.message())
    response_ast = general_feedback.get_payload("ast", None)
    
    # Analyse the structure of the response, and ensure that it has the same function/class
    # heirarchy as the correct answer.
    structure_feedback = check_structure(
        response_ast,
        answer_ast,
        check_names=params.get('check_names', False)
    )
    if not structure_feedback.passed():
        return Result(is_correct=False, feedback=structure_feedback.message())

    # Did the answer print anything to stdout?
    if correct_output:
        is_correct, res_msg = check_answer_with_output(response, correct_output)
        if not is_correct and not check_list_defined:
            # if check_list != 0, it means that output is not the importance
            error_feedback = "The output is different to given answer: \n"
            diff = output_diffs(res_msg, correct_output)
            return Result(is_correct=False, feedback=markdown_format(error_feedback + diff))
        else:
            return Result(is_correct=True, feedback=correct_feedback)
    elif check_each_letter(response, answer):
            return Result(is_correct=True, feedback=correct_feedback)

    # if the checklist is not given, it is meaningless to check the variables, then we will call for AI
    if check_list_defined:
        is_correct, feedback, remaining_check_list, response = check_global_variable_content(response, answer,
                                                                                             check_list)
        if not is_correct:
            variable_list = get_err_vars()
            _, res_var_dict = extract_modules(variable_content(response))
            _, ans_var_dict = extract_modules(variable_content(answer))
            diff = variables_content_compare(variable_list, res_var_dict, ans_var_dict)
            return Result(is_correct=False, feedback=markdown_format(f"{feedback}\n{diff}"))
        else:
            if len(remaining_check_list) == 0:
                return Result(is_correct=True, feedback=correct_feedback)
            is_correct, feedback = check_local_variable_content(response, answer, remaining_check_list)
            if is_correct:
                if feedback != "NotDefined":
                    return Result(is_correct=True, feedback=correct_feedback)
            else:
                return Result(is_correct=False, feedback=markdown_format(feedback))

    result = ai_feedback(response, answer)
    feedback = result[
        'Feedback'] if check_list_defined else f"{result['Feedback']}\nContact your teacher to give checklist if possible"
    return Result(is_correct=result['Bool'], feedback=markdown_format(feedback))


def check_answer_with_output(response, correct_output):
    """
    The function is called iff the answer is unique. i.e. aList = [1,2,3,4,5] is the unique answer
    Notice that styles (at least they can pass general check) are NOT sensitive
    """
    res_feedback = ""
    try:
        response_output = subprocess.run(['python', '-c', response], capture_output=True, text=True)
        if response_output.returncode != 0:
            res_feedback = f"Error: {response_output.stderr.strip()}"
        else:
            res_feedback = response_output.stdout.strip()
    except Exception as e:
        res_feedback = f"Exception"
    return check_each_letter(res_feedback, correct_output), res_feedback


def check_each_letter(response, answer):
    """
    The function is called iff the answer and the response are unique. i.e. aList = [1,2,3,4,5] is the unique answer and response
    Notice that styles (at least they can pass general check) are NOT sensitive
    """
    return answer.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "") == response.replace(
        " ", "").replace("\t", "").replace("\n", "").replace("\r", "")


def ai_feedback(response, answer):
    """
    use chat GPT-4 to give feedback. However, there has a tiny probability to get the wrong reply content and format of
    AI feedback
    """
    reply = ai_check(response, answer)
    result = ai_content_format(reply)
    return result


if __name__ == '__main__':
    pass
