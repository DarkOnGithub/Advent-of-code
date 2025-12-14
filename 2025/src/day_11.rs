use std::collections::{HashMap, HashSet};

pub fn day_11_solver_part_1(input: &str) -> usize {
    let graph = parse_graph(input);
    let paths = find_all_paths(&graph, "you", "out");
    paths.len()
}

pub fn day_11_solver_part_2(input: &str) -> usize {
    let graph = parse_graph(input);
    count_paths_visiting_both(&graph, "svr", "out", "dac", "fft")
}

fn parse_graph(input: &str) -> HashMap<String, Vec<String>> {
    let mut graph = HashMap::new();

    for line in input.lines() {
        if line.trim().is_empty() {
            continue;
        }

        let parts: Vec<&str> = line.split(':').collect();
        if parts.len() != 2 {
            continue;
        }

        let device = parts[0].trim().to_string();
        let outputs: Vec<String> = parts[1]
            .split_whitespace()
            .map(|s| s.to_string())
            .collect();

        graph.insert(device, outputs);
    }

    graph
}

fn find_all_paths(graph: &HashMap<String, Vec<String>>, start: &str, end: &str) -> Vec<Vec<String>> {
    let mut paths = Vec::new();
    let mut current_path = Vec::new();
    let mut visited = HashSet::new();

    dfs(graph, start, end, &mut current_path, &mut visited, &mut paths);

    paths
}

fn count_paths_visiting_both(
    graph: &HashMap<String, Vec<String>>,
    start: &str,
    end: &str,
    required1: &str,
    required2: &str,
) -> usize {
    let mut cache = HashMap::new();
    let mut visited = HashSet::new();

    dfs_count_visiting_both(
        graph,
        start,
        end,
        required1,
        required2,
        &mut visited,
        &mut cache,
        false,
        false,
    )
}

fn dfs(
    graph: &HashMap<String, Vec<String>>,
    current: &str,
    end: &str,
    current_path: &mut Vec<String>,
    visited: &mut HashSet<String>,
    paths: &mut Vec<Vec<String>>,
) {
    current_path.push(current.to_string());
    visited.insert(current.to_string());

    if current == end {
        paths.push(current_path.clone());
    } else {
        if let Some(outputs) = graph.get(current) {
            for output in outputs {
                if !visited.contains(output) {
                    dfs(graph, output, end, current_path, visited, paths);
                }
            }
        }
    }

    current_path.pop();
    visited.remove(current);
}

fn dfs_count_visiting_both(
    graph: &HashMap<String, Vec<String>>,
    current: &str,
    end: &str,
    required1: &str,
    required2: &str,
    visited: &mut HashSet<String>,
    cache: &mut HashMap<(String, bool, bool), usize>,
    visited_req1: bool,
    visited_req2: bool,
) -> usize {
    let cache_key = (current.to_string(), visited_req1, visited_req2);

    if let Some(&result) = cache.get(&cache_key) {
        return result;
    }

    visited.insert(current.to_string());

    let new_visited_req1 = visited_req1 || current == required1;
    let new_visited_req2 = visited_req2 || current == required2;

    let mut count = 0;

    if current == end {
        if new_visited_req1 && new_visited_req2 {
            count = 1;
        }
    } else {
        if let Some(outputs) = graph.get(current) {
            for output in outputs {
                if !visited.contains(output) {
                    count += dfs_count_visiting_both(
                        graph,
                        output,
                        end,
                        required1,
                        required2,
                        visited,
                        cache,
                        new_visited_req1,
                        new_visited_req2,
                    );
                }
            }
        }
    }

    visited.remove(current);
    cache.insert(cache_key, count);
    count
}

