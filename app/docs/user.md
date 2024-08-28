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
types like numpy arrays.
  
The response will be marked correct if the return value for each test case matches the value
returned by the same function in `answer`.

#### Example

Parameters:

```
{
    "check_func": "sum"
}
```

Response:

```
def sum(a, b):
    return a - (-b)
```

Answer:

```
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