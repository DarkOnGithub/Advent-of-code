from typing import List, Dict, Set, Tuple
from dataclasses import dataclass

def read_input() -> Tuple[List[str], List[str]]:
    with open("input.txt") as f:
        patterns, documents = f.read().strip().split('\n\n')
        return (
            [p.strip() for p in patterns.split(',')],
            [d.strip() for d in documents.split('\n')]
        )

def count_matches(document: str, patterns: List[str], memo: Dict[str, int] = None) -> int:
    if memo is None:
        memo = {}
    
    if document in memo:
        return memo[document]
    
    if not document:
        return 1
        
    matches = 0
    for pattern in patterns:
        if document.startswith(pattern):
            remaining = document[len(pattern):]
            matches += count_matches(remaining, patterns, memo)
            
    memo[document] = matches
    return matches

def process_documents(patterns: List[str], documents: List[str]) -> Tuple[int, int]:
    valid_docs = 0
    total_matches = 0
    
    for doc in documents:
        matches = count_matches(doc, patterns)
        valid_docs += bool(matches)
        total_matches += matches
        
    return valid_docs, total_matches

def solve() -> Tuple[int, int]:
    patterns, documents = read_input()
    return process_documents(patterns, documents)

if __name__ == "__main__":
    part1, part2 = solve()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")