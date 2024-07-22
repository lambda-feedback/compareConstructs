import ast


def extract_definitions(node, parent=None):
    definitions = []
    for child in ast.iter_child_nodes(node):

        if isinstance(child, ast.FunctionDef):
            if parent is None:
                definitions.append((child.name, "2"))
            else:
                definitions.append((child.name, "2"))
            definitions.extend(extract_definitions(child, parent=child.name))
        elif isinstance(child, ast.ClassDef):
            if parent is None:
                definitions.append((child.name, "2"))
            else:
                definitions.append((child.name, "2"))
            definitions.extend(extract_definitions(child, parent=child.name))
    return definitions


def split_structure(code_str):
    tree = ast.parse(code_str)
    hierarchy = extract_definitions(tree)
    # guarantee the root of the tree is unique
    hierarchy.append(("2", "1"))
    return hierarchy


def structure_check(response, answer):
    return set(split_structure(response)) == set(split_structure(answer))
