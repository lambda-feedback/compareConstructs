import ast
from inspect import signature

from .check_result import CheckResult

def check_func(response_ast: ast.Module, answer_ast: ast.Module, func_name: str) -> CheckResult:
    response_code = compile(response_ast, '<string>', 'exec')
    answer_code = compile(answer_ast, '<string>', 'exec')
    
    # Execute the response and answer code to set up the environment that the functions
    # expect, e.g. imports, global variables, etc.
    response_context = {}
    eval(response_code, response_context)
    answer_context = {}
    eval(answer_code, answer_context)
    
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
    if not num_response_args:
        return (
            CheckResult(False)
            .add_message(f'did you declare a function called "{func_name}"?')
        )
    if not num_answer_args:
        return (
            CheckResult(False)
            .add_message(f'the answer does not declare a function called "{func_name}". Please contact your teacher.')
        )
    if num_response_args != num_answer_args:
        return (
            CheckResult(False)
            .add_message(f'the signature of "{func_name}" is incorrect. Try checking its arguments.')
        )

    # Extract the list of tests from the answer's context
    tests = answer_context.get('tests', None)
    if not tests:
        return CheckResult(False).add_message('no tests given in answer')
    if not isinstance(tests, list):
        return CheckResult(False).add_message('tests must be a list of tuples')

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
        return eval(f'equals(_a, _b)', answer_context)

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
            return CheckResult(False).add_message('incorrect test cases.')
        elif not isinstance(args, tuple) and num_response_args != 1:
            return CheckResult(False).add_message('incorrect test cases.')

        # Add args as a global variable for the answer and response
        response_context['args'] = args
        answer_context['args'] = args

        # Evaluate the response function.
        response_val = eval(expr, response_context)
        answer_val = eval(expr, answer_context)
        
        if not equals(answer_val, response_val):
            return (
                CheckResult(False)
                .add_message(f'wanted {answer_val}, got {response_val}')
            )

    return CheckResult(True)
