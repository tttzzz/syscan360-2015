# Edgar Barbosa

# Script to generate Z3 formulas

from itertools import product
    
functions_arity = {'bvadd':  2, 
                   'bvnot':  1,
                   'bvneg':  1, 
                   'bvurem': 2,
                   'bvsub':  2,
                   'bvand':  2}

class Z3Output(object):
    def __init__(self):
        self.vars = None
    def parse(self,text):
        vars = {}
        lines = text.split("\n")
        if lines[0].strip() == 'sat':
            if lines[1].strip() == '(model':
                previous = ''
                for l in lines[2:]:
                    r = l.strip()
                    if "define-fun" in r:
                        n = r[12:14]
                        previous = n
                    elif '#' in r:
                        # value
                        vars[previous]=r
        self.vars = vars
        #print vars
        return

class Z3Variable(object):
    def __init__(self,name,size):
        self.name = name
        self.size = size

class Z3Formula(object):
    def __init__(self):
        self.variables = []
    def add_variable(self,z3v):
        found = False
        for variable in self.variables:
            if variable.name == z3v.name:
                return
        self.variables.append(z3v)

def phase2(level,arity,psize=0):
    # generates a list of all possible instruction operands combinations!
    # example: [('p0', 'p0'), ('p0', 'p1'), ('p1', 'p0'), ('p1', 'p1')]
    l = []
    r = []
    for i in range(level):
        l.append('%'+str(i))

    if psize == 0:
        for i in range(arity):
            l.append('p'+str(i))
        psize = i+1
    else:
        for i in range(psize):
            l.append('p'+str(i))
        if arity > 1:
            i+=1
            l.append('p'+str(i))

    for p in product(l,repeat=arity):
        r.append(p)   

    #print r, psize 
    return r, psize

def phase1(s):  
    # s --> product element (instructions X instructions X ...)
    global combs
    global sats

    n_instrs = len(s)   #number of instructions
    params = []
 
    list_of_products = []
    
    psize = 0
    for i in xrange(n_instrs):
        nl, psize = phase2(i,functions_arity[s[i]], psize)
        list_of_products.append(nl)
    
    for p in product(*list_of_products):
        # ready to generate a new formula
        
        log = open("log.txt","w")
        z3f = Z3Formula()
        lines = []
        for i in range(len(p)):
            z3f.add_variable(Z3Variable('%'+str(i),32))
            z3f.add_variable(Z3Variable('p0',32))
            z3f.add_variable(Z3Variable('p1',32))
            
            # add example 2
            z3f.add_variable(Z3Variable('p0a',32))
            #z3f.add_variable(Z3Variable('p1a',32))
            #z3f.add_variable(Z3Variable('%'+str(n_instrs-1)+"a",32))

            for var in p[i]:
                z3f.add_variable(Z3Variable(var,32))
            line = "(assert (= " + '%' + str(i) + " (" + s[i] + " "
            for var in p[i]:
                line = line + " " + var
            line += ")))"
            lines.append(line)
            combs +=1
        
        declarations = []
        for v in z3f.variables:
            vd = "(declare-const "+v.name+" (_ BitVec " + str(v.size)+"))"
            declarations.append(vd)
            log.write(vd+"\n")
            if v.name[0]=='%':
                newname = v.name+"a"
                newvd = "(declare-const "+newname+" (_ BitVec " + str(v.size)+"))"
                log.write(newvd+"\n")
        for line in lines:
            log.write(line+"\n") 
            
        # copy and replace for example 2
        #log.write(";-----debug - copy lines\n")
        for line in lines:
            perc = line.find("%")
            newline = line
            while perc != -1:
                newline = newline[:perc+2]+"a "+newline[perc+2:]
                perc = newline.find("%",perc+1)
            newline = newline.replace("p0","p0a")
            #newline = newline.replace("p1","p1a")
            if "%1" in line and "%1a" not in newline:
                print 'Error in formula generation'
                print newline
                import sys
                sys.exit()
            log.write(newline+"\n")

        # add EXAMPLES
        # 1 -> 2
        # 2 -> 3
        last = len(p) - 1
        log.write("(assert (= p0 #x00000001))\n")
        log.write("(assert (= %"+str(last)+" #x00000002))\n")
        
        log.write("(assert (= p0a #x00000002))\n")
        log.write("(assert (= %"+str(last)+"a"+" #x00000003))\n")

        # check if examples vars are in lines:
        vp0 = False
        vlast = False
        for line in lines:
            if 'p0' in line:
                vp0 = True
            if '%'+str(last) in line:
                vlast = True
        if not (vp0 and vlast):
            log.close()
            continue

        log.write("(check-sat)\n")
        log.write("(get-model)\n")
        log.close()
        
        import subprocess
        try:
            out = subprocess.check_output(["z3","-smt2","log.txt"])
            
            print '-'*80
            #print ">>>SAT!!!"
            sats += 1
            print 'Formula found! Length',len(p)
            print '-'*80
            print subprocess.check_output(["cat","log.txt"])
            print '-'*80
            print 'MODEL'
            print '-'*80
            print out
        
        except subprocess.CalledProcessError as e:
            error = e.output.split("\n")
            if False:
                print '-'*80
                print 'exception', e.output
                print subprocess.check_output(["cat","log.txt"])
    return

# it will be necessary to check if the operator
# accepts the choosen parameters since they may
# have an invalid size, like bvadd bv32, bv16!
def generate(rep):
    
    vars = ['p1','p2']
    
    counter = 0
    # generate the product with the following commands/instructions
    instructions = ['bvadd','bvsub','bvneg','bvand']
    print "Product generation with these instructions:", instructions
    for p in product(instructions,repeat=rep):
        #s = ' -> '.join(p)
        #print '-'*100
        phase1(p)
        counter+=1
        
    print '# of products =', counter
    print 'Total of combinations', combs
 
#globals
combs = 0
sats = 0

if __name__ == '__main__':
    if True:
        for i in range(8):
            print "-"*80
            print 'Generating formulas with', i, 'instructions.'
            generate(i)
            if sats > 0:
                break
        print
        print "SAT #", sats
    else:
        generate(2)


