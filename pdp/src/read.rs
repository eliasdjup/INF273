use std::error::Error;
use std::fs::File;
use std::io::{prelude::*, BufReader};
mod pdp;

pub fn run(filename: String) -> Result<pdp::Problem, Box<dyn Error>> {
    let file = File::open(filename)?;
    let reader = BufReader::new(file);
    let mut file_iter = reader.lines();

    file_iter.next();

    let n_nodes = parse_number(file_iter.next().unwrap().ok());

    file_iter.next();

    let n_veichles = parse_number(file_iter.next().unwrap().ok());

    file_iter.next();

    let mut veichles = vec![];
    for _i in 1..=n_veichles {
        let line = file_iter.next().unwrap().ok().unwrap();
        let numbers: Result<Vec<i32>, _> = line.split(",").map(|x| x.parse()).collect();
        let veichle_info = numbers.unwrap();
        veichles.push(veichle_info)
    }

    file_iter.next();

    let n_calls = parse_number(file_iter.next().unwrap().ok());

    file_iter.next();

    let mut veichle_calls = vec![];
    for _i in 1..=n_veichles {
        let line = file_iter.next().unwrap().ok().unwrap();
        let numbers: Result<Vec<i32>, _> = line.split(",").map(|x| x.parse()).collect();
        let veichle_call = numbers.unwrap();
        veichle_calls.push(veichle_call);
    }

    file_iter.next();

    let mut calls = vec![];
    for _i in 1..=n_calls {
        let line = file_iter.next().unwrap().ok().unwrap();
        let numbers: Result<Vec<i32>, _> = line.split(",").map(|x| x.parse()).collect();
        let call = numbers.unwrap();
        calls.push(call);
    }

    file_iter.next();

    let mut edges = vec![];
    for _i in 1..=n_veichles * n_nodes * n_nodes {
        let line = file_iter.next().unwrap().ok().unwrap();
        let numbers: Result<Vec<i32>, _> = line.split(",").map(|x| x.parse()).collect();
        let edge = numbers.unwrap();
        edges.push(edge)
    }

    file_iter.next();

    let mut nodes = vec![];
    for _i in 1..=n_veichles * n_calls {
        let line = file_iter.next().unwrap().ok().unwrap();
        let numbers: Result<Vec<i32>, _> = line.split(",").map(|x| x.parse()).collect();
        let node = numbers.unwrap();
        nodes.push(node);
    }

    let p = pdp::Problem::construct(n_nodes, n_veichles, n_calls, veichles, veichle_calls, calls, edges, nodes);

    let ret = Ok(p);
    return ret;
}

fn parse_number(inp: std::option::Option<std::string::String>) -> i32 {
    return inp.unwrap().parse::<i32>().unwrap();
}
