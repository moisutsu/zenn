from classopt import classopt

@classopt
class Args:
    long_name_variable: int

args: Args = Args.from_args()

args.long_name_variable
