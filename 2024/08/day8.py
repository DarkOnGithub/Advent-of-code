<<<<<<< HEAD
from typing import List

def parse_input(input: str) -> List[int]:
    return list(map(int, list(input.strip())))

def checksum(disk: List[int]) -> int:
    return sum(i * e if e != -1 else 0 for i,e in enumerate(disk))

def compact_disk_frag(disk: List[int]) -> List[int]:
    i, j = 0, len(disk) - 1
    while i < j:
        i_value, j_value = disk[i], disk[j]
        if i_value == -1 and j_value != -1:
            disk[i], disk[j] = disk[j], disk[i]
            i, j = i + 1, j - 1
        elif j_value == -1:j -= 1
        elif i_value != -1:i += 1
    return disk
            
def compact_disk_unify(disk: List[int]) -> List[int]:
    file_id, files, free_spans, i = 0, [], [], 0

    while i < len(disk):
        start = i
        while i < len(disk) and disk[i] == (disk[start] if disk[start] != -1 else -1):
            i += 1
        if disk[start] != -1:
            files.append((disk[start], start, i - start))
        else:
            free_spans.append((start, i - start))

    files.sort(reverse=True, key=lambda x: x[0])

    for file_id, file_start, file_length in files:
        for span_start, span_length in free_spans:
            if span_length >= file_length and span_start < file_start:
                disk[span_start:span_start + file_length] = [file_id] * file_length
                disk[file_start:file_start + file_length] = [-1] * file_length

                free_spans.append((file_start, file_length))
                free_spans.remove((span_start, span_length))
                if span_length > file_length:
                    free_spans.append((span_start + file_length, span_length - file_length))
                free_spans.sort() 
                break
    return disk

def main(disk_map: List[int]):
    disk = []
    id = 0
    for i, e in enumerate(disk_map):
        if i % 2 == 0:
            disk.extend([id] * e)
            id += 1
        else:
            disk.extend([-1] * e)
    
    return (checksum(compact_disk_frag(disk.copy())), checksum(compact_disk_unify(disk.copy())))
if __name__ == "__main__":
    with open("./input.txt", "r") as file:
        disk_map = parse_input(file.read())
        print(main(disk_map))        
=======
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
>>>>>>> da774379b7ad77326f7c66aab3027859290bf29e
