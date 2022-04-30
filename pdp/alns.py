import numpy as np
import random
from statistics import mean
import time
from pdp.operators.one_insert import one_insert
from pdp.operators.two_exchange import two_exchange
from pdp.operators.three_exchange import three_exchange
import progressbar
import math
from pdp.operators.dummy_to_best import dummy_to_best
from pdp.operators.route_shuffle import route_shuffle
from pdp.operators.two_exchange_capacity import two_exhange_capacity

from pdp.utils import cost_function, feasibility_check, generate_s_0, load_problem

MAX_ITER = 10000
MAX_TIME = 120
RUN_MODE = False
FOUND = set()


def alns(s_0, instance):
    best_s = [s_0, cost_function(s_0, instance)]
    incumbent = [s_0, cost_function(s_0, instance)]

    operators = [two_exhange_capacity, dummy_to_best, route_shuffle, one_insert, two_exchange, three_exchange]
    escape_its = 500

    curr_weights = [1.0 for _ in operators]
    usage = [0 for _ in operators]
    total_usage = [0 for _ in operators]


    prev_weights = curr_weights.copy()
    end = time.time() + MAX_TIME

    its_since_upd, iteration, diversification_its = 0, 0, 0
    
    t0 = 38
    t = t0
    a = 0.998
    weights_refresh_rate = 200
    diversification_rate = 250
    iteration = 0

    bar = progressbar.ProgressBar(
        maxval=MAX_ITER,
        widgets=[progressbar.Bar("=", "[", "]"), " ", progressbar.Percentage()],
    )
    bar.start()

    while iteration < MAX_ITER and (not RUN_MODE or time.time() < end):
        if its_since_upd == escape_its:
            incumbent = [s_0, cost_function(s_0, instance)]
            t0 = 38
            t = t0
            its_since_upd = 0
            curr_weights.clear()
            usage.clear()
            FOUND.clear()
            curr_weights = [1.0 for _ in operators]
            usage = [0 for _ in operators]
            prev_weights = curr_weights.copy()

        if its_since_upd > diversification_rate:
            #print(" need to diversify")
            #current = obo.move_to_dummy(s) DO diversification operator
            diversification_its += 1

        if iteration % weights_refresh_rate == 0 and iteration > 0:
            prev_weights = curr_weights
            curr_weights = regulate_weights(prev_weights, curr_weights, usage)
            for i in range(len(operators)):
                usage[i] = 0

        chosen_operator = random.choices(operators, prev_weights, k=1)[0]
        chosen_operator_index = operators.index(chosen_operator)

        new_s = chosen_operator(incumbent, instance)
        new_s_feasiblity, c = feasibility_check(new_s, instance)
        curr_weights = update_weights(new_s[0], curr_weights, chosen_operator_index, new_s[1], best_s[1])
        usage[chosen_operator_index] += 1

        if new_s_feasiblity:
            new_s_cost = cost_function(new_s, instance)
            delta_e = new_s_cost - incumbent[1]

            if delta_e < 0:
                incumbent = [new_s, new_s_cost]
                its_since_upd = 0
                if incumbent[1] < best_s[1]:
                    best_s = incumbent
                    

            elif random.uniform(0, 1) < math.e ** (-delta_e / t):
                incumbent = [new_s, new_s_cost]
                its_since_upd = 0
            else:
                its_since_upd +=1

        else:
            its_since_upd +=1

        t = a * t
        iteration += 1
        bar.update(iteration)
    
    bar.finish()

    if RUN_MODE:
        print("\n%d: diversification" % diversification_its)
        print("\nTotal iterations:", (iteration), "\n")

    return best_s



def update_weights(current, weights, index, f_curr, f_best):
    if f_curr < current:
        weights[index] += 1
    t = hash(current)
    if t not in FOUND:
        weights[index] += 3
        FOUND.add(t)
    if f_curr < f_best:
        weights[index] += 9
    return weights


def regulate_weights(prev, curr, usage):
    new_curr = prev
    for i in range(len(new_curr)):
        new_curr[i] = prev[i] * 0.8 + 0.2 * (curr[i] / max(usage[i], 1))
    return new_curr

def main():
    problems = ["./pdp/data/Call_7_Vehicle_3.txt"]
    """"
    problems = [
        "./pdp/data/Call_7_Vehicle_3.txt",
        "./pdp/data/Call_18_Vehicle_5.txt",
        "./pdp/data/Call_35_Vehicle_7.txt",
        "./pdp/data/Call_80_Vehicle_20.txt",
        "./pdp/data/Call_130_Vehicle_40.txt",
        "./pdp/data/Call_300_Vehicle_90.txt",
    ]"""

    print("--------------- ALNS ---------------")
    for file in problems:
        print("-------------------------------------------")

        
        print("Problem: ", file)

        prob = load_problem(file)

        s_0 = generate_s_0(prob["n_vehicles"], prob["n_calls"])
        cost_s0 = cost_function(s_0, prob)

        if RUN_MODE:

            start_time = time.time()
            sol = alns(s_0, prob)
            end_time = time.time()
            dur = end_time - start_time

            improvement = 100 * (cost_s0 - sol[1]) / sol[1]
            print("")
            print("Best solution: ", sol[0])
            print("Best objective: ", sol[1])
            print("Improvement : ", improvement, "%")
            print("Running time : ", dur)
            return


        else:
            runs = []

            for iteration in range(1, 11):
                print("Iteration " + str(iteration))
                start_time = time.time()
                sol = alns(s_0, prob)

                end_time = time.time()
                dur = end_time - start_time
                sol.append(dur)
                runs.append(sol)

            runs.sort(key=lambda x: x[1])
            avg_obj = mean([obj[1] for obj in runs])
            best = runs[0]
            improvement = 100 * (cost_s0 - best[1]) / best[1]
            print("")
            print("Avg objective: ", avg_obj)
            print("Best solution: ", best[0])
            print("Best objective: ", best[1])
            print("Improvement : ", improvement, "%")
            print("Running time : ", best[2])
            return
