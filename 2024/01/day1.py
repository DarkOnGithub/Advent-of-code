from typing import List, Union
import math

def main(input: str) -> int:
    
    
    left, right = map(sorted,parse_input(input))
    
    #Part 1
    output_part_1 = sum(abs(int(l) - int(r)) for l,r in zip(left, right))
    
    
    #Part 2
    output_part_2 = sum(right.count(i) * int(i) for i in left)
    
    return output_part_1, output_part_2


def parse_input(input: str) ->  Union[List[int], List[int]]:
    left, right = map(list, zip(*(line.split("   ") for line in input.split("\n"))))
    return left, right

if __name__ == "__main__":
    with open("./input.txt", "r") as input:
        print(main(input.read()))