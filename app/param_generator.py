import ast
import random
import string

import numpy
import numpy as np


def guess_param_type(variable, body):
    try:
        tree = ast.parse(body)
    except SyntaxError as e:
        return f"Invalid syntax: {e}"

    class TypeGuesser(ast.NodeVisitor):
        def __init__(self, var_name):
            self.guess = set()
            self.var_name = var_name

        def visit_BinOp(self, node):
            if isinstance(node.left, ast.Name) and node.left.id == self.var_name:
                if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow)):
                    self.guess.update({int, float, complex})
            elif isinstance(node.right, ast.Name) and node.right.id == self.var_name:
                if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow)):
                    self.guess.update({int, float, complex})
            self.generic_visit(node)

        def visit_Call(self, node):
            if isinstance(node.func, ast.Attribute):
                if isinstance(node.func.value, ast.Name) and node.func.value.id == self.var_name:
                    if node.func.attr in get_methods(list):
                        self.guess.add(list)
                    elif node.func.attr in get_methods(str):
                        self.guess.add(str)
                    elif node.func.attr in get_methods(set):
                        self.guess.add(set)
                    elif node.func.attr in get_methods(dict):
                        self.guess.add(dict)
                    elif node.func.attr in get_methods(int):
                        self.guess.add(int)
                    elif node.func.attr in get_methods(float):
                        self.guess.add(float)
                    elif node.func.attr in get_methods(complex):
                        self.guess.add(complex)
                    elif node.func.attr in get_methods(numpy.ndarray):
                        self.guess.add(numpy.ndarray)

            self.generic_visit(node)

        def visit_For(self, node):
            if isinstance(node.iter, ast.Name) and node.iter.id == self.var_name:
                self.guess.add(iter)
            if isinstance(node.iter, ast.Call) and isinstance(node.iter.func,
                                                              ast.Name) and node.iter.func.id == 'range':
                # If the variable is used in range(), it should be int
                self.guess.add(int)
            self.generic_visit(node)

        def visit_Subscript(self, node):
            if isinstance(node.value, ast.Name) and node.value.id == self.var_name:
                if isinstance(node.slice, ast.Index) and isinstance(node.slice.value, ast.Str):
                    self.guess.add(str)
                elif isinstance(node.slice, ast.Index) and isinstance(node.slice.value, ast.Num):
                    self.guess.add(str)
            self.generic_visit(node)

    guesser = TypeGuesser(variable)
    guesser.visit(tree)
    return guesser.guess or set()


def get_methods(method_type):
    return [method for method in dir(method_type) if callable(getattr(method_type, method)) and not (
            method.startswith('__') and method.endswith('__'))]


def param_generator(params, body):

    param_result_dict = {}
    for param in params:
        result = []
        possible_types = guess_param_type(param, body)
        for possible_type in possible_types:
            result.append(type_generator(possible_type))
        param_result_dict[param] = result

    return param_result_dict


def type_generator(possible_type):
    length = random.randint(1, 10)

    def string_generator():
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def float_generator(decimal=2):
        return round(random.uniform(-1, 1) * 1000, decimal)

    def complex_generator():
        return complex(float_generator(), float_generator())

    result = None
    if possible_type == int:
        result = random.randint(-1000, 1000)
    elif possible_type == float:
        result = float_generator()
    elif possible_type == complex:
        result = complex_generator()
    elif possible_type == str:
        result = string_generator()
    elif possible_type == list or possible_type == iter:
        # there are three types of element in list: int, float, complex, and string
        result = [[random.randint(-1000, 1000) for _ in range(length)], [float_generator() for _ in range(length)],
                  [complex_generator() for _ in range(length)], [string_generator() for _ in range(length)]]
    elif possible_type == set:
        result = [{random.randint(-1000, 1000) for _ in range(length)}, {float_generator() for _ in range(length)},
                  {complex_generator() for _ in range(length)}, {string_generator() for _ in range(length)}]
    elif possible_type == dict:
        result = [{string_generator(): random.randint(-1000, 1000) for _ in range(length)},
                  {string_generator(): float_generator() for _ in range(length)},
                  {string_generator(): complex_generator() for _ in range(length)},
                  {string_generator(): string_generator() for _ in range(length)}]
    elif possible_type == np.ndarray:
        result = [np.random.randint(-1000, 1001, 10), np.round(1000 * np.random.uniform(-1, 1, length))]

    return result
