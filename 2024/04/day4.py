XMAS = "XMAS"
DIRECTIONS = [
    (0, 1), (0, -1), (1, 0), (-1, 0),
    (1, 1), (-1, -1), (1, -1), (-1, 1)
]

def is_valid(grid, r, c):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])

def search_xmas(grid, r, c, dr, dc):
    for i in range(len(XMAS)):
        nr, nc = r + dr * i, c + dc * i
        if not is_valid(grid, nr, nc) or grid[nr][nc] != XMAS[i]:
            return False
    return True

def find_xmas(grid):
    return sum(
        search_xmas(grid, r, c, dr, dc)
        for r in range(len(grid))
        for c in range(len(grid[0]))
        if grid[r][c] == "X"
        for dr, dc in DIRECTIONS
    )

def find_x_mas(grid):
    rows, cols = len(grid), len(grid[0])
    return sum(
        grid[y][x] in "MS" and
        y + 2 < rows and x + 2 < cols and
        grid[y+1][x+1] == "A" and
        grid[y+2][x+2] in "MS" and
        grid[y+2][x] in "MS" and grid[y][x+2] in "MS" and
        grid[y+2][x] != grid[y][x+2] and grid[y+2][x+2] != grid[y][x]
        for y in range(rows) for x in range(cols)
    )

def main():
    with open("./input.txt", "r") as file:
        grid = [list(line.strip()) for line in file]
    print(find_xmas(grid), find_x_mas(grid))

if __name__ == "__main__":
    main()