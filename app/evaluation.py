import random
from typing import Any, TypedDict, Union

from .checks.output_check import check_answer_with_output
from .format.output_traceback_format import output_diffs
from .format.general_format import ai_content_format, markdown_format
from .checks.ai_prompt_check import ai_check
from .checks.global_variable_check import check_global_variable_content
from .checks.general_check import check_style, validate_answer
from .checks.structure_check import check_structure
from .checks.func_check import check_func
import subprocess


class Params(TypedDict):
    global_variable_check_list: Union[str, list]
    check_names: bool
    check_func: str
    local_variable_check_list_in_method: dict
    output_eval: bool

class Result(TypedDict):
    is_correct: bool
    feedback: str


def evaluation_function(response: Any, answer: Any, params: Params) -> Result:
    check_list = set(params.get('global_variable_check_list', {}))
    if isinstance(check_list, str):
        # check list is a set as the repeated variable name is not accepted
        check_list = {var.strip() for var in check_list.split(',') if len(var.strip()) > 0}

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
    
    # If a function test is desired, run tests to ensure that a particular function returns the 
    # correct values
    check_func_name = params.get('check_func', None)
    if check_func_name:
        result = check_func(response_ast, answer_ast, check_func_name)
        if result.passed():
            return Result(is_correct=True, feedback=correct_feedback)
        else:
            return Result(is_correct=False, feedback=result.message())

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
        is_output_eval = params.get('output_eval', True)
        is_correct, res_msg = check_answer_with_output(response, correct_output, is_output_eval)
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
        local_check_dict = params.get('local_variable_check_list_in_method', dict())
        check_result = check_global_variable_content(response_ast, answer_ast, check_list)
        if not check_result.passed():
            return Result(is_correct=False, feedback=markdown_format(check_result.message()))
        else:
            if not local_check_dict:
                return Result(is_correct=True, feedback=correct_feedback)
            # if len(remaining_check_list) == 0:
            #     return Result(is_correct=True, feedback=correct_feedback)
            # is_correct, feedback = check_local_variable_content(
            #     response, answer, res_var_dict, ans_var_dict, remaining_check_list, response_ast, answer_ast)
            # if is_correct:
            #     if feedback != "NotDefined":
            #         return Result(is_correct=True, feedback=correct_feedback)
            # else:
            #     return Result(is_correct=False, feedback=markdown_format(feedback))

    result = ai_feedback(response, answer)
    feedback = result[
        'Feedback'] if check_list_defined else f"{result['Feedback']}\nContact your teacher to give checklist if possible"
    return Result(is_correct=result['Bool'], feedback=markdown_format(feedback))




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
