import random
from typing import Any, TypedDict

try:
    from .global_variable_check import check_global_variable_content
    from .local_variable_check import check_local_variable_content
    from .general_check import check, check_syntax
    from .structure_check import check_structure
except ImportError:
    from general_check import check, check_syntax
    from structure_check import check_structure
    from global_variable_check import check_global_variable_content
    from local_variable_check import check_local_variable_content
import os
import subprocess

try:
    from .format import message_format, ai_content_format
    from .dynamic_import import module_import
    from .aifeedback import ai_check
except ImportError:
    # run it on the local machine
    from format import message_format
    from dynamic_import import module_import
    from aifeedback import ai_check


class Params(TypedDict):
    # TODO it will be list after the website updates
    check_list: str


class Result(TypedDict):
    is_correct: bool
    feedback: str


def evaluation_function(response: Any, answer: Any, params: Params) -> Result:
    check_list = [var.strip() for var in params['check_list'].split(',') if len(var.strip()) > 0]
    correct_feedback = random.choice(["Good Job!", "Well Done!", "Awesome"])
    general_feedback = check(response)
    syntax = check_syntax(answer)
    is_correct_answer, msg = syntax

    if not is_correct_answer:
        return Result(is_correct=False, feedback="Please contact your teacher to give correct answer!")
    if general_feedback != "General check passed!":
        return Result(is_correct=False, feedback=general_feedback)
    if not check_structure(response, answer):
        return Result(is_correct=False, feedback="The methods or classes are not correctly defined.\n")


    if msg:
        if not check_answer_with_output(response, msg):
            # if check_list != 0, it means that output is not the importance
            if len(check_list) == 0:
                error_feedback = "The output is different to given answer: \n"
                return Result(is_correct=False, feedback=error_feedback)
        else:
            return Result(is_correct=True, feedback=correct_feedback)
    else:
        if check_each_letter(response, answer):
            return Result(is_correct=True, feedback=correct_feedback)
    is_correct, feedback, remaining_check_list, response = check_global_variable_content(response, answer, check_list)
    if not is_correct:
        return Result(is_correct=False, feedback=feedback)
    else:
        if len(remaining_check_list) == 0:
            return Result(is_correct=True, feedback=correct_feedback)
        is_correct, feedback = check_local_variable_content(response, answer, remaining_check_list)
        if is_correct:
            if feedback != "NotDefined":
                return Result(is_correct=True, feedback=correct_feedback)
        else:
            return Result(is_correct=False, feedback=feedback)

    result = ai_feedback(response, answer)
    return Result(is_correct=result['Bool'], feedback=result['Feedback'])


def check_answer_with_output(response, output_msg):
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
    return check_each_letter(res_feedback, output_msg)


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
