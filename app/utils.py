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

    # zero indent only occur when they are no any syntax like (if, for)
    if indent_difference == 0:
        return all(indent_level == 0 for indent_level in indent_levels)

    # correct indents
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
        result = subprocess.run(['python', "temp.py"], capture_output=True, text=True)
        os.remove("temp.py")
        if result.returncode != 0:
            return False, f"Error: {result.stderr.strip()}"
        else:
            return True, result.stdout.strip()
    except Exception as e:
        return False, f"Exception occurred: {str(e)}"


def check_answer_with_output(response, answer):
    """
    The function is called iff the answer is unique. i.e. aList = [1,2,3,4,5] is the unique answer
    Notice that styles (at least they can pass general check) are NOT sensitive
    """
    with open("res_tmp.py", 'w') as file:
        file.write(response)
    with open("ans_tmp.py", 'w') as file:
        file.write(answer)
    res_feedback = ""
    ans_feedback = ""
    try:
        res_result = subprocess.run(['python', "res_tmp.py"], capture_output=True, text=True)
        os.remove("res_tmp.py")
        if res_result.returncode != 0:
            res_feedback = f"Error: {res_result.stderr.strip()}"
        else:
            res_feedback = res_result.stdout.strip()
    except Exception as e:
        res_feedback = f"Exception occurred: {str(e)}"
    try:
        ans_result = subprocess.run(['python', "ans_tmp.py"], capture_output=True, text=True)
        os.remove("ans_tmp.py")
        if ans_result.returncode != 0:
            ans_feedback = f"Error: {ans_result.stderr.strip()}"
        else:
            ans_feedback = ans_result.stdout.strip()
    except Exception as e:
        ans_feedback = f"Exception occurred: {str(e)}"

    return res_feedback == ans_feedback


def check_each_letter(response, answer):
    """
    The function is called iff the answer and the response are unique. i.e. aList = [1,2,3,4,5] is the unique answer and response
    Notice that styles (at least they can pass general check) are NOT sensitive
    """
    return answer.replace(" ", "").replace("\t", "").replace("\n", "") == response.replace(" ", "").replace("\t",
                                                                                                            "").replace(
        "\n", "")


if __name__ == '__main__':
    response = """
for i in range(5):
    print(i)
"""
    answer = """
count = 0
while count < 5:
    print(count)
    count += 1
"""
    print(check_answer_with_output(response, answer))
