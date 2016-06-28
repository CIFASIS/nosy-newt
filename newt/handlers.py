from pintool import *
from triton  import *

from newt.utils import *

import newt.gstate

def handle_entry_read(std):
    #global current_syscall
    #print "read!!!"
    fd = getSyscallArgument(std, 0)      
    ptr = getSyscallArgument(std, 1)      

    newt.gstate.syscall = (SYSCALL.READ, [fd,ptr])
    
    #print "read",fd,hex(ptr)

def handle_exit_read(args):

    fd,ptr = args
    #print newt.gstate.fds

    if newt.gstate.fds[fd] in newt.gstate.filename:
        print "Hooking read of",newt.gstate.fds[fd]
        n = getCurrentRegisterValue(REG.RAX)
        symbolize(ptr, n)
        newt.gstate.input_data = newt.gstate.input_data + (list(read_buffer(ptr,n)))
    #print "read", buf



def handle_entry_open(std):
    #global current_syscall

    arg0 = getSyscallArgument(std, 0)      
    filename = read_string(arg0)
    newt.gstate.syscall = (SYSCALL.OPEN,[filename])
    #print "open", filename

def handle_exit_open(args):

    #global fds
    #global current_syscall

    filename = args[0]
    ret = getCurrentRegisterValue(REG.RAX)
    newt.gstate.fds[ret] = filename

    #print "fid", ret

