#!/usr/bin/python2

import argparse
import shutil

from os import listdir, system
from os.path import isfile, join

from newt.config import *

import newt.gstate

explored_inputs = set()
explored_files = set()

input_dir = newt.gstate.outdir

def refresh_inputs(d):
  return [join(d,f) for f in listdir(d) if isfile(join(d, f))]

if __name__ == "__main__":

     # Arguments
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("-i", help="", type=str, default="inputs", required=True, dest="input_dir")
    parser.add_argument("-n", help="", type=int, default=5, required=True, dest="n")
    #parser.add_argument("-m", help="", type=str, nargs='+', dest="mods")
    parser.add_argument("cmd", help="", type=str, default=None)
    options = parser.parse_args()
    input_filename = "test.tar"
   
    cmd = options.cmd
    input_dir = options.input_dir
    n = options.n

    prepared_cmd = cmd.split("@@")
    prepared_cmd = prepared_cmd[0].split(" ") + [input_filename] + prepared_cmd[1].split(" ")
    prepared_cmd = filter(lambda x: x<>'', prepared_cmd)
    print "Using",prepared_cmd, "as arguments"

    for it in range(n):
        inputs = refresh_inputs(input_dir)
        for filename in inputs:
            content = hash(open(filename).read())

            if not (filename in explored_inputs) and not (content in explored_files):
                shutil.copy(filename, input_filename) 
                print "Exploring",filename, "executing", prepared_cmd[0]               
                system("triton nn.py "+" ".join(prepared_cmd)) 
                explored_inputs.add(filename)
                explored_files.add(content)
