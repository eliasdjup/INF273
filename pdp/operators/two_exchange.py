import random

from pdp.operators.utils import get_calls, rand_from_call, shuffle_call


def two_exchange(solution, prob):
    calls = get_calls(solution[0])

    rand1 = random.randrange(0, prob["n_vehicles"] + 1)
    rand2 = random.randrange(0, prob["n_vehicles"] + 1)

    while rand2 == rand1:
        rand2 = random.randrange(0, prob["n_vehicles"] + 1)

    if calls[rand1] == calls[rand2]:
        return solution[0]

    elif calls[rand1] == [0]:
        switch = rand_from_call(calls[rand2])
        calls[rand2].remove(switch)
        calls[rand2].remove(switch)

        calls[rand1].insert(0, switch)
        calls[rand1].insert(0, switch)

        calls[rand2] = shuffle_call(calls[rand2])
        return sum(calls, [])

    elif calls[rand2] == [0]:
        switch = rand_from_call(calls[rand1])
        calls[rand1].remove(switch)
        calls[rand1].remove(switch)

        calls[rand2].insert(0, switch)
        calls[rand2].insert(0, switch)

        calls[rand1] = shuffle_call(calls[rand1])
        return sum(calls, [])

    else:

        is_one_insert = random.choice([0, 1, 2]) == 0

        if is_one_insert:
            switch = rand_from_call(calls[rand2])
            calls[rand2].remove(switch)
            calls[rand2].remove(switch)

            calls[rand1].insert(0, switch)
            calls[rand1].insert(0, switch)

            calls[rand2] = shuffle_call(calls[rand2])
            return sum(calls, [])

        else:
            switch1 = rand_from_call(calls[rand1])
            switch2 = rand_from_call(calls[rand2])

            calls[rand1].remove(switch1)
            calls[rand1].remove(switch1)

            calls[rand2].remove(switch2)
            calls[rand2].remove(switch2)

            calls[rand1].insert(0, switch2)
            calls[rand1].insert(0, switch2)

            calls[rand2].insert(0, switch1)
            calls[rand2].insert(0, switch1)

            calls[rand1] = shuffle_call(calls[rand1])
            calls[rand2] = shuffle_call(calls[rand2])
            return sum(calls, [])
