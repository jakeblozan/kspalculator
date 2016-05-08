#!/usr/bin/env python3

from argparse import ArgumentParser

epilog = """
deltav:pressure tuples:
You specify which delta-v (in m/s) at which pressure (0.0 = vacuum, 1.0 = ATM)
your ship must be able to reach. You might specify more than one of these
tuples. This might be useful if you're going to fly through different
environments, e.g. starting in atmosphere and later flying through vacuum.
"""

parser = ArgumentParser(description='Determine best rocket design', epilog=epilog)
parser.add_argument('payload', type=float, help='Payload in kg')
parser.add_argument('acceleration', type=float, help='Required minimum acceleration in m/s^2')
parser.add_argument('dvtuples', metavar='deltav:pressure', nargs='+', help='deltav:pressure tuples')
# TODO: implement type check for dvtuples
parser.add_argument('-c', '--cheapest', action='store_true', help='Sort by cost instead of weight')
parser.add_argument('-S', '--preferred-size', choices=['tiny', 'small', 'large', 'extralarge'], help='Preferred width of the stage')
parser.add_argument('-b', '--best-gimbal', action='store_true', help='Not only compare whether engine has gimbal or not, but also the maximum trust vectoring angle')
parser.add_argument('--keep', action='store_true', help='Do not hide bad solutions')

args = parser.parse_args()

# we have the import here (instead of above) to have short execution time in
# case of calling with e.g. '-h' only.
from design import FindDesigns
from parts import RadialSize

ps = None
if args.preferred_size is not None:
    if args.preferred_size == "tiny":
        ps = RadialSize.Tiny
    elif args.preferred_size == "small":
        ps = RadialSize.Small
    elif args.preferred_size == "large":
        ps = RadialSize.Large
    else:
        ps = RadialSize.ExtraLarge

dv = [float(s.partition(':')[0]) for s in args.dvtuples]
pr = [float(s.partition(':')[2]) for s in args.dvtuples]

all_designs = FindDesigns(args.payload, pr, dv, args.acceleration, ps, args.best_gimbal)

if args.keep:
    D = all_designs
else:
    D = [d for d in all_designs if d.IsBest]

if args.cheapest:
    D = sorted(D, key=lambda dsg: dsg.cost)
else:
    D = sorted(D, key=lambda dsg: dsg.mass)

for d in D:
    d.printinfo()
    print("")
