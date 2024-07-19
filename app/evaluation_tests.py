import unittest

from .evaluation import Params, evaluation_function


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
        response1 = """
def hello():
    for i in range(5):
        if i == 3:
            print(i)
"""
        response2 = """
def hello():
    for i in range(5):
        if i == 3:
            print(i)
            return 2
"""
        result1 = evaluation_function(response1, "",
                                      Params(is_unique_answer=True, is_multiple_answers=False, is_ai_feedback=False, has_output=True))
        result2 = evaluation_function(response2, "",
                                      Params(is_unique_answer=True, is_multiple_answers=False, is_ai_feedback=False, has_output=True))
        assert result1['is_correct']
        assert result2['is_correct']


if __name__ == "__main__":
    unittest.main()
