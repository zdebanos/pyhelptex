#!/bin/python3

import os
import sys
import argparse
import copy
import csv.main

class Pyhelptex:
    def __init__(self):
        self.script_fn = {}
        self.str_list_of_fns = "Supported cmds: "
        self.empty = True
        self.csv = self.__register("csv", csv.main.CsvFunction("csv"))

    def __register(self, fn_name, fn_obj):
        if self.empty:
            self.str_list_of_fns = self.str_list_of_fns + str(fn_name)
        else:
            self.str_list_of_fns = self.str_list_of_fns + ", " + str(fn_name)

        self.script_fn[fn_name] = fn_obj.call_script
        self.empty = False
        return fn_obj

    def get_str_list_of_fns(self):
        return self.str_list_of_fns

    def script_call(self, fn_name, arguments):
        self.script_fn[fn_name](arguments)


if __name__ == "__main__":
    pyhelptex = Pyhelptex()

    parser = argparse.ArgumentParser()
    parser.add_argument
    parser.add_argument("command", help=pyhelptex.get_str_list_of_fns())
    #example below of voluntary argument
    #parser.add_argument("--foo", '-f', action="store_true", help="foobar")
    parser.add_argument("Other args: used for the called function", nargs=argparse.REMAINDER, help=argparse.SUPPRESS)
    args = parser.parse_args()

    # delete first argument passed to subfunctions
    arguments = sys.argv
    if len(sys.argv) >= 1:
        arguments.pop(0)

    if args.command in pyhelptex.script_fn:
        pyhelptex.script_call(args.command, arguments)
    else:
        print("Unknown command!")
