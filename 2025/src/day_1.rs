pub fn day_1_solver_part_1(input: &str) -> i32 {
    let mut current = 50;
    let mut zero_count = 0;
    for line in input.lines() {
        let first_char = line.chars().next().unwrap();
        let direction = if first_char == 'L' { -1 } else { 1 };
        let number: i32 = line[1..].trim().parse().unwrap();
        let new_position = current + (direction * number);
        current = ((new_position % 100) + 100) % 100;
        if current == 0 {
            zero_count += 1;
        }
    }
    zero_count
}

pub fn day_1_solver_part_2(input: &str) -> i32 {
    let mut current = 50;
    let mut zero_count = 0;
    for line in input.lines() {
        let first_char = line.chars().next().unwrap();
        let direction = if first_char == 'L' { -1 } else { 1 };
        let number: i32 = line[1..].trim().parse().unwrap();

        for _ in 0..number {
            current = ((current + direction) % 100 + 100) % 100;
            if current == 0 {
                zero_count += 1;
            }
        }
    }
    zero_count
}


