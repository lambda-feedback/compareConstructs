import random
from typing import Any, TypedDict
from .general_check import check
from .structure import structure_check
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
    pass


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
    general_feedback = check(response)
    if general_feedback != "General check passed!":
        return Result(is_correct=False, feedback=general_feedback)

    msg = check_has_output(answer)
    correct_feedback = random.choice(["Good Job!", "Well Done!"])
    error_feedback = ""
    if msg:
        if not check_answer_with_output(response, msg):
            error_feedback = "The output is different to given answer: \n"
            extra_error_feedback = not_ai_feedback(response, answer)
            error_feedback += extra_error_feedback
            return Result(is_correct=False, feedback=error_feedback)
        else:
            return Result(is_correct=True, feedback=correct_feedback)
    else:
        if check_each_letter(response, answer):
            return Result(is_correct=True, feedback=correct_feedback)

    error_feedback = not_ai_feedback(response, answer)
    # if no extra error feedback, we might need to call for AI
    if error_feedback:
        return Result(is_correct=False, feedback=error_feedback)
    result = ai_feedback(response, answer)
    return Result(is_correct=result['Bool'], feedback=result['Feedback'])


def check_has_output(answer):
    try:
        ans_result = subprocess.run(['python', '-c', answer], capture_output=True, text=True)
        if ans_result.returncode != 0:
            ans_feedback = f"Error: {ans_result.stderr.strip()}"
        else:
            ans_feedback = ans_result.stdout.strip()
    except Exception as e:
        ans_feedback = f"Exception occurred: {str(e)}"
    return ans_feedback


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
    return res_feedback == output_msg


def check_each_letter(response, answer):
    """
    The function is called iff the answer and the response are unique. i.e. aList = [1,2,3,4,5] is the unique answer and response
    Notice that styles (at least they can pass general check) are NOT sensitive
    """
    return answer.replace(" ", "").replace("\t", "").replace("\n", "") == response.replace(" ", "").replace("\t",
                                                                                                            "").replace(
        "\n", "")


def ai_feedback(response, answer):
    """
    use chat GPT-4 to give feedback. However, there has a tiny probability to get the wrong reply content and format of
    AI feedback
    """
    reply = ai_check(response, answer)
    result = ai_content_format(reply)
    return result


def not_ai_feedback(response, answer):
    feedback = ""
    if not structure_check(response, answer):
        feedback = "The methods or classes are not correctly defined.\n"
    # TODO implement other check functionalities
    return feedback
