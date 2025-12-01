from typing import List, Tuple
from itertools import combinations
def parse_input(input: str) -> Tuple[List[List[int]], List[List[int]]]:
    keys, locks = [], []

    for block in input.strip().split('\n\n'):
        lines = block.split('\n')
        pins = [sum(char == '#' for char in col) for col in zip(*lines[1:-1])]
        (keys if all(c == '#' for c in lines[0]) else locks).append(pins)
    return keys, locks


def main(keys: List[List[int]], locks: List[List[int]]) -> int:
    c = 0
    for key_heightmap in keys:
        for lock_heightmap in locks:
            if any(h1 + h2 > 5 for h1, h2 in zip(key_heightmap, lock_heightmap)):
                continue
            else:
                c += 1

if __name__ == "__main__":
    with open("input.txt") as file:
        data = parse_input(file.read().strip())
        main(*data)