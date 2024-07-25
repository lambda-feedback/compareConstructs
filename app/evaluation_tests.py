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
arr1 = []
def hi():
    arr2 = []
    arr1.append(1)
arr1.append(3)
def hello():
    arr1.append(2)
hello()
"""


        answer = """
arr1 = []
def hi():
    arr2 = []
    arr1.append(2)
arr1.append(3)
def hello():
    arr1.append(1)
hi()
"""
        result = evaluation_function(response, answer, Params(check_list=['arr1', 'arr2']))
        print(result['is_correct'])
        print(result['feedback'])


if __name__ == "__main__":
    unittest.main()


