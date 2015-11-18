import subprocess
import os
import drcompare


def get_drrun_path():
    args = []
    args.append("uname")
    args.append("-m")
    try:
        out = subprocess.check_output(args,stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print "Error callind uname -m\nQuitting"
        import sys
        sys.exit(-1)

    out=out.strip("\n")
    suffix = '64'
    if out == "i686" or out == "i386":
        suffix = '32'
    
    path = "/home/edgarmb/src/DynamoRIO/bin" + suffix + "/drrun"
    return path
    

#--------------------------------------------------------------------------------------------------------------------------------------------------
def bruteforce(file_offset,file_len,initials):
    
    # file_offset == len(initials)
    
    if len(initials) != file_offset:
        print "lim", [hex(x) for x in initials]
    
    while len(initials) > file_offset:
        del initials[-1]
    print "running bruteforce", file_offset, [hex(x) for x in initials]
    
    # remove previous drcov files
    files = [filename for filename in os.listdir(os.getcwd()) if 'drcov' in filename]
    for f in files:
        os.remove(f)
    
    for i in range(256):

        # initialize buffer
        s = ''
        for c in initials:
            s+=chr(c)
        buffer = s+'\x00'*(file_len-len(s))
        
        buffer = buffer[:file_offset]+chr(i)+buffer[file_offset+1:]
        
        f = open("seed.elf","wb")
        f.write(buffer)
        f.close()
        
        if i == 0:
            out = subprocess.check_output(["hexdump","-Cv","seed.elf"])
            print out
            out = subprocess.check_output(["cp","seed.elf","sample_"+s+"_seed.elf"])
        
        # execute drcov
        name = "offset_"+hex(i)+".trace"
        # check file and rename
        files = [filename for filename in os.listdir(os.getcwd()) if 'drcov' in filename]
        if len(files):
            print "The number of files should be ZERO!"
            raise
        try:
            args = []
            args.append(DRRUN_PATH)
            args.append("-t")
            args.append("drcov")
            args.append("-dump_text")
            args.append("--")
            
            #readelf
            args.append("readelf")
            args.append("-a")
            #unzip
            #args.append("unzip")
            #nm
            #args.append("nm")
            #file
            #args.append("file")
            
            args.append("seed.elf")
            # exec
            out = subprocess.check_output(args,stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            pass

        # check file and rename
        files = [filename for filename in os.listdir(os.getcwd()) if 'drcov' in filename]
        if len(files) != 1:
            print "Check error here"
            raise
        os.rename(files[0],name)
        
        
    i = drcompare.compare()
    v = i.values()
    offsets = []
    for offset in v:
        offsets.append(offset[0])
    
    return offsets
#--------------------------------------------------------------------------------------------------------------------------------------------------

def gen(file_offset,init):
    # init -> list of initial byte values
    # file_offset = how many bytes it will search in sequence
    if file_offset == 7:
        #print "\tbacktrack"
        return
    offsets = bruteforce(file_offset,0x40,init)
    for offset in offsets:
        #print "debug",file_offset, len(init)
        if file_offset == len(init):
            init.append(offset)
        else:
            init[file_offset]=offset
        gen(file_offset+1,init)

if __name__ == "__main__":
    init_values = []
    DRRUN_PATH = get_drrun_path()
    print "DRRUN path =>", DRRUN_PATH
    gen(0,init_values)
