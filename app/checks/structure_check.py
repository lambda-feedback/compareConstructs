import ast
from ast import Module
from enum import Enum
from .check_result import CheckResult

class NodeType(Enum):
    ROOT = 0
    CLASS = 1
    FUNCTION = 2

    def __str__(self) -> str:
        if self == NodeType.CLASS:
            return "Class"
        elif self == NodeType.FUNCTION:
            return "Function"
        else:
            return ""

class Node:
    def __init__(self, type: NodeType, name: str, check_names: bool):
        self.type = type
        self.name = name
        self.check_names = check_names
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Node):
            return False
        else:
            if self.type != other.type:
                return False
            if self.check_names and self.name != other.name:
                return False
            for child1, child2 in zip(self.children, other.children):
                if child1 != child2:
                    return False
            return True

    def __str__(self) -> str:
        if len(self.children) == 0:
            return str(self.type)
        
        out = f"{self.type} ["
        for i, child in enumerate(self.children):
            out += str(child)
            if i != len(self.children) - 1:
                out += ", "
        return f"{out}]"


def extract_definitions(node, parent, check_names: bool):
    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.FunctionDef):
            child_node = extract_definitions(child, Node(NodeType.FUNCTION, child.name, check_names), check_names)
            parent.add_child(child_node)
        elif isinstance(child, ast.ClassDef):
            child_node = extract_definitions(child, Node(NodeType.CLASS, child.name, check_names), check_names)
            parent.add_child(child_node)
    return parent


def check_structure(response: Module, answer: Module, check_names: bool = False) -> CheckResult:
    """Checks that the response has the same class and function heirarchy as the answer"""

    response_tree = extract_definitions(response, Node(NodeType.ROOT, "", False), check_names)
    answer_tree = extract_definitions(answer, Node(NodeType.ROOT, "", False), check_names)
    same = response_tree == answer_tree
    message = ""
    if not same:
        message = "Are you sure all the correct classes and functions are defined?"

    return CheckResult(same).add_message(message)


if __name__ == '__main__':
    response = """
def hi():
    return "hi"

def f(x, y):
    return x ** 2 + y ** 3
"""

    answer = """
def hi():
    return "hillo"[0:2]

def f(x, y):
    return x * x + y ** 3

    """
    print(NodeType.CLASS)
    print(check_structure(response, answer))
