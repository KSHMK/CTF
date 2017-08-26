import angr
import simuvex

class SubScan(simuvex.SimProcedure):
    def run(self):
        stat = self.state
        stat.memory.store(0x8049A98,stat.se.BVS('ans',20*8))
        return 20
