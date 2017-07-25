import os.path

from pintool import *
from triton  import *

import newt.gstate

def dump_input(outdir,ident, label, xs):
  filename = outdir+"/"+str(hash(ident))+label+".dat"

  if os.path.isfile(filename):
    return

  f = open(filename,"w")
  print "Dumping",filename,"with",repr("".join(xs))
  for x in xs:
     f.write(x)

#def check_input(ident, label, xs):
#  filename = str(hash(ident))+label+".dat"
#  f = open("inputs/"+filename,"w")
#  for x in xs:
#     f.write(x)


def read_string(ptr, max_size=100):

    x = getCurrentMemoryValue(MemoryAccess(ptr, CPUSIZE.BYTE))
    r = ""
    #print x,chr(x),hex(ptr)

    while (x <> 0 and max_size > 0):
         r = r + chr(x)
         ptr = ptr + 1
         x = getCurrentMemoryValue(MemoryAccess(ptr, CPUSIZE.BYTE))
         max_size = max_size - 1
    return r

def read_buffer(ptr, max_size):

    x = getCurrentMemoryValue(MemoryAccess(ptr, CPUSIZE.BYTE))
    r = ""
    #print x,chr(x),hex(ptr)

    while (max_size > 0):
         r = r + chr(x)
         ptr = ptr + 1
         x = getCurrentMemoryValue(MemoryAccess(ptr, CPUSIZE.BYTE))
         max_size = max_size - 1
    return r

def symbolize(ptr, n):
   
    while (n > 0):
         newt.gstate.ctx.taintMemory(MemoryAccess(ptr, CPUSIZE.BYTE))
         concreteValue = getCurrentMemoryValue(ptr)
         #print hex(concreteValue)
         newt.gstate.ctx.setConcreteMemoryValue(ptr, getCurrentMemoryValue(ptr))
         newt.gstate.ctx.convertMemoryToSymbolicVariable(MemoryAccess(ptr, CPUSIZE.BYTE))
         print "symbolized",hex(ptr),"with",hex(concreteValue)
         ptr = ptr + 1
         n = n - 1


