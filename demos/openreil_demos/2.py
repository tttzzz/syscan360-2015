from pyopenreil.REIL import *
from pyopenreil.utils import asm
# initialise raw instruction reader

reader = ReaderRaw(ARCH_X86, '\x33\xC0\xC3', addr = 0)

# Create translator instance.
# We are not passing storage instance, translator will create
# instance of CodeStorageMem automatically in this case.
tr = CodeStorageTranslator(reader)

# translate single basic block
bb = tr.get_bb(0)

# print basic block information
print 'addr = %s, size = %d bytes' % (bb.ir_addr, bb.size)

# print address of the first and last instruction
print 'first = 0x%x, last = 0x%x' % (bb.first.addr, bb.last.addr)

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

# translate first basic block
bb = tr.get_bb(0)

# Get symbolic representation of basic block.
# False value of temp_regs argument indicates that
# we don't need expressions for REIL temp registers.
sym = bb.to_symbolic(temp_regs = False)

# print SymState object
print sym
