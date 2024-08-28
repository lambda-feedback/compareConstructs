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
    def test_eval(self):
        response = """
def hi():
    return "hi"

def f(x, y):
    return x ** 2 + y **  3
        """

        answer = """
def hi():
    return "hillo"[0:2]

def f(x, y):
    return x * x + y ** 3

            """
        check_list = ['f', 'hi']

        result = evaluation_function(response, answer, Params(check_list=check_list))
        self.assertTrue(result['is_correct'])
    
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
        self.assertEqual(validate_result.get_payload("correct_output"), "Hello, World!\n")
        # This sample's syntax is correct, but it will cause a runtime error
        self.assertFalse(validate_answer("foo('Hello, World!')").passed())
        # This sample's syntax is incorrect
        self.assertFalse(validate_answer("print('Hello, World!)").passed())

    def test_general(self):
        response = """
a=3"""
        answer = """
a=2"""
        print(evaluation_function(response, answer, Params(check_list="a", check_names=False)))


if __name__ == "__main__":
    unittest.main()


