import ast
import builtins
import types
import copy
import numpy as np

try:
    from .same_variable_content_check import check_same_content_with_different_variable
except ImportError:
    from same_variable_content_check import check_same_content_with_different_variable

tolerance = 1e-8


class VariableVisitor(ast.NodeVisitor):
    def __init__(self):
        self.variables = set()

    def visit_Name(self, node):
        if node.id not in dir(builtins):
            self.variables.add(node.id)
        self.generic_visit(node)


# Function to execute the code and check the content of variables
def variable_content(code_str) -> dict:
    visitor = VariableVisitor()
    tree = ast.parse(code_str)
    visitor.visit(tree)
    variables = visitor.variables
    context = {}
    try:
        exec(code_str, context)
    except NameError:
        return {"err": ""}
    except SystemExit:
        pass
    except Exception:
        return {"NotDefined": ""}

    return {var: context.get(var) for var in variables if not isinstance(context.get(var), types.FunctionType)}


def check_global_variable_content(response, answer, check_list: list, global_response_variable_content="",
                                  global_answer_variable_content=""):
    """
    Teacher should give a variable check-list for us due to the importance of the variables relying on the Teacher's goal
    """
    response = f"{global_response_variable_content}\n{response}"

    answer = f"{global_answer_variable_content}\n{answer}"
    response_var_dict = variable_content(response)
    answer_var_dict = variable_content(answer)

    # sometimes students give us different variable names, but we could figure the difference
    response, response_var_dict = check_same_content_with_different_variable(response, check_list, response_var_dict,
                                                                             answer_var_dict)
    # sometimes local variables are defined in the outer scope
    if "err" in answer_var_dict.keys():
        return False, "NameError", check_list, response
    if "err" in response_var_dict.keys():
        return False, "NameError", check_list, response

    # params type are not declared and generated variables do not fit the type of the variable
    if "NotDefined" in answer_var_dict.keys():
        return True, "NotDefined", check_list, response
    if "NotDefined" in response_var_dict.keys():
        return True, "NotDefined", check_list, response
    # check whether they have the same variable names
    answer_var_set = answer_var_dict.keys()
    response_var_set = response_var_dict.keys()
    intersections = response_var_set & answer_var_set
    error_var_contents = []
    is_defined = True

    remaining_check_list = copy.deepcopy(check_list)

    for var in check_list:
        # sometimes execute the code doesn't change the variable value i.e. local variable in a method
        if var in intersections:

            if answer_var_dict[var] is not None:
                is_correct, msg, error_var_contents, remaining_check_list = is_equal(
                    var, response_var_dict[var], answer_var_dict[var], error_var_contents,
                    remaining_check_list
                )
                if not is_correct:
                    return False, msg, remaining_check_list, response
            else:
                is_defined = False

    if len(error_var_contents) == 0:
        if is_defined:
            return True, "", remaining_check_list, response
        else:
            return True, "NotDefined", remaining_check_list, response
    else:
        feedback = ""
        if 0 < len(error_var_contents) < 2:
            feedback += f"""The value of '{"', '".join(error_var_contents)}' is not correct respect to the answer\n"""
        elif len(error_var_contents) >= 2:
            feedback += f"""The values of '{"', '".join(error_var_contents)}' are not correct respect to the answer\n"""
        return False, feedback, remaining_check_list, response


def is_equal(variable_name, response_variable_content, answer_variable_content, error_var_contents,
             remaining_check_list):
    if type(response_variable_content) != type(answer_variable_content):
        return False, f"The type of '{variable_name}' is not correct. Expected: {type(answer_variable_content).__name__}", \
            error_var_contents, remaining_check_list

    if isinstance(answer_variable_content, np.ndarray):
        try:
            is_correct = np.allclose(response_variable_content, answer_variable_content)
        except Exception as e:
            return False, f"{type(e).__name__} of '{variable_name}': {e}", error_var_contents, remaining_check_list


    else:
        try:
            is_correct = response_variable_content == answer_variable_content
        except Exception as e:
            return False, f"{type(e).__name__} of '{variable_name}': {e}", error_var_contents, remaining_check_list


    if is_correct:
        remaining_check_list.pop()
        return True, "", error_var_contents, remaining_check_list

    else:
        # the error message will be checked later
        error_var_contents.append(variable_name)
        return True, "", error_var_contents, remaining_check_list


if __name__ == '__main__':
    str = """
import sys

a = 5
b = 10
sys.exit()
    """
    print(variable_content(str))