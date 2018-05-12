regStatus=
inStatus = {}
regs = [0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0] 
for  x in range(16):
    regStatus+=["load0"]

resStation = {"load0":[False,"","","","","","",""],
              "load1":[False,"","","","","","",""],
              "load2":[False,"","","","","","",""],
              "mul0":[False,"","","","","","",""],
              "mul1":[False,"","","","","","",""],
              "mul2":[False,"","","","","","",""],
              "add0":[False,"","","","","","",""],
              "add1":[False,"","","","","","",""],
              "add2":[False,"","","","","","",""]}


filepath = 'code.txt'  
with open(filepath) as fp:  
   line = fp.readline()
   cnt = 1
   while line:
       inStatus[cnt]=[str(line[:-1]).split(),[False,False,False]]
       line = fp.readline()
       cnt += 1

def printInStatus(i):
    o = list(i.keys())
    o.sort()
    print("Instruction Status")
    for x in o:
        print(inStatus[x][0],inStatus[x][1])

def printRegStatus(r):
    p=""
    for x in r:
        p+=str(x)+"   "
    print("Register Status")
    print(p)
    
def printRegs(r):
    p=""
    for x in r:
        p+=str(x)+"   "
    print("Registers Valus")
    print(p)
    
printRegStatus(regStatus)
printRegs(regs)
printInStatus(inStatus)
