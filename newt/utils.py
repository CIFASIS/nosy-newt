import os.path

from pintool import *
from triton  import *

def dump_input(outdir,ident, label, xs):
  filename = outdir+"/i"+str(hash(ident))

  if os.path.isfile(filename):
    return

  f = open(filename,"w")
  print "Dumping",filename,"with",repr("".join(xs))
  for x in xs:
     f.write(x)

def exists_input(outdir,ident):
  filename = outdir+"/i"+str(hash(ident))
  return os.path.isfile(filename)


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
         taintMemory(MemoryAccess(ptr, CPUSIZE.BYTE))
         concreteValue = getCurrentMemoryValue(MemoryAccess(ptr, CPUSIZE.BYTE))
         #print hex(concreteValue)
         convertMemoryToSymbolicVariable(MemoryAccess(ptr, CPUSIZE.BYTE, concreteValue))
         print "symbolized",hex(ptr),"with",hex(concreteValue)
         ptr = ptr + 1
         n = n - 1


