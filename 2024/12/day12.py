from typing import Dict, List, Set, Tuple



def parse_input() -> Dict[Tuple[int, int], str]:
    with open("./input.txt", "r") as file:
        return {
            (row, col): value 
            for row, line in enumerate(file.read().strip().split('\n'))
            for col, value in enumerate(line)
        }

def explore_connected_region(
    start_position: Tuple[int, int], 
    grid_map: Dict[Tuple[int, int], str], 
    explored_positions: Set[Tuple[int, int]], 
    search_directions: List[Tuple[int, int]]
) -> Tuple[List[Tuple[int, int]], Set[Tuple[int, int, int, int]]]:
    region_value = grid_map[start_position]
    region_positions = [start_position]
    region_boundary = set()
    visited_positions = set()

    for current_row, current_col in region_positions:
        visited_positions.add((current_row, current_col))
        
        for delta_row, delta_col in search_directions:
            next_row = current_row + delta_row
            next_col = current_col + delta_col
            
            if (next_row, next_col) in grid_map and (next_row, next_col) not in visited_positions:
                if grid_map[(next_row, next_col)] == region_value:
                    explored_positions.add((next_row, next_col))
                    visited_positions.add((next_row, next_col))
                    region_positions.append((next_row, next_col))
                else:
                    region_boundary.add((next_row, next_col, delta_row, delta_col))

    return region_positions, region_boundary

def count_unique_boundary_segments(
    region_boundary: Set[Tuple[int, int, int, int]], 
    search_directions: List[Tuple[int, int]]
) -> int:
    boundary_segments = set()
    visited_boundary_positions = set()

    for boundary_position in region_boundary:
        r, c = boundary_position[:2]
        
        if (r, c) in visited_boundary_positions:
            continue

        current_segment = [(r, c)]
        visited_boundary_positions.add((r, c))
        boundary_segments.add((r, c))

        while current_segment:
            curr_r, curr_c = current_segment.pop()
            
            for dr, dc in search_directions:
                nr, nc = curr_r + dr, curr_c + dc
                
                neighbor_boundary = [bp for bp in region_boundary if bp[:2] == (nr, nc)]
                
                for _ in neighbor_boundary:
                    if (nr, nc) not in visited_boundary_positions:
                        current_segment.append((nr, nc))
                        visited_boundary_positions.add((nr, nc))
                        boundary_segments.add((nr, nc))

    return len(boundary_segments)

def analyze_grid_regions() -> Tuple[int, int]:
    grid_map = parse_input()
    explored_positions = set()
    search_directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]

    part1_total = 0
    part2_total = 0

    for position in grid_map:
        if position in explored_positions:
            continue

        region_cells, region_boundary = explore_connected_region(
            position, grid_map, explored_positions, search_directions
        )
        
        part1_total += len(region_cells) * len(region_boundary)
        
        boundary_segments = count_unique_boundary_segments(
            region_boundary, search_directions
        )
        part2_total += len(region_cells) * boundary_segments

    return part1_total, part2_total

def main():
    part1_result, part2_result = analyze_grid_regions()
    print(part1_result, part2_result)

if __name__ == '__main__':
    main()