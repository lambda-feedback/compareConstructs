# Security

Currently, there is no isolation of response execution. This has potentially major security
implications, as any code submitted by users will run directly on the server and have all the 
capabilities that the host eval function does (including the use of `sudo`).

This should probably be the first thing that any new developers on the project consider,
before adding any new features.

## Solutions
There are many potential ways to solve this issue. Some of these considered by the authors 
are given here. Note that any other solution would be acceptable, as long as it effectively
prevents user code from gaining privileged access to the host system.

### Linux process isolation
The Linux operating system provides ways to reduce the permissions of processes and remove
access to system resources. These include
- `chroot`: this changes the root directory of the filesystem, preventing access to any other
  files.
- User and group permissions: a process can be made to run under an unprivileged user and group,
  which prevents the use of `sudo` and any privileged syscalls.
- `seccomp`: This allows granular control of which syscalls the process is allowed to use.

The author made an attempt to implement this, and while it had the potential to work well,
permissions issues on AWS Lambda meant that it was not viable. It is possible that with some
more research this could be made to work, so the code for this can be found in `checks/run_checks.py`, and is gated behind a command-line option.

### Containers
Running the user's code in a container would essentially be a pre-packaged implementation of the 
above. For a developer with experience using Docker or other containerisation projects, this may
be an attractive option, but it is currently unknown whether the aforementioned permissions issues
would allow this.

### Emulation
Running a Python interpreter in a fully emulated virtual machine would provide the most effective 
isolation possible between the user's code and the host machine. A promising possibility for
achieving this is [Pyodide](https://pyodide.org/en/stable/), which is a Python interpreter
runnning on the [WebAssembly](https://webassembly.org/) (Wasm) virtual machine.

While Wasm is primarily intended to run in web browsers, it is also gaining popularity for 
server-side use. Using this for compareConstructs would involve making use of Node.js (or 
any other framework that provides a Wasm interpreter, like [wasmtime](https://github.com/bytecodealliance/wasmtime)) to run Pyodide, which would then interpret the user's response.

The advantage of this is complete isolation without needing any special permissions, as everything
is handled without operating system intervention. The possible downsides include reduced
performance and added complexity.

### Static analysis
It may be possible to analyse the code to determine whether it would do anything malicious.

It is quite straightforward to restrict access to `import`s and certain built-in functions
when using `eval()`, but as this [blog post](https://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html) describes, there are several methods to to sidestep
these restrictions and gain access to dangerous functions like `os.system()` anyway.

However, it appears that all such methods involve poking around with Python's "magic" attributes,
which all have the form `__<whatever>__`. It may be possible to prevent this by analysing 
the AST to find any use of these attributes, which are unlikely to be needed in "normal" code.
It would also be necessary to disallow the use of nested `eval()`, which would let you
obfuscate your access to these methods (e.g. `eval("_" + "_import_" + "_")`). 

It is unknown whether this would provide sufficient protection against malicious code. It may be 
best to use this in conjunction with another isolation method. It is also highly Python-specific,
so it would not be easy to abstract this to allow for the use of other languages.
