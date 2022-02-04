use std::error::Error;
use std::fs::File;
use std::io::{prelude::*, BufReader};

pub fn run() -> Result<(), Box<dyn Error>> {
    let filename = "data/Call_18_Vehicle_5.txt";
    let file = File::open(filename)?;
    let reader = BufReader::new(file);
    let mut file_iter = reader.lines();

    file_iter.next();
    let n_nodes = parse_number(file_iter.next().unwrap());
    println!("Number of nodes: {}", n_nodes);
    file_iter.next();
    let n_veichles = parse_number(file_iter.next().unwrap());
    println!("Number of vehicles: {}", n_veichles);

    println!("{:?}", file_iter.next());

    for i in 1..n_veichles {}

    Ok(())
}

fn parse_number(inp: std::result::Result<std::string::String, std::io::Error>) -> i32 {
    return inp.ok().unwrap().parse::<i32>().unwrap();
}


