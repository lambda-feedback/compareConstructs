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
Dx = 0.1
y = np.arange(-np.pi,2*np.pi+Dx,Dx)
Dt = 0.05
# define t range
t = np.arange(0,10+Dt,Dt)
# set meshgrids
(Yg, Xg, Tg) = np.meshgrid(y,x,t)
# compute r
r = np.sin(Xg)*np.cos(Yg) * np.exp(-0.5*Tg)
z=5
"""


        answer = """

import numpy as np
Dx = 0.1
x = np.arange(-2*np.pi,2*np.pi+Dx,Dx)
y = np.arange(-np.pi,2*np.pi+Dx,Dx)
Dt = 0.05
t = np.arange(0,10+Dt,Dt)
(Yg, Xg, Tg) = np.meshgrid(y,x,t)
r = np.sin(Xg)*np.cos(Yg) * np.exp(-0.5*Tg)
z = 5

"""
        check_list = "z"
        is_correct = True
        result = evaluation_function(response, answer, Params(check_list=check_list))
        print(result['is_correct'])
        print(result['feedback'])


if __name__ == "__main__":
    unittest.main()


