#!/bin/python3

import os
import sys
import argparse
import copy
import csv.main

class Pyhelptex:
    def __init__(self):
        self.functions = {}
        self.str_list_of_fns = "Supported cmds: "
        self.empty = True
        self.__register("csv", csv.main.script_wrapper)

    def __register(self, fn_name, real_fn):
        if self.empty:
            self.str_list_of_fns = self.str_list_of_fns + str(fn_name)
        else:
            self.str_list_of_fns = self.str_list_of_fns + ", " + str(fn_name)
        self.functions[fn_name] = real_fn
        self.empty = False

    def script_call(self, fn_name, arguments, **kwargs):
        self.fns.functions[fn_name](arguments)

    def call(self, fn_name, *args):
        self.fns.functions[fn_name](args)

if __name__ == "__main__":
    pyhelptex = Pyhelptex()

    parser = argparse.ArgumentParser()
    parser.add_argument
    parser.add_argument("command", help=fns.str_list_of_fns)
    #example below of voluntary argument
    #parser.add_argument("--foo", '-f', action="store_true", help="foobar")
    parser.add_argument("Other args: used for the called function", nargs=argparse.REMAINDER, help=argparse.SUPPRESS)
    args = parser.parse_args()

    # delete first argument passed to subfunctions
    arguments = sys.argv
    if len(sys.argv) >= 1:
        arguments.pop(0)

    if args.command in pyhelptex.functions:
        pyhelptex.script_call(args.command, arguments)
    else:
        print("Unknown command!")
