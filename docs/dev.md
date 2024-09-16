# compareConstructs
compareConstructs is an evaluation function that checks and verifies Python code against a given
correct answer. 

## WARNING
Currently, there is little to no security implemented in this function. User-submitted
responses are evaluated using Python's `eval()` and `exec()` functions, which provide 
no isolation whatsoever. This means that user code can trivially run any command on the 
server, potentially stealing secrets and taking advantage of server resources. 

It is VERY IMPORTANT that this situation is resolved before releasing this to students.
More information and some potential solutions are given [here](security.md).

## Current State
Currently, compareConstructs provides the following checking methods, which are each described
in detail in their own documents:

- [Syntax and style](syntax_and_style.md) (`checks/general_check.py`)
- [Console output](console_output.md) (`checks/output_check.py`)
- [Variable content](variable_content.md) (`checks/global_variable_check.py`)
- [Functions](functions.md) (`checks/func_check.py`)

## Architecture Overview
By convention, all Lambda Feedback evaluation functions written in Python have a function called
`evaluation_function(answer, response, params)`. In this case, `response` is the code entered
by the student, `answer` is the answer written by the teacher, and `params` are 
[parameters](parameters.md) configured for this particular question. This is found in
`evaluation.py`. The return value contains the feedback to give to the student through the web
client. 

In compareConstructs, this function calls `run_checks()`, which runs the above checks sequentially.
Exactly which checks are run depends on  the `param` given. If none of these checks are run,
a request is made to the OpenAI API to mark the response.

## Future Improvements
The scope of this project is very open ended, so there is a lot of room to add features and make
improvements.
Some suggestions are listed in [future_improvements.md](future_improvements.md).

## Contact
compareConstructs was started in the summer of 2024 by Jieyu Zhao, with significant contributions
from Max Hurlow, who also wrote the documentation. If you have any questions about the project,
feel free to contact me (Max). I'm sure you can figure out how.
