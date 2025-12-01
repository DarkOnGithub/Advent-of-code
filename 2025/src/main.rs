use std::fs::File;
use std::io::{BufRead, BufReader};

mod day_1;

use day_1::*;


const EXAMPLES_SEPARATOR: &str = "--[[--]]--";


fn parse_input(file_path: &str) -> Vec<String> {
    let file = File::open(file_path).unwrap();
    let reader = BufReader::new(file);
    let mut input = String::new();
    for line in reader.lines() {
        input.push_str(&line.unwrap());
        input.push('\n');
    }
    input.split(EXAMPLES_SEPARATOR).map(|s| s.trim().to_string()).collect()
}

fn solve_day(input_path: &str, solver: fn(&str) -> i32) {
    let input = parse_input(&format!("inputs/{}", input_path));
    for (index, section) in input.iter().enumerate() {
        println!("Test {}: {}", index + 1, solver(section));
    }
}
fn main() {
    solve_day("day_1.txt", day_1_solver_part_1);
    solve_day("day_1.txt", day_1_solver_part_2);

}
