"""Parses the output of a lizard run into easier to use data
"""
import lizard
import argparse
from fnmatch import fnmatch
from itertools import chain
import sys

def analyze(file_paths):
    extensions = lizard.get_extensions(["cpre"], False)
    analysis = lizard.analyze(file_paths,
                              threads=4,
                              extensions=extensions)
    return process_code_info(analysis, extensions)

def process_code_info(analysis, extensions):
    """Processes FileInformation objects into dictionary described below

    Structure of the dictionary produced by this tool is:
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
    """
    data_dict= {}
    for module_info in analysis:
        data_dict[module_info.filename] = {}
        file_name = module_info.filename
        data_dict[file_name]["nloc"] = module_info.nloc
        data_dict[file_name]["average_nloc"] = module_info.average_NLOC
        data_dict[file_name]["average_tokens"] = module_info.average_token
        data_dict[file_name]["average_ccn"] = module_info.average_CCN

        for extension in extensions:
            if hasattr(extension, 'reduce'):
                extension.reduce(module_info)
        if module_info:
            #all_functions.append(module_info)
            for fun in module_info.function_list:
                name1 = module_info.filename
                name2 = fun.name
                data_dict[name1][name2] = {}
                data_dict[name1][name2]["nloc"] = fun.nloc
                data_dict[name1][name2]["ccn"] = fun.cyclomatic_complexity
                data_dict[name1][name2]["tokens"] = fun.token_count
                data_dict[name1][name2]["parameters"] = fun.parameter_count
                data_dict[name1][name2]["start_line"] = fun.start_line
                data_dict[name1][name2]["end_line"] = fun.end_line
                data_dict[name1][name2]["length"] = fun.length

    return data_dict

def main(path, function):
    """The main function for this script"""
    options = argparse.Namespace()
    options.paths = path
    options.extensions = lizard.get_extensions(["cpre"], False)
    options.warnings_only = False
    options.whitelist = "whitelizard.txt"
    options.verbose = True
    options.sorting = []
    # default maximum cyclomatic complexity
    options.CCN = 30
    # default maximum function length
    options.length = 300
    # default maximum number of arguments
    options.arguments = 8
    options.number = 0
    options.working_threads = 4

    analysis = lizard.analyze(path,
                              threads=options.working_threads,
                              extensions=options.extensions)

    print(process_code_info(analysis, options.extensions))

if __name__ == "__main__":
    # set up the parser
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file_path', metavar='file', type=str)
    parser.add_argument('--function', type=str, help='function to extract data for')
    parser.add_argument('--output', type=str, help='where to write JSON data to')

    # parse the args and pass them to main
    args = parser.parse_args()
    main(path=[args.file], function=args.function)
