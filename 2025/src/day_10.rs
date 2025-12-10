use std::collections::{HashMap, VecDeque};

#[derive(Debug, Clone)]
struct Machine {
    target_lights: u64,
    n_lights: usize,
    buttons: Vec<u64>,
    joltage: Vec<i64>,
}

fn parse_input(input: &str) -> Vec<Machine> {
    input.lines()
        .filter_map(|line| {
            let line = line.trim();
            if line.is_empty() {
                return None;
            }

            let diagram_start = line.find('[')?;
            let diagram_end = line.find(']')?;
            let diagram = &line[diagram_start+1..diagram_end];

            let n_lights = diagram.len();
            let mut target_lights: u64 = 0;
            for (i, c) in diagram.chars().enumerate() {
                if c == '#' {
                    target_lights |= 1 << i;
                }
            }

            let brace_start = line.find('{')?;
            let buttons_part = &line[diagram_end+1..brace_start].trim();
            let buttons: Vec<u64> = buttons_part
                .split(')')
                .filter(|s| !s.trim().is_empty())
                .map(|button_str| {
                    let button_str = button_str.trim().strip_prefix('(').unwrap_or(button_str.trim());
                    if button_str.is_empty() {
                        0
                    } else {
                        let mut mask: u64 = 0;
                        for num_str in button_str.split(',') {
                            if let Ok(idx) = num_str.trim().parse::<usize>() {
                                mask |= 1 << idx;
                            }
                        }
                        mask
                    }
                })
                .filter(|&mask| mask != 0)
                .collect();

            let brace_end = line.find('}')?;
            let joltage_part = &line[brace_start+1..brace_end];
            let joltage: Vec<i64> = joltage_part
                .split(',')
                .filter_map(|s| s.trim().parse().ok())
                .collect();

            Some(Machine { target_lights, n_lights, buttons, joltage })
        })
        .collect()
}

fn find_minimum_presses_bfs(machine: &Machine) -> u64 {
    if machine.target_lights == 0 {
        return 0;
    }
    
    if machine.buttons.is_empty() {
        return 0;
    }

    let max_state = 1u64 << machine.n_lights;
    let mut dist: HashMap<u64, u64> = HashMap::new();
    let mut queue: VecDeque<u64> = VecDeque::new();
    
    queue.push_back(0);
    dist.insert(0, 0);
    
    while let Some(state) = queue.pop_front() {
        let current_dist = dist[&state];
        
        for &button_mask in &machine.buttons {
            let new_state = state ^ button_mask;
            
            if new_state == machine.target_lights {
                return current_dist + 1;
            }
            
            if new_state < max_state && !dist.contains_key(&new_state) {
                dist.insert(new_state, current_dist + 1);
                queue.push_back(new_state);
            }
        }
    }
    
    0
}

fn find_minimum_presses_subset(machine: &Machine) -> u64 {
    if machine.target_lights == 0 {
        return 0;
    }
    
    let n_buttons = machine.buttons.len();
    if n_buttons == 0 {
        return 0;
    }
    
    if n_buttons <= 20 {
        let mut min_presses = u64::MAX;

        for subset in 0u64..(1 << n_buttons) {
            let mut state: u64 = 0;
            let mut presses = 0u64;

            for (i, &button_mask) in machine.buttons.iter().enumerate() {
                if subset & (1 << i) != 0 {
                    state ^= button_mask;
                    presses += 1;
                }
            }

            if state == machine.target_lights && presses < min_presses {
                min_presses = presses;
            }
        }

        if min_presses == u64::MAX {
            return 0;
        }
        return min_presses;
    }

    let half = n_buttons / 2;
    let first_half = &machine.buttons[..half];
    let second_half = &machine.buttons[half..];
    
    let mut first_map: HashMap<u64, u64> = HashMap::new();
    for subset in 0u64..(1 << first_half.len()) {
        let mut state: u64 = 0;
        let mut presses = 0u64;
        
        for (i, &button_mask) in first_half.iter().enumerate() {
            if subset & (1 << i) != 0 {
                state ^= button_mask;
                presses += 1;
            }
        }
        
        first_map.entry(state)
            .and_modify(|p| *p = (*p).min(presses))
            .or_insert(presses);
    }
    
    let mut min_presses = u64::MAX;
    for subset in 0u64..(1 << second_half.len()) {
        let mut state: u64 = 0;
        let mut presses = 0u64;
        
        for (i, &button_mask) in second_half.iter().enumerate() {
            if subset & (1 << i) != 0 {
                state ^= button_mask;
                presses += 1;
            }
        }
        
        let needed_state = machine.target_lights ^ state;
        
        if let Some(&first_presses) = first_map.get(&needed_state) {
            let total = presses + first_presses;
            if total < min_presses {
                min_presses = total;
            }
        }
    }
    
    if min_presses == u64::MAX { 0 } else { min_presses }
}

fn find_minimum_presses_part1(machine: &Machine) -> u64 {
    if machine.n_lights <= 10 {
        find_minimum_presses_bfs(machine)
    } else {
        find_minimum_presses_subset(machine)
    }
}

fn button_to_indices(button: u64, max_idx: usize) -> Vec<usize> {
    (0..max_idx).filter(|&i| button & (1 << i) != 0).collect()
}

fn find_minimum_presses_joltage_bfs(buttons: &[Vec<usize>], targets: &[i64]) -> u64 {
    let n = targets.len();
    
    if targets.iter().all(|&t| t == 0) {
        return 0;
    }
    
    let targets_u: Vec<u64> = targets.iter().map(|&t| t as u64).collect();
    
    let start: Vec<u64> = vec![0; n];
    
    let mut visited: HashMap<Vec<u64>, u64> = HashMap::new();
    let mut queue: VecDeque<Vec<u64>> = VecDeque::new();
    
    visited.insert(start.clone(), 0);
    queue.push_back(start);
    
    while let Some(state) = queue.pop_front() {
        let dist = visited[&state];
        
        for button in buttons {
            let mut new_state = state.clone();
            let mut valid = true;
            
            for &idx in button {
                if idx < n {
                    new_state[idx] += 1;
                    if new_state[idx] > targets_u[idx] {
                        valid = false;
                        break;
                    }
                }
            }
            
            if !valid {
                continue;
            }
            
            if new_state == targets_u {
                return dist + 1;
            }
            
            if !visited.contains_key(&new_state) {
                visited.insert(new_state.clone(), dist + 1);
                queue.push_back(new_state);
            }
        }
    }
    
    0
}

fn solve_linear_system(buttons: &[Vec<usize>], targets: &[i64]) -> Option<u64> {
    let n_counters = targets.len();
    let n_buttons = buttons.len();

    if n_buttons == 0 {
        return if targets.iter().all(|&t| t == 0) { Some(0) } else { None };
    }

    let mut matrix: Vec<Vec<f64>> = vec![vec![0.0; n_buttons + 1]; n_counters];
    
    for (j, button) in buttons.iter().enumerate() {
        for &i in button {
            if i < n_counters {
                matrix[i][j] = 1.0;
            }
        }
    }
    
    for i in 0..n_counters {
        matrix[i][n_buttons] = targets[i] as f64;
    }

    let mut pivot_col = 0;
    let mut pivot_row = 0;
    let mut pivot_cols: Vec<usize> = Vec::new();

    while pivot_row < n_counters && pivot_col < n_buttons {
        let mut max_row = pivot_row;
        let mut max_val = matrix[pivot_row][pivot_col].abs();

        for row in pivot_row + 1..n_counters {
            if matrix[row][pivot_col].abs() > max_val {
                max_val = matrix[row][pivot_col].abs();
                max_row = row;
            }
        }

        if max_val < 1e-10 {
            pivot_col += 1;
            continue;
        }

        matrix.swap(pivot_row, max_row);

        let scale = matrix[pivot_row][pivot_col];
        for j in pivot_col..=n_buttons {
            matrix[pivot_row][j] /= scale;
        }

        for row in 0..n_counters {
            if row != pivot_row {
                let factor = matrix[row][pivot_col];
                for j in pivot_col..=n_buttons {
                    matrix[row][j] -= factor * matrix[pivot_row][j];
                }
            }
        }

        pivot_cols.push(pivot_col);
        pivot_row += 1;
        pivot_col += 1;
    }

    for row in pivot_row..n_counters {
        if matrix[row][n_buttons].abs() > 1e-10 {
            return None; // No solution
        }
    }
    
    let free_cols: Vec<usize> = (0..n_buttons)
        .filter(|c| !pivot_cols.contains(c))
        .collect();
    
    let n_free = free_cols.len();
    
    let mut max_free: Vec<i64> = vec![i64::MAX; n_free];
    for (fi, &fc) in free_cols.iter().enumerate() {
        for &idx in &buttons[fc] {
            if idx < n_counters {
                max_free[fi] = max_free[fi].min(targets[idx]);
            }
        }
        max_free[fi] = max_free[fi].min(300);
    }

    let mut min_total = i64::MAX;
    
    fn enumerate_free(
        matrix: &[Vec<f64>],
        pivot_cols: &[usize],
        free_cols: &[usize],
        max_free: &[i64],
        n_buttons: usize,
        targets: &[i64],
        current: &mut Vec<i64>,
        idx: usize,
        min_total: &mut i64,
    ) {
        if idx == free_cols.len() {
            let mut x: Vec<f64> = vec![0.0; n_buttons];

            for (fi, &fc) in free_cols.iter().enumerate() {
                x[fc] = current[fi] as f64;
            }

            for (pi, &pc) in pivot_cols.iter().enumerate().rev() {
                let mut val = matrix[pi][n_buttons];
                for j in pc + 1..n_buttons {
                    val -= matrix[pi][j] * x[j];
                }
                x[pc] = val;
            }

            let mut valid = true;
            let mut total: i64 = 0;
            
            for &xi in &x {
                let rounded = xi.round();
                if (xi - rounded).abs() > 1e-6 || rounded < -0.5 {
                    valid = false;
                    break;
                }
                total += rounded as i64;
            }
            
            if valid && total >= 0 && total < *min_total {
                *min_total = total;
            }
            
            return;
        }
        
        let max_val = max_free[idx].min(300) as i64;
        for val in 0..=max_val {
            current.push(val);
            enumerate_free(matrix, pivot_cols, free_cols, max_free, n_buttons, targets, current, idx + 1, min_total);
            current.pop();

            if *min_total <= (current.len() as i64) {
                break;
            }
        }
    }
    
    if n_free <= 6 {
        let mut current: Vec<i64> = Vec::new();
        enumerate_free(&matrix, &pivot_cols, &free_cols, &max_free, n_buttons, targets, &mut current, 0, &mut min_total);
    } else {
        let mut x: Vec<f64> = vec![0.0; n_buttons];
        
        for (pi, &pc) in pivot_cols.iter().enumerate().rev() {
            let mut val = matrix[pi][n_buttons];
            for j in pc + 1..n_buttons {
                val -= matrix[pi][j] * x[j];
            }
            x[pc] = val;
        }
        
        let mut valid = true;
        let mut total: i64 = 0;
        
        for &xi in &x {
            let rounded = xi.round();
            if (xi - rounded).abs() > 1e-6 || rounded < -0.5 {
                valid = false;
                break;
            }
            total += rounded as i64;
        }
        
        if valid && total >= 0 {
            min_total = total;
        }

        for trial in 0..100 {
            let mut x: Vec<f64> = vec![0.0; n_buttons];
            
            for (fi, &fc) in free_cols.iter().enumerate() {
                x[fc] = ((trial >> fi) & 3) as f64; // Try 0, 1, 2, 3
            }
            
            for (pi, &pc) in pivot_cols.iter().enumerate().rev() {
                let mut val = matrix[pi][n_buttons];
                for j in pc + 1..n_buttons {
                    val -= matrix[pi][j] * x[j];
                }
                x[pc] = val;
            }
            
            let mut valid = true;
            let mut total: i64 = 0;
            
            for &xi in &x {
                let rounded = xi.round();
                if (xi - rounded).abs() > 1e-6 || rounded < -0.5 {
                    valid = false;
                    break;
                }
                total += rounded as i64;
            }
            
            if valid && total >= 0 && total < min_total {
                min_total = total;
            }
        }
    }
    
    if min_total == i64::MAX {
        None
    } else {
        Some(min_total as u64)
    }
}

fn find_minimum_presses_part2(machine: &Machine) -> u64 {
    let buttons: Vec<Vec<usize>> = machine.buttons.iter()
        .map(|&mask| button_to_indices(mask, 64))
        .collect();
    
    let state_space: u64 = machine.joltage.iter()
        .map(|&t| (t as u64).saturating_add(1))
        .fold(1u64, |acc, x| acc.saturating_mul(x));

    if state_space <= 5_000_000 && machine.joltage.iter().all(|&t| t <= 100) {
        find_minimum_presses_joltage_bfs(&buttons, &machine.joltage)
    } else {
        solve_linear_system(&buttons, &machine.joltage).unwrap_or(0)
    }
}

pub fn day_10_solver_part_1(input: &str) -> u64 {
    let machines = parse_input(input);
    machines.iter().map(|machine| find_minimum_presses_part1(machine)).sum()
}

pub fn day_10_solver_part_2(input: &str) -> u64 {
    let machines = parse_input(input);
    machines.iter().map(|machine| find_minimum_presses_part2(machine)).sum()
}
