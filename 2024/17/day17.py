import re
from typing import List

def parse_input(input: str) -> List[int]:
    return list(map(int, re.findall(r'\d+', input))

def eval_program(a: int, b: int, c: int, prog: List[int]) -> List[int]:
    i = 0
    R: List[int] = []
    while i < len(prog):
        C = {0: 0, 1: 1, 2: 2, 3: 3, 4: a, 5: b, 6: c}
        match prog[i:i+2]:
            case [0, op]:
                a = a >> C[op]
            case [1, op]:
                b = b ^ op
            case [2, op]:
                b = 7 & C[op]
            case [3, op]:
                i = op - 2 if a else i
            case [4, op]:
                b = b ^ c
            case [5, op]:
                R.append(C[op] & 7)
            case [6, op]:
                b = a >> C[op]
            case [7, op]:
                c = a >> C[op]
        i += 2
    return R

def find_sequence(a: int, i: int, b: int, c: int, prog: List[int]) -> None:
    if eval_program(a, b, c, prog) == prog:
        print(a)
    if eval_program(a, b, c, prog) == prog[-i:] or i == 0:
        for n in range(8):
            find_sequence(8 * a + n, i + 1, b, c, prog)

def main(input: List[int]):
    a, b, c, *prog = input
    print(*eval_program(a, b, c, prog), sep=',')
    find_sequence(0, 0, b, c, prog)

if __name__ == "__main__":
    with open("input.txt") as f:
        data = parse_input(f.read())
    main(data)