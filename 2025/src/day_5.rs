use std::ops::RangeInclusive;

pub fn day_5_solver_part_1(input: &str) -> i32 {
    let parts: Vec<&str> = input.split("\n\n").collect();
    let mut ranges: Vec<RangeInclusive<i64>> = Vec::new();
    for line in parts[0].lines() {
        let range: Vec<i64> = line.split("-").map(|e| e.trim().parse::<i64>().unwrap()).collect();
        let range_inc = range[0]..=range[1];
        ranges.push(range_inc);
    }
    let mut count = 0;
    for line in parts[1].lines() {
        let id = line.trim().parse::<i64>().unwrap();
        if ranges.iter().any(|range| range.contains(&id)) {
            count += 1;
        }
    }
    count
}

pub fn day_5_solver_part_2(input: &str) -> i64 {
    let parts: Vec<&str> = input.split("\n\n").collect();
    let mut ranges: Vec<(i64, i64)> = Vec::new();

    for line in parts[0].lines() {
        let range: Vec<i64> = line.split("-").map(|e| e.trim().parse::<i64>().unwrap()).collect();
        ranges.push((range[0], range[1]));
    }

    ranges.sort_by_key(|r| r.0);

    let mut merged: Vec<(i64, i64)> = Vec::new();
    for range in ranges {
        if let Some(last) = merged.last_mut() {
            if range.0 <= last.1 + 1 {
                last.1 = last.1.max(range.1);
            } else {
                merged.push(range);
            }
        } else {
            merged.push(range);
        }
    }

    let mut total = 0i64;
    for (start, end) in merged {
        total += end - start + 1;
    }

    total
}