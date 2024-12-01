use std::io::{self, BufRead};
use std::collections::HashMap;

fn parse_line(s: String) -> Option<(usize, usize)> {
    let mut g = s
        .split_whitespace()
        .map(|ns| ns.parse::<usize>().unwrap());
    return Some((g.next().unwrap(), g.next().unwrap()))
}

fn part1(lines: &Vec<(usize, usize)>) -> usize {
    let (mut llist, mut rlist): (Vec<_>, Vec<_>) = lines
        .iter()
        .cloned()
        .unzip();

    llist.sort();
    rlist.sort(); 

    return llist
        .iter()
        .zip(rlist)
        .map(|(&l, r)| (l as isize - r as isize).abs() as usize)
        .sum();
}

fn counter(v: &Vec<usize>) -> HashMap<usize, usize> {
    let mut res = HashMap::new();
    for &n in v {
        *res.entry(n).or_insert(0) += 1;
    }
    return res;
}

fn part2(lines: &Vec<(usize, usize)>) -> usize {
    let (mut llist, mut rlist): (Vec<_>, Vec<_>) = lines
        .iter()
        .cloned()
        .unzip();

    let rc = counter(&rlist);
    return llist
        .iter()
        .map(|n| *rc.get(&n).unwrap_or(&0) * n)
        .sum();
}

fn main() -> io::Result<()> {
    let stdin = io::stdin();
    let lines: Vec<_> = stdin
        .lock()
        .lines()
        .filter_map(|line_res| parse_line(line_res.unwrap()))
        .collect::<Vec<_>>();

    println!("part1 {:?}", part1(&lines));
    println!("part2 {:?}", part2(&lines));

    Ok(())
} 
