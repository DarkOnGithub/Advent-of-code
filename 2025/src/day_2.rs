
pub fn day_2_solver_part_1(input: &str) -> i64 {
    let mut count: i64 = 0;
    for s in input.split(",") {
        let range: Vec<i64> = s.split("-")
            .map(|num_str| num_str.trim().parse::<i64>().unwrap())
            .collect();
        let lower = range[0];
        let upper = range[1];
        for n in lower..=upper {
            let num_str = n.to_string();
            if num_str.len() % 2 == 0 {
                let mid = num_str.len() / 2;
                let first_half = &num_str[..mid];
                let second_half = &num_str[mid..];
                if first_half == second_half {
                    count += n;
                }
            }
        }
    }
    count
}


fn has_repeating_sequence(num_str: &str) -> bool {
    let len = num_str.len();
    if len <= 1 {
        return false;
    }

    for seq_len in 1..=len/2 {
        if len % seq_len == 0 {
            let sequence = &num_str[..seq_len];
            let mut is_repeating = true;

            for i in (seq_len..len).step_by(seq_len) {
                if &num_str[i..i+seq_len] != sequence {
                    is_repeating = false;
                    break;
                }
            }

            if is_repeating {
                return true;
            }
        }
    }
    false
}

pub fn day_2_solver_part_2(input: &str) -> i64 {
    let mut count: i64 = 0;
    for s in input.split(",") {
        let range: Vec<i64> = s.split("-")
            .map(|num_str| num_str.trim().parse::<i64>().unwrap())
            .collect();
        let lower = range[0];
        let upper = range[1];
        for n in lower..=upper {
            let num_str = n.to_string();
            if has_repeating_sequence(&num_str) {
                count += n;
            }
        }
    }
    count
}
