use std::env;
mod utils;

fn main() {

    let args: Vec<String> = env::args().collect();
    let filename = args[1].clone();
    let p = utils::read::run(filename);

    println!("{:?}", p)
}
