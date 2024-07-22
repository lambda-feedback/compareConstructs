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
for i in range(5):
    print(i)"""

        answer = """
count = 0
while count < 5:
    print(count)
    count += 1"""
        result = evaluation_function(response, response, Params(is_unique_answer=False, is_ai_feedback=True, is_multiple_answers=False, has_output=True))
        assert result['is_correct']
        print(result['feedback'])


if __name__ == "__main__":
    unittest.main()
