#!/usr/bin/python2

#import ast

from pintool import *
from triton  import *
from ast import *
from copy import copy

from newt.handlers import *

import newt.gstate


def entry_callbacks(threadId, std):
    #print "entry",std, getSyscallNumber(std)
    if getSyscallNumber(std) == SYSCALL.OPEN:
        handle_entry_open(std)
    elif getSyscallNumber(std) == SYSCALL.READ:
        handle_entry_read(std)


def exit_callbacks(threadId, std):
    #print "exit", newt.gstate.current_syscall
    syscall,args = newt.gstate.syscall

    if syscall == SYSCALL.OPEN:
        handle_exit_open(args)
    elif syscall == SYSCALL.READ:
        handle_exit_read(args)

    newt.gstate.syscall = (None, None)

def fini_callbacks():
    #global fds
    #print newt.gstate.fds
    #global current_input  

    current_input = newt.gstate.input_data
    outdir = newt.gstate.outdir

    pcs = getPathConstraints()
    previousConstraints = equal(bvtrue(), bvtrue())
    taken = []
    #pcs = getPathConstraintsAst()
    for pc in pcs:
      taken.append(pc.getTakenAddress())
      if pc.isMultipleBranches():

        # Get all branches
        branches = pc.getBranchConstraints()        
        print "Solving path conditions.."

        for branch in branches:
          if branch['taken'] == False:
            f = assert_(land(previousConstraints, branch['constraint']))
            models = getModel(f)
            new_input = copy(current_input)
            for k, v in models.items():
              #print k,type(k)
              new_input[k] = chr(v.getValue())
            if new_input <> current_input:
              #print new_input
              dump_input(outdir,str(f),"",new_input)
            else:              
              print ".",
        previousConstraints = land(previousConstraints, pc.getTakenPathConstraintAst())

    clearPathConstraints()
