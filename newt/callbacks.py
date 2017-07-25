#!/usr/bin/python2

from pintool import *
from triton  import SYSCALL64 as SYSCALL
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
    ctx = newt.gstate.ctx
    astctx = newt.gstate.ctx.getAstContext()

    pcs = ctx.getPathConstraints()
    print pcs
    previousConstraints = astctx.equal(astctx.bvtrue(),astctx.bvtrue())
    taken = []
    for pc in pcs:
      if pc.isMultipleBranches():

        # Get all branches
        branches = pc.getBranchConstraints()
        print "Solving path conditions..",

        for branch in branches:
          if branch['isTaken'] == False:

            pid = tuple(taken + [str(branch['constraint'])])
            print "pid:",hash(pid)
            if exists_input(outdir, pid):
                continue

            f = astctx.land([previousConstraints, branch['constraint']])
            models = ctx.getModel(f)
            new_input = copy(current_input)
            #print models
            for k, v in models.items():
              #print k,type(k)
              new_input[k] = chr(v.getValue())
            if new_input <> current_input:
              print "SAT!"
              dump_input(outdir,pid,"",new_input)
            else:              
              print ".",

      previousConstraints = astctx.land([previousConstraints, pc.getTakenPathConstraintAst()])
      taken.append(pc.getTakenAddress())
      #previousConstraints = ast.land(previousConstraints, pc.getTakenPathConstraintAst())

    ctx.clearPathConstraints()
