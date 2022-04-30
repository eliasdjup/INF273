from pdp.operators.utils import get_calls, rand_from_call, shuffle_call
from pdp.utils import feasibility_check, cost_function


def dummy_to_best(solution, prob):
    calls = get_calls(solution[0])
    # print(calls)
    if calls[-1] == []:
        return solution[0]

    # Select a random call in dummy
    dummy_call = rand_from_call(calls[-1])

    # Keep the best call
    best_p_s = solution[1]
    best_s = solution[0]

    # Place it in every veichle and check cost
    for i in range(prob["n_vehicles"]):
        calls = get_calls(solution[0])
        placement_calls = switch_call(calls, i, dummy_call)
        placement = sum(placement_calls, [])

        if feasibility_check(placement, prob):
            p_s = cost_function(placement, prob)
            if p_s < best_p_s:
                best_p_s = p_s
                best_s = placement

    return best_s


def switch_call(calls, i, dummy_call):
    res = calls.copy()
    res[-1].remove(dummy_call)
    res[-1].remove(dummy_call)

    res[i].insert(0, dummy_call)
    res[i].insert(0, dummy_call)

    res[i] = shuffle_call(res[i])
    return res
