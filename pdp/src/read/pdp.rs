#[derive(Debug)]
pub struct Problem {
    n_nodes: i32,
    n_veichles: i32,
    n_calls: i32,
    veichles: std::vec::Vec<std::vec::Vec<i32>>,
    veichle_calls: std::vec::Vec<std::vec::Vec<i32>>,
    calls: std::vec::Vec<std::vec::Vec<i32>>,
    edges: std::vec::Vec<std::vec::Vec<i32>>,
    nodes: std::vec::Vec<std::vec::Vec<i32>>,
}
impl Problem {
    pub fn construct(
        n_nodes: i32,
        n_veichles: i32,
        n_calls: i32,
        veichles: std::vec::Vec<std::vec::Vec<i32>>,
        veichle_calls: std::vec::Vec<std::vec::Vec<i32>>,
        calls: std::vec::Vec<std::vec::Vec<i32>>,
        edges: std::vec::Vec<std::vec::Vec<i32>>,
        nodes: std::vec::Vec<std::vec::Vec<i32>>,
    ) -> Problem {
        Problem {
            n_nodes: n_nodes,
            n_veichles: n_veichles,
            n_calls: n_calls,
            veichles: veichles,
            veichle_calls: veichle_calls,
            calls: calls,
            edges: edges,
            nodes: nodes,
        }
    }
    pub fn display(self) {
        println!("Number of nodes: {}", self.n_nodes);
    }
}
