import random
import numpy as np

from pdp.operators.utils import get_calls, rand_from_call, shuffle_call


def two_exhange_capacity(solution, prob):
    calls = get_calls(solution[0])
    biggest_capacity, smallest_capacity = split_list(np.argsort(-prob["VesselCapacity"]))


    if [calls[i] for i in smallest_capacity] == [[0]]*len(smallest_capacity):
        return solution[0]
    
    frm = smallest_capacity[0]
    for i in smallest_capacity:
        if calls[i] != [0]:
            frm = i
            break
    
    wheights = [1/n for n in range(2,len(biggest_capacity)+2)]
    to = random.choices(biggest_capacity, weights=wheights, k=1)[0]

    frm_remove = rand_from_call(calls[frm])

    calls[frm].remove(frm_remove)
    calls[frm].remove(frm_remove)

    calls[to].insert(0, frm_remove)
    calls[to].insert(0, frm_remove)

    calls[to] = shuffle_call(calls[to])

    return sum(calls, [])
    
def split_list(a_list):
    half = len(a_list)//2
    return a_list[:half], a_list[half:]
