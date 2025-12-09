fn parse_input(input: &str) -> Vec<(i64, i64)> {
    input.lines()
        .map(|line| {
            let nums: Vec<i64> = line.split(',')
                .map(|num_str| num_str.trim().parse().unwrap())
                .collect();
            (nums[0], nums[1])
        })
        .collect()
}

fn is_on_edge(px: i64, py: i64, x1: i64, y1: i64, x2: i64, y2: i64) -> bool {
    if x1 == x2 {
        x1 == px && py >= y1.min(y2) && py <= y1.max(y2)
    } else {
        y1 == py && px >= x1.min(x2) && px <= x1.max(x2)
    }
}

fn is_inside_or_on_boundary(px: i64, py: i64, points: &[(i64, i64)]) -> bool {
    for i in 0..points.len() {
        let (x1, y1) = points[i];
        let (x2, y2) = points[(i + 1) % points.len()];
        if is_on_edge(px, py, x1, y1, x2, y2) {
            return true;
        }
    }

    let mut inside = false;
    let mut j = points.len() - 1;
    for i in 0..points.len() {
        let (xi, yi) = points[i];
        let (xj, yj) = points[j];
        
        if yi != yj && (yi > py) != (yj > py) {
            let x_intersect = xi + (xj - xi) * (py - yi) / (yj - yi);
            if px < x_intersect {
                inside = !inside;
            }
        }
        j = i;
    }
    
    inside
}

fn rectangle_fully_inside(min_x: i64, max_x: i64, min_y: i64, max_y: i64, points: &[(i64, i64)]) -> bool {
    if !is_inside_or_on_boundary(min_x, min_y, points) { return false; }
    if !is_inside_or_on_boundary(min_x, max_y, points) { return false; }
    if !is_inside_or_on_boundary(max_x, min_y, points) { return false; }
    if !is_inside_or_on_boundary(max_x, max_y, points) { return false; }

    for i in 0..points.len() {
        let (x1, y1) = points[i];
        let (x2, y2) = points[(i + 1) % points.len()];
        
        if x1 == x2 {
            if x1 > min_x && x1 < max_x {
                let edge_min_y = y1.min(y2);
                let edge_max_y = y1.max(y2);
                if edge_max_y > min_y && edge_min_y < max_y {
                    let mid_y = (edge_min_y.max(min_y) + edge_max_y.min(max_y)) / 2;
                    if !is_inside_or_on_boundary(x1 - 1, mid_y, points) ||
                       !is_inside_or_on_boundary(x1 + 1, mid_y, points) {
                        return false;
                    }
                }
            }
        } else {
            if y1 > min_y && y1 < max_y {
                let edge_min_x = x1.min(x2);
                let edge_max_x = x1.max(x2);
                if edge_max_x > min_x && edge_min_x < max_x {
                    let mid_x = (edge_min_x.max(min_x) + edge_max_x.min(max_x)) / 2;
                    if !is_inside_or_on_boundary(mid_x, y1 - 1, points) ||
                       !is_inside_or_on_boundary(mid_x, y1 + 1, points) {
                        return false;
                    }
                }
            }
        }
    }
    
    true
}

pub fn day_9_solver_part_1(input: &str) -> i64 {
    let points = parse_input(input);
    let mut max = 0i64;
    for p1 in 0..points.len() {
        for p2 in (p1 + 1)..points.len() {
            let (x1, y1) = points[p1];
            let (x2, y2) = points[p2];
            let width = (x1 - x2).abs() + 1;
            let height = (y1 - y2).abs() + 1;
            let area = width * height;
            if area > max {
                max = area;
            }
        }
    }
    max
}

pub fn day_9_solver_part_2(input: &str) -> i64 {
    let points = parse_input(input);
    let mut max = 0i64;

    for p1 in 0..points.len() {
        for p2 in (p1 + 1)..points.len() {
            let (x1, y1) = points[p1];
            let (x2, y2) = points[p2];

            let min_x = x1.min(x2);
            let max_x = x1.max(x2);
            let min_y = y1.min(y2);
            let max_y = y1.max(y2);

            if rectangle_fully_inside(min_x, max_x, min_y, max_y, &points) {
                let width = max_x - min_x + 1;
                let height = max_y - min_y + 1;
                let area = width * height;
                if area > max {
                    max = area;
                }
            }
        }
    }

    max
}
