from typing import Dict, Tuple

def calculate_fewest_key_presses(code: str, max_layers: int) -> int:
    Coordinates = Dict[str, Tuple[int, int]]
    
    key_positions = {
        key: (x, y) for y, row in enumerate([" ^A", "<v>"]) for x, key in enumerate(row)
    }
    
    key_distances = {
        (0, start_key, end_key): 1 for start_key in key_positions for end_key in key_positions
    }
    
    def total_key_presses(layer: int, key_sequence: str) -> int:
        return sum(
            key_distances[(layer, start, end)] 
            for start, end in zip('A' + key_sequence, key_sequence)
        )
    
    for layer in range(1, max_layers + 1):
        if layer == max_layers:
            key_positions = {
                key: (x, y) for y, row in enumerate(["789", "456", "123", " 0A"]) for x, key in enumerate(row)
            }
        
        for start_key, (start_x, start_y) in key_positions.items():
            for end_key, (end_x, end_y) in key_positions.items():
                horizontal_keys = ('>' if end_x > start_x else '<') * abs(end_x - start_x)
                vertical_keys = ('^' if end_y < start_y else 'v') * abs(end_y - start_y)
                
                horizontal_first = (
                    total_key_presses(layer - 1, horizontal_keys + vertical_keys + 'A')
                    if (end_x, start_y) != key_positions[' '] else float('inf')
                )
                
                vertical_first = (
                    total_key_presses(layer - 1, vertical_keys + horizontal_keys + 'A')
                    if (start_x, end_y) != key_positions[' '] else float('inf')
                )
                
                key_distances[(layer, start_key, end_key)] = min(horizontal_first, vertical_first)
    
    return total_key_presses(layer, code)

def main() -> None:
    with open("./input.txt", "r") as f:
        input_data = f.read()
    
    part_1 = sum(
        calculate_fewest_key_presses(code, 3) * int(code[:-1]) 
        for code in input_data.splitlines()
    )
    
    part_2 = sum(
        calculate_fewest_key_presses(code, 26) * int(code[:-1]) 
        for code in input_data.splitlines()
    )
    print(part_1, part_2)    

if __name__ == "__main__":
    main()
