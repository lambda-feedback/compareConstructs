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

    def test_general_eval(self):
        response = """
x = 1
y = 2
"""
        answer = """
x = 1
y = 3
"""
        check_list = "x,y"
        is_correct = False
        result = evaluation_function(response, answer, Params(check_list=check_list))
        print(result['is_correct'])
        print(result['feedback'])


if __name__ == "__main__":
    unittest.main()


