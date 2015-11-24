[lizard](https://github.com/terryyin/lizard) is a simple code complexity
analyzer that doesn't care about header files or imports. It can deal
with:

	- C/C++ (works with C++14)
	- Java
	- JavaScript
	- Objective C.
	- Python
	- TTCN-3

It counts:

	- the nloc (lines of code without comments),
	- CCN (cyclomatic complexity number),
	- token count of functions.
	- parameter count of functions.

This tool provides a simple wrapper that makes lizard easier to use
in the following contexts. First, the `lizardpp` provides a simplified
`analyze()` function which only needs a file path to be provided. The
information returned by this function is then in a dictionary of the
format:

    {
        <file_name>: {
            "nloc": <file.nloc>,
            "average_nloc": <file.average_NLOC>,
            "average_tokens": <file.average_token>,
            "average_ccn": <file.average_CCN>,
            <function_name>: {
               "nloc": <FunctionInfo.nloc>,
               "ccn": <FunctionInfo.cyclomatic_complexity>,
               "tokens": <FunctionInfo.token_count>,
               "parameters": <FunctionInfo.parameter_count>,
               "start_line": <FunctionInfo.start_line>,
               "end_line": <FunctionInfo.end_line>,
               "length": <FunctionInfo.length>
            }
            # functions can then be repeated until all are included
        }
    }

This is useful when using `lizardpp` as in importable Python module. The
tool also wraps the command line functionality to simplify it to the
following options:

- `file_path` - The path to the file to be analyzed. This can be a
glob or "." as well.
- `--function` - The function name to return results for, if not
provided, results are returned for the whole file.
- `--output` - The file path to write the JSON data to. If not
provided output goes to STDIN.

Finally, this package also provides a Qt based GUI which is useful for
easily monitoring statistics of files and functions as you work on them.
This functionality is provided by the complexity.py script.
