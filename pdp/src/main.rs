use std::env;
use std::process;

use pdp::Config;

fn main() {
    // --snip--
    let args: Vec<String> = env::args().collect();

    let config = Config::new(&args).unwrap_or_else(|err| {
        println!("Problem parsing arguments: {}", err);
        process::exit(1);
    });

    println!("In file {}", config.filename);

    if let Err(e) = pdp::run(config) {
        // --snip--
        println!("Application error: {}", e);

        process::exit(1);
    }
}
