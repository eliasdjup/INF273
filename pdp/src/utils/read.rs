use std::error::Error;
use std::fs::File;
use std::io::{prelude::*, BufReader};
mod pdp;

pub fn run(filename: String) -> Result<pdp::Problem, Box<dyn Error>> {
    let file = File::open(filename)?;
    let reader = BufReader::new(file);
    let mut file_iter = reader.lines();

    file_iter.next();

    let n_nodes = parse_int(file_iter.next().unwrap().ok());

    file_iter.next();

    let n_veichles = parse_int(file_iter.next().unwrap().ok());

    file_iter.next();

    let mut a = vec![];
    for _i in 1..=n_veichles {
        a.push(parse_integers(file_iter.next().unwrap().ok().unwrap()));
    }

    file_iter.next();

    let n_calls = parse_int(file_iter.next().unwrap().ok());

    file_iter.next();

    let mut b = vec![];
    for _i in 1..=n_veichles {
        b.push(parse_integers(file_iter.next().unwrap().ok().unwrap()));
    }

    file_iter.next();

    let mut cargo = vec![];
    for _i in 1..=n_calls {
        let line = file_iter.next().unwrap().ok().unwrap();
        let splitted: Vec<&str> = line.split(",").collect();
        let strings: Vec<String> = splitted.iter().map(|&x| String::from(x)).collect();
        let mut floats: Vec<f32> = strings.iter().map(|x| parse_float(x)).collect();
        floats.remove(0);
        cargo.push(floats);
    }

    file_iter.next();

    let mut d = vec![];
    for _i in 1..=n_veichles * n_nodes * n_nodes {
        d.push(parse_integers(file_iter.next().unwrap().ok().unwrap()))
    }

    file_iter.next();

    let mut e = vec![];
    for _i in 1..=n_veichles * n_calls {
        e.push(parse_integers(file_iter.next().unwrap().ok().unwrap()));
    }

    let mut travel_time = vec![
        vec![vec![0; (n_nodes + 1) as usize]; (n_nodes + 1) as usize];
        (n_veichles + 1) as usize
    ];
    let mut travel_cost = vec![
        vec![vec![0; (n_nodes + 1) as usize]; (n_nodes + 1) as usize];
        (n_veichles + 1) as usize
    ];

    for j in 0..d.len() {
        travel_time[d[j][0] as usize][d[j][1] as usize][(d[j][2]) as usize] = d[j][3];
        travel_cost[d[j][0] as usize][d[j][1] as usize][(d[j][2]) as usize] = d[j][4];
    }

    /*
    VesselCapacity = np.zeros(num_vehicles)
    StartingTime = np.zeros(num_vehicles)
    FirstTravelTime = np.zeros((num_vehicles, num_nodes))
    FirstTravelCost = np.zeros((num_vehicles, num_nodes))
    A = np.array(A, dtype=np.int)
    for i in range(num_vehicles):
        VesselCapacity[i] = A[i, 3]
        StartingTime[i] = A[i, 2]
        for j in range(num_nodes):
            FirstTravelTime[i, j] = TravelTime[i + 1, A[i, 1], j + 1] + A[i, 2]
            FirstTravelCost[i, j] = TravelCost[i + 1, A[i, 1], j + 1]

            */

    let p = pdp::Problem::construct(n_nodes, n_veichles, n_calls);

    let ret = Ok(p);
    return ret;
}

fn parse_int(inp: std::option::Option<std::string::String>) -> i32 {
    return inp.unwrap().parse::<i32>().unwrap();
}

fn parse_integers(inp: std::string::String) -> Vec<i32> {
    let numbers: Result<Vec<i32>, _> = inp.split(",").map(|x| x.parse()).collect();
    let ret = numbers.unwrap();
    return ret;
}

fn parse_float(inp: &std::string::String) -> f32 {
    if inp.len() == 1 {
        return inp.parse::<f32>().unwrap();
    } else {
        let mut ret = inp.clone();
        ret.insert(1, '.');
        return ret.parse::<f32>().unwrap();
    }
}
