def parse_input():
    maze = {}
    start = end = (0, 0)
    
    with open("input.txt") as f:
        for i, line in enumerate(f.read().splitlines()):
            for j, char in enumerate(line):
                maze[(i, j)] = char
                if char == 'S': start = (i, j)
                elif char == 'E': end = (i, j)
    return maze, start, end

def find_paths(maze, start, end):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    visited = {}
    paths = [(0, (0, 1), [start])]
    completed = []

    for _ in range(1000):
        next_paths = []
        for score, dir, positions in sorted(paths):
            x, y = positions[-1]
            
            for dx, dy in directions:
                next_pos = (x + dx, y + dy)
                if next_pos not in maze or maze[next_pos] == '#':
                    continue
                    
                new_score = score + (1000 if (dx, dy) != dir else 1)
                visit_key = (next_pos, (dx, dy))
                
                if visit_key in visited and visited[visit_key] < new_score:
                    continue
                    
                new_path = (new_score, (dx, dy), positions + [next_pos])
                visited[visit_key] = new_score
                next_paths.append(new_path)
                
                if next_pos == end:
                    completed.append(new_path)
        paths = next_paths
    return visited, completed

def get_min_score(visited, end):
    max_score = max(visited.values())
    return min(visited.get((end, d), max_score) 
              for d in [(0, 1), (0, -1), (1, 0), (-1, 0)])

def get_unique_tiles(paths, min_score):
    best_paths = [p for p in paths if p[0] == min_score]
    return len({pos for _, _, positions in best_paths for pos in positions[1:]})

def solve():
    maze, start, end = parse_input()
    visited, completed = find_paths(maze, start, end)
    answer1 = get_min_score(visited, end)
    answer2 = get_unique_tiles(completed, answer1)
    return answer1, answer2

if __name__ == "__main__":
    part1, part2 = solve()
    print(part1, part2)