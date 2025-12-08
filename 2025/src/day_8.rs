
pub fn day_8_solver_part_1(input: &str) -> i64 {
    let boxes: Vec<(i64, i64, i64)> = input
        .lines()
        .filter(|line| !line.is_empty())
        .map(|line| {
            let parts: Vec<i64> = line.split(',').map(|s| s.parse().unwrap()).collect();
            (parts[0], parts[1], parts[2])
        })
        .collect();

    let n = boxes.len();

    let mut pairs: Vec<(i64, usize, usize)> = Vec::new();
    for i in 0..n {
        for j in (i + 1)..n {
            let dx = boxes[i].0 - boxes[j].0;
            let dy = boxes[i].1 - boxes[j].1;
            let dz = boxes[i].2 - boxes[j].2;
            let dist_sq = dx * dx + dy * dy + dz * dz;
            pairs.push((dist_sq, i, j));
        }
    }
    
    pairs.sort_by_key(|&(dist, _, _)| dist);
    
    let mut parent: Vec<usize> = (0..n).collect();
    let mut rank: Vec<usize> = vec![0; n];
    
    fn find(parent: &mut [usize], x: usize) -> usize {
        if parent[x] != x {
            parent[x] = find(parent, parent[x]);
        }
        parent[x]
    }
    
    fn union(parent: &mut [usize], rank: &mut [usize], x: usize, y: usize) -> bool {
        let px = find(parent, x);
        let py = find(parent, y);
        if px == py {
            return false;
        }
        if rank[px] < rank[py] {
            parent[px] = py;
        } else if rank[px] > rank[py] {
            parent[py] = px;
        } else {
            parent[py] = px;
            rank[px] += 1;
        }
        true
    }

    let connections_to_make = 1000;
    let mut connections_made = 0;
    
    for (_, i, j) in &pairs {
        if connections_made >= connections_to_make {
            break;
        }
        union(&mut parent, &mut rank, *i, *j);
        connections_made += 1;
    }

    let mut circuit_sizes: std::collections::HashMap<usize, i64> = std::collections::HashMap::new();
    for i in 0..n {
        let root = find(&mut parent, i);
        *circuit_sizes.entry(root).or_insert(0) += 1;
    }

    let mut sizes: Vec<i64> = circuit_sizes.values().cloned().collect();
    sizes.sort_by(|a, b| b.cmp(a)); // Sort descending

    let result = sizes.iter().take(3).product();
    result
}

pub fn day_8_solver_part_2(input: &str) -> i64 {
    let boxes: Vec<(i64, i64, i64)> = input
        .lines()
        .filter(|line| !line.is_empty())
        .map(|line| {
            let parts: Vec<i64> = line.split(',').map(|s| s.parse().unwrap()).collect();
            (parts[0], parts[1], parts[2])
        })
        .collect();
    
    let n = boxes.len();

    let mut pairs: Vec<(i64, usize, usize)> = Vec::new();
    for i in 0..n {
        for j in (i + 1)..n {
            let dx = boxes[i].0 - boxes[j].0;
            let dy = boxes[i].1 - boxes[j].1;
            let dz = boxes[i].2 - boxes[j].2;
            let dist_sq = dx * dx + dy * dy + dz * dz;
            pairs.push((dist_sq, i, j));
        }
    }
    
    pairs.sort_by_key(|&(dist, _, _)| dist);
    
    let mut parent: Vec<usize> = (0..n).collect();
    let mut rank: Vec<usize> = vec![0; n];
    
    fn find(parent: &mut [usize], x: usize) -> usize {
        if parent[x] != x {
            parent[x] = find(parent, parent[x]);
        }
        parent[x]
    }
    
    fn union(parent: &mut [usize], rank: &mut [usize], x: usize, y: usize) -> bool {
        let px = find(parent, x);
        let py = find(parent, y);
        if px == py {
            return false;
        }
        if rank[px] < rank[py] {
            parent[px] = py;
        } else if rank[px] > rank[py] {
            parent[py] = px;
        } else {
            parent[py] = px;
            rank[px] += 1;
        }
        true
    }

    let mut num_circuits = n;
    let mut last_connection: (usize, usize) = (0, 0);

    for (_, i, j) in &pairs {
        if num_circuits == 1 {
            break;
        }
        if union(&mut parent, &mut rank, *i, *j) {
            num_circuits -= 1;
            last_connection = (*i, *j);
        }
    }

    boxes[last_connection.0].0 * boxes[last_connection.1].0
}
