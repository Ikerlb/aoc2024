// cargo-deps: regex="1.11.1"
extern crate regex;

use std::io::{self, BufRead};
use regex::Regex;

fn part1(text: &str) -> usize {
    let re = Regex::new(r"mul\((\d{1,3}),(\d{1,3})\)").unwrap();
    return re
        .captures_iter(text)
        .map(|caps| {
            return caps
                .extract::<2>().1
                .iter()
                .map(|n| n.parse::<usize>().unwrap()) 
                .reduce(|a, b| a*b)
                .unwrap()
        })
        .sum::<usize>();
}

fn part2(text: &str) -> usize {
    let re = Regex::new(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)").unwrap();    
    let mut res = 0;
    let mut on = 1;
    for cap in re.captures_iter(text) {
        let m = &cap[0];
        if m == "do()" {
            on = 1;
        } else if m == "don't()" {
            on = 0;
        } else {
            let fst = &cap[1].parse::<usize>().unwrap(); 
            let snd = &cap[2].parse::<usize>().unwrap(); 
            res += fst * snd * on;
        }
    }
    return res;
}

fn main() -> io::Result<()> {
    let stdin = io::stdin();
    let text = stdin
        .lock()
        .lines()
        .map(|line_res| line_res.unwrap())
        .collect::<String>();

    println!("part 1 is {}", part1(&text)); 
    println!("part 2 is {}", part2(&text)); 

    Ok(())
}
