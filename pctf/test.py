import angr
import simuvex
class SubPtrArgRead(simuvex.SimProcedure):
    def run(self, arg1,arg2,arg3):
        print arg2
        self.state.memory.store(arg2,self.state.se.BVS('S',0x20*8))
        self.state.regs.rax = 32
        return 32
class SubPtrArgRet1(simuvex.SimProcedure):
    def run(self, arg1):
        self.state.regs.rax = 1
        return 1
                    
def main():
    p = angr.Project("./no_flo",load_options={'auto_load_libs':False})
    find = 0x4027EC
    avoid = 0x4027F8
    p.hook_symbol("read",SubPtrArgRead)
    p.hook(0x4027D8,SubPtrArgRet1,length=5)
    init = p.factory.blank_state()
    init.options.remove(simuvex.o.LAZY_SOLVES)

    pgp = p.factory.path_group(init)
    print "START"
    ex = pgp.explore(find=find,avoid=avoid)
    
    print ex

    s = pgp.found[0].state
    print s.se.any_str(argv0)
if __name__ in '__main__':
    main()
