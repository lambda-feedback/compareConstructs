import ast
from inspect import signature
import numpy as np

from evaluation_function.checks.check_result import CheckResult
from evaluation_function.format.variable_compare_format import get_array_feedback, WrongShape, WrongValue, WrongValueMultidimensional, WrongWhole, Equal


def check_func(response_ast: ast.Module, answer_ast: ast.Module, func_name: str) -> CheckResult:
    response_code = compile(response_ast, '<string>', 'exec')
    answer_code = compile(answer_ast, '<string>', 'exec')

    # Execute the response and answer code to set up the environment that the functions
    # expect, e.g. imports, global variables, etc.
    try:
        response_context = {}
        eval(response_code, response_context)
        answer_context = {}
        eval(answer_code, answer_context)
    except Exception as e:
        return (
            CheckResult(False)
            .add_message(f'Failed to evaluate response: {e}')
        )

    # Check that both the response and the answer declare a function called [func_name],
    # and both take the same number of arguments
    def func_exists(context):
        func = context.get(func_name, None)
        if callable(func):
            sig = signature(func)
            # Return the number of arguments the function needs
            return len(sig.parameters)
        else:
            return None

    num_response_args = func_exists(response_context)
    num_answer_args = func_exists(answer_context)
    if num_response_args == None:
        return (
            CheckResult(False)
            .add_message(f'Did you declare a function called "{func_name}"?')
        )
    if num_answer_args == None:
        return (
            CheckResult(False)
            .add_message(f'The answer does not declare a function called "{func_name}". Please contact your teacher.')
        )
    if num_response_args != num_answer_args:
        return (
            CheckResult(False)
            .add_message(f'The signature of "{func_name}" is incorrect. Try checking its arguments.')
        )

    # Extract the list of tests from the answer's context
    tests = answer_context.get('tests', None)
    if not tests:
        return CheckResult(False).add_message('No tests given in answer')
    if not isinstance(tests, list):
        return CheckResult(False).add_message('Tests must be a list of tuples')

    # Create an expression that calls the function with the given arguments.
    # This is parsed and compiled ahead of time for efficiency.
    # The star is not required if only one argument is needed.
    star = '' if num_response_args == 1 else '*'
    expr = compile(ast.parse(f'{func_name}({star}args)', mode='eval'), '<string>', 'eval')

    # Create a closure that tests for equality between the answer and the response.
    # By default, this just uses '==', but can be overridden.
    equals = lambda a, b: a == b
    equals_func = answer_context.get('equals', None)

    def equals_override(a, b):
        answer_context['_a'] = a
        answer_context['_b'] = b
        result = None
        try:
            result = eval(f'equals(_a, _b)', answer_context)
        except:
            return False
        return result

    if equals_func:
        if callable(equals_func):
            if len(signature(equals_func).parameters) != 2:
                return CheckResult(False).add_message('"equals" must take 2 arguments')
            equals = lambda a, b: equals_override(a, b)
        else:
            return CheckResult(False).add_message('"equals" must be callable')

    for args in tests:
        # Check that the number of arguments given and the number expected by 
        # the function are equal.
        if isinstance(args, tuple) and len(args) != num_response_args:
            return CheckResult(False).add_message('Incorrect test cases.')
        elif not isinstance(args, tuple) and num_response_args != 1:
            return CheckResult(False).add_message('Incorrect test cases.')

        # Add args as a global variable for the answer and response
        response_context['args'] = args
        answer_context['args'] = args

        # Evaluate the response function.
        response_val = None
        answer_val = None
        try:
            response_val = eval(expr, response_context)
            answer_val = eval(expr, answer_context)
        except Exception as e:
            return (
                CheckResult(False)
                .add_message(f'Failed to evaluate response: {e}')
            )
        
        # The answer and response must be the same type
        response_type = type(response_val)
        answer_type = type(answer_val)
        if response_type != answer_type:
            return (
                CheckResult(False)
                .add_message(f'The types do not match: your function returned a "{response_type}", but a "{answer_type}" was required.')
            )

        # Special case if the value is an array
        if response_type == list or response_type == np.ndarray:
            f = get_array_feedback(response_val, answer_val)
            match f:
                case WrongValue(idx, req_val, act_val):
                    return (
                        CheckResult(False)
                        .add_message(f'There is an incorrect value at index {idx}: Expected {req_val}, got {act_val}')
                    )
                case WrongShape(res_shape, ans_shape):
                    return (
                        CheckResult(False)
                        .add_message(f'Your array has the wrong shape: Expected {ans_shape}, got {res_shape}')
                    )
                case WrongValueMultidimensional(idx, req_val, act_val):
                    return (
                        CheckResult(False)
                        .add_message(
                            f'The multi-dimensional array returned has the correct shape, but an incorrect value at {f.error_index}.\n'
                            f'Expected {req_val}, got {act_val}'
                        )
                    )
                case WrongWhole(_):
                    return (
                        CheckResult(False)
                        .add_message(f'Your array is incorrect: Expected f{answer_val}, got f{response_val}')
                    )
                case Equal(_):
                    pass

        elif not equals(answer_val, response_val):
            return (
                CheckResult(False)
                .add_message(f'wanted {answer_val}, got {response_val}')
            )
        
    return CheckResult(True)
