import ast
import builtins


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
    exec(code_str, context)
    return {var: context.get(var) for var in variables}


def check_variable_content(response, answer, check_list):
    """
    Teacher should give a variable check-list for us due to the importance of the variables relying on the Teacher's goal
    TODO Implement content check in a method and class
    """
    response_var_dict = variable_content(response)
    answer_var_dict = variable_content(answer)
    # check whether they have the same variable names
    answer_var_set = answer_var_dict.keys()
    response_var_set = response_var_dict.keys()
    intersections = response_var_set & answer_var_set
    error_vars = []
    error_var_contents = []
    is_correct = True
    is_defined = True

    for var in check_list:
        if var not in intersections:
            error_vars.append(var)
            is_correct = False
        else:
            # sometimes execute the code doesn't change the variable value i.e. local variable in a method
            if answer_var_dict[var] is not None:

                if response_var_dict[var] != answer_var_dict[var]:
                    error_var_contents.append(var)
                    is_correct = False
            else:
                is_defined = False


    if is_correct:
        if is_defined:
            return True, ""
        else:
            return True, "NotDefined"
    else:
        feedback = ""
        if 0 < len(error_vars) < 2:
            feedback += f"""The variable '{"', '".join(error_vars)}' is not defined\n"""
        elif len(error_vars) >= 2:
            feedback += f"""The variables '{"', '".join(error_vars)}' are not defined\n"""
        if 0 < len(error_var_contents) < 2:
            feedback += f"""The value of '{"', '".join(error_var_contents)}' is not correct\n"""
        elif len(error_var_contents) >= 2:
            feedback += f"""The values of '{"', '".join(error_var_contents)}' are not correct\n"""
        return False, feedback




# response = """
#
# arr = []
# for i in range(4):
#     arr.append(i)"""
#
# answer = """
#
# arr = []
# i = 0
# while i < 4:
#     arr.append(i)
#     i += 1
# arr.append(3)"""
#
#
#
# check_list = ['arr', 'i']
# print(check_variable_content(response, answer, check_list))