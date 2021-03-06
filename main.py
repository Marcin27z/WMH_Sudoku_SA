from algorithm import algorithm
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from mode import Mode
from pathlib import Path
import csv

if __name__ == '__main__':

    ap = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    ap._action_groups.pop()
    required = ap.add_argument_group("required arguments")
    required.add_argument("-r",  "--reduce_fields", required=True,  help="number of reduced fields on board", type=int)
    required.add_argument("-t",  "--temperature", required=True,  help="starting temperature", type=float)
    required.add_argument("-f",  "--frequency",   required=True,  help="frequency of temperature changes", type=int)
    required.add_argument("-cf",  "--cooling_factor",  required=True,  help="cooling factor", type=float)
    optional = ap.add_argument_group("optional arguments")
    optional.add_argument("-fc", "--from_cache",   required=False, action="store_true", help="run file from cache", default=True)
    optional.add_argument("-b",  "--board",       required=False, help="board number", type=int, default=0)
    optional.add_argument("-m",  "--mode",        required=False, help="random or not random", type=Mode.argparse, default=Mode.NOT_RANDOM, choices=list(Mode))
    optional.add_argument("--disable_cache",  required=False, action="store_true", help="disable storing in cache")
    optional.add_argument("--repeat", required=False, help="how many times run algorithm for one set of parameters", type=int, default=0 )
    args = vars(ap.parse_args())

    result = 0
    i = 0
    while i < int(args["repeat"]):
        i+=1
        print(i)
#        result, is_correct = algorithm(args)
        result, cost = algorithm(args)

        print("Srednia liczba iteracji: " + str(result))
        file_name = "test2_mode_random_r"+str(args["reduce_fields"])+".csv"
        my_file = Path(file_name)

        if my_file.is_file():
            with open(file_name, 'a', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow([str(args["reduce_fields"]), str(args["temperature"]), str(args["frequency"]), str(args["cooling_factor"]), str(args["board"]), str(args["repeat"]), str(i), str(100), str(result), str(cost)])
        else:
            with open(file_name, 'w', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                #writer.writerow(["reduce_fields", "temperature", "frequency", "cooling_factor", "board", "repeat", "iter", "acceptance_ratio_iter","no_of_iterations", "is_correct"])
                writer.writerow(
                    ["reduce_fields", "temperature", "frequency", "cooling_factor", "board", "repeat", "iter",
                     "acceptance_ratio_iter", "no_of_iterations", "cost"])
                writer.writerow([str(args["reduce_fields"]), str(args["temperature"]), str(args["frequency"]), str(args["cooling_factor"]), str(args["board"]), str(args["repeat"]), str(i), str(100), str(result), str(cost)])
