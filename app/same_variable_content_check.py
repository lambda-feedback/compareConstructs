import ast
import astor
import numpy as np
import copy

def check_same_content_with_different_variable(response, check_list, response_var_dict: dict, answer_var_dict: dict):
    """
    The method is called when students input different variable names with the same content,
    and we try to figure the similarities and replace the response to the desired (same) variable names for checklist
    """

    answer_var_set = answer_var_dict.keys()
    response_var_set = response_var_dict.keys()
    intersection = answer_var_set & response_var_set
    response_diff = response_var_set - intersection
    answer_diff = answer_var_set - intersection

    for answer_key in answer_diff:
        answer_val = answer_var_dict[answer_key]
        if answer_key in check_list:
            for response_key in response_diff:
                response_val = response_var_dict[response_key]
                if is_equal(response_val, answer_val) and answer_key != response_key:
                    del response_var_dict[response_key]
                    response_var_dict[answer_key] = answer_val
                    response = replace_variable_in_code(response, response_key, answer_key)
                    response_diff.remove(response_key)
                    response_diff.add(answer_key)

    return response, response_var_dict


class VariableRenamer(ast.NodeTransformer):
    def __init__(self, old_name, new_name):
        self.old_name = old_name
        self.new_name = new_name

    def visit_Name(self, node):
        # Check if the name is in a Store context (assignment, for loop target, etc.)
        if isinstance(node.ctx, (ast.Store, ast.Load)) and node.id == self.old_name:
            node.id = self.new_name
        return node


def replace_variable_in_code(code, old_name, new_name):
    tree = ast.parse(code)
    renamer = VariableRenamer(old_name, new_name)
    tree = renamer.visit(tree)
    ast.fix_missing_locations(tree)
    return astor.to_source(tree)


def is_equal(response_variable_content, answer_variable_content):
    if type(response_variable_content) != type(answer_variable_content):
        return False
    if isinstance(answer_variable_content, np.ndarray):
        try:
            is_correct = np.allclose(response_variable_content, answer_variable_content)
        except Exception:
            return False
        return is_correct



    else:
        try:
            is_correct = response_variable_content == answer_variable_content
        except Exception:
            return False
        return is_correct


if __name__ == '__main__':
    response = """
    
    
    """

    new_code = replace_variable_in_code(response, 'i', 'idx')
    print(new_code)
