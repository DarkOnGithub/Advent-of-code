from collections import defaultdict
from typing import List, Tuple, Dict

def parse_input(input_data: str) -> Tuple[Dict[int, List[int]], List[List[int]]]:
    rules = defaultdict(list)
    sections = input_data.split("\n\n")
    for line in sections[0].strip().split("\n"):
        rule_id, rule_value = map(int, line.split("|"))
        rules[rule_value].append(rule_id)

    updates = [list(map(int, line.split(","))) for line in sections[1].strip().split("\n") if line]
    return rules, updates

def process_rules(rules: Dict[int, List[int]], updates: List[List[int]]) -> Tuple[int, int]:
    output_1, output_2 = 0, 0

    for update in updates:
        if all(all(rule not in update[idx:] for rule in rules[num]) for idx, num in enumerate(update)):
            output_1 += update[len(update) // 2]

        modified = False
        while True:
            valid = True
            for i, num in enumerate(update):
                for rule in rules[num]:
                    if rule in update[i:]:
                        valid, modified, swap_idx = False, True, update.index(rule)
                        update[i], update[swap_idx] = update[swap_idx], update[i]
                        break
                if not valid:break
            if valid:break
            
        if modified:
            output_2 += update[len(update) // 2]
    return output_1, output_2

if __name__ == "__main__":
    with open("./input.txt", "r") as file:
        rule_set, updates = parse_input(file.read())
        print(process_rules(rule_set, updates))
