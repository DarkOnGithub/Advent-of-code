fn can_access(lines: &[Vec<char>], x: i32, y: i32) -> bool {
    let height = lines.len() as i32;
    let width = lines[0].len() as i32;
    let mut adjacent_paper_count = 0;

    for x_adj in -1..=1 {
        for y_adj in -1..=1 {
            if x_adj == 0 && y_adj == 0 {
                continue;
            }

            let local_x = x + x_adj;
            let local_y = y + y_adj;

            if local_x >= 0 && local_x < width && local_y >= 0 && local_y < height {
                if lines[local_y as usize][local_x as usize] == '@' {
                    adjacent_paper_count += 1;
                }
            }
        }
    }

    adjacent_paper_count < 4
}

pub fn solver(input: &str, repeat: bool) -> i32 {
    let mut lines: Vec<Vec<char>> = input.lines().map(|line| line.chars().collect()).collect();
    let mut total_count = 0;
    let mut iter_count = 0;
    while total_count == 0 || iter_count != 0 {
        iter_count = 0;
        for y in 0..lines.len() {
            for x in 0..lines[y].len() {
                if lines[y][x] == '@'{
                    if can_access(&lines, x as i32, y as i32){
                        lines[y][x] = 'x';
                        total_count += 1;
                        iter_count += 1;
                    }
                }
            }
        }
        if !repeat {break}
    }
    total_count
}


pub fn day_4_solver_part_1(input: &str) -> i32 {
    solver(input, false)
}

pub fn day_4_solver_part_2(input: &str) -> i32 {
    solver(input, true)
}