# YourFunctionName

## Parameters

### check_func

If this parameter is not null, it is expected to be a string containing the name of a function.
  
This parameter allows a function to be tested against a battery of test cases. If this parameter
is set, the `answer` field is interpreted differently. `answer` is expected to contain a function
with the same name as the value of `check_func`, and a global variable called `tests`, which is a 
list of tuples. Each tuple inside `tests` contains arguments that will be given to the function 
under test. If only one argument is required for each function invocation, no tuple is required.
  
For each tuple in `tests`, the function given in `answer` will be evaluated with the given
arguments. The corresponding function in the student response will also be evaluated with the
same arguments. 
  
By default, the return values will be tested for equality using the `==` operator, but if `answer`
contains a function called `equals`, taking two arguments and returning a `bool`, this function
will be used to test equality. An `equals` function should be provided for non-trivial return
types like NumPy arrays.
  
The response will be marked correct if the return value for each test case matches the value
returned by the same function in `answer`.

#### Example

Parameters (JSON):

```json
{
    "check_func": "sum"
}
```

Response (Python):

```python
def sum(a, b):
    return a - (-b)
```

Answer (Python):

```python
def sum(a, b):
    return a + b

tests = [
    (0, 0),
    (1, 1),
    (100, 165),
    (730, 21),
    #etc...
]

```

#### Advanced use

Since `tests` is a normal Python variable, it need not be declared statically, so test cases can be
dynamically generated. An example where you may want to do this would be to generate a large number
of random tests with problem-specific constraints. Arbitrary code can be used to generate the tests,
and any built-in Python library can be used, as well as some others like NumPy.
  
N.B. if it is desired that the same random numbers are produced on each run, the random number
generator can be given a constant seed using `random.seed()`.
  
The following example creates 1000 random tests to ensure that the `sum` function works as intended.

Response (Python):
```python
def sum(a, b):
    return a - (-b)
```

Answer (Python):
```python
from random import randint

def sum(a, b):
    return a + b

tests = [(randint(0, 10), randint(0, 10)) for _ in range(1000)]

```

