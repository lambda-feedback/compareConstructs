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
        # Verify that structures with the same parent names are not 
        # marked as correct (this would have returned true before)
        self.assertFalse(check_structure("""
def hello():
    def foo():
        pass
    def hello():
        def bar():
            pass
""", """
class hello:
    def foo():
        pass
    
    def bar():
        pass
    
    def hello():
        pass
"""))
        # Code with the same structure but different function/class
        # names should still be accepted.
        self.assertTrue(check_structure("""
class hello:
    def foo():
        pass
    
    def bar():
        pass
    
    def hello():
        pass
""", """
class lorem:
    def ipsum():
        pass
    
    def dolor():
        pass
    
    def sit():
        pass
"""))
        
    def test_structure_check_names(self):
        from .checks.structure_check import check_structure
        # These samples have the same structure but different names.
        # check_structure should mark them as different when 
        # check_names is True

        self.assertFalse(check_structure("""
class hello:
    def foo():
        pass
    
    def bar():
        pass
    
    def hello():
        pass
""", """
class lorem:
    def ipsum():
        pass
    
    def dolor():
        pass
    
    def sit():
        pass
""", check_names=True))
        


if __name__ == "__main__":
    unittest.main()


