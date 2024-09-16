# Future Improvements

This project was started with an open-ended brief, so there are many ways that it could be expanded and built upon.
Some potential avenues to explore are given below. Note that these are just suggestions, so any relevant features 
would be welcome.

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
      - Useful for teaching algorithms. If the question specifically specifies a particular algorithm,
        there is currently no way to ensure this is being used. For example, a student could write a 
        bubble sort when a quicksort was required, and still be marked correct.
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
