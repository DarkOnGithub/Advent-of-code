from typing import List
import re
import numpy as np
def parse_input(input: str) -> List[List[List[int]]]:
    pattern = r'(?:X\+|X=)(\d+).*?(?:Y\+|Y=)(\d+)'
    matches = re.findall(pattern, input, re.DOTALL)
    return [
        [
            [int(matches[i][0]), int(matches[i + 1][0])], 
            [int(matches[i][1]), int(matches[i+1][1])], 
            [int(matches[i+2][0]), int(matches[i+2][1])] 
        ] for i in range(0, len(matches), 3)
    ]

def main(matrices: List[List[List[int]]], offset: int):
    c = 0
    for matrix in matrices:
        mat = np.array([matrix[0], matrix[1]])
        p = np.array(matrix[2]) + offset
        res = np.linalg.solve(mat, p).round()
        if all(mat @ res == p): c += res @ [3,1]
    return c
if __name__ == "__main__":
    with open("./input.txt", "r") as f:
        matrices = parse_input(f.read())
        print(main(matrices, 0))
        print(main(matrices, 1e13))
