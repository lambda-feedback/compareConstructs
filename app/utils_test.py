import unittest

from .utils import *


class TestUtilsFunction(unittest.TestCase):
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

    def test_general_check(self):
        response1 = """
def hello():
 print(1)
  print()
"""
        response2 = """
def hello():
    for i in range(5):
        if i == 3:
            print(i)
            return 2
        """
        response3 = """
def hello():
    print()
      print()     
"""

        is_syntax_correct1, _ = check_syntax(response1)
        assert not check_indents(response1)
        assert not is_syntax_correct1

        is_syntax_correct2, _ = check_syntax(response2)
        assert check_indents(response2)
        assert check_syntax(response2)

        is_syntax_correct3, _ = check_syntax(response3)
        assert not check_indents(response3)
        assert not is_syntax_correct3


if __name__ == "__main__":
    unittest.main()
