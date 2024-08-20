import difflib
import numpy as np


def variables_content_compare(variable_list, res_dict: dict, ans_dict: dict):
    feedback = ""
    for variable_name in variable_list:
        feedback += (variable_content_compare(variable_name, res_dict[variable_name], ans_dict[variable_name]) + "\n\n")
    return feedback


def variable_content_compare(variable_name, res_content, ans_content):
    general_feedback = f"The value of '{variable_name}' is: {res_content}\nExpected: {ans_content}"
    if isinstance(ans_content, str):
        if len(ans_content) < 30:
            return general_feedback
        else:
            res_content, ans_content, index = get_string_differences(res_content, ans_content)
            if ans_content is not None and res_content is not None:
                feedback = f"The value of '{variable_name}' at index {index} is: {res_content}\nExpected: {ans_content}"
                return feedback
            else:
                return ''

    elif isinstance(ans_content, list):
        if len(ans_content.__str__()) < 30:
            return general_feedback
        else:
            is_same_len, idx = get_list_difference(res_content, ans_content)
            if idx != -1:
                feedback = f"The value of '{variable_name}' at index {idx} is: {res_content[idx]}\nExpected: {ans_content[idx]}"
                if is_same_len:
                    return feedback
                else:
                    return f"The length of '{variable_name}' is not the same as the answer\n{feedback}"
            else:
                return ''

    elif isinstance(ans_content, np.ndarray):
        if len(ans_content.__str__()) < 50:
            return f"The value of '{variable_name}' is:\n{res_content}\nExpected: \n{ans_content}"
        else:
            if ans_content.shape != res_content.shape:
                return f"The shape of '{variable_name}' is: {res_content.shape}\nExpected: {ans_content.shape}"
            first_diff, idx = get_ndarray_difference(res_content, ans_content)
            return f"The value of '{variable_name}' at index {idx} is:\n{res_content[idx]}\nExpected:\n{ans_content[idx]}"


    else:
        return general_feedback


def get_string_differences(res_content, answer_content, n=5):
    """
    get the first difference only
    """
    s = difflib.SequenceMatcher(None, res_content, answer_content)
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag != 'equal':
            start1 = max(0, i1 - n)
            end1 = min(len(res_content), i2 + n)
            start2 = max(0, j1 - n)
            end2 = min(len(answer_content), j2 + n)

            if end1 - start1 > 30:
                res_diff = res_content[start1: start1 + 30]
            else:
                res_diff = res_content[start1:end1]
            if end2 - start2 > 30:
                ans_diff = answer_content[start2: start2 + 30]
            else:
                ans_diff = answer_content[start2:end2]
            return res_diff, ans_diff, start2

    return None, None, -1


def get_list_difference(res_list: list, ans_list: list):
    is_same_len = len(res_list) == len(ans_list)
    for i in range(len(min(res_list, ans_list))):
        if res_list[i] != ans_list[i]:
            return is_same_len, i
    return is_same_len, -1


def get_ndarray_difference(res_ndarray, ans_ndarray):
    difference = np.abs(res_ndarray - ans_ndarray)
    indices = np.where(difference != 0)
    result = ans_ndarray[indices]
    if indices is not None:
        return result[0], indices[0]
    return None, None


if __name__ == '__main__':
    alist = np.array([[1, 2, 2, 232323223, 232323223], [323, 42, 424, 232323223, 232323223]])
    rlist = np.array([[1, 2, 3, 232323223, 232323223], [323, 42, 421, 232323223, 232323223]])
    print(variable_content_compare('x', rlist, alist))
