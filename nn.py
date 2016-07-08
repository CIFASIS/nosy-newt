#!/usr/bin/env python2
## -*- coding: utf-8 -*-

import sys

from pintool import *
from triton  import *

from newt.config import *
from newt.callbacks import *

if __name__ == '__main__':
    # Set arch
    setArchitecture(ARCH.X86_64)
    #enableSymbolicEmulation(False)
    #assert(isSymbolicEmulationEnabled())

    # Start JIT at the entry point
    startAnalysisFromEntry()
  
    enableSymbolicOptimization(OPTIMIZATION.ONLY_ON_TAINTED, True)

    # Add callback
    addCallback(entry_callbacks, CALLBACK.SYSCALL_ENTRY)
    addCallback(exit_callbacks, CALLBACK.SYSCALL_EXIT)
    addCallback(fini_callbacks, CALLBACK.FINI)

    # Run Program
    runProgram()

