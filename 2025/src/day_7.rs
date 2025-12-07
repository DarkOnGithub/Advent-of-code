pub fn day_7_solver_part_1(input: &str) -> i64 {
    let lines: Vec<&str> = input.lines().collect();
    let len = lines.first().unwrap().chars().count();
    let mut current_row_vec = vec![false; len];
    let mut next_row_vec = vec![false; len];
    let mut total = 0;
    for line in lines {
        for (i, char) in line.chars().enumerate() {
            if char == 'S' {
                next_row_vec[i] = true;
            }else if char == '^' {
                if !current_row_vec[i] { continue; } 
                total += 1;
                if i > 0 { next_row_vec[i - 1] = true; }
                if i < len - 1 { next_row_vec[i + 1] = true; }
            } else if char == '.' {
                if current_row_vec[i] { next_row_vec[i] = true; }
            }
        }
        current_row_vec.clone_from(&next_row_vec);
        next_row_vec.fill(false);
    }
    total
}
pub fn day_7_solver_part_2(input: &str) -> i64 {
    let lines: Vec<&str> = input.lines().collect();
    if lines.is_empty() { return 0; }
    
    let width = lines[0].len();
    
    let mut current_counts: Vec<i64> = vec![0; width];

    for line in lines {
        let mut next_counts: Vec<i64> = vec![0; width];
        let chars: Vec<char> = line.chars().collect();

        for i in 0..width {
            let char = chars[i];
            
            if char == 'S' {
                next_counts[i] += 1; 
            }
            else if current_counts[i] > 0 {
                if char == '.' {
                    next_counts[i] += current_counts[i];
                } else if char == '^' {
                    if i > 0 {
                        next_counts[i - 1] += current_counts[i];
                    }
                    if i < width - 1 {
                        next_counts[i + 1] += current_counts[i];
                    }
                }
            }
        }
        
        current_counts = next_counts;
    }

    current_counts.iter().sum()
}