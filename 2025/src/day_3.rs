
fn largest_k_digit_number(digits: &[u32], k: usize) -> u64 {
    if digits.len() < k {
        return 0;
    }

    let to_remove = digits.len() - k;
    let mut stack = Vec::new();
    let mut removed = 0;

    for &digit in digits {
        while !stack.is_empty() && *stack.last().unwrap() < digit && removed < to_remove {
            stack.pop();
            removed += 1;
        }
        stack.push(digit);
    }

    while removed < to_remove {
        stack.pop();
        removed += 1;
    }

    let mut result = 0u64;
    for &digit in &stack {
        result = result * 10 + digit as u64;
    }
    result
}

pub fn day_3_solver_part_1(input: &str) -> u64 {
    let mut total = 0;
    for line in input.lines() {
        let digits: Vec<u32> = line
            .chars()
            .filter_map(|c| c.to_digit(10))
            .collect();

        total += largest_k_digit_number(&digits, 2);
    }
    total
}

pub fn day_3_solver_part_2(input: &str) -> u64 {
    let mut total = 0;
    for line in input.lines() {
        let digits: Vec<u32> = line
            .chars()
            .filter_map(|c| c.to_digit(10))
            .collect();

        total += largest_k_digit_number(&digits, 12);
    }
    total
}
