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

## Code Structure:
To better maintain the module, please see the code carefully in evaluation.py. 
The code structure is not complex, however, some logics might affect or interact with other scripts too much. 
If any developers have further ideas and any confusion about the codes, please feel free to ask me.

## Potential problems:

- Pay attention to same_variable_content_check.py. The aim is to give more 
flexibility for student to name their variables but have same effect on codes. 
However, I do think there might have some edge cases that might crush the code,
but I currently have no idea to find such cases.
- There are tiny probablity that AI will give the wrong answer, so please check 
the AI response carefully.

## TODOs:
There are several long-time maintenances depending on what packages students use in the future:

- is_equal() in global_variable_check.py, the equal method does rely on the equivalence 
relation in different packages
- variable_content_compare() in compare.py, the comparison should depend on the type of the variable
- message_format() in format.py, the common errors are formatted, other errors message should append if 
students have the error
- type_generator() in param_generator.py, to better cover the possible types of params, 
it should be improved depending on the courses 

## Possible Improvements

- Add configuration: depending on the params input from Lambda feedback
- class check: It might be too restricted to check a class currently as 'self' param could not be random-generated.
However, the structure check is feasible

If Lambda feedback allows to store variables:

- variable storage: Please refer to https://github.com/Johnnyallen07/codefeedback.git for more details about 
the set_global_variables() 
- wrong message count: give stage feedback depending on how many times students get wrong response

