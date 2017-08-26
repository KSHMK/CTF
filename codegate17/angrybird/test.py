import angr
import simuvex

# Fgets hooking
class SubFgets(simuvex.SimProcedure):
    def run(self,buf,n,fd):
        stat = self.state
        stat.memory.store(buf,stat.se.BVS('ans',0x21*8))
        return 0x21

def main():
    p = angr.Project("angrybird",load_options={'auto_load_libs': False})

    find = 0x404FAB
    avoid = 0x4005E0

    p.hook_symbol("fgets",SubFgets)

    init = p.factory.blank_state(addr=0x400761)
    init.options.remove(simuvex.o.LAZY_SOLVES)
    
    init.memory.store(0x606038,"hello")
    pg = p.factory.path_group(init)
    print "START"
    ex = pg.explore(find=find,avoid=avoid)
    print ex

    s = pg.found[0].state
    print s.se.any_str(s.memory.load(0x7fffffffffeffa8,0x21))

if __name__ == "__main__":
    main()
