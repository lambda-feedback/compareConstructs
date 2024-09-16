# Syntax and Style

## Motivation
Before any dynamic analysis can take place, it must be verified that the student's response is
syntactically correct. This check ensures that this is the case, and supplies a suitable
error message in the case of a syntax error.

Additionally, it is important to stick to a consistent, widely-used code style when writing
"real" code. compareConstructs aims to encourage this by providing feedback when improvements
could be made. At this time, only indentation is checked, but we hope that other lints will
be implemented in the future.

## Implementation
Syntax is checked by using Python's `ast` module to parse the source into an abstract syntax tree.
This process cannot complete if there are syntax errors, so if this is the case a feedback message
is returned and the response is marked incorrect. The resultant AST is returned by the function
so it can be reused by later checks. 

The source code is also processed to ensure a consistent indentation style of either two or four
spaces is used throughout the response.

This check is implemented in `checks/general_check.py`.

## Examples

```python
print("Hello, World! " # This is incorrect as there is no closing bracket.

for i in range(0, 10) # There should be a colon at the end of the 'for' statement.
  print(i)
```
