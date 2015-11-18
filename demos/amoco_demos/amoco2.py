import amoco

def generate(instrs):
    import subprocess

    f = open("target.asm","w")
    f.write("segment .text\n")
    f.write("    global _start\n")
    f.write("_start:\n")
    for line in instrs:
        f.write(line+"\n")
    f.write("ret\n")
    f.close()

    subprocess.check_output(["nasm","-f","elf","target.asm"])
    subprocess.check_output(["ld","-m","elf_i386","-s","-o","target","target.o"])

generate(["mov eax, 0x0","inc eax","inc eax","inc eax"])
p = amoco.system.loader.load_program("target")
z = amoco.lsweep(p)
ib = z.iterblocks()

b = next(ib)

print b
print b.map


