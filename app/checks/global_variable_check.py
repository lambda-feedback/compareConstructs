import ast
import builtins
import types
import copy
import numpy as np
import io
import contextlib

try:
    from .same_variable_content_check import check_same_content_with_different_variable
except ImportError:
    from same_variable_content_check import check_same_content_with_different_variable

tolerance = 1e-8
GLOBAL_ERR_VAR_CONTENT = []


# Function to execute the code and check the content of variables
def variable_content(code_str, tree) -> (bool, dict):
    class VariableVisitor(ast.NodeVisitor):
        def __init__(self):
            self.variables = set()

        def visit_FunctionDef(self, node):
            # Skip the function name and only visit the body
            for stmt in node.body:
                self.visit(stmt)

        def visit_Name(self, node):
            if node.id not in dir(builtins):
                self.variables.add(node.id)
            self.generic_visit(node)

    visitor = VariableVisitor()
    visitor.visit(tree)
    variables = visitor.variables
    context = {}
    try:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exec(code_str, context)
    except SystemExit:
        pass
    except Exception as e:
        return False, {"err": e}

    return True, {var: context.get(var) for var in variables if
                  not isinstance(context.get(var), types.FunctionType) and context.get(var) is not None}


def check_global_variable_content(response, answer, check_list: list, response_ast, answer_ast):
    """
    Teacher should give a variable check-list for us due to the importance of the variables relying on the Teacher's goal
    """

    global GLOBAL_ERR_VAR_CONTENT

    # get variable contents by executing the code
    is_res_exec, response_var_dict = variable_content(response, response_ast)
    is_ans_exec, answer_var_dict = variable_content(answer, answer_ast)

    if not is_ans_exec:
        return False, f"The given answer is wrong:\n{answer_var_dict['err']}", check_list, response

    if not is_res_exec:
        return False, response_var_dict['err'], check_list, response

    # sometimes students give us different variable names, but we can figure out the difference
    response, response_var_dict = check_same_content_with_different_variable(
        response, response_var_dict, answer_var_dict, response_ast, answer_ast, check_list)

    # get the same variables
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
                    GLOBAL_ERR_VAR_CONTENT = error_var_contents
                    return False, msg, remaining_check_list, response
            else:
                is_defined = False

    # TMP is used for local variable checks
    if "TMP" in remaining_check_list:
        remaining_check_list.remove("TMP")
        if len(remaining_check_list) == 0:
            return True, "", remaining_check_list, response
        if "TMP" in error_var_contents:
            error_var_contents.remove("TMP")
            return False, "The return value is not the same as the given answer", remaining_check_list, response
        if "TMP" in intersections:
            return True, "", remaining_check_list, response
        else:
            if "TMP" in answer_var_set:
                return False, "The return statement is lacking", remaining_check_list, response
            elif "TMP" in response_var_set:
                return False, "The return statement is redundant", remaining_check_list, response

    # error_contents occur when student provides the same answer but
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

        GLOBAL_ERR_VAR_CONTENT = error_var_contents
        return False, feedback, remaining_check_list, response


def get_err_vars():
    return GLOBAL_ERR_VAR_CONTENT


def is_equal(variable_name, response_variable_content, answer_variable_content, error_var_contents,
             remaining_check_list):
    # TODO: add other equivalent relation:
    #  Notice that the return type contains: (is_correct, feedback, error_var, remaining_check_list)
    if type(response_variable_content) != type(answer_variable_content):
        error_var_contents.append(variable_name)
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
        remaining_check_list.remove(variable_name)
        return True, "", error_var_contents, remaining_check_list

    else:
        # the error message will be checked later
        error_var_contents.append(variable_name)
        return True, "", error_var_contents, remaining_check_list
