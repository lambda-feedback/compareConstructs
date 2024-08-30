import difflib
import numpy as np
from dataclasses import dataclass
from typing import Union

import sys
this = sys.modules[__name__]

def variables_content_compare(variable_list, res_dict: dict, ans_dict: dict):
    feedback = ""
    for variable_name in variable_list:
        feedback += (variable_content_compare(variable_name, res_dict[variable_name], ans_dict[variable_name]) + "\n\n")
    return feedback

# Declare some classes to hold the different response cases
# I'm imagining this is Rust and we have algebraic datatypes available,
# but unfortunately this is Python, so we don't, so we have to use workarounds.
@dataclass
class WrongShape:
    response_shape: tuple
    answer_shape: tuple

@dataclass
class WrongValue:
    error_index: int
    required_value: any
    actual_value: any

class WrongValueMultidimensional:
    error_index: tuple
    required_value: any
    actual_value: any

class WrongWhole:
    pass

class Equal:
    pass

ArrayFeedback = Union[WrongShape, WrongValue, WrongValueMultidimensional, WrongWhole, Equal]

MAX_STRING_LEN = 30

def get_array_feedback(response_array, answer_array) -> ArrayFeedback:
    """Compares two arrays (which can be NumPy arrays or Python lists) and
    returns an ArrayFeedback type to allow a custom feedback message to be
    created. The exact format of this message is context-specific, so 
    the feedback from this function is as generic as possible.
    See variable_content_compare for an example of use.
    Uses numpy.isclose.
    """
    answer_string = str(answer_array)
    response_string = str(response_array)

    # numpy arrays can have different shapes
    if isinstance(answer_array, np.ndarray):
        response_shape = np.shape(response_array)
        answer_shape = np.shape(answer_array)
        if response_shape != answer_shape:
            return WrongShape(response_shape, answer_shape)
        elif len(response_shape) != 1:
            if np.allclose(response_array, answer_array):
                return Equal()
            else:
                differences = get_array_differences_multi(answer_array, response_array)
                error_idx = differences[0]
                WrongValueMultidimensional(error_idx, answer_array[error_idx], response_array[error_idx])

    diffs = get_array_differences(answer_array, response_array);

    if len(response_array) != len(answer_array):
        return WrongShape((len(response_array),), (len(answer_array),))

    if len(diffs) == 0:
        return Equal()

    if len(answer_string) <= MAX_STRING_LEN and len(response_string) <= MAX_STRING_LEN:
        return WrongWhole()

    return WrongValue(diffs[0], answer_array[diffs[0]], response_array[diffs[0]])


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

    elif isinstance(ans_content, list) or isinstance(ans_content, np.ndarray):
        feedback = get_array_feedback(res_content, ans_content)
        if isinstance(feedback, WrongShape):
            return f"The shape of '{variable_name}' is: {feedback.response_shape}\nExpected: {feedback.answer_shape}"
        elif isinstance(feedback, WrongValue):
                f"The value of '{variable_name}' at index {feedback.error_index} is: {feedback.actual_value}\nExpected: {feedback.required_value}"
        elif isinstance(feedback, WrongValueMultidimensional):
            f"There is an incorrect value in your multidimensional array."
        elif isinstance(feedback, WrongWhole):
            return general_feedback
        elif isinstance(feedback, Equal):
            return ""

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

def get_array_differences(a, b) -> list:
    """Given two arrays/lists a and b, returns a list of indices where they differ.
    WARNING: only works correctly for single-dimensional arrays
    """
    return [index for index, (e1, e2) in enumerate(zip(a, b)) if not np.isclose(e1, e2)]


def get_array_differences_multi(a: np.ndarray, b: np.ndarray) -> list:
    """Like `get_array_differences`, but works on multidimensional arrays of any dimension.
    WARNING: it is assumed that a and b have the same shape.
    """
    assert np.shape(a) == np.shape(b)
    differences = np.nonzero((~np.isclose(a, b)).astype(int))
    return list(zip(*differences))
