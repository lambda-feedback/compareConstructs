from typing import Any, TypedDict
from .utils import *


# TODO Implement three general types of feedbacks:
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
