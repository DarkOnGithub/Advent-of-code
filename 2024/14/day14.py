import re
from typing import List, Tuple, Set

def parse_input(input: str) -> List[List[int]]:
    return [list(map(int, re.findall(r'-?\d+', line))) for line in input]

def project_bot_position(x: int, y: int, velocity_x: int, velocity_y: int, time_step: int, grid_width: int, grid_height: int) -> Tuple[int, int]:
    projected_x = (x + velocity_x * time_step) % grid_width - grid_width // 2
    projected_y = (y + velocity_y * time_step) % grid_height - grid_height // 2
    return projected_x, projected_y

def quandrant(bots: List[List[int]], grid_width: int, grid_height: int, time_step: int) -> int:
    quadrant_counts = [0, 0, 0, 0]
    for bot in bots:
        x, y = project_bot_position(*bot, time_step, grid_width, grid_height)
        if x > 0 and y > 0:
            quadrant_counts[0] += 1
        elif x > 0 and y < 0:
            quadrant_counts[1] += 1
        elif x < 0 and y > 0:
            quadrant_counts[2] += 1
        elif x < 0 and y < 0:
            quadrant_counts[3] += 1

    return quadrant_counts[0] * quadrant_counts[1] * quadrant_counts[2] * quadrant_counts[3]


def main() -> None:
    WIDTH, HEIGHT = 101, 103
    with open("./input.txt", "r") as f:
        robots = parse_input(f)
        quadrant_product = quandrant(robots, WIDTH, HEIGHT, 100)
        print(quadrant_product)

        for time_step in range(10000):
            unique_positions = {project_bot_position(*bot, time_step, WIDTH, HEIGHT) for bot in robots}
            if len(unique_positions) == len(robots):
                print(time_step)

if __name__ == "__main__":
    main()
