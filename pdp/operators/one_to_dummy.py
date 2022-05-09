import random

from pdp.operators.utils import get_calls, rand_from_call, shuffle_call


def one_to_dummy(solution, prob):
    calls = get_calls(solution[0])
    rand = random.randrange(0, prob["n_vehicles"])

    # Corner case: if all calls are empty, place from dummy to vehicle
    if calls[:-1] == [[0]] * prob["n_vehicles"]:
        switch = rand_from_call(calls[-1])

        calls[-1].remove(switch)
        calls[-1].remove(switch)

        calls[rand].insert(0, switch)
        calls[rand].insert(0, switch)

        return sum(calls, [])

    while calls[rand] == [0]:
        rand = random.randrange(0, prob["n_vehicles"])

    switch = rand_from_call(calls[rand])

    calls[rand].remove(switch)
    calls[rand].remove(switch)

    calls[-1].insert(0, switch)
    calls[-1].insert(0, switch)

    calls[-1] = shuffle_call(calls[-1])
    return sum(calls, [])
