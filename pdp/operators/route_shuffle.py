import random

from pdp.operators.utils import get_calls, rand_from_call, shuffle_call
from pdp.utils import cost_function, feasibility_check


def route_shuffle(solution, prob):
    calls = get_calls(solution[0])

    rand_v = random.randrange(0, prob["n_vehicles"])

    if calls[rand_v] == [0]:
        return solution[0]

    n_shuffles = 3

    best_shuffle_c = cost_function(
        solution[0],
        prob,
    )
    best_shuffle = solution[0]

    for i in range(n_shuffles):

        calls = get_calls(solution[0])
        shuffled_calls = shuffle_call(calls)
        shuffled = sum(shuffled_calls, [])

        if feasibility_check(shuffled, prob):
            current_c = cost_function(shuffled, prob)
            if current_c < best_shuffle_c:
                best_shuffle_c = current_c
                best_shuffle = sum(calls, [])

    return best_shuffle
