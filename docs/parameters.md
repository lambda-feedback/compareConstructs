# Parameters

Parameters are communicated from the web application to the evaluation function in JSON format,
which are passed to `evaluation_function()` as a dictionary.

This dictionary has several fields:

- `global_variables_check_list`: This is either a list of strings, or a comma-delimited string
  containing a list of variable names to check. If this list is present, a
  [global variable check](variable_content.md) is performed, and the given variables are compared
  between the response and the answer.
- `check_func`: This is a string containing the name of a function. If this is present,
  a [function check](functions.md) is performed on this function
- `check_names`: A boolean. If this is true, all functions and classes in the response must
  match with the answer exactly.
- `output_inexact`: A boolean. If this is true, a tolerance is applied to values printed to the
  console. This is useful for comparing numbers, where for example `0`, `0.0` and `0.000000005`
  should be considered the same due to floating point precision. Otherwise, string comparisons
  are used.

This parameter format is simple, but flawed. It is not possible to specify exactly which checks
are run. For example, currently, if `check_func` is set, the specified function will be tested
but the global variables will not be checked, even if `global_variables_check_list` is given.
This is a clear area for improvement.
