from itertools import product
from typing import Dict, Tuple, List, Set, Iterator

Grid = Dict[Tuple[int, int], str]
Position = Tuple[int, int]

def parse_input(filename: str) -> Tuple[Grid, Position, Position]:
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]
    grid: Grid = {}
    x_lim, y_lim = len(lines[0]), len(lines)
    start, goal = (0, 0), (0, 0)
    for x, y in product(range(x_lim), range(y_lim)):
        grid[(x, y)] = lines[y][x]
        if lines[y][x] == 'S':
            start = (x, y)
        elif lines[y][x] == 'E':
            goal = (x, y)
    return grid, start, goal

def bfs(grid: Grid, start: Position, goal: Position) -> List[Position]:
    queue: List[List[Position]] = [[start]]
    visited: Set[Position] = {start}
    valid = lambda n: n not in visited and grid.get(n, '#') != '#'
    
    for path in queue:
        node = path[-1]
        if node == goal:
            return path
        for neighbor in filter(valid, get_circle(node, 1)):
            visited.add(neighbor)
            queue.append(path + [neighbor])
    return []

def get_circle(pos: Position, radius: int) -> Iterator[Position]:
    offsets = {(i, radius - i) for i in range(radius + 1)} | \
              {(-i, -(radius - i)) for i in range(radius + 1)} | \
              {(i, -(radius - i)) for i in range(radius + 1)} | \
              {(-i, radius - i) for i in range(radius + 1)}
    return ((pos[0] + dx, pos[1] + dy) for dx, dy in offsets)

def p1(grid: Grid, start: Position, goal: Position) -> Tuple[List[Position], Dict[Position, int]]:
    path_list = bfs(grid, start, goal)
    path = {pos: i for i, pos in enumerate(path_list)}
    c = 0
    lim = 100
    for i, pos in enumerate(path_list):
        valid = lambda n: n in path and path[n] - i - 2 >= lim
        c += sum(valid(n) for n in get_circle(pos, 2))
    print(c)
    return path_list, path

def p2(path_list: List[Position], path: Dict[Position, int]) -> None:
    c = 0
    lim = 50 if len(path_list) == 85 else 100
    for i, pos in enumerate(path_list):
        for steps in range(2, 21):
            valid = lambda n: n in path and path[n] - i - steps >= lim
            c += sum(valid(n) for n in get_circle(pos, steps))
    print(c)

def main() -> None:
    puzzle_input = parse_input("input.txt")
    path_list, path = p1(*puzzle_input)
    p2(path_list, path)

if __name__ == "__main__":
    main()
