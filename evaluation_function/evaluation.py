import os
import sys
from typing import Any, TypedDict, Union

from .format.general_format import ai_content_format, markdown_format
from .checks.ai_prompt_check import ai_check
from .checks.run_checks import run_checks

class Params(TypedDict):
    global_variable_check_list: Union[str, list]
    check_names: bool
    check_func: str
    output_inexact: bool

class Result(TypedDict):
    is_correct: bool
    feedback: str

def _coerce_file_specs(raw: Any) -> list:
    """Normalise a raw files value into a list of {url, name} dicts.

    Entries may already be dicts, or JSON-encoded strings — the LF web
    client currently serialises each upload entry to a string.
    """
    if not isinstance(raw, (list, tuple)):
        return []
    specs = []
    for entry in raw:
        if isinstance(entry, str):
            try:
                entry = json.loads(entry)
            except (ValueError, TypeError):
                continue
        if isinstance(entry, dict):
            specs.append(entry)
    return specs

def _unwrap_payload(value: Any) -> tuple[str, list]:
    payload = value
    if isinstance(payload, str):
        try:
            parsed = json.loads(payload)
        except (ValueError, TypeError):
            parsed = None
        if isinstance(parsed, dict) and ("code" in parsed or "files" in parsed):
            payload = parsed

    if isinstance(payload, dict):
        return str(payload.get("code") or ""), _coerce_file_specs(payload.get("files"))
    if isinstance(payload, str):
        return payload, []
    return str(payload), []

def _resolve_submission(response: Any, params: Params) -> tuple[str, list]:
    """Split the submission into (code, file_specs).

    Files listed in the response take precedence; params["files"] is the
    fallback.
    """
    code, response_files = _unwrap_payload(response)
    file_specs = response_files or _coerce_file_specs(params.get("files"))
    return code, file_specs


def _answer_code(answer: Any) -> str:
    """The code string from the answer field, unwrapping a {code, files}
    payload the same way the submission is unwrapped."""
    return _unwrap_payload(answer)[0]


def evaluation_function(response: Any, answer: Any, params: Params) -> Result:
    sandbox = not (int(os.environ.get("NO_SANDBOX", "0")) == 1 or "--no-sandbox" in sys.argv)

    response, _ = _resolve_submission(response, params)
    answer = _answer_code(answer)


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
