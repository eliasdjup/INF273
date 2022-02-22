#[derive(Debug)]
pub struct Problem {
    n_nodes: i32,
    n_veichles: i32,
    n_calls: i32,
}
impl Problem {
    pub fn construct(
        n_nodes: i32,
        n_veichles: i32,
        n_calls: i32,
    ) -> Problem {
        Problem {
            n_nodes: n_nodes,
            n_veichles: n_veichles,
            n_calls: n_calls,
        }
    }
    pub fn display(self) {
        println!("Number of nodes: {}", self.n_nodes);
    }
}
