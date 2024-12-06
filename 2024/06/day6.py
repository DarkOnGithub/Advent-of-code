from typing import List, Tuple, Dict, Set
from copy import deepcopy

def parse_input(input_str: str) -> List[List[str]]:
    return [list(line) for line in input_str.strip().split("\n")]

def is_within_bounds(grid: List[List[str]], pos: Tuple[int, int]) -> bool:
    return 0 <= pos[0] < len(grid) and 0 <= pos[1] < len(grid[0])

def find_visited_positions(grid: List[List[str]]) -> Set[Tuple[int, int]]:
    start_pos = next((i, j) for i, row in enumerate(grid) for j, element in enumerate(row) if element == '^')
    current_pos, current_direction, visited_positions = start_pos, (-1, 0), set([start_pos])    
    while True:
        next_pos = (current_pos[0] + current_direction[0], current_pos[1] + current_direction[1])
        
        if (not is_within_bounds(grid, next_pos) or 
            grid[next_pos[0]][next_pos[1]] == '#'):
            current_direction = (current_direction[1], -current_direction[0])
            continue
        current_pos = next_pos
        visited_positions.add(current_pos)
        
        if (current_pos[0] == 0 or current_pos[0] == len(grid) - 1 or
            current_pos[1] == 0 or current_pos[1] == len(grid[0]) - 1):
            break
            
    return visited_positions

def is_loop(grid: List[List[str]], start_pos: Tuple[int, int]) -> bool:
    visited_states, current_pos, direction, max_iterations, iterations = set(), start_pos, (-1, 0), len(grid) * len(grid[0]) * 4, 0
    
    while iterations < max_iterations:
        current_state = (current_pos, direction)

        if current_state in visited_states:
            return True

        visited_states.add(current_state)
        
        next_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])
        if not is_within_bounds(grid, next_pos):
            return False
        
        if (grid[next_pos[0]][next_pos[1]] in '#O'):
            direction = (direction[1], -direction[0])
            continue
            
        current_pos = next_pos
        iterations += 1
        
    return False

def find_loop_positions(grid: List[List[str]]) -> int:
    start_pos = next((i, j) for i, row in enumerate(grid) for j, element in enumerate(row) if element == '^')
    visited_positions = find_visited_positions(grid)
    loop_positions = 0
    for i in range(len(grid)): 
        for j in range(len(grid[0])): 
            if grid[i][j] != '.' or (i, j) == start_pos: continue
            if (i, j) not in visited_positions: continue
            test_grid = deepcopy(grid)
            test_grid[i][j] = 'O'
            if is_loop(test_grid, start_pos):
                loop_positions += 1
    return loop_positions


if __name__ == "__main__":

    with open("./input.txt", "r") as f:
        grid = parse_input(f.read())
        print(len(find_visited_positions(grid)),find_loop_positions(grid) )
