import random
from typing import Any, TypedDict

from .format.output_traceback_format import output_diffs
from .format.variable_compare_format import variables_content_compare
from .format.general_format import ai_content_format, markdown_format
from .checks.ai_prompt_check import ai_check
from .checks.global_variable_check import check_global_variable_content, get_err_vars, variable_content
from .checks.local_variable_check import check_local_variable_content, extract_modules
from .checks.general_check import check, check_syntax
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
    check_list = params['check_list']
    if isinstance(check_list, str):
        check_list = [var.strip() for var in check_list.split(',') if len(var.strip()) > 0]
    is_defined = True
    if len(check_list) == 0:
        is_defined = False
    correct_feedback = random.choice(["Good Job!", "Well Done!", "Awesome"])
    general_feedback = check(response)
    is_correct_answer, msg = check_syntax(answer)

    if not is_correct_answer:
        return Result(is_correct=False, feedback="Please contact your teacher to give correct answer!")
    if general_feedback != "General check passed!":
        return Result(is_correct=False, feedback=general_feedback)
    if not check_structure(response, answer, check_names=params.get('check_names', False)):
        return Result(is_correct=False, feedback="The methods or classes are not correctly defined.")

    if msg:
        is_correct, res_msg = check_answer_with_output(response, msg)
        if not is_correct:
            # if check_list != 0, it means that output is not the importance
            if not is_defined:
                error_feedback = "The output is different to given answer: \n"
                diff = output_diffs(res_msg, msg)
                return Result(is_correct=False, feedback=markdown_format(error_feedback + diff))
        else:
            return Result(is_correct=True, feedback=correct_feedback)
    else:
        if check_each_letter(response, answer):
            return Result(is_correct=True, feedback=correct_feedback)

    # if the checklist is not given, it is meaningless to check the variables, then we will call for AI
    if is_defined:
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
        'Feedback'] if is_defined else f"{result['Feedback']}\nContact your teacher to give checklist if possible"
    return Result(is_correct=result['Bool'], feedback=markdown_format(feedback))


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
        res_feedback = f"Exception"
    return check_each_letter(res_feedback, output_msg), res_feedback


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
