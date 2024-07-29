"""
The script is used only the Teacher forgets to input the check_list, or lacking of global variables
"""
import re
import ast
import sys
import types

import astor

try:
    from .global_variable_check import variable_content, check_global_variable_content
    from .format import local_missing_modules_and_variables_format
except:
    from global_variable_check import variable_content, check_global_variable_content
    from format import local_missing_modules_and_variables_format


class MethodParamBodyExtractor(ast.NodeVisitor):

    def extract_method_names(self, astree):

        for child in ast.iter_child_nodes(astree):

            if isinstance(child, ast.FunctionDef):
                self.method_list.append(child.name)
                self.extract_method_names(child)

    def __init__(self, astree):
        self.method_params_and_body_list = {}
        self.method_list = []
        self.extract_method_names(astree)

    def visit_FunctionDef(self, node):
        for method_name in self.method_list:
            if node.name == method_name:
                args = [arg.arg for arg in node.args.args]
                body = ''.join(astor.to_source(node) for node in node.body)
                pattern = r'\breturn\b.*'
                # Replace matched 'return' with 'sys.exit()'
                body = re.sub(pattern, 'sys.exit()', body)
                self.method_params_and_body_list[method_name] = (args, body)
            self.generic_visit(node)


def extract_params_and_body(code_str):
    astree = ast.parse(code_str)
    extractor = MethodParamBodyExtractor(astree)
    extractor.visit(astree)
    return extractor.method_params_and_body_list


def check_local_variable_content(response, answer, check_list: list):
    """
    TODO The checklist will be randomly generated when the checklist is empty (it's teachers' input)
    otherwise, the local variable will be checked

    """
    answer_method_params_and_body_list = extract_params_and_body(answer)
    response_method_params_and_body_list = extract_params_and_body(response)
    method_names = answer_method_params_and_body_list.keys()
    remaining_check_list = check_list
    feedback = ""

    # it still needs to check the global variable content at first
    response_var_dict = variable_content(response)
    answer_var_dict = variable_content(answer)

    # add sys to the dict, it changes locally but not globally
    response_var_dict['sys'] = sys
    answer_var_dict['sys'] = sys

    for method_name in method_names:
        response_arg_list, response_body = response_method_params_and_body_list[method_name]
        answer_arg_list, answer_body = answer_method_params_and_body_list[method_name]
        is_correct, feedback, remaining_check_list, response = check_global_variable_content(response_body, answer_body,
                                                                                             remaining_check_list)

        # sometimes local variables are defined in the outer scope
        if feedback == "NameError":
            response_modules, response_var_dict = extract_modules(response_var_dict)
            answer_modules, answer_var_dict = extract_modules(answer_var_dict)
            global_response_variable_content = local_missing_modules_and_variables_format(
                response_modules, response_var_dict, response_arg_list)
            global_answer_variable_content = local_missing_modules_and_variables_format(
                answer_modules, answer_var_dict, answer_arg_list)



            is_correct, feedback, remaining_check_list, response = check_global_variable_content(response_body,
                                                                                                 answer_body,
                                                                                                 remaining_check_list,
                                                                                                 global_response_variable_content,
                                                                                                 global_answer_variable_content)
            if feedback == "NotDefined":
                return True, feedback
            response_body = f"{global_response_variable_content}\n{response}"
            answer_body = f"{global_answer_variable_content}\n{answer}"
            response_var_dict.update(variable_content(response_body))
            answer_var_dict.update(variable_content(answer_body))
        else:
            is_correct, feedback, remaining_check_list = check_global_variable_content(response_body, answer_body,
                                                                                       remaining_check_list)
            response_var_dict.update(variable_content(response_body))
            answer_var_dict.update(variable_content(answer_body))

        if not is_correct:
            return False, feedback

    if len(remaining_check_list) == 0:
        return (True, "") if feedback != "NotDefined" else (True, feedback)
    else:
        if len(remaining_check_list) == 1:
            return False, f"The variable of {remaining_check_list[0]} is not defined"
        else:
            return False, f"""The variable of '{"', '".join(remaining_check_list)}' is not defined"""


def extract_modules(var_dict):

    modules = []
    for var_name, module_part in var_dict.items():
        if isinstance(module_part, types.ModuleType):
            modules.append((var_name, module_part.__name__))
    for var_name, _ in modules:
        del var_dict[var_name]
    return modules, var_dict
