import importlib
import sys
import subprocess


def module_dependency(code_lines):
    module_list = []
    for line in code_lines:
        segment_list = line.split(' ')
        # check the format like from modulename import ...
        if 'from' in segment_list and 'import' in segment_list:
            module_list.append(segment_list[segment_list.index('from') + 1])
        # check the format like: import numpy as np
        if 'import' in segment_list:
            module_list.append(segment_list[segment_list.index('import') + 1])
    return module_list


def cmd_import(module_list):
    for module_name in module_list:
        try:
            # check whether the module exists
            importlib.import_module(module_name)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
            importlib.import_module(module_name)


def module_import(code_string):
    lines = code_string.strip().split('\n')
    module_list = module_dependency(lines)
    cmd_import(module_list)

