from pyopenreil.REIL import *
from pyopenreil.utils import asm

# create assembly instruction reader
reader = asm.Reader(ARCH_X86, ( 'push ebp',
                                'mov ebp, esp',
                                'xor eax, eax',
                                'test ecx, ecx', 
                                'jz _quit',
                                'inc eax',
                                '_quit: leave',
                                'ret'), addr = 0)

# create translator instance
tr = CodeStorageTranslator(reader)

# print first instruction


if True:
    i = tr.get_insn(0)

    for il in i:
        print il.to_str()



# translate first basic block
# bb = tr.get_bb(0)

# Get symbolic representation of basic block.
# False value of temp_regs argument indicates that
# we don't need expressions for REIL temp registers.
# sym = bb.to_symbolic(temp_regs = False)

# print SymState object
# print sym
