from __future__ import print_function

import sys
import json
import os
import argparse



def search(terms):
    """
    search
    """
    path_to_general_file = os.path.join(os.path.dirname(__file__), 'texts', 'general' + '.json')
    with open(path_to_general_file, 'r') as f:
        data = json.load(f)
        output = []
        for content in data:
            text_list = content.values()
            if is_match(terms, text_list):
                output.append(content)

    console(output)


def add(cmd, detail):
    """
    adds a command to a file
    """
    path_to_general_file = os.path.join(os.path.dirname(__file__), 'texts', 'general' + '.json')
    content = {
        "cmd": cmd,
        "detail": detail
    }

    with open(path_to_general_file, 'a+') as f:
        data = json.load(f)
        data.append(content)
        json.dump(data, f)
        console('command added')

def show():
    path_to_general_file = os.path.join(os.path.dirname(__file__), 'texts', 'general' + '.json')
    with open(path_to_general_file, 'r') as f:
        data = json.load(f)
        console(data)

# parser.add_argument('--verbose', action='store_true', help='more verbosity')
# parser.add_argument('--verbose', type=int, choices=[0,1,2], help='more verbosity')
#
# if args.verbose == 2:
#     print ('square of {0} equals {1}'.format(args.square, answer))
# elif args.verbose == 1:
#     print ('{0}^2 {1}'.format(args.square, answer))
# else:
#     print (answer)
#

parser = argparse.ArgumentParser()

parser.add_argument('state', choices=['search', 'add', 'show'],  help='supply a given state')
parser.add_argument('--query', help='supply a query')
parser.add_argument('--cmd',   help='your command')
parser.add_argument('--detail', help='command detail')

args = parser.parse_args()

if args.state == 'search':
    if not args.query:
        raise Exception('Must supply query')
    terms = args.query.split('+')
    search(terms)
elif args.state == 'add':
    if not args.cmd or not args.detail:
        raise Exception('Supply cmd and detail')
    add(args.cmd, args.detail)
elif args.state == 'show':
    show()
else:
    console('invalid state')

