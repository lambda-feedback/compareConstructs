# Compare Construct

## Description:
This method aims to help students check their codes. The checking methods currently include: 
syntax, indentation, variable, structure, and method check. If students' codes could not be checked within
the scope, the AI will be used to define the correctness of the response.

## Teacher Instruction

- It is crucial to give the checklist. (currently support variables, and simple method with return statement) 
The checklist is a table input or string input: i.e. "x,y,z" means that we need to check 'x', 'y', 'z' respect 
to the answer
- give the correct answer in the configuration


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

