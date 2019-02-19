import sys


NO_COLOR = False 

WATER = lambda msg: ('\033[34m%s\033[0m' % msg
        if sys.stdout.isatty() and not NO_COLOR else msg)
SUNK = lambda msg: ('\033[91m%s\033[0m' % msg
        if sys.stdout.isatty() and not NO_COLOR else msg)
HIT = lambda msg: ('\033[31m%s\033[0m' % msg
        if sys.stdout.isatty() and not NO_COLOR else msg)
