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
import numpy as np
Dx = 0.1
x = np.arange(-2*np.pi,2*np.pi+Dx,Dx)
y = np.arange(-np.pi,2*np.pi+Dx,Dx)
(Xg, Yg) = np.meshgrid(x,y)

# compute f and g
f_xy = np.sin(Xg)*np.cos(Yg)
g_xy = np.cos(Xg)*np.sin(Yg)

# B2
# compute s and p
s = f_xy + g_xy
p = f_xy * g_xy
"""


        answer = """
import numpy as np
Dx = 0.1
x = np.arange(-2*np.pi,2*np.pi+Dx,Dx)
y = np.arange(-np.pi,2*np.pi+Dx,Dx)
(Xg, Yg) = np.meshgrid(x,y)
print(len(x))
print(len(y))
print(np.shape(Xg))
print(np.shape(Yg))
f = np.sin(Xg)*np.cos(Yg)
g = np.cos(Xg)*np.sin(Yg)
s = f + g
p = f * g
"""
        result = evaluation_function(response, answer, Params(check_list="x,y,f,g,s,p"))
        print(result['is_correct'])
        print(result['feedback'])


if __name__ == "__main__":
    unittest.main()


