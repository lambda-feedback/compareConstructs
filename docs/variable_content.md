# Variable Content

## Motivation

While the [function checking](functions.md) approach may be preferable for testing algorithms, depending on the question it may
be more natural to check values assigned to variables. compareConstructs provides a capability for doing this.

## Implementation

The `global_variables_check_list` parameter contains a list of variables to check. Depending on preference, this can be in the form of
a list of strings, each string containing a variable name, or a single comma-delimited string, with variable names separated by commas.

The response and answer will both be evaluated, and after evaluation is complete the values in the variables in the list will be 
compared. If any required variables do not exist, or if any have different values to the answer, the response will be marked incorrect.

If the variable stores float or a complex number, a tolerance will be applied to account for floating point imprecision.

It is possible that the student's response assigns the correct values, but does so to variables with incorrect names. The checking function
can detect this, and still return a correct result. This facility is experimental however, and should not be relied upon. It is recommended
that any future developers consider improving this feature, and possibly gate it behind a parameter. 

This checking function is implemented in `checks/global_variable_check.py`.

## Example

The response in this case will be marked correct.

Response:
```python
test1 = []
for i in range(10)
    test1.append(i)

test2 = 10 + 32
```
Answer:
```python
test1 = [i for i in range(10)]
test2 = 42
```
Params:
```json
{
    "global_variables_check_list": ["test1", "test2"]
}
```
