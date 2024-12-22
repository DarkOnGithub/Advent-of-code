from typing import List, Dict, Tuple

def read_input(input: str) -> List[int]:
    return [int(line) for line in input.strip().split('\n')]

def get_next_secret(secret: int) -> int:
    secret = ((secret * 64) ^ secret) % 16777216
    secret = ((secret >> 5) ^ secret) % 16777216
    secret = ((secret * 2048) ^ secret) % 16777216
    return secret

def get_price(secret: int) -> int:
    return secret % 10

def find_patterns(initial_secret: int, num_iterations: int = 2000) -> Tuple[int, Dict[Tuple[int, ...], int]]:
    prices: List[int] = []
    differences: List[int] = []
    pattern_prices: Dict[Tuple[int, ...], int] = {}
    current_secret = initial_secret

    for _ in range(num_iterations):
        current_price = get_price(current_secret)
        prices.append(current_price)
        
        if len(prices) > 1:
            differences.append(prices[-1] - prices[-2])
            
        if len(differences) > 3:
            pattern = tuple(differences[-4:])
            if pattern not in pattern_prices:
                pattern_prices[pattern] = current_price
                
        current_secret = get_next_secret(current_secret)
    
    return current_secret, pattern_prices

def main(initial_secrets: List[int]) -> Tuple[int, int]:
    all_patterns: Dict[Tuple[int, ...], int] = {}
    final_sum = 0

    for secret in initial_secrets:
        final_secret, patterns = find_patterns(secret)
        final_sum += final_secret
        
        for pattern, price in patterns.items():
            all_patterns[pattern] = all_patterns.get(pattern, 0) + price

    return final_sum, max(all_patterns.values())

def main() -> None:
    with open('input.txt') as f:
        initial_secrets = read_input(f.read())
        part1, part2 = main(initial_secrets)
        print(part1)
        print(part2)

if __name__ == "__main__":
    main()