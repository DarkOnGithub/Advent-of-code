from typing import List

def is_valid(line: List[int]) -> bool:
    if len(line) <= 1:
        return True
    
    for i in range(1, len(line)):
        diff = line[i] - line[i - 1]
        if not (0 < abs(diff) <= 3 and (diff > 0) == (line[1] > line[0])):
            return False
    
    return True

def can_remove_one(line: List[int]) -> bool:
    n = len(line)
    for j in range(n):
        if is_valid(line[:j] + line[j + 1:]):
            return True
    return False

def main(input_lines: List[List[int]]) -> tuple[int, int]:
    valid_count = 0
    valid_or_one_removed_count = 0
    
    for line in input_lines:
        if not line:
            continue
        is_valid_line = is_valid(line)
        valid_count += is_valid_line
        valid_or_one_removed_count += is_valid_line or can_remove_one(line)
    
    return valid_count, valid_or_one_removed_count

def parse_input(input_str: str) -> List[List[int]]:
    return [
        list(map(int, line.split()))
        for line in input_str.splitlines()
        if line.strip()
    ]


if __name__ == "__main__":
    with open("input.txt") as f:
        input_data = parse_input(f.read())
    print(main(input_data))