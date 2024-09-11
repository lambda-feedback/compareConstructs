from ..format.general_format import response_format, message_format
from .check_result import CheckResult

import ast
from contextlib import redirect_stdout
from io import StringIO


def check_indents(formatted_code_lines) -> bool:
    """
    This function checks the indentation correctness of the given Python code.
    Notice that indentation depends on student preference: (2 spaces or 4 spaces are acceptable)
    """
    indent_levels = []
    for line in formatted_code_lines:
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


def format_syntax_error(e: SyntaxError) -> str:
    caret = "".join(' ' for _ in range(e.offset - 1)) + '^'
    return f"{e.msg}\n{e.text.rstrip()}\n{caret}"


def get_ast(code_string: str) -> CheckResult:
    try:
        tree = ast.parse(code_string)
        return (
            CheckResult(True)
            .add_payload("ast", tree)
        )
    except SyntaxError as e:
        return (
            CheckResult(False)
            .add_message(format_syntax_error(e))
        )
    except:
        return (
            CheckResult(False)
            .add_message(f"Exception raised when parsing")
        )


def check_style(code_string) -> CheckResult:
    """Checks that the response is correct syntactically, and uses correct indentation"""

    formatted_code_lines = response_format(code_string)
    if not check_indents(formatted_code_lines):
        return (
            CheckResult(False)
            .add_message(f"Indent error, the indent should only be multiple of 2 or 4")
        )

    # Attempt to parse the code into an AST. If it is not syntactically correct,
    # this will fail and return False.
    return get_ast(code_string)


def validate_answer(code_string: str) -> CheckResult:
    """Ensures that the answer is valid.
    Additionally, executes the answer code to obtain the values it 
    prints to stdout.
    """

    answer_ast_result = get_ast(code_string)
    if not answer_ast_result.passed():
        return answer_ast_result

    try:
        result = StringIO()
        with redirect_stdout(result):
            exec(code_string, {})
    except SystemExit:
        pass
    except Exception as e:
        return CheckResult(False).add_message("Please contact your teacher to give the correct answer")
    return (
        CheckResult(True)
        .add_payload("correct_output", result.getvalue().strip())
        .combine(answer_ast_result)
    )
