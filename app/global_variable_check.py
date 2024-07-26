import ast
import builtins
import types
import copy
import numpy as np

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
    # sometimes local variables are defined in the outer scope
    if "err" in answer_var_dict.keys():
        return False, "NameError", check_list
    if "err" in response_var_dict.keys():
        return False, "NameError", check_list
    # check whether they have the same variable names
    answer_var_set = answer_var_dict.keys()
    response_var_set = response_var_dict.keys()
    intersections = response_var_set & answer_var_set
    error_var_contents = []
    is_correct = True
    is_defined = True

    remaining_check_list = copy.deepcopy(check_list)

    for var in check_list:
        # sometimes execute the code doesn't change the variable value i.e. local variable in a method
        if var in intersections:

            if answer_var_dict[var] is not None:
                if type(response_var_dict[var]) != type(answer_var_dict[var]):
                    return False, f"The type of '{var}' is not correct. Expected: {type(answer_var_dict[var])}", remaining_check_list

                if isinstance(answer_var_dict[var], np.ndarray):
                    try:
                        error_var_contents, is_correct, remaining_check_list = update_info(
                            var, np.allclose(response_var_dict[var], answer_var_dict[var], atol=tolerance),
                            error_var_contents, remaining_check_list
                        )
                    except Exception as e:
                        return False, f"{type(e).__name__} of '{var}': {e}", remaining_check_list
                else:
                    error_var_contents, is_correct, remaining_check_list = update_info(
                        var, response_var_dict[var] == answer_var_dict[var],
                        error_var_contents, remaining_check_list
                    )

            else:
                is_defined = False

    if is_correct:
        if is_defined:
            return True, "", remaining_check_list
        else:
            return True, "NotDefined", remaining_check_list
    else:
        feedback = ""
        if 0 < len(error_var_contents) < 2:
            feedback += f"""The value of '{"', '".join(error_var_contents)}' is not correct\n"""
        elif len(error_var_contents) >= 2:
            feedback += f"""The values of '{"', '".join(error_var_contents)}' are not correct\n"""
        return False, feedback, remaining_check_list


def update_info(var, is_equal, error_var_contents, remaining_check_list):
    is_correct = True
    if is_equal:
        remaining_check_list.remove(var)
    else:
        error_var_contents.append(var)
        is_correct = False
    return error_var_contents, is_correct, remaining_check_list
