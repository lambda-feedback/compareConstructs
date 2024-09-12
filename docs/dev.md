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

Some potential avenues to explore are given below:
- Security
  - This has been mentioned before, but security is currently very poor or nonexistant.
  - There are [many possible ways](security.md) this could be improved.
  - A difficult problem with lots of room for experimentation and innovation.
- Checking
  - The current checks perform well in some cases, but are sometimes unreliable.
    - More unit tests are needed to prevent incorrect feedback.
  - Potential improvements to checking functions:
    - Check that a consistent naming convention is used for variable and function names
      (camelCase, snake_case etc.).
    - Currently only one function can be checked at once. Add the ability to check
      an arbitrary number of functions in the response (harder than it seems because of 
      the current method used; see [functions.md](functions.md)).
    - Add the ability to check class methods as well as bare functions.
    - Performance checking:
      - Currently all algorithms that yield a correct result will be treated equally.
      - compareConstructs could check whether an optimal algorithm was used to produce the
        result, and give feedback if it wasn't.
      - Example: a question asks to write a function that sorts a list. compareConstructs
        could check how the execution time scales with the size of the list over many evaluations,
        and use statistical methods to determine its time complexity.
- Feedback
  - The feedback given to students is quite bare-bones in some cases. 
  - It would be beneficial if more helpful advice was given for incorrect responses, or if 
    areas for improvement were identified for correct responses.
- Architecture
  - The current architecture applies checks sequentially, which results in dependencies: if
    one check fails, the others will not be run, leading to misleading feedback.
  - Checks should be made more independent of each other, which could potentially allow
    parallelisation.
  - The current [parameters](parameters.md) system doesn't provide very good control over
    exactly which checks are run, and it is unclear to users exactly what is being checked.
    This should be replaced by a more robust system.

## Contact
compareConstructs was started in the summer of 2024 by Jieyu Zhao, with significant contributions
from Max Hurlow, who also wrote the documentation. If you have any questions about the project,
feel free to contact me (Max). I'm sure you can figure out how.
