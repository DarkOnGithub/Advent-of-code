use std::fs::File;
use std::io::{BufRead, BufReader};


mod day_1;
mod day_2;
mod day_3;
mod day_4;
mod day_5;
mod day_6;
mod day_7;
mod day_8;
mod day_9;
mod day_10;
mod day_11;
mod day_12;

use day_1::*;
use day_2::*;
use day_3::*;
use day_4::*;
use day_5::*;
use day_6::*;
use day_7::*;
use day_8::*;
use day_9::*;
use day_10::*;
use day_11::*;
use day_12::*;


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

fn solve_day<T: std::fmt::Display>(input_path: &str, solver: fn(&str) -> T) {
    println!("\nSolving {}", input_path);
    let input = parse_input(&format!("inputs/{}", input_path));
    for (index, section) in input.iter().enumerate() {
        println!("Test {}: {}", index + 1, solver(section));
    }
}

fn main() {
    // solve_day("day_1.txt", day_1_solver_part_1);
    // solve_day("day_1.txt", day_1_solver_part_2);
    // solve_day("day_2.txt", day_2_solver_part_1);
    // solve_day("day_2.txt", day_2_solver_part_2);
    // solve_day("day_3.txt", day_3_solver_part_1);
    // solve_day("day_3.txt", day_3_solver_part_2);
    // solve_day("day_4.txt", day_4_solver_part_1);
    // solve_day("day_4.txt", day_4_solver_part_2);
    // solve_day("day_5.txt", day_5_solver_part_1);
    // solve_day("day_5.txt", day_5_solver_part_2);
    // solve_day("day_6.txt", day_6_solver_part_1);
    // solve_day("day_6.txt", day_6_solver_part_2);
    // solve_day("day_7.txt", day_7_solver_part_1);
    // solve_day("day_7.txt", day_7_solver_part_2);
    // solve_day("day_8.txt", day_8_solver_part_1);
    // solve_day("day_8.txt", day_8_solver_part_2);
    // solve_day("day_9.txt", day_9_solver_part_1);
    // solve_day("day_9.txt", day_9_solver_part_2);
    // solve_day("day_10.txt", day_10_solver_part_1);
    // solve_day("day_10.txt", day_10_solver_part_2);
    solve_day("day_11.txt", day_11_solver_part_1);
    solve_day("day_11.txt", day_11_solver_part_2);
    solve_day("day_12.txt", day_12_solver_part_1);
}
