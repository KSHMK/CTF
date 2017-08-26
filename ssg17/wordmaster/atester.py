from pwn import *
import angr
import simuvex

def Solver():
    p = angr.Project("TESTA",load_options={'auto_load_libs': False})
