import ast
import builtins
import types
import copy
import numpy as np
import io
import contextlib

from .same_variable_content_check import check_same_content_with_different_variable
from ..format.variable_compare_format import variable_content_compare

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


def check_global_variable_content(response, answer, check_list: set, response_ast, answer_ast):
    """
    Teacher should give a variable check-list for us due to the
    importance of the variables relying on the Teacher's goal
    It will return the first error encountered
    """

    # get variable contents by executing the code
    is_res_exec, response_var_dict = variable_content(response, response_ast)
    is_ans_exec, answer_var_dict = variable_content(answer, answer_ast)

    if not is_ans_exec:
        return False, f"The given answer is wrong:\n{answer_var_dict['err']}"

    if not is_res_exec:
        return False, response_var_dict['err']

    # sometimes students give us different variable names, but we can figure out the difference
    response, response_var_dict = check_same_content_with_different_variable(
        response, response_var_dict, answer_var_dict, response_ast, answer_ast, check_list)

    # get the variable sets
    answer_var_set = answer_var_dict.keys()
    response_var_set = response_var_dict.keys()
    intersections = response_var_set & answer_var_set

    # If the variables in checklist are not included in intersection, get wrong
    # since any params in checklist should be declared with same value (could be different names)
    if not check_list <= intersections:
        remaining_variables = check_list - (check_list & intersections)
        if len(remaining_variables) == 1:
            feedback = f"The variable '{remaining_variables.pop()}' " \
                       f"is not defined or different value respect to the answer"
        else:
            feedback = f"""The variables '{"', '".join(list(remaining_variables))}' are not defined """ \
                       f"or different values respect to the answer"
        return False, feedback

    for var in check_list:
        if answer_var_dict[var] is not None:
            is_correct, feedback = is_equal(
                var, response_var_dict[var], answer_var_dict[var])
            if not is_correct:
                return is_correct, feedback

    return True, ""


def is_equal(variable_name, response_variable_content, answer_variable_content):
    # TODO: add other equivalent relation:
    if type(response_variable_content) != type(answer_variable_content):
        return False, f"The type of '{variable_name}' is not correct. " \
                      f"Expected: {type(answer_variable_content).__name__}"

    if isinstance(answer_variable_content, np.ndarray):
        try:
            is_correct = np.allclose(response_variable_content, answer_variable_content)
        except Exception as e:
            return False, f"{type(e).__name__} of '{variable_name}': {e}"
    else:
        try:
            is_correct = response_variable_content == answer_variable_content
        except Exception as e:
            return False, f"{type(e).__name__} of '{variable_name}': {e}"

    if is_correct:
        return True, ""
    else:
        feedback = variable_content_compare(variable_name, response_variable_content, answer_variable_content)
        return False, feedback

