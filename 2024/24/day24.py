from typing import Dict, Tuple
from collections import OrderedDict


def apply_operator(b1: bool, b2: bool, operator: str):
    match operator:
        case 'AND':
            return b1 and b2
        case 'OR':
            return b1 or b2
        case "XOR":
            return b1 != b2
        case _:
            print(operator, b1, b2)

def parse_input(input: str) -> Tuple[Dict[str, bool], OrderedDict[str, Tuple[str, str, str]]]:
    input = input.strip().split('\n\n')
    visited_values = set()
    values = {}
    for line in input[0].split("\n"):
        key, value = line.split(": ")
        visited_values.add(key)
        values[key] = value == "1"
    operations = OrderedDict()
    operations_queue = input[1].split("\n")
    while operations_queue:
        line = operations_queue.pop(0)
        operation, value = line.split(" -> ")
        operation = operation.split(" ")
        if operation[0] in visited_values and operation[2] in visited_values:
            operations[value] = (operation[0], operation[1], operation[2])
            visited_values.add(value)
        else:
            operations_queue.append(line)

    return values, operations

def main(values: Dict[str, bool], operations: OrderedDict[str, Tuple[str, str, str]]) -> None:
    filtered_values = {}
    for key, operation in operations.items():
        b1, b2 = values[operation[0]], values[operation[2]]
        values[key] = apply_operator(b1, b2, operation[1])
        if key.startswith('z'):
            filtered_values[key] = 1 if values[key] else 0 

    filtered_values = dict(sorted(
        filtered_values.items(), 
        key=lambda x: int(x[0][1:]),
        reverse=True
    ))
    mismatch = set()
    for key, operation in operations.items():
        if key.startswith('z') and operation[1] != "XOR" and key != list(filtered_values.keys())[0]:
            mismatch.add(key)
        if operation[1] == "XOR" and key[0] not in ["x", "y", "z"] and operation[0][0] not in ["x", "y", "z"] and operation[2][0] not in ["x", "y", "z"]:
            mismatch.add(key)
        
        if operation[1] == "AND" and "x00" not in operation:
            for s_res, s_operation in operations.items():
                if (key == s_operation[0] or key == s_operation[2]) and s_operation[1] != "OR":
                    mismatch.add(key)
        if operation[1] == "XOR":
            for s_res, s_operation in operations.items():
                if (key == s_operation[0] or key == s_operation[2]) and s_operation[1] == "OR":
                    mismatch.add(key)
    return int("".join(map(str, filtered_values.values())), 2), ",".join(sorted(mismatch))

if __name__ == "__main__":
    with open("input.txt") as f:
        values, operations = parse_input(f.read())
        print(main(values, operations))

