from typing import List, Tuple
from time import time
from functools import cache

# Constants
GAP = "X"
DIGIT_KEYPAD = ["789", "456", "123", "X0A"]
DIRECTIONAL_KEYPAD = ["X^A", "<v>"]

def find_position(key: str, keypad: List[str]) -> Tuple[int, int]:
    for r, row in enumerate(keypad):
        for c, char in enumerate(row):
            if char == key:
                return r, c
    return (-1, -1)

def build_shortest_path(key1: str, key2: str, keypad: List[str]) -> List[str]:
    r1, c1 = find_position(key1, keypad)
    r2, c2 = find_position(key2, keypad)
    r_gap, c_gap = find_position(GAP, keypad)
    
    dr, dc = r2 - r1, c2 - c1
    row_moves = "v" * abs(dr) if dr >= 0 else "^" * abs(dr)
    col_moves = ">" * abs(dc) if dc >= 0 else "<" * abs(dc)

    if dr == dc == 0:
        return [""]
    elif dr == 0:
        return [col_moves]
    elif dc == 0:
        return [row_moves]
    elif (r1, c2) == (r_gap, c_gap):
        return [row_moves + col_moves]
    elif (r2, c1) == (r_gap, c_gap):
        return [col_moves + row_moves]
    else:
        return [row_moves + col_moves, col_moves + row_moves]

def build_sequence_paths(seq: str, keypad: List[str]) -> List[List[str]]:
    result = []
    for key1, key2 in zip("A" + seq, seq):
        paths = [p + "A" for p in build_shortest_path(key1, key2, keypad)]
        result.append(paths)
    return result

@cache
def solve(seq: str, depth: int) -> int:
    print(depth)
    if depth == 1:
        return len(seq)

    keypad = DIGIT_KEYPAD if any(c in seq for c in "0123456789") else DIRECTIONAL_KEYPAD
    
    total = 0
    for paths in build_sequence_paths(seq, keypad):
        total += min(solve(path, depth - 1) for path in paths)
    return total

def main():
    time_start = time()
    with open("input.txt", "r") as f:
        codes = [line.strip() for line in f]

    ans1 = sum(solve(code, 4) * int(''.join(c for c in code if c.isdigit()).lstrip('0') or '0') 
               for code in codes)
    print(f"Part 1: {ans1} ({time() - time_start:.3f}s)")

    ans2 = sum(solve(code, 27) * int(''.join(c for c in code if c.isdigit()).lstrip('0') or '0') 
               for code in codes)
    print(f"Part 2: {ans2} ({time() - time_start:.3f}s)")

if __name__ == "__main__":
    main()