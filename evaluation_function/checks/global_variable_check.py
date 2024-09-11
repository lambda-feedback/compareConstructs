import ast
import builtins
import traceback
import types
import numpy as np

try:
    from evaluation_function.checks.same_variable_content_check import check_same_content_with_different_variable
    from evaluation_function.checks.check_result import CheckResult
    from evaluation_function.format.variable_compare_format import variable_content_compare
except:
    from .same_variable_content_check import check_same_content_with_different_variable
    from .check_result import CheckResult
    from ..format.variable_compare_format import variable_content_compare

def check_global_variable_content(response_ast, answer_ast, check_list: set) -> CheckResult:
    """
    Teacher should give a variable check-list for us due to the
    importance of the variables relying on the Teacher's goal
    It will return the first error encountered
    """

    # get variable contents by executing the code
    response_result = variable_content(response_ast)
    answer_result = variable_content(answer_ast)

    if not answer_result.passed():
        return (
            CheckResult(False)
            .add_message(f"The given answer is wrong:\n{answer_result.message()}")
        )

    if not response_result.passed():
        return (
            CheckResult(False)
            .add_message(response_result.message())
        )

    response_var_values = response_result.get_payload("values")
    answer_var_values = answer_result.get_payload("values")

    # sometimes students give us different variable names, but we can figure out the difference
    response, response_var_dict = check_same_content_with_different_variable(
        response_var_values, answer_var_values, response_ast, answer_ast, check_list)

    # get the variable sets
    answer_var_set = answer_var_values.keys()
    response_var_set = response_var_dict.keys()
    intersections = response_var_set & answer_var_set

    # If the variables in checklist are not included in intersection, get wrong
    # any params in checklist should be declared with same value (could be different names)
    if not check_list <= intersections:
        remaining_variables = check_list - (check_list & intersections)
        if len(remaining_variables) == 1:
            import os
            feedback = f"The variable '{remaining_variables.pop()}' " \
                       f"is not defined or different value respect to the answer"\
                       f" PID = {os.getpid()}"
        else:
            feedback = f"""The variables '{"', '".join(list(remaining_variables))}' are not defined """ \
                       f"or different values respect to the answer"
        return CheckResult(False).add_message(feedback)

    for var in check_list:
        if answer_var_values.get(var) is not None:
            is_correct, feedback = is_equal(
                var, response_var_dict[var], answer_var_values[var])
            if not is_correct:
                return CheckResult(False).add_message(feedback)

    return CheckResult(True)


# Function to execute the code and check the content of variables
def variable_content(tree: ast.Module) -> CheckResult:
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
        exec(compile(tree, "<string>", "exec"), context)
    except SystemExit:
        pass
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)

        # Extract the last traceback entry to get the line number
        error_line = tb[-1].lineno
        return CheckResult(False).add_message(f"{type(e).__name__} at line {error_line}: {e}")

    variable_values = {
        var: context.get(var)
        for var in variables
        if not isinstance(context.get(var), types.FunctionType)
           and context.get(var) is not None
    }

    return CheckResult(True).add_payload("values", variable_values)


def is_equal(variable_name, response_variable_content, answer_variable_content):
    # TODO: add other equivalent relation:
    if type(response_variable_content) != type(answer_variable_content):
        return False, f"The type of '{variable_name}' is not correct. " \
                      f"Expected: {type(answer_variable_content).__name__}"

    is_correct = False
    if isinstance(answer_variable_content, np.ndarray):
        if np.shape(response_variable_content) == np.shape(answer_variable_content):
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
