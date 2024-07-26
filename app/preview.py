from typing import Any, TypedDict

# TODO Implement three general types of feedbacks:

class Params(TypedDict):
    is_unique_answer: bool
    is_enumerable_answer: bool
    is_ai_feedback: bool

class Result(TypedDict):
    preview: Any


def preview_function(response: Any, params: Params) -> Result:
    """
    Function used to preview a student response.
    ---
    The handler function passes three arguments to preview_function():

    - `response` which are the answers provided by the student.
    - `params` which are any extra parameters that may be useful,
        e.g., error tolerances.

    The output of this function is what is returned as the API response
    and therefore must be JSON-encodable. It must also conform to the
    response schema.

    Any standard python library may be used, as well as any package
    available on pip (provided it is added to requirements.txt).

    The way you wish to structure you code (all in this function, or
    split into many) is entirely up to you.
    """


    return Result(preview=response)







import numpy as np
x1 = np.arange(-5, -2, 0.5)
x2 = np.arange(-2, 3, 0.05)
x3 = np.arange(3, 5+0.5, 0.5)
x = np.concatenate((x1, x2, x3))