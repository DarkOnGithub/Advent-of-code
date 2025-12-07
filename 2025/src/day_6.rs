fn calculate(grid: Vec<Vec<&str>>) -> i64{
    let last_line = grid.last().unwrap();
    let mut total = 0i64;

    for (i, &operation) in last_line.iter().enumerate() {
        let mut col = grid[0][i].parse::<i64>().unwrap();

        for row in &grid[1..grid.len() - 1] {
            let num = row[i].parse::<i64>().unwrap();
            match operation {
                "*" => col *= num,
                "+" => col += num,
                _ => {}
            }
        }

        total += col;
    }
    total
}
pub fn day_6_solver_part_1(input: &str) -> i64 {
    let grid: Vec<Vec<&str>> = input
        .lines()
        .map(|line| line.split_whitespace().collect())
        .collect();
    calculate(grid)
}

fn calculate_right_to_left(grid: Vec<Vec<char>>) -> i64 {
    if grid.is_empty() {
        return 0;
    }

    let rows = grid.len();
    let cols = grid[0].len();
    let mut total = 0i64;
    let mut numbers: Vec<i64> = Vec::new();

    for col in (0..cols).rev() {
        let mut digits = String::new();
        for row in 0..rows - 1 {
            let ch = grid[row][col];
            if !ch.is_whitespace() {
                digits.push(ch);
            }
        }

        let op = grid[rows - 1][col];
        let is_separator = digits.is_empty() && op.is_whitespace();
        if is_separator {
            continue;
        }

        let value = digits.parse::<i64>().unwrap();
        numbers.push(value);

        if op == '+' || op == '*' {
            let result = match op {
                '+' => numbers.iter().copied().sum::<i64>(),
                '*' => numbers.iter().copied().product::<i64>(),
                _ => unreachable!(),
            };
            total += result;
            numbers.clear();
        }
    }

    total
}

pub fn day_6_solver_part_2(input: &str) -> i64 {
    let lines: Vec<&str> = input.lines().collect();
    let max_len = lines.iter().map(|line| line.len()).max().unwrap_or(0);

    let grid: Vec<Vec<char>> = lines
        .into_iter()
        .map(|line| {
            let mut chars: Vec<char> = line.chars().collect();
            if chars.len() < max_len {
                chars.extend(std::iter::repeat(' ').take(max_len - chars.len()));
            }
            chars
        })
        .collect();

    calculate_right_to_left(grid)
}
