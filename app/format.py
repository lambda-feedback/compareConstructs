import re

general_errors = ["NameError", "TypeError", "IndexError", "ValueError", "AttributeError",
                  "ModuleNotFoundError", "ZeroDivisionError", "FileNotFoundError", "OverflowError",
                  "UnboundLocalError"]
syntax_errors = ["SyntaxError", "IndentationError"]
no_message_errors = ["MemoryError"]


def message_format(message):
    message_lines = message.splitlines()
    error_msg = message_lines[-1]
    error_type = error_msg.split(":")[0]

    if error_type in syntax_errors:
        return syntax_error_format(error_type, message_lines)
    elif error_type == "KeyError":
        return key_error_format(message_lines)
    elif error_type == "FileNotFoundError":
        return file_not_found_error_format(message_lines)
    elif error_type in general_errors:
        return general_error_format(error_type, message_lines)
    elif error_type in no_message_errors:
        return no_message_error_format(error_type, message_lines)
    else:
        return message


def file_not_found_error_format(message_lines):
    line_location = message_lines[-2].split(",")[1].lstrip()
    not_found_file_detail = message_lines[-1].split(":")[2].lstrip()
    return f"FileNotFoundError: at {line_location}, No such file or directory: {not_found_file_detail}"


def no_message_error_format(error_type, message_lines):
    line_location = message_lines[-2].split(",")[1].lstrip()
    return f"{error_type}: at {line_location}"


def syntax_error_format(error_type, message_lines):
    line_location = message_lines[0].split(",")[1].lstrip()
    code_location = message_lines[1:-1]
    syntax_detail = '<br>'.join(code_location)
    return f"{error_type}: at {line_location},<br>{syntax_detail}"


def key_error_format(message_lines):
    line_location = message_lines[-2].split(",")[1].lstrip()
    error_detail = message_lines[-1].split(":")[1].lstrip()
    return f"KeyError: at {line_location}, {error_detail} is not found"


def general_error_format(error_type, message_lines):
    line_location = message_lines[-2].split(",")[1].lstrip()
    error_detail = message_lines[-1].split(":")[1].lstrip()
    return f"{error_type}: at {line_location}, {error_detail}"


def ai_content_format(reply_content):
    result = {}

    # get the Bool pair:
    pair_idx = reply_content.find("Feedback")
    bool_msg = reply_content[:pair_idx]
    feedback_msg = reply_content[pair_idx:]
    if 'True' in bool_msg:
        result['Bool'] = True
    else:
        result['Bool'] = False
    result['Feedback'] = feedback_msg[feedback_msg.find(': ') + 1:].lstrip()

    return result


def annotation_format(code_string):
    """
    This format includes:
    replace annotation to a single line
    """
    # TODO
    pass


def response_format(code_string):
    """
    This format includes:
    remove the unnecessary indents
    categorize the structure of the format: classes and methods
    """
    code_lines = code_string.strip().split('\n')
    return [re.sub(r'\n\s*\n+', '\n', code_line) for code_line in code_lines]







