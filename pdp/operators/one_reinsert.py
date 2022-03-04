
import random

def one_reinsert(solution, prob):
    calls = get_routes_as_list_w_zeroes(solution[0])
    rand = random.randrange(0, prob["n_vehicles"])
    one_reinsert_list = calls[rand]
    if len(one_reinsert_list) <= 1:
        add_list = calls[prob["n_vehicles"]]
        add = add_list[random.randrange(0, len(add_list))]
        calls[rand].insert(0, add)
        calls[rand].insert(0, add)

        calls[prob["n_vehicles"]].remove(add)
        calls[prob["n_vehicles"]].remove(add)

        return sum(calls, [])
    else:
        rand1 = random.choice(one_reinsert_list)
        if rand1 == 0:
            return solution[0]
        one_reinsert_list = [i for i in one_reinsert_list if i != rand1]
        calls[rand] = one_reinsert_list
    rand = random.randrange(1, prob["n_vehicles"])
    while rand == rand1:
        rand = random.randrange(1, prob["n_vehicles"])
    calls[rand].insert(0, rand1)
    calls[rand].insert(0, rand1)
    return sum(calls, [])



def get_routes_as_list_w_zeroes(solution):
    vehicles = []
    route = []
    for i in range(len(solution)):
        if solution[i] == 0:
            route.append(solution[i])
            vehicles.append(route)
            route = []
        else:
            route.append(solution[i])
    vehicles.append(route)
    return vehicles

