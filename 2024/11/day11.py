from typing import List, Dict

def parse_input(text: str) -> Dict[int, int]:
    return {int(i) : 1 for i in text.split(" ")}

def add(stones: Dict[int, int], stone_key: int, quantity: int):
    if not stone_key in stones:
        stones[stone_key] = quantity
    else:
        stones[stone_key] += quantity

def main(stones: Dict[int, int], blinks: int):
    for _   in range(blinks):
        new_blink_stones = {}
        for stone in stones:
            if stone == 0:
                add(new_blink_stones, 1, stones[stone])
            elif len(str(stone)) % 2 == 0:
                s = str(stone)
                mid = len(s) // 2
                add(new_blink_stones, int(s[:mid]), stones[stone])
                add(new_blink_stones, int(s[mid:]), stones[stone])
            else:
                add(new_blink_stones, stone * 2024, stones[stone])
        stones = new_blink_stones

    return sum(stones.values())

if __name__ == "__main__":
  with open("./input.txt", "r") as f: 
      stones = parse_input(f.read())
      print(main(stones, 25))
      print(main(stones, 75))
  
