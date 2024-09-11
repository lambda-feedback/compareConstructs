import numpy as np
from contextlib import redirect_stdout
from io import StringIO

def check_answer_with_output(response, correct_output, is_output_eval):
    """
    The function is called iff the answer is unique. i.e. aList = [1,2,3,4,5] is the unique answer
    Notice that styles (at least they can pass general check) are NOT sensitive
    """

    try:
        result = StringIO()
        with redirect_stdout(result):
            exec(response, {})
    except SystemExit:
        pass
    except Exception as e:
        return False, f"Error: {e}"
    return is_different(result.getvalue().strip(), correct_output, is_output_eval), result.getvalue()


def is_different(res_output, correct_output, is_output_eval):
    if is_output_eval:
        res_output_lines = res_output.split('\n')
        correct_output_lines = correct_output.split('\n')
        if len(res_output_lines) != len(correct_output_lines):
            return False
        for i in range(len(res_output_lines)):
            res_line = res_output_lines[i].strip()
            ans_line = correct_output_lines[i].strip()
            try:
                is_equal = np.isclose(complex(res_line), complex(ans_line))
                if not is_equal:
                    return False
            except ValueError:
                is_equal = res_line == ans_line
                if not is_equal:
                    return False
        return True

    else:
        return res_output == correct_output
