import collections
from typing import Dict, Set, Iterator, List

def read_graph(file) -> Dict[str, Set[str]]:
    graph = collections.defaultdict(set)
    for line in file:
        node1, node2 = line.strip().split('-')
        graph[node1].add(node2)
        graph[node2].add(node1)
    return graph

def find_triple(graph: Dict[str, Set[str]]) -> Set[str]:
    triples = set()
    for node1 in graph:
        for node2 in graph[node1]:
            for node3 in graph[node2]:
                if node3 in graph[node1]:  
                    if any(n.startswith('t') for n in (node1, node2, node3)):
                        triples.add(','.join(sorted([node1, node2, node3])))
    return triples

def find_maximum_clique(graph: Dict[str, Set[str]]) -> List[str]:
    def bron_kerbosch(result: Set[str], candidates: Set[str], excluded: Set[str]) -> Iterator[Set[str]]:
        if not candidates and not excluded:
            yield result
            return

        for vertex in list(candidates):  
            new_candidates = candidates & graph[vertex]
            new_excluded = excluded & graph[vertex]
            yield from bron_kerbosch(
                result | {vertex},
                new_candidates,
                new_excluded
            )
            candidates.remove(vertex)
            excluded.add(vertex)

    max_clique = max(
        bron_kerbosch(set(), set(graph.keys()), set()),
        key=len
    )
    return sorted(max_clique)

def main(graph: Dict[str, Set[str]]) -> None:
    print(len(find_triple(graph)))
    print( ','.join(find_maximum_clique(graph)))

if __name__ == '__main__':
    with open("input.txt") as f:
        graph = read_graph(f)
        main(graph)