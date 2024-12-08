from typing import Dict, Tuple, List

def parse_grid(input_data: str) -> Tuple[List[List[str]], Dict[str, List[Tuple[int, int]]]]:
    positions = {}
    grid = [list(line) for line in input_data.strip().split('\n')]
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char != ".":
                positions.setdefault(char, []).append((y, x))
    return grid, positions

def are_collinear(p1: Tuple[int, int], p2: Tuple[int, int], p3: Tuple[int, int]) -> bool:
    if p1[0] == p2[0] == p3[0] or p1[1] == p2[1] == p3[1]:
        return True
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) == (p3[0] - p1[0]) * (p2[1] - p1[1])

def count_antinodes(grid: List[List[str]], positions: Dict[str, List[Tuple[int, int]]]) -> int:
    antinodes = set()
    height, width = len(grid), len(grid[0])

    for coords in positions.values():
        if len(coords) < 2:
            continue
        for i in range(len(coords)):
            for j in range(i + 1, len(coords)):
                y1, x1 = coords[i]
                y2, x2 = coords[j]

                dy, dx = y2 - y1, x2 - x1
                
                candidates = [
                    (y2 + dy, x2 + dx),  
                    (y1 - dy, x1 - dx)   
                ]

                for y, x in candidates:
                    if 0 <= y < height and 0 <= x < width:
                        antinodes.add((y, x))

    return len(antinodes)

def count_collinear_antinodes(grid: List[List[str]], positions: Dict[str, List[Tuple[int, int]]]) -> int:
    antinodes = set()
    height, width = len(grid), len(grid[0])

    for coords in positions.values():
        for i in range(len(coords)):
            for j in range(i + 1, len(coords)):
                a, b = coords[i], coords[j]

                if a[1] == b[1]:  
                    for y in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
                        antinodes.add((y, a[1]))
                elif a[0] == b[0]:  
                    for x in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
                        antinodes.add((a[0], x))
                else:  
                    dy, dx = b[0] - a[0], b[1] - a[1]
                    for t in range(-height - width, height + width):
                        y, x = a[0] + t * dy, a[1] + t * dx
                        if 0 <= y < height and 0 <= x < width:
                            antinodes.add((y, x))

        if len(coords) > 1:
            antinodes.update(coords)

    return len(antinodes)

def main(grid: List[List[str]], positions: Dict[str, List[Tuple[int, int]]]):
    print(count_antinodes(grid, positions))
    print(count_collinear_antinodes(grid, positions))

if __name__ == "__main__":
    with open("./input.txt", "r") as f:
        grid, positions = parse_grid(f.read())
        main(grid, positions)
