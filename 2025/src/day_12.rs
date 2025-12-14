pub fn day_12_solver_part_1(input: &str) -> usize {
    let (shapes, regions) = parse_input(input);
    let mut count = 0;

    for region in regions {
        if can_fit_presents(&shapes, &region) {
            count += 1;
        }
    }

    count
}

#[derive(Clone, Debug)]
struct Shape {
    grid: Vec<Vec<bool>>,
    width: usize,
    height: usize,
}

#[derive(Clone, Debug)]
struct Region {
    width: usize,
    height: usize,
    required: Vec<usize>,
}

fn parse_input(input: &str) -> (Vec<Shape>, Vec<Region>) {
    let lines: Vec<&str> = input.lines().collect();

    let mut split_index = 0;
    for (i, line) in lines.iter().enumerate() {
        if line.contains('x') {
            split_index = i;
            break;
        }
    }

    let shapes_section = &lines[0..split_index];
    let regions_section = &lines[split_index..];

    let shapes = parse_shapes(&shapes_section.join("\n"));
    let regions = parse_regions(&regions_section.join("\n"));

    (shapes, regions)
}

fn parse_shapes(section: &str) -> Vec<Shape> {
    let mut shapes = Vec::new();
    let mut current_shape: Vec<Vec<bool>> = Vec::new();
    let mut shape_index = None;

    for line in section.lines() {
        if line.trim().is_empty() {
            continue;
        }

        if line.contains(':') {
            if let Some(idx) = shape_index {
                let height = current_shape.len();
                let width = if height > 0 { current_shape[0].len() } else { 0 };
                shapes.push(Shape {
                    grid: current_shape,
                    width,
                    height,
                });
            }

            shape_index = Some(line.trim_end_matches(':').parse::<usize>().unwrap());
            current_shape = Vec::new();
        } else {
            let row: Vec<bool> = line.chars().map(|c| c == '#').collect();
            current_shape.push(row);
        }
    }

    if !current_shape.is_empty() {
        let height = current_shape.len();
        let width = if height > 0 { current_shape[0].len() } else { 0 };
        shapes.push(Shape {
            grid: current_shape,
            width,
            height,
        });
    }

    shapes
}

fn parse_regions(section: &str) -> Vec<Region> {
    let mut regions = Vec::new();

    for line in section.lines() {
        if line.trim().is_empty() {
            continue;
        }

        let parts: Vec<&str> = line.split(':').collect();
        if parts.len() != 2 {
            continue;
        }

        let size_part = parts[0].trim();
        let counts_part = parts[1].trim();

        let size_parts: Vec<&str> = size_part.split('x').collect();
        let width = size_parts[0].parse::<usize>().unwrap();
        let height = size_parts[1].parse::<usize>().unwrap();

        let required: Vec<usize> = counts_part
            .split_whitespace()
            .map(|s| s.parse::<usize>().unwrap())
            .collect();

        regions.push(Region {
            width,
            height,
            required,
        });
    }

    regions
}

fn can_fit_presents(shapes: &[Shape], region: &Region) -> bool {
    let mut total_area_needed = 0;
    for (shape_idx, &count) in region.required.iter().enumerate() {
        total_area_needed += count * shapes[shape_idx].width * shapes[shape_idx].height;
    }
    let total_grid_area = region.width * region.height;

    if total_area_needed > total_grid_area {
        return false;
    }

    let all_placements = precompute_placements(shapes, region);

    let mut placements_by_shape: Vec<Vec<(usize, usize, Shape)>> = vec![Vec::new(); shapes.len()];
    for (shape_idx, x, y, transform) in all_placements {
        placements_by_shape[shape_idx].push((x, y, transform));
    }

    let mut to_place = Vec::new();
    for (shape_idx, &count) in region.required.iter().enumerate() {
        for _ in 0..count {
            to_place.push(shape_idx);
        }
    }

    let mut grid = vec![vec![false; region.width]; region.height];
    improved_backtrack(&mut grid, &placements_by_shape, &to_place, 0)
}

fn precompute_placements(shapes: &[Shape], region: &Region) -> Vec<(usize, usize, usize, Shape)> {
    let mut placements = Vec::new();

    for (shape_idx, shape) in shapes.iter().enumerate() {
        let transformations = generate_transformations(shape);

        for transform in transformations {
            for y in 0..=(region.height.saturating_sub(transform.height)) {
                for x in 0..=(region.width.saturating_sub(transform.width)) {
                    placements.push((shape_idx, x, y, transform.clone()));
                }
            }
        }
    }

    placements
}

fn improved_backtrack(
    grid: &mut Vec<Vec<bool>>,
    placements_by_shape: &[Vec<(usize, usize, Shape)>],
    to_place: &[usize],
    index: usize,
) -> bool {
    if index == to_place.len() {
        return true;
    }

    let shape_idx = to_place[index];
    let possible_placements = &placements_by_shape[shape_idx];

    for &(x, y, ref transform) in possible_placements {
        if can_place(grid, transform, x, y) {
            place_shape(grid, transform, x, y);

            if improved_backtrack(grid, placements_by_shape, to_place, index + 1) {
                return true;
            }

            remove_shape(grid, transform, x, y);
        }
    }

    false
}

fn generate_transformations(shape: &Shape) -> Vec<Shape> {
    use std::collections::HashSet;

    let mut transformations = Vec::new();
    let mut seen = HashSet::new();

    let mut candidates = Vec::new();

    candidates.push(shape.clone());
    let mut current = shape.clone();
    for _ in 0..3 {
        current = rotate_90(&current);
        candidates.push(current.clone());
    }

    let flipped_h = flip_horizontal(shape);
    candidates.push(flipped_h.clone());
    current = flipped_h.clone();
    for _ in 0..3 {
        current = rotate_90(&current);
        candidates.push(current.clone());
    }

    for candidate in candidates {
        let key = format!("{:?}", candidate.grid);
        if !seen.contains(&key) {
            seen.insert(key);
            transformations.push(candidate);
        }
    }

    transformations
}

fn rotate_90(shape: &Shape) -> Shape {
    let new_height = shape.width;
    let new_width = shape.height;
    let mut new_grid = vec![vec![false; new_width]; new_height];

    for y in 0..shape.height {
        for x in 0..shape.width {
            new_grid[x][shape.height - 1 - y] = shape.grid[y][x];
        }
    }

    Shape {
        grid: new_grid,
        width: new_width,
        height: new_height,
    }
}

fn flip_horizontal(shape: &Shape) -> Shape {
    let mut new_grid = shape.grid.clone();
    for row in &mut new_grid {
        row.reverse();
    }
    Shape {
        grid: new_grid,
        width: shape.width,
        height: shape.height,
    }
}

fn flip_vertical(shape: &Shape) -> Shape {
    let mut new_grid = shape.grid.clone();
    new_grid.reverse();
    Shape {
        grid: new_grid,
        width: shape.width,
        height: shape.height,
    }
}

fn can_place(grid: &Vec<Vec<bool>>, shape: &Shape, x: usize, y: usize) -> bool {
    for dy in 0..shape.height {
        for dx in 0..shape.width {
            let grid_y = y + dy;
            let grid_x = x + dx;

            if shape.grid[dy][dx] && grid[grid_y][grid_x] {
                return false;
            }
        }
    }
    true
}

fn place_shape(grid: &mut Vec<Vec<bool>>, shape: &Shape, x: usize, y: usize) {
    for dy in 0..shape.height {
        for dx in 0..shape.width {
            let grid_y = y + dy;
            let grid_x = x + dx;

            if shape.grid[dy][dx] {
                grid[grid_y][grid_x] = true;
            }
        }
    }
}

fn remove_shape(grid: &mut Vec<Vec<bool>>, shape: &Shape, x: usize, y: usize) {
    for dy in 0..shape.height {
        for dx in 0..shape.width {
            let grid_y = y + dy;
            let grid_x = x + dx;

            if shape.grid[dy][dx] {
                grid[grid_y][grid_x] = false;
            }
        }
    }
}