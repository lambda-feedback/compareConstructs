import os
import subprocess


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

    if indent_difference != 2 and indent_difference != 4:
        return False

    return all(indent_level % indent_difference == 0 for indent_level in indent_levels)


def general_check(code_string) -> str:
    if not check_indents(code_string):
        return f"Indent error, the indent should only be multiple of 2 or 4"
    is_syntax_correct, msg = check_syntax(code_string)
    if not is_syntax_correct:
        return f"Syntax error, check the details below: "
    # TODO implement the message format
    return "General check passed!"


def check_syntax(code_string):
    with open("temp.py", 'w') as file:
        file.write(code_string)
    try:
        # Execute the Python script
        result = subprocess.run(['python', "temp.py"], capture_output=True, text=True)
        os.remove("temp.py")
        # Check if there were any errors
        if result.returncode != 0:
            return False, f"Error: {result.stderr.strip()}"
        else:
            return True, result.stdout.strip()
    except Exception as e:
        return False, f"Exception occurred: {str(e)}"



if __name__ == '__main__':
    response = """
def hello():
print(hello)
"""
    print(general_check(response))