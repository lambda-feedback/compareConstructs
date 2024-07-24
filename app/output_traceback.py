import re


def output_traceback(response_output, answer_output, response, answer):
    is_double, result = parse_to_double(answer_output)
    extra_feedback = "\n"
    if is_double:
        extra_feedback += "The value of output is wrong"


def parse_to_double(value):
    try:
        result = float(value)
        return True, result
    except ValueError:
        return False, -1.0


def extract_var_from_output(print_line: str):
    """
    the var name from print supports only two types:
    regular print and formatted print using regular expression
    """
    print_message = print_line.strip()[6:-1]

    pattern = r'[,+]'
    # replace `f"..."` with placeholders to avoid splitting inside f-strings and double quota
    f_placeholders = re.findall(r'f"[^"]*"', print_message)
    f_placeholder_replacement = [f'__F_PLACEHOLDER_{i}__' for i in range(len(f_placeholders))]
    dq_placeholders = re.findall(r'"[^"]*"', print_message)
    dq_placeholder_replacement = [f'__Q_PLACEHOLDER_{i}__' for i in range(len(dq_placeholders))]
    sq_placeholders = re.findall(r"'[^']*'", print_message)
    sq_placeholder_replacement = [f'__Q_PLACEHOLDER_{i}__' for i in range(len(sq_placeholders))]
    for ph, rep in zip(f_placeholders, f_placeholder_replacement):
        print_message = print_message.replace(ph, rep)
    for ph, rep in zip(dq_placeholders, dq_placeholder_replacement):
        print_message = print_message.replace(ph, rep)
    for ph, rep in zip(sq_placeholders, sq_placeholder_replacement):
        print_message = print_message.replace(ph, rep)
    parts = re.split(pattern, print_message)
    for ph, rep in zip(f_placeholder_replacement, f_placeholders):
        parts = [part.replace(ph, rep) for part in parts]
    for ph, rep in zip(dq_placeholder_replacement, dq_placeholders):
        parts = [part.replace(ph, rep) for part in parts]
    for ph, rep in zip(sq_placeholder_replacement, sq_placeholders):
        parts = [part.replace(ph, rep) for part in parts]
    # Strip leading and trailing spaces from each part

    var_list = []
    for part in parts:
        part = part.strip()
        if is_f_string(part):
            extract_var_from_f_string(part)

    return parts


def extract_var_from_f_string(code_str):
    # Define a pattern to match expressions inside curly braces in an f-string
    pattern = r'\{([^}]+)\}'

    # Find all matches of the pattern in the code string
    matches = re.findall(pattern, code_str)

    return matches


def is_double_quota_string(text):
    pattern = r'^"[^"]*"$'
    if re.match(pattern, text) is not None:
        return True
    return False


def is_f_string(text):
    pattern = r'^f"[^"]*"{0,1}[^"]*"$'
    if re.match(pattern, text) is not None:
        return True
    return False


text = '"sdafj alfkas "ekl f"'

print(is_double_quota_string(text))

print_msg = "print('hello, ')"

print(extract_var_from_output(print_msg))