import amoco
#-------------------------------------------------------------------------------------------------
def generate_executable(newline):
    import subprocess
    
    f = open("target.asm","w")
    f.write("segment .text\n")
    f.write("    global _start\n")
    f.write("_start:\n")
    f.write(newline+"\n")
    f.write("    ret\n")
    f.close()
    
    try:
        out = subprocess.check_output(["nasm","-f","elf","target.asm"])
    except:
        print "ERROR while assembling", newline
        return False
        
    try:
        out = subprocess.check_output(["ld","-m","elf_i386","-s","-o","target","target.o"])
    except:
        print "ERROR while linking"
        return False
    
    return True
#-------------------------------------------------------------------------------------------------
def run_amoco(executable):
    p = amoco.system.loader.load_program(executable)
    
    print p.mmap

    # linear sweep disassembly
    z = amoco.lsweep(p)
    # block iterator
    ib = z.iterblocks()
    b = next(ib)

    print b         # instruction
    print '--------- symbolic execution -----------'
    print b.map     # symbolic execution

    print '------ eflags -------'
    print "CF [0:1]   ->", b.map[p.cpu.eflags][0:1]
    print "PF [2:3]   ->", b.map[p.cpu.eflags][2:3]
    print "AF [4:5]   ->", b.map[p.cpu.eflags][4:5]
    print "ZF [6:7]   ->", b.map[p.cpu.eflags][6:7]
    print "SF [7:8]   ->", b.map[p.cpu.eflags][7:8]
    print "OF [11:12] ->", b.map[p.cpu.eflags][11:12]

    #print b.map[p.cpu.eflags][0:1].to_smtlib().sexpr()

if __name__ == "__main__":
    if generate_executable("xor eax, ebx"):
        run_amoco("target")
        
        
