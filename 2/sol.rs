use std::io::{self, BufRead};

fn parse(s: String) -> Vec<usize> {
    return s
        .split(" ")
        .map(|ss| ss.parse::<usize>().unwrap())
        .collect();
}

fn is_treshold_ascending(report: &Vec<usize>, treshold: usize) -> bool {
    return report
        .iter()
        .zip(report.iter().skip(1))
        .all(|(a, b)| b > a && (b - a) < treshold);
}

fn is_safe(report: &Vec<usize>, treshold: usize) -> bool {
    let fst = is_treshold_ascending(report, treshold);
    let rev = report.iter().rev().map(|&n| n).collect();
    let snd = is_treshold_ascending(&rev, treshold);
    return fst || snd;
}

fn part1(lines: &Vec<Vec<usize>>) -> usize {
    return lines
        .iter()
        .filter(|line| is_safe(line, 4))
        .count();
} 

fn rem_single_pos(v: &Vec<usize>) -> Vec<Vec<usize>> {
    return (0..v.len())
        .map(|i| {
            return v[..i]
                .iter()
                .cloned()
                .chain(v[i+1..].iter().cloned())
                .collect()
        })
        .collect();
}

fn part2(lines: &Vec<Vec<usize>>) -> usize {
    return lines
        .iter()
        .filter(|report| {
            return rem_single_pos(report)
                .iter()
                .any(|vs| is_safe(vs, 4))
        })
        .count();
}

fn main() -> io::Result<()> {
    let stdin = io::stdin();
    let lines = stdin
        .lock()
        .lines()
        .map(|line_res| parse(line_res.unwrap()))
        .collect::<Vec<_>>();

    println!("part 1: {}", part1(&lines));
    println!("part 2: {}", part2(&lines));
    Ok(())
}
