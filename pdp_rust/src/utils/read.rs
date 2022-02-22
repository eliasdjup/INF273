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


    let mut vessel_capacity = vec![];
    let mut starting_time = vec![];
    let mut first_travel_time = vec![vec![0; (n_nodes) as usize]; (n_veichles) as usize];
    let mut first_travel_cost = vec![vec![0; (n_nodes) as usize]; (n_veichles) as usize];


    for i in 0..n_veichles {
        vessel_capacity.push(a[i as usize][3]);
        starting_time.push(a[i as usize][2]);
        for j in 0..n_nodes {
            first_travel_time[i as usize][j as usize] = (travel_time[(i+1) as usize][a[i as usize][1] as usize][(j+1) as usize]) + (a[i as usize][2]);
            first_travel_cost[i as usize][j as usize] = travel_cost[(i+1) as usize][a[i as usize][1] as usize][(j+1) as usize];
        }
    }

    let travel_time_ret = slice(travel_time);
    let travel_cost_ret = slice(travel_cost);

    let mut vessel_cargo = vec![];

    for i in 0..n_veichles {
        let temp = &b[i as usize][1..];

        vessel_cargo[i as usize][b[i as usize][1..]]
    }

    /*
    TravelTime = TravelTime[1:, 1:, 1:]
    TravelCost = TravelCost[1:, 1:, 1:]
    VesselCargo = np.zeros((num_vehicles, num_calls + 1))
    B = np.array(B, dtype=object)
    for i in range(num_vehicles):
        VesselCargo[i, np.array(B[i][1:], dtype=np.int)] = 1
    VesselCargo = VesselCargo[:, 1:]

    LoadingTime = np.zeros((num_vehicles + 1, num_calls + 1))
    UnloadingTime = np.zeros((num_vehicles + 1, num_calls + 1))
    PortCost = np.zeros((num_vehicles + 1, num_calls + 1))
    E = np.array(E, dtype=np.int)
    for i in range(num_vehicles * num_calls):
        LoadingTime[E[i, 0], E[i, 1]] = E[i, 2]
        UnloadingTime[E[i, 0], E[i, 1]] = E[i, 4]
        PortCost[E[i, 0], E[i, 1]] = E[i, 5] + E[i, 3]
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

fn slice(inp: std::vec::Vec<std::vec::Vec<std::vec::Vec<i32>>>) -> std::vec::Vec<std::vec::Vec<std::vec::Vec<i32>>> {

    let mut ret = vec![];

    for x in &inp[1..] {
        let mut x_l = vec![];
        for y in &x[1..] {
            let mut y_l = vec![];
            for z in &y[1..] {
                y_l.push(z.clone());
            }
            x_l.push(y_l);
        }
        ret.push(x_l);
    }

    return ret;
}
