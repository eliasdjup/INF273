use std::env;
mod read;

fn main() {

    let args: Vec<String> = env::args().collect();
    let filename = args[1].clone();
    let p = read::run(filename);

    println!("{:?}", p)
}
