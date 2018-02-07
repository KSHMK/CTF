import angr
import simuvex
class SubPtrArgfgets(simuvex.SimProcedure):
    def run(self, arg1,arg2,arg3):
        print arg1
        PT = self.state.se.BVS('c',8*28)
        for byte in PT.chop(8):
            self.state.add_constraints(byte != '\x00')
            self.state.add_constraints(byte >= ' ')
            self.state.add_constraints(byte <= '~')
        self.state.add_constraints(PT.chop(8)[22] != 'b')
        self.state.add_constraints(PT.chop(8)[22] != 'c')
        self.state.memory.store(arg1,PT)
        self.state.regs.rax = 28
        return 0
class SubPtrArgRet0(simuvex.SimProcedure):
    def run(self, arg1,arg2,arg3):
        self.state.regs.rax = 0
        return 0
p = angr.Project("./RedVelvet",load_options={'auto_load_libs':False})

find = (0x401537,)
avoid = (0x4007D0,)
p.hook_symbol("fgets",SubPtrArgfgets)
p.hook_symbol("ptrace",SubPtrArgRet0)
init = p.factory.blank_state()
#init.options.remove(simuvex.o.LAZY_SOLVES)
pgp = p.factory.path_group(init)
print "START"
    
ex = pgp.explore(find=find,avoid=avoid)
    
print ex
s = pgp.found[0].state
print s.se.any_str(s.memory.load(0x7fffffffffefec8,28))
