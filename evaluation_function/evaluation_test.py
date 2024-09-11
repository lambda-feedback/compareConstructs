import ast
import unittest

try:
    from .evaluation import Params, evaluation_function
except ImportError:
    from evaluation import Params, evaluation_function


class TestEvaluationFunction(unittest.TestCase):
    """
    TestCase Class used to test the algorithm.
    ---
    Tests are used here to check that the algorithm written
    is working as it should.
    It's best practise to write these tests first to get a
    kind of 'specification' for how your algorithm should
    work, and you should run these tests before committing
    your code to AWS.
    Read the docs on how to use unittest here:
    https://docs.python.org/3/library/unittest.html
    Use evaluation_function() to check your algorithm works
    as it should.
    """
    
    def test_structure_check(self):
        from .checks.structure_check import check_structure
        import ast
        # Verify that structures with the same parent names are not 
        # marked as correct (this would have returned true before)
        self.assertFalse(check_structure(ast.parse("""
def hello():
    def foo():
        pass
    def hello():
        def bar():
            pass
"""), ast.parse("""
class hello:
    def foo():
        pass
    
    def bar():
        pass
    
    def hello():
        pass
""")).passed())
        # Code with the same structure but different function/class
        # names should still be accepted.
        self.assertTrue(check_structure(ast.parse("""
class hello:
    def foo():
        pass
    
    def bar():
        pass
    
    def hello():
        pass
"""), ast.parse("""
class lorem:
    def ipsum():
        pass
    
    def dolor():
        pass
    
    def sit():
        pass
""")).passed())
        
    def test_structure_check_names(self):
        from .checks.structure_check import check_structure
        import ast
        # These samples have the same structure but different names.
        # check_structure should mark them as different when 
        # check_names is True

        self.assertFalse(check_structure(ast.parse("""
class hello:
    def foo():
        pass
    
    def bar():
        pass
    
    def hello():
        pass
"""), ast.parse("""
class lorem:
    def ipsum():
        pass
    
    def dolor():
        pass
    
    def sit():
        pass
"""), check_names=True).passed())
    
    def test_syntax_check(self):
        from .checks.general_check import check_style

        # This sample is correct, so it should pass the check
        self.assertTrue(check_style("print('Hello, World!')").passed())
        # This sample has a missing quote, so it should fail
        check_result = check_style("print('Hello, World!)")
        self.assertFalse(check_result.passed())
        self.assertTrue(len(check_result.message()) != 0)
    
    def test_answer_validate(self):
        from .checks.general_check import validate_answer

        # This sample is correct, so it should pass the check
        validate_result = validate_answer("print('Hello, World!')")
        self.assertTrue(validate_result.passed())
        # This sample's syntax is correct, but it will cause a runtime error
        self.assertFalse(validate_answer("foo('Hello, World!')").passed())
        # This sample's syntax is incorrect
        self.assertFalse(validate_answer("print('Hello, World!)").passed())

    def test_check_func(self):
        from .checks.func_check import check_func
        import ast

        response = """
def sum(a, b):
    return a - (-b)
"""
        answer = """
def sum(a, b):
    return a + b

tests = [
    (0, 0),
    (1, 1),
    (100, 165),
    (730, 21),
]
"""
        # All the test cases should pass, so this should return True
        result = check_func(ast.parse(response), ast.parse(answer), "sum")
        self.assertTrue(result.passed())

        response = """
def sum(a, b):
    return a - b
"""
        # The response function no longer acts as it should, so this should fail
        result = check_func(ast.parse(response), ast.parse(answer), "sum")
        self.assertFalse(result.passed())

        response = """
def sum(a, b, c):
    return a + b
"""
        # This response works, but the function has the wrong signature
        result = check_func(ast.parse(response), ast.parse(answer), "sum")
        self.assertFalse(result.passed())

        response = """
def foo(a, b):
    return a + b
"""
        # No function called "sum" is declared
        result = check_func(ast.parse(response), ast.parse(answer), "sum")
        self.assertFalse(result.passed())
    
    def test_check_func_with_globals(self):
        from .checks.func_check import check_func
        import ast

        # Functions should be able to use globals, including imports

        response = """
import numpy
n = 10
def test(a):
    return numpy.full(n, a)
"""
        answer = """
import numpy
def test(a):
    return numpy.full(10, a)

def equals(a, b):
    return numpy.allclose(a, b)

tests = [
    0,
    1,
    2,
    3,
    4,
]
"""
        # All the test cases should pass, so this should return True
        result = check_func(ast.parse(response), ast.parse(answer), "test")
        self.assertTrue(result.passed())

    def test_func_check_eval(self):
        response = """
def sum(a, b):
    return a - (-b)
"""
        answer = """
def sum(a, b):
    return a + b

tests = [
    (0, 0),
    (1, 1),
    (100, 165),
    (730, 21),
]
"""
        result = evaluation_function(response, answer, Params(check_func="sum"))
        print(result["feedback"])
        self.assertTrue(result['is_correct'])

    def test_output(self):
        response = "print(0.0)"
        answer = "print(0)"
        result = evaluation_function(response, answer, Params(output_eval=True))
        self.assertTrue(result['is_correct'])

        response = "print(-0.4597640704689031)"
        answer = "print(-0.45976407046890333)"
        result = evaluation_function(response, answer, Params(output_eval=True))
        self.assertTrue(result['is_correct'])

    def test_func_check_dynamic(self):
        from .checks.func_check import check_func
        import ast
        response = """
def sum(a, b):
    return a + b
"""
        answer = """
from random import randint

def sum(a, b):
    return a + b

tests = [(randint(0, 10), randint(0, 10)) for _ in range(1000)]
"""
        # check_func should support dynamic generation of test cases
        result = check_func(ast.parse(response), ast.parse(answer), "sum")
        self.assertTrue(result.passed())

    def test_array_feedback(self):
        from .format.variable_compare_format import get_array_feedback
        from .format.variable_compare_format import WrongShape, WrongValue, WrongWhole, WrongValueMultidimensional, Equal
        from .format import variable_compare_format
        import numpy as np

        # Set the max string size to a small value for testing
        variable_compare_format.MAX_STRING_LEN = 10

        # These arrays are equal, so Equal() should be returned
        a = np.array([0, 1, 2, 3, 4])
        b = np.array([0, 1, 2, 3, 4])
        feedback = get_array_feedback(a, b)
        if not isinstance(feedback, variable_compare_format.Equal):
            self.fail(type(feedback))
        # These arrays are equal until index 3
        a = np.array([0, 1, 2, 3, 4])
        b = np.array([0, 1, 2, 4, 4])
        feedback = get_array_feedback(a, b)
        if isinstance(feedback, WrongValue):
            self.assertEqual(feedback.error_index, 3)
            self.assertEqual(feedback.required_value, 4)
            self.assertEqual(feedback.actual_value, 3)
        else:
            self.fail(feedback)
        # These arrays are not equal, but they are shorter than MAX_STRING_LEN
        a = np.array([0, 1, 2])
        b = np.array([0, 1, 3])
        feedback = get_array_feedback(a, b)
        if not isinstance(feedback, WrongWhole):
            self.fail(feedback)
        # These arrays have different shapes
        a = np.array([[0, 0], [1, 1], [2, 2], [3, 3]])
        b = np.array([0, 1, 2, 3])
        feedback = get_array_feedback(a, b)
        if isinstance(feedback, WrongShape):
            self.assertEqual(feedback.response_shape, (4, 2))
            self.assertEqual(feedback.answer_shape, (4,))
        else:
            self.fail(feedback)
        # These arrays are multidimensional but equal
        a = np.array([[0, 0], [1, 1], [2, 2], [3, 3]])
        b = np.array([[0, 0], [1, 1], [2, 2], [3, 3]])
        feedback = get_array_feedback(a, b)
        if not isinstance(feedback, Equal):
            self.fail(feedback)
        # These arrays are multidimensional but unequal
        a = np.array([[0, 0], [1, 1], [2, 2], [3, 3]])
        b = np.array([[0, 0], [1, 1], [2, 2], [3, 2]])
        feedback = get_array_feedback(a, b)
        if not isinstance(feedback, WrongValueMultidimensional):
            self.fail(feedback)
    
    def test_global_var_check(self):
        import ast
        from .checks.global_variable_check import check_global_variable_content
        # The simplest case of only one global variable
        answer = ast.parse("""Lambda = 'Feedback'""")
        response = ast.parse("Lambda = 'Fedback'")
        result = check_global_variable_content(response, answer, {"Lambda"})
        self.assertFalse(result.passed())
        answer = ast.parse("""Lambda = 'Feedback'""")
        response = ast.parse("Lambda = 'Feedback'")
        result = check_global_variable_content(response, answer, {"Lambda"})
        self.assertTrue(result.passed())

        # Multiple variables
        answer = """
test1 = 42
test2 = "Hello!"
"""
        response = """
test1 = 41 + 1
test2 = "He" + "llo!"
"""
        result = check_global_variable_content(ast.parse(response), ast.parse(answer), {"test1", "test2"})
        self.assertTrue(result.passed())
        # Should also work when invoked through evaluation_function
        result = evaluation_function(response, answer, {"global_variable_check_list": ["test1", "test2"]})
        print(result["feedback"])
        self.assertTrue(result["is_correct"])

    def test_error_message_in_variable(self):
        from .checks.global_variable_check import variable_content
        string_code = """
def f(x):
    return i
test1 = "abcd"
test2 = f(2)
test3 = 2
"""
        result = variable_content(ast.parse(string_code))
        self.assertTrue("line 3" in result.message())

    def test_sandbox(self):
        import os
        # Only run this test if NO_SANDBOX=0
        if int(os.environ.get("NO_SANDBOX", "0")) == 1:
            return
        # This test will only work on Unix
        if os.name != "posix":
            return

        answer = "print('Hello, World')"
        # This file shouldn't exist in the sandbox, will if running on a Linux system if it doesn't work.
        response = """
with open("/bin/bash", "r") as f: 
    print("Hello, World")
"""
        result = evaluation_function(response, answer, {})
        self.assertFalse(result["is_correct"])

if __name__ == "__main__":
    unittest.main()