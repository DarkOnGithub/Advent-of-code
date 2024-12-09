from typing import List, Tuple

def parse_input(input_str: str) -> List[Tuple[int, List[int]]]:
    return [
        (int(parts[0]), list(map(int, parts[1].split())))
        for line in input_str.strip().split("\n")
        for parts in [line.split(": ")]
    ]

def count_valid_equations(equations: List[Tuple[int, List[int]]], allow_concat: bool = False) -> int:
    total = 0
    for result, numbers in equations:
        previous_operations, current_operations = set(), {numbers[0]}
        for number in numbers[1:]:
            previous_operations, current_operations = current_operations, set()
            for op in previous_operations:
                for op1 in [op + number, op * number]:
                    if op1 <= result:
                        current_operations.add(op1)
                if allow_concat:
                    current_operations.add(number)
                    concat_val = int(str(op) + str(number))
                    if concat_val <= result:
                        current_operations.add(concat_val)
        total += result if result in current_operations else 0
    return total
import time
def main():
    with open("./input.txt", "r") as f:
        equations = parse_input(f.read())
    start = time.time()
    (count_valid_equations(equations))
    print(time.time() - start)
    start = time.time()
    
    (count_valid_equations(equations, allow_concat=True))
    print(time.time() - start)
if __name__ == "__main__":
    main()
