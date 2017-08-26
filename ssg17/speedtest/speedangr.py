import angr
import simuvex

def solve():
    p = angr.Project("speedtest",load_options={'auto_load_libs':False})
    cfg = p.analyses.CFG()
    print "It has %d nodes and %d edges" % (len(cfg.graph.nodes()), len(cfg.graph.edges()))
    raw_input("GO")
    find = 0x804BC10
    avoid = 0x804BD1A

    argv1 = angr.claripy.BVS("argv1",30*8)

    state = p.factory.entry_state(args=["./speed_test",argv1])

    for i,k in enumerate("PASS_SSGCTF{"):
        state.add_constraints(argv1[i] == ord(k))

    pg = p.factory.path_group(state)

    ex = pg.explore(find=find,avoid=avoid)

    print ex

    print pg.found[0].state.se.any_str(argv1)
if __name__ == "__main__":
    solve()
