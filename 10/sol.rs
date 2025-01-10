use std::io::{self, BufRead};
use std::collections::{VecDeque, HashSet};

fn parse_line(s: String) -> Vec<usize> {
    return s
        .chars()
        .map(|c| c.to_digit(10).unwrap() as usize)
        .collect::<Vec<_>>();
}

fn neighbors(grid: &mut Vec<Vec<usize>>, r: usize, c: usize) -> Vec<(usize, usize)> {
    let dirs = vec![(1,0), (0,1), (-1,0), (0,-1)];
    let ri = r as isize;
    let ci = c as isize;
    let n = grid.len() as isize;
    let m = grid[0].len() as isize;
    let mut res = Vec::new();
    for (dr, dc) in dirs {
        if ri + dr < 0 || ri + dr >= n {
            continue;
        } else if ci + dc < 0 || ci + dc >= m {
            continue;
        } else {
            res.push((ri as usize, ci as usize));
        }
    }
    return res;
}

fn main() -> io::Result<()> {
    let stdin = io::stdin();
    let grid = stdin
        .lock()
        .lines()
        .map(|res_s| parse_line(res_s.unwrap()))
        .collect::<Vec<_>>();

    

    Ok(())
}
