import ast
import os
import glob

def check_file(filepath):
    with open(filepath, 'r') as f:
        try:
            tree = ast.parse(f.read(), filename=filepath)
        except SyntaxError:
            print(f"SyntaxError in {filepath}")
            return

    for node in ast.walk(tree):
        if isinstance(node, ast.Assert):
            # Check for assert True / assert 1 / assert "string"
            if isinstance(node.test, ast.Constant):
                # node.test.value is the value of the constant
                if node.test.value: # assert True, assert 1, etc.
                     print(f"Suspicious constant assertion in {filepath}: assert {node.test.value}")
            
            # Check for assert x == x
            if isinstance(node.test, ast.Compare):
                left = node.test.left
                # We only check the first comparator for simplicity, as most simple bad assertions are binary
                if len(node.test.comparators) > 0:
                    right = node.test.comparators[0]
                    
                    # Compare if left and right are structurally identical
                    if ast.dump(left) == ast.dump(right):
                        print(f"Suspicious self-comparison in {filepath} on line {node.lineno}")

target_dir = "eval/final_approaches/API/just_human_coverage_final_table126/tests/generated_tests/P0"
files = glob.glob(os.path.join(target_dir, "**/*.py"), recursive=True)

for file in files:
    check_file(file)
