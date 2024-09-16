# Console Output

# Motivation

In some circumstances, particularly in the early stages of teaching programming, it is more intuitive for students to write imperative
code that prints its results directly to the console, as opposed to storing results in variables or writing functions. This checking
function captures console output and compares it to the accepted answer. 

## Implementation

This checking function captures the console output of the `exec()` call using `redirect_stdout()` from the `contextlib` module.
Depending on the value of the `output_inexact` parameter, the output will either be compared using simple string comparison, or
an attempt will be made to convert to a float and apply a tolerance. This avoids issues caused by floating point precision,
e.g. `0`, `0.0` and `0.00000005` should all be considered the same. 

This function is implemented in `checks/output_check.py`.

## Examples

<table>
  <tr>
    <th>Response</th>
    <th>Answer</th>
    <th>Correct?</th>
  </tr>
  <tr>
    <td><code>print("Hello, World")</code></td>
    <td><code>print("Hello, World!")</code></td>
    <td>No</td>
  </tr>
  <tr>
    <td><code>print(0)</code></td>
    <td><code>print(0.0)</code></td>
    <td>Yes (if <code>output_inexact</code> is true)</td>
  </tr>
  <tr>
    <td><pre>print(1)<br>print(2)<br>print(3)<br></pre></td>
    <td><pre>for i in range(1, 4):<br>  print(i)</pre></td>
    <td>Yes</td>
  </tr>
</table>
