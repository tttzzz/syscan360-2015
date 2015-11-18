import subprocess
import pprint 

#-------------- FORMAT --------------------------------
#DRCOV VERSION: 2
#DRCOV FLAVOR: drcov-32
#Module Table: 7
# 0, 12288, /home/opcode/src/bruteforce/crasher
# 1, 20480, /lib/i386-linux-gnu/libdl-2.19.so
# 2, 1761280, /lib/i386-linux-gnu/libc-2.19.so
# 3, 32768, /home/opcode/src/dynamorio/tools/lib32/release/libdrcov.so
# 4, 69632, /home/opcode/src/dynamorio/lib32/release/libdrpreload.so
# 5, 1638400, /home/opcode/src/dynamorio/lib32/release/libdynamorio.so.5.0
# 6, 139264, /lib/i386-linux-gnu/ld-2.19.so
#BB Table: 893 bbs
#module id, start, size:
#module[  4]: 0x00000488,  14
#module[  6]: 0x0000ed37,  10
#module[  6]: 0x0000ed80,   8
#module[  6]: 0x0000ee64,   2
#module[  6]: 0x0000ee30,  10
#module[  6]: 0x0000ee3a,  18
#module[  6]: 0x0000ee4c,  24
#module[  6]: 0x0000ecd0,  26



def test3(tracename):

    f = open(tracename,"r")
    m = {}

    nr_modules = None
    module_info = False
    mod_ct = 0
    
    allowed_module_indexes = set()
    basicblocks = set()

    for line in f:
        
        text = line.strip("\n")
        
        if text.startswith("Module Table"):
            nr_modules = int(text.strip("\n").split()[-1])
            module_info = True
            continue
            
        if module_info:
            if "dynamorio" not in text:
                index = text.split()[0].strip(",")
                allowed_module_indexes.add(index)
            mod_ct += 1
            if mod_ct == nr_modules:
                module_info = False
                
        if text.startswith("module["):
            index = text.split()[1].strip(":").strip("]")
            bbid  = text.split()[2].strip(",")
            
            if index in allowed_module_indexes:
                basicblocks.add(bbid)
    
    f.close()
    return basicblocks    

def compare():
    inverse = {}

    bbs0 = test3("offset_0x0.trace")

    # compare with all other traces
    for i in range(1,256):
        name = "offset_"+hex(i)+".trace"

        bbs1 = test3(name)
        diff = bbs1 - bbs0

        if len(diff):
            #print "-->", name
            first = list(diff)[0]
            #pprint.pprint()
            if first in inverse:
                inverse[first].append(i)
            else:
                inverse[first]=[i]
                
    return inverse
    

