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
import matplotlib.pyplot as pl
start = -5
end = -2
step = 0.5

num_points = int((end - start) / step) + 1

# Generate the same array using np.linspace
x1 = np.linspace(start, end, num_points)
x2 = np.arange(-2+0.05, 3, 0.05)
x3 = np.arange(3, 5+0.5, 0.5)
x = np.concatenate((x1, x2, x3))
f = np.sin(x)
g = np.sin(x**2+np.pi)

"""


        answer = """
import numpy as np
import matplotlib.pyplot as pl
Dx = 0.5
x1 = np.arange(-5,-2+Dx,Dx)

Dx = 0.05
x2 = np.arange(-2+Dx,3,Dx)

Dx = 0.5
x3 = np.arange(3,5+Dx,Dx)

x = np.hstack((x1,x2,x3))

fx = np.sin(x)
gx = np.sin(x**2+np.pi)
pl.scatter(x,fx,c='red',marker='d')
pl.scatter(x,gx,c='magenta',marker='o')
"""
        result = evaluation_function(response, answer, Params(check_list="x,fx,gx"))
        print(result['is_correct'])
        print(result['feedback'])


if __name__ == "__main__":
    unittest.main()


