#!/usr/bin/env python3

import argparse
import sys
import time

parser = argparse.ArgumentParser()
parser.description = "Async process test emulator"
parser.add_argument('-s', '--stdout', action='store_true', help="Write to stdout")
parser.add_argument('-e', '--stderr', action='store_true', help="Write to stderr")
parser.add_argument('-i', '--iterations', default=3, nargs=1, type=int, help='Number of iterations (seconds)')

args = parser.parse_args()

for i in range(0, args.iterations[0]):
    time.sleep(0.3)
    if args.stdout:
        print('[%3d] stdout' % i, file=sys.stdout)
    time.sleep(0.3)
    if args.stderr:
        print('[%3d] stderr' % i, file=sys.stderr)
    time.sleep(0.4)
