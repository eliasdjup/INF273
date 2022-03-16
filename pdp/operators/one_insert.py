import random

from operators.utils import get_calls, rand_from_call, shuffle_call


def one_insert(solution, prob):
    calls = get_calls(solution[0])
    rand1 = random.randrange(0, prob["n_vehicles"] + 1)

    if calls[rand1] == [0]:
        rand2 = random.randrange(0, prob["n_vehicles"] + 1)
        while calls[rand2] == [0]:
            rand2 = random.randrange(0, prob["n_vehicles"] + 1)

        switch = rand_from_call(calls[rand2])
        calls[rand2].remove(switch)
        calls[rand2].remove(switch)

        calls[rand1].insert(0, switch)
        calls[rand1].insert(0, switch)

        calls[rand2] = shuffle_call(calls[rand2])
        return sum(calls, [])

    else:
        rand2 = random.randrange(0, prob["n_vehicles"] + 1)
        while rand2 == rand1:
            rand2 = random.randrange(0, prob["n_vehicles"] + 1)

        switch = rand_from_call(calls[rand1])
        calls[rand1].remove(switch)
        calls[rand1].remove(switch)

        calls[rand2].insert(0, switch)
        calls[rand2].insert(0, switch)

        calls[rand1] = shuffle_call(calls[rand1])
        calls[rand2] = shuffle_call(calls[rand2])
        return sum(calls, [])