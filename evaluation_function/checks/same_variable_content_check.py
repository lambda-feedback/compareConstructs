import ast
import astor
import numpy as np


def check_same_content_with_different_variable(response_var_dict: dict, answer_var_dict: dict,
                                               res_ast, ans_ast, check_list: set):
    """
    The method is called when students input different variable names with the same content,
    and we try to figure the similarities and replace the response to the desired (same) variable names for checklist
    """

    answer_var_set = answer_var_dict.keys()
    response_var_set = response_var_dict.keys()
    intersection = answer_var_set & response_var_set
    response_diff = response_var_set - intersection
    answer_diff = answer_var_set - intersection

    response = ""

    for answer_key in answer_diff:
        answer_val = answer_var_dict[answer_key]

        changed_dict = {}

        if answer_key in check_list:
            for response_key in response_diff:
                response_val = response_var_dict[response_key]
                if is_equal(response_val, answer_val) and answer_key != response_key:
                    response = replace_variable_in_code(response_key, answer_key, ans_ast)
                    changed_dict.update({response_key: answer_key})
                    break

        for old, new in changed_dict.items():
            response_diff.discard(old)
            del response_var_dict[old]
            response_var_dict[new] = answer_val
    return response, response_var_dict


def replace_variable_in_code(old_name, new_name, tree):
    class VariableRenamer(ast.NodeTransformer):
        def __init__(self, old_name, new_name):
            self.old_name = old_name
            self.new_name = new_name

        def visit_Name(self, node):
            # Check if the name is in a Store context (assignment, for loop target, etc.)
            if isinstance(node.ctx, (ast.Store, ast.Load)) and node.id == self.old_name:
                node.id = self.new_name
            return node

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


def replace_keys(original_dict, replacement_dict):
    # Create a reverse mapping from values to new keys
    value_to_new_key = {v: k for k, v in replacement_dict.items()}

    # Construct the new dictionary
    new_dict = {value_to_new_key.get(v, k): v for k, v in original_dict.items()}

    return new_dict
