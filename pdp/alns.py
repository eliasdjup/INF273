import random
from statistics import mean
import time
from pdp.operators.one_insert import one_insert
from pdp.operators.one_to_dummy import one_to_dummy
from pdp.operators.two_exchange import two_exchange
from pdp.operators.three_exchange import three_exchange
import progressbar
import math
from pdp.operators.dummy_to_best import dummy_to_best
from pdp.operators.route_shuffle import route_shuffle
from pdp.operators.two_exchange_capacity import two_exhange_capacity

from pdp.utils import cost_function, feasibility_check, generate_s_0, load_problem


RUN_MODE = False

if RUN_MODE:
    MAX_ITER = 20000
else:
    MAX_ITER = 10000

TIME_THRESHOLD = 0.5


FOUND = set()


def alns(s_0, instance, time_limit):
    best_s = [s_0, cost_function(s_0, instance)]
    incumbent = [s_0, cost_function(s_0, instance)]

    operators = [
        two_exhange_capacity,
        dummy_to_best,
        route_shuffle,
        one_insert,
        two_exchange,
        three_exchange,
    ]

    curr_weights = [1.0 for _ in operators]
    usage = [0 for _ in operators]

    prev_weights = curr_weights.copy()
    end = time.time() + (time_limit - TIME_THRESHOLD)

    t0 = 48
    t = t0
    a = 0.998

    if instance["n_vehicles"] < 30:
        escape_condition = 300
        refresh_rate = 75
        diversification_rate = 150

    else:
        escape_condition = 600
        refresh_rate = 150
        diversification_rate = 200

    last_update = 0
    iteration = 0

    bar = progressbar.ProgressBar(
        maxval=MAX_ITER,
        widgets=[progressbar.Bar("=", "[", "]"), " ", progressbar.Percentage()],
    )
    bar.start()

    while iteration < MAX_ITER and (not RUN_MODE or time.time() < end):
        if last_update == escape_condition:
            incumbent = [s_0, cost_function(s_0, instance)]
            t = t0
            last_update = 0
            curr_weights.clear()
            usage.clear()
            FOUND.clear()
            curr_weights = [1.0 for _ in operators]
            usage = [0 for _ in operators]
            prev_weights = curr_weights.copy()

        if last_update > diversification_rate:
            diversify_incumbent = one_to_dummy(incumbent, instance)
            incumbent = [diversify_incumbent, cost_function(diversify_incumbent, instance)]

        if iteration % refresh_rate == 0 and iteration >= 49:
            prev_weights = curr_weights
            curr_weights = refresh_weights(prev_weights, curr_weights, usage)
            for i in range(len(operators)):
                usage[i] = 0

        chosen_operator = random.choices(operators, prev_weights, k=1)[0]
        chosen_operator_index = operators.index(chosen_operator)

        new_s = chosen_operator(incumbent, instance)
        new_s_feasiblity, c = feasibility_check(new_s, instance)
        curr_weights = update_weights(
            new_s[0], curr_weights, chosen_operator_index, new_s[1], best_s[1]
        )
        usage[chosen_operator_index] += 1

        if new_s_feasiblity:
            new_s_cost = cost_function(new_s, instance)
            delta_e = new_s_cost - incumbent[1]

            if delta_e < 0:
                incumbent = [new_s, new_s_cost]
                last_update = 0
                if incumbent[1] < best_s[1]:
                    best_s = incumbent

            elif random.uniform(0, 1) < math.e ** (-delta_e / t):
                incumbent = [new_s, new_s_cost]
                last_update = 0
            else:
                last_update += 1

        else:
            last_update += 1

        t = a * t
        iteration += 1

        bar.update(iteration)

    bar.finish()

    return best_s, iteration


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


def refresh_weights(prev, curr, usage):
    new_curr = prev
    for i in range(len(new_curr)):
        new_curr[i] = prev[i] * 0.8 + 0.2 * (curr[i] / max(usage[i], 1))
    return new_curr


def main():

    results = []

    # problems = ["./pdp/data/Call_7_Vehicle_3.txt"]

    problems = [
        "./pdp/data/Call_7_Vehicle_3.txt",
        "./pdp/data/Call_18_Vehicle_5.txt",
        "./pdp/data/Call_35_Vehicle_7.txt",
        "./pdp/data/Call_80_Vehicle_20.txt",
        "./pdp/data/Call_130_Vehicle_40.txt",
    ]

    time_limits = [15, 25, 30, 160, 670]

    total_dur = []

    print("--------------- ALNS ---------------")
    for ix, file in enumerate(problems, start=0):
        print("-------------------------------------------")

        print(f"Problem: {file}")

        prob = load_problem(file)

        s_0 = generate_s_0(prob["n_vehicles"], prob["n_calls"])
        cost_s0 = cost_function(s_0, prob)

        if RUN_MODE:
            print(f"Time budget: {time_limits[ix]:.1f} seconds")

            start_time = time.time()
            sol, iteration = alns(s_0, prob, time_limits[ix])
            end_time = time.time()
            dur = end_time - start_time

            improvement = 100 * (cost_s0 - sol[1]) / sol[1]
            print("")
            print(f"Best solution: {sol[0]}")
            print(f"Best objective: {sol[1]}")
            print(f"Improvement : {improvement:.1f}%")
            print(f"Running time : {dur:.1f}")
            print(f"Completed iterations: {iteration}")
            print("")

            # Adjust time budget for next problem
            if time_limits[ix] - dur > 0.5 and ix <= len(problems) - 2:
                time_limits[ix + 1] = time_limits[ix + 1] + (time_limits[ix] - dur)

            total_dur.append(dur)
            results.append(sol[0])

        else:
            runs = []

            for iteration in range(1, 11):
                print("Iteration " + str(iteration))
                start_time = time.time()
                sol, iteration = alns(s_0, prob, 0)

                end_time = time.time()
                dur = end_time - start_time
                sol.append(dur)
                runs.append(sol)

            runs.sort(key=lambda x: x[1])
            avg_obj = mean([obj[1] for obj in runs])
            best = runs[0]
            improvement = 100 * (cost_s0 - best[1]) / best[1]
            print("")
            print(f"Best solution: {best[0]}")
            print(f"Best objective: {best[1]}")
            print(f"Avg objective: {avg_obj}")
            print(f"Improvement : {improvement:.1f}%")
            print(f"Running time : {best[2]:.1f}")
            print("")

    if RUN_MODE:
        print(f"Total running time: {sum(total_dur):.1f} seconds \n")

        print("Writing solutions to .txt file...")
        with open("results.txt", "w") as f:
            for sol in results:
                f.write(str(sol) + "\n")

        print("Done!")
