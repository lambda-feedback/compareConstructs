# Function Check

## Motivation

This function, implemented in `checks/func_check.py`, subjects a function written by a student to a list of 
tests provided by the teacher. This ensures that the implementation of the function is correct for any valid
arguments, and because the students do not know what these tests will be, they cannot "cheat" or write 
over-specialised code.

## Implementation

When this check is used (if the `check_func` field is set in the [parameters](parameters.md)), the answer 
provided by the teacher is interpreted differently. It must contain at least two items:
- A function with the same name as the `check_func` parameter, which provides a "reference implementation"
  that all the tests are run against. 
- A variable called `tests`, which is a list of tuples. Each tuple represents an individual test case, and the
  values in the tuple are the arguments that will be passed to the function for each case. If the function takes
  only one argument, it is not necessary to wrap it in a tuple.

For each test case in the `tests` variable, the student's response function and the reference function will both
be evaluated with the arguments for that case. Their return values will then be compared.

By default, this comparison is done using the `==` operator, and there is a built-in special case for
NumPy arrays. If a more advanced comparison is required, the answer can include a function called `equals`.
This function takes two arguments and returns a boolean indicating if its arguments were considered equal.
If this function is present, it is always used instead of the built-in comparisons.

If the output of the two functions is equal for each test case, the student's response will be marked correct.

## Example

An example question might test a trivial function called `sum` that simply adds together its two arguments. 
The answer for this question might be the following:
```python
def sum(a, b):
    return a + b

tests = [
    (0, 0),
    (1, 0),
    (100, 165),
    (730, 21),
    #etc...
]
```
The student's response will be evaluated with arguments of (0, 0), (1, 0), (100, 165) etc., and if any value
it returns differs from the value returned by the reference function, it will be marked incorrect.

## Advanced
Since `tests` is a normal Python variable, it need not be declared statically, so test cases can be dynamically 
generated. An example where you may want to do this would be to generate a large number of random tests with
problem-specific constraints. Arbitrary code can be used to generate the tests, and any built-in Python library
can be used, as well as some others like NumPy.

The following example creates 1000 random tests to ensure that the `sum` function works as intended.

Answer:
```python
from random import randint

def sum(a, b):
    return a + b

tests = [(randint(0, 10), randint(0, 10)) for _ in range(1000)]
```
