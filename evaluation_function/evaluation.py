import os
from typing import Any, TypedDict, Union

from .format.general_format import ai_content_format, markdown_format
from .checks.ai_prompt_check import ai_check
from .checks.run_checks import run_checks

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
    sandbox = int(os.environ.get("NO_SANDBOX", "0")) == 0

    check_result = run_checks(response, answer, dict(params), sandbox)
    if check_result.get_payload("ai", False):
        result = ai_feedback(response, answer)
        feedback = result['Feedback']
        return Result(is_correct=result['Bool'], feedback=markdown_format(feedback))
    else:
        return Result(is_correct=check_result.passed(), feedback=check_result.message())


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
