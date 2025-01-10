use std::io::{self, BufRead};
use std::collections::{HashMap};

fn digits(mut n: usize) -> Vec<usize> {
    let mut res = if n != 0 {
        Vec::new()
    } else {
        vec![0]
    };
    while n > 0 {
        res.push(n % 10);
        n = n / 10;
    }
    res.reverse();
    return res;
}

fn from_digs(digs: &[usize]) -> usize {
    let mut res = 0;
    for d in digs {
        res = (res * 10) + d;
    }

    return res;
}

fn steps(mut stones: Vec<usize>, n: usize) -> Vec<usize> {
    for i in 0..n {
        stones = step(stones);
    }
    return stones; 
}

fn step(stones: Vec<usize>) -> Vec<usize> {
    let mut nstones = Vec::with_capacity(stones.len());
    for s in stones {
        if s == 0 {
            nstones.push(1usize);
            continue;
        }
        let digs = digits(s);
        if digs.len() % 2 == 0 {
            let half = digs.len() >> 1;
            nstones.push(from_digs(&digs[..half]));
            nstones.push(from_digs(&digs[half..]));
        } else {
            nstones.push(s * 2024);
        }
    }
    return nstones;
}

fn dp(cache: &mut HashMap<(usize, usize), usize>, n: usize, s: usize) -> usize {
    if s == 0 {
        return 1;
    }

    if let Some(&res) = cache.get(&(n, s)) {
        return res;
    }

    if n == 0 {
        let res = dp(cache, 1, s - 1);
        cache.insert((n, s), res);
        return res;
    }
    let digs = digits(n);
    let res = if digs.len() % 2 == 0 {
        let half = digs.len() >> 1;
        let lhs = dp(cache, from_digs(&digs[..half]), s - 1);
        let rhs = dp(cache, from_digs(&digs[half..]), s - 1);
        lhs + rhs
    } else {
        dp(cache, n * 2024, s - 1)
    };
    cache.insert((n, s), res);
    return res;
}

fn part1(stones: &Vec<usize>) -> usize {
    let nstones = stones
        .iter()
        .map(|&n| n)
        .collect::<Vec<_>>();
    return steps(nstones, 25).len()
}

fn part2(stones: &Vec<usize>) -> usize {
    let mut cache = HashMap::new();
    return stones
        .iter()
        .map(|&s| dp(&mut cache, s, 75))
        .sum();
}

fn main() -> io::Result<()> {
    let stdin = io::stdin();
    let mut lines = stdin
        .lock()
        .lines();
    let stones = lines
        .next()
        .unwrap()
        .unwrap()
        .split(" ")
        .map(|n| n.parse::<usize>().unwrap())
        .collect::<Vec<_>>();

    // p1
    println!("{}", part1(&stones));
    println!("{}", part2(&stones));

    Ok(())
}
