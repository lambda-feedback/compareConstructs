import ast
from enum import Enum

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
    def __init__(self, type: NodeType):
        self.type = type
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Node):
            return False
        else:
            if self.type != other.type:
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


def extract_definitions(node, parent):
    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.FunctionDef):
            child_node = extract_definitions(child, Node(NodeType.FUNCTION))
            parent.add_child(child_node)
        elif isinstance(child, ast.ClassDef):
            child_node = extract_definitions(child, Node(NodeType.CLASS))
            parent.add_child(child_node)
    return parent


def split_structure(code_str):
    tree = ast.parse(code_str)
    hierarchy = extract_definitions(tree, Node(NodeType.ROOT))
    return hierarchy


def check_structure(response, answer):
    return split_structure(response) == split_structure(answer)


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
    print(split_structure(response))
    print(split_structure(answer))
    print(check_structure(response, answer))
