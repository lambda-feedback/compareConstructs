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
in detail in their own pages:

- [Syntax and style](syntax_and_style.md) (`checks/general_check.py`)
- [Console output](console_output.md) (`checks/output_check.py`)
- [Variable content](variable_content.md) (`checks/global_variable_check.py`)
- [Functions](functions.md) (`checks/func_check.py`)

## Future Improvements

## Contact
compareConstructs was started in the summer of 2024 by Jieyu Zhao, with significant contributions
from Max Hurlow, who  also wrote the documentation. If you have any questions about the project,
feel free to contact me (Max). I'm sure you can figure out how.
