from algorithm import algorithm
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from mode import Mode

if __name__ == '__main__':
    ap = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    ap._action_groups.pop()
    required = ap.add_argument_group("required arguments")
    required.add_argument("-r",  "--reduce-fields", required=True,  help="number of reduced fields on board", type=int)
    required.add_argument("-t",  "--temperature", required=True,  help="starting temperature", type=float)
    required.add_argument("-f",  "--frequency",   required=True,  help="frequency of temperature changes", type=int)
    required.add_argument("-cf",  "--cooling-factor",  required=True,  help="cooling factor", type=float)
    optional = ap.add_argument_group("optional arguments")
    optional.add_argument("-fc", "--from-cache",   required=False, action="store_true", help="run file from cache")
    optional.add_argument("-b",  "--board",       required=False, help="board number", type=int, default=0)
    optional.add_argument("-m",  "--mode",        required=False, help="random or not random", type=Mode.argparse, default=Mode.NOT_RANDOM, choices=list(Mode))
    optional.add_argument("--disable-cache",  required=False, action="store_true", help="disable storing in cache")

    args = vars(ap.parse_args())
    print(args)
    algorithm(args)
