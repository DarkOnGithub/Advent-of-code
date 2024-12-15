from typing import List, Tuple, Optional, Set

DIRECTIONS = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1)
}

def parse_input(input: str) -> Tuple[List[List[str]], List[str]]:
    return ([list(line) for line in input.split("\n\n")[0].splitlines()],
            list(input.split("\n\n")[1].replace("\n", "")))

def add_tuple(t1: Tuple[int, int], t2: Tuple[int, int]) -> Tuple[int, int]:
    return (t1[0] + t2[0], t1[1] + t2[1])

def can_push(grid: List[List[str]], pos: Tuple[int, int], direction: Tuple[int, int]) -> Tuple[bool, Optional[Tuple[int, int]]]:
    if not (0 <= pos[0] + direction[0] < len(grid) and 0 <= pos[1] + direction[1] < len(grid[0])):
        return (False, None)
    if grid[pos[0]][pos[1]] == "#":
        return (False, None)
    if grid[pos[0]][pos[1]] == ".":
        return (True, pos)
    next_pos = add_tuple(pos, direction)
    return can_push(grid, next_pos, direction)

def print_grid(grid: List[List[str]]) -> None:
    for row in grid:
        print("".join(row))
    print()

def calculate_gps(grid: List[List[str]]) -> int:
    return sum(i * 100 + j for i, row in enumerate(grid) for j, cell in enumerate(row) if cell == 'O')

def part_1(grid: List[List[str]], instructions: List[str]) -> int:
    current_position = next((i, j) for i, row in enumerate(grid) for j, cell in enumerate(row) if cell == '@')
    for instruction in instructions:
        push, free_position = can_push(grid, current_position, DIRECTIONS[instruction])
        if push and free_position:
            grid[free_position[0]][free_position[1]] = "O"
            next_pos = add_tuple(current_position, DIRECTIONS[instruction])
            grid[next_pos[0]][next_pos[1]] = "@"
            grid[current_position[0]][current_position[1]] = "."
            current_position = next_pos
    return calculate_gps(grid)

def can_push_wide(grid: List[List[str]], pos: Tuple[int, int], direction: Tuple[int, int]) -> Tuple[bool, Optional[Tuple[int, int]]]:
    next_pos = add_tuple(pos, direction)
    if not (0 <= next_pos[0] < len(grid) and 0 <= next_pos[1] < len(grid[0]) - 1):
        return (False, None)

    current = grid[next_pos[0]][next_pos[1]]
    if current == '#' or (current == '#' and grid[next_pos[0]][next_pos[1] + 1] == '#'):
        return (False, None)
    if current == '.' and grid[next_pos[0]][next_pos[1] + 1] == '.':
        return (True, next_pos)
    if current == '[' and grid[next_pos[0]][next_pos[1] + 1] == ']':
        return can_push_wide(grid, next_pos, direction)
    return (False, None)

def part_2(grid: List[List[str]], instructions: List[str]) -> int:
    boxlefts = {(i, j) for i, line in enumerate(grid) 
                                      for j, char in enumerate(line) if char == '['}
    walls = {(i, j) for i, line in enumerate(grid) 
                                   for j, char in enumerate(line) if char == '#'}
    robot = next((i, j) for i, line in enumerate(grid) 
                                  for j, char in enumerate(line) if char == '@')

    def check_intersect(coords: Tuple[int, int], boxlefts: Set[Tuple[int, int]]) -> Tuple[int, int]:
        if coords in boxlefts:
            return coords
        elif add_tuple(coords, (0, -1)) in boxlefts:
            return add_tuple(coords, (0, -1))
        return ()

    def try_move(start: Tuple[int, int], direction: Tuple[int, int], boxlefts: Set[Tuple[int, int]]) -> Tuple[bool, Set[Tuple[int, int]]]:
        target = add_tuple(start, direction)
        if target in walls:
            return (False, set())

        nextbox = check_intersect(target, boxlefts)
        if not nextbox:
            return (True, set())

        if direction[1] == -1:
            next_move = try_move(nextbox, direction, boxlefts)
            return (next_move[0], next_move[1] | {nextbox})
        elif direction[1] == 1:
            next_move = try_move(add_tuple(nextbox, (0, 1)), direction, boxlefts)
            return (next_move[0], next_move[1] | {nextbox})
        else:
            next_move1 = try_move(nextbox, direction, boxlefts)
            next_move2 = try_move(add_tuple(nextbox, (0, 1)), direction, boxlefts)
            return (next_move1[0] and next_move2[0],
                    next_move1[1] | next_move2[1] | {nextbox})

    for move in instructions:
        direction = DIRECTIONS[move]
        can_move, moving_boxes = try_move(robot, direction, boxlefts)
        if can_move:
            boxlefts = {box for box in boxlefts if box not in moving_boxes} | \
                       {add_tuple(box, direction) for box in moving_boxes}
            robot = add_tuple(robot, direction)

    return sum(100 * i + j for i, j in boxlefts)

if __name__ == "__main__":
    with open("./input.txt", "r") as f:
        input_data = f.read()
        print(part_1(*parse_input(input_data)))
        print(part_2(*parse_input(input_data
                                  .replace("#", "##")
                                  .replace("O", "[]")
                                  .replace(".", "..")
                                  .replace("@", "@."))))
