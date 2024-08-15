"""
The script is used only the Teacher forgets to input the check_list, or lacking of global variables
"""
import re
import ast
import sys
import types
import itertools
import astor

try:
    from .global_variable_check import variable_content, check_global_variable_content
    from .format import local_missing_modules_and_variables_format
    from .param_generator import param_generator, guess_param_type
    from .same_variable_content_check import check_same_content_with_different_variable
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
                body_ast = ast.parse(''.join(astor.to_source(node) for node in node.body))
                transformer = ReturnToExitTransformer()
                transformed_ast = transformer.visit(body_ast)
                body = astor.to_source(transformed_ast)
                self.method_params_and_body_list[method_name] = (args, body)
            self.generic_visit(node)


class ReturnToExitTransformer(ast.NodeTransformer):
    def visit_Return(self, node):
        assign_node = ast.Assign(
            targets=[ast.Name(id='TMP', ctx=ast.Store())],
            value=node.value
        )
        exit_node = ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='sys', ctx=ast.Load()),
                    attr='exit',
                    ctx=ast.Load()
                ),
                args=[],
                keywords=[]
            )
        )
        return [assign_node, exit_node]


def extract_params_and_body(code_str):
    astree = ast.parse(code_str)
    extractor = MethodParamBodyExtractor(astree)
    extractor.visit(astree)
    return extractor.method_params_and_body_list


# code = """
# def example_function(x):
#     return x ** 2 + 1
# """
# print(extract_params_and_body(code))

def check_local_variable_content(response, answer, check_list: list):
    """
    TODO The checklist will be randomly generated when the checklist is empty (it's teachers' input)
    otherwise, the local variable will be checked

    """
    answer_method_params_and_body_list = extract_params_and_body(answer)
    response_method_params_and_body_list = extract_params_and_body(response)

    # only the same function name will be checked
    method_names = answer_method_params_and_body_list.keys() & response_method_params_and_body_list.keys()

    remaining_check_list = check_list
    feedback = ""

    # it still needs to check the global variable content at first
    response_var_dict = variable_content(response)
    answer_var_dict = variable_content(answer)

    for method_name in method_names:
        # add sys to the dict, it changes locally but not globally
        response_var_dict['sys'] = sys
        answer_var_dict['sys'] = sys
        response_arg_list, response_body = response_method_params_and_body_list[method_name]
        answer_arg_list, answer_body = answer_method_params_and_body_list[method_name]

        # add all variables globally to the local variables
        response_modules, response_var_dict = extract_modules(response_var_dict)
        answer_modules, answer_var_dict = extract_modules(answer_var_dict)

        global_response_variable_content = local_missing_modules_and_variables_format(
            response_modules, response_var_dict)
        global_answer_variable_content = local_missing_modules_and_variables_format(
            answer_modules, answer_var_dict)

        # If the input parameter is not given, we need to generate some of them
        if 0 < len(answer_arg_list) == len(response_arg_list):

            # get the params dict with name and possible types
            answer_params_dict = {param: guess_param_type(param, answer_body) for param in answer_arg_list}
            response_params_dict = {param: guess_param_type(param, response_body) for param in response_arg_list}
            response_body, response_params_dict = check_same_content_with_different_variable(
                response_body, response_params_dict, answer_params_dict, mode='param')

            if response_params_dict != answer_params_dict:
                if method_name in remaining_check_list:
                    return False, f"The arguments of the method {method_name} are not correct: check inputs and types of the params"
                return True, "NotDefined"
            param_result_dict = param_generator(answer_arg_list, answer_body)
            # There are tiny probability that the generated answer is false positive
            correct_count = 0
            false_count = 0
            is_next = False

            for _ in range(5):

                for choice in permutation(param_result_dict):
                    if is_next:
                        break
                    response_params_msg = "\n".join(f"{key}={value}" for key, value in choice.items())
                    answer_params_msg = "\n".join(f"{key}={value}" for key, value in choice.items())
                    response_body = f"{global_response_variable_content}\n{response_params_msg}\n{response_body}"
                    answer_body = f"{global_answer_variable_content}\n{answer_params_msg}\n{answer_body}"
                    remaining_check_list.append("TMP")
                    is_correct, feedback, remaining_check_list, response_body = \
                        check_global_variable_content(response_body, answer_body, remaining_check_list)

                    response_var_dict = variable_content(response_body)
                    answer_var_dict = variable_content(answer_body)
                    response_var_dict = {k: v for k, v in response_var_dict.items() if
                                         k not in list(response_params_dict.keys()) and k != "TMP"}
                    answer_var_dict = {k: v for k, v in answer_var_dict.items() if
                                       k not in answer_arg_list and k != "TMP"}

                    # only correct when there is no execution err (WellDefined), no remaining check list, and correct
                    if is_correct and feedback != "NotDefined":
                        if correct_count > 1:
                            if method_name in remaining_check_list:
                                remaining_check_list.remove(method_name)
                            if len(remaining_check_list) == 0:
                                return True, ""
                            else:

                                is_next = True
                        correct_count += 1
                    elif not is_correct and feedback != "NameError":
                        false_count += 1
                    if false_count > 1:
                        if feedback != "NameError" and method_name in remaining_check_list:
                            return False, f"The method {method_name} is not correct: {feedback}"



        else:
            response_body = f"{global_response_variable_content}\n{response_body}"
            answer_body = f"{global_answer_variable_content}\n{answer_body}"

            remaining_check_list.append("TMP")

            response_var_dict.update(variable_content(response_body))
            answer_var_dict.update(variable_content(answer_body))
            is_correct, feedback, remaining_check_list, response_body = check_global_variable_content(response_body,
                                                                                                      answer_body,
                                                                                                      remaining_check_list)
            # response might have different argument input and execution error
            if feedback == "NameError":
                return False, f"The arguments of the method {method_name} are not correct: check inputs and types of the params"
            if feedback == "NotDefined":
                return True, feedback
            if not is_correct:
                return False, feedback
            else:
                if method_name in remaining_check_list:
                    remaining_check_list.remove(method_name)

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


def permutation(param_dict):
    filtered_params = [p for p in param_dict.values() if p]
    empty_params_dict = {k: [] for k, v in param_dict.items() if not v}

    permutations = itertools.product(*filtered_params)
    keys = [k for k, v in param_dict.items() if v]
    perm_dict_list = [{**dict(zip(keys, permutation)), **empty_params_dict} for permutation in permutations]
    return perm_dict_list
