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

    # Start JIT at the entry point
    startAnalysisFromEntry()
    enableMode(MODE.ONLY_ON_SYMBOLIZED, True)

    # Add callback
    insertCall(entry_callbacks, INSERT_POINT.SYSCALL_ENTRY)
    insertCall(exit_callbacks, INSERT_POINT.SYSCALL_EXIT)
    insertCall(fini_callbacks, INSERT_POINT.FINI)

    # Run Program
    runProgram()

