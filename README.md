# compareConstructs

## About

compareConstructs is an evaluation function for [Lambda Feedback](www.lambdafeedback.com) that
aims to check and provide feedback on Python code. The intended use case is in teaching the
various Mathematics and Computing modules across Imperial College, where the advanced equation entry
features already present on the platform can be combined with code to provide a more cohesive
experience for students.
  
Currently, compareConstructs focusses on the following aspects of code checking:
- Syntax and style: 
    - Aims to provide helpful feedback in the case of a syntax error.
    - Checks for correct and consistent indentation style.
- Console output:
    - Verifies that `print`'ed values match between the response and answer.
- Variable content:
    - Compares the contents of specified global variables between the response and answer.
    - Special feedback cases for NumPy arrays.
- Functions:
    - Functions written by students can be subjected to a battery of tests to ensure that they
      work correctly for any input.

If these tests are inconclusive, as an experimental feature the checking can be handled by GPT-4,
which can provide reasonably accurate feedback.

## Further Information

Further documentation on the exact implementation of these features can be found in the 'docs'
directory. Start by reading [dev.md](docs/dev.md), which contains lots of information on this
function from a developer's perspective. 
