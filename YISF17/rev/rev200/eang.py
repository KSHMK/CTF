import angr
import simuvex
import logging
from pwn import *
def Subwrite(state):
    state.memory.store(0x6045D5,"\x7f")
    
l = logging.getLogger("angr")
l.setLevel(logging.DEBUG)
p = angr.Project("tmp2")
p.hook(0x404129,Subwrite,length = 5)
init = p.factory.blank_state()
pgp = p.factory.path_group(init)
print "START"
ex = pgp.explore(find=0x404161,avoid =0x404185)
print ex
import IPython
IPython.embed()

s = ex.found[0].state
print s.posix.dumps(0)
