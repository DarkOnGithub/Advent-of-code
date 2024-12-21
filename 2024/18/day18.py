from typing import List, Tuple, Dict

def part1(coords: List[Tuple[int, int]]) -> None:

    n, m = 71, 71
    grid = [['.'] * m for _ in range(n)]
    for i in range(1024):
        x, y = coords[i]
        grid[y][x] = "#"
    print(bfs(grid))

def bfs(grid: List[List[str]]) -> int:

    n, m = len(grid), len(grid[0])
    queue = [(0, 0, 0)]
    visited = set()
    k = 0
    while k < len(queue):
        i, j, steps = queue[k]
        visited.add((i, j))
        if i == n - 1 and j == m - 1:
            return steps
        for ii, jj in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
            if (0 <= ii < n and 0 <= jj < m and 
                (ii, jj) not in visited and grid[ii][jj] != "#"):
                queue.append((ii, jj, steps + 1))
                visited.add((ii, jj))
        k += 1
    return 0

def part2(coords: List[Tuple[int, int]]) -> None:

    n, m = 71, 71
    grid = [['.'] * m for _ in range(n)]
    parents: Dict[Tuple[int, int], Tuple[int, int]] = {}
    compsize: Dict[Tuple[int, int], int] = {}

    for x, y in coords:
        grid[y][x] = "#"

    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char == ".":
                parents[(i, j)] = (i, j)
                compsize[(i, j)] = 1
                for ii, jj in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
                    if (0 <= ii < n and 0 <= jj < m and 
                        grid[ii][jj] == "." and (ii, jj) not in parents):
                        parents[(ii, jj)] = (ii, jj)
                        compsize[(ii, jj)] = 1
                        merge(parents, (i, j), (ii, jj), compsize)

    k = -1
    while repres(parents, (0, 0)) != repres(parents, (n - 1, m - 1)):
        j, i = coords[k]
        grid[i][j] = "."
        parents[(i, j)] = (i, j)
        compsize[(i, j)] = 1
        for ii, jj in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
            if 0 <= ii < n and 0 <= jj < m and grid[ii][jj] == ".":
                merge(parents, (i, j), (ii, jj), compsize)
        k -= 1
    print(j, i)

def merge(parents: Dict[Tuple[int, int], Tuple[int, int]],
          a: Tuple[int, int],
          b: Tuple[int, int],
          compsize: Dict[Tuple[int, int], int]) -> None:

    a, b = repres(parents, a), repres(parents, b)
    if a == b:
        return
    if compsize[a] < compsize[b]:
        a, b = b, a
    parents[b] = a
    compsize[a] += compsize[b]

def repres(parents: Dict[Tuple[int, int], Tuple[int, int]],
           x: Tuple[int, int]) -> Tuple[int, int]:

    if x not in parents:
        parents[x] = x
    while x != parents[x]:
        x = parents[x]
    return x

if __name__ == "__main__":
    fname = "input.txt"
    with open(fname) as file:
        coords = [[int(x) for x in line.strip().split(",")] for line in file]
    part1(coords)
    part2(coords)