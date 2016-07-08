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
    elif getSyscallNumber(std) == SYSCALL.MMAP:
        handle_entry_mmap(std)
    elif getSyscallNumber(std) == SYSCALL.READ:
        handle_entry_read(std)


def exit_callbacks(threadId, std):
    #print "exit", newt.gstate.current_syscall
    syscall,args = newt.gstate.syscall

    if syscall == SYSCALL.OPEN:
        handle_exit_open(args)
    elif syscall == SYSCALL.MMAP:
        handle_exit_mmap(args)
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
    print pcs
    previousConstraints = equal(bvtrue(), bvtrue())
    taken = []
    #pcs = getPathConstraintsAst()
    for pc in pcs:
      if pc.isMultipleBranches():

        # Get all branches
        branches = pc.getBranchConstraints()        
        print "Solving path conditions..",
        #print branches

        for branch in branches:
          if branch['taken'] == False:
            #taken.append(branch['target'])
            #print hex(branch['target'])
            #print branch['constraint']
            #print previousConstraints
            pid = taken+[branch['target']]
            f = assert_(land(previousConstraints, branch['constraint']))
            models = getModel(f)
            new_input = copy(current_input)
            #print models
            for k, v in models.items():
              #print k,type(k)
              new_input[k] = chr(v.getValue())
            if new_input <> current_input:
              print ""
              dump_input(outdir,str(f),"",new_input)
            else:              
              print ".",

      previousConstraints = land(previousConstraints, pc.getTakenPathConstraintAst())
      taken.append(pc.getTakenAddress())

    clearPathConstraints()
