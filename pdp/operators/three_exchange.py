import random

from operators.utils import get_calls, rand_from_call, shuffle_call


def three_exchange(solution, prob):
    calls = get_calls(solution[0])

    rand1 = random.randrange(0, prob["n_vehicles"] + 1)
    rand2 = random.randrange(0, prob["n_vehicles"] + 1)
    rand3 = random.randrange(0, prob["n_vehicles"] + 1)

    while (
        rand1 == rand2
        or rand2 == rand3
        or rand1 == rand3
        and calls[rand1] == calls[rand2] == calls[rand3]
    ):
        rand1 = random.randrange(0, prob["n_vehicles"] + 1)
        rand2 = random.randrange(0, prob["n_vehicles"] + 1)
        rand3 = random.randrange(0, prob["n_vehicles"] + 1)

    into1 = rand_from_call(calls[rand3])
    into2 = rand_from_call(calls[rand1])
    into3 = rand_from_call(calls[rand2])


    rand1_is_one_insert = random.choice([0, 1, 2]) == 0
    rand2_is_one_insert = random.choice([0, 1, 2]) == 0
    rand3_is_one_insert = random.choice([0, 1, 2]) == 0

    if into1 != 0 and not rand1_is_one_insert:

        calls[rand3].remove(into1)
        calls[rand3].remove(into1)

        calls[rand1].insert(0, into1)
        calls[rand1].insert(0, into1)

    if into2 != 0 and not rand2_is_one_insert:
        calls[rand1].remove(into2)
        calls[rand1].remove(into2)

        calls[rand2].insert(0, into2)
        calls[rand2].insert(0, into2)

    if into3 != 0 and not rand3_is_one_insert:
        calls[rand2].remove(into3)
        calls[rand2].remove(into3)

        calls[rand3].insert(0, into3)
        calls[rand3].insert(0, into3)

    calls[rand1] = shuffle_call(calls[rand1])
    calls[rand2] = shuffle_call(calls[rand2])
    calls[rand3] = shuffle_call(calls[rand3])

    return sum(calls, [])
