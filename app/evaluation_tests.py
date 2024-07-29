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

def trapzeqd(x,y):
    # get the interval h: distance between any two consecutives nodes
    h = x[1] - x[0]
    # get the number of intervals
    N = len(x) - 1  # obviously x and y must have same length
    
    # compute the integral
    
    # compute the sum for the intermediate points
    S = 0.0
    for n in range(1,N):
        S += y[n]  # add the current calue of y
    # add first and last points: see the formula for trapezoidal method
    I = h * (y[0]/2 + S + y[-1]/2 )
    
    # an alternative approach, with slicing and the function np.sum(), the integral can be computed within one line
    I = h * (y[0]/2 + np.sum(y[1:-1]) + y[-1]/2 )
    
    return I

# make it different

def f(x):
    y = 1/np.sqrt(x**17.10+2023)
    #y = 1/np.sqrt(x**1.10+2023)
    #y = np.sin(x)
    return y

"""


        answer = """
import numpy as np

def trapzeqd(x,y):
    # get the interval h: distance between any two consecutives nodes
    h = x[1] - x[0]
    # get the number of intervals
    N = len(x) - 1  # obviously x and y must have same length
    
    # compute the integral
    
    # compute the sum for the intermediate points
    S = 0.0
    for n in range(1,N):
        S += y[n]  # add the current calue of y
    # add first and last points: see the formula for trapezoidal method
    I = h * (y[0]/2 + S + y[-1]/2 )
    
    # an alternative approach, with slicing and the function np.sum(), the integral can be computed within one line
    I = h * (y[0]/2 + np.sum(y[1:-1]) + y[-1]/2 )
    
    return I
    
def f(x):
    y = 1/np.sqrt(x**17.10+2023)
    #y = 1/np.sqrt(x**1.10+2023)
    #y = np.sin(x)
    return y
    


"""
        check_list = ""
        is_correct = True
        result = evaluation_function(response, answer, Params(check_list=check_list))
        assert is_correct == result['is_correct']
        print(result['feedback'])


if __name__ == "__main__":
    unittest.main()


