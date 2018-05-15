instInit  = []
instFinish = []
pE = eval(input("Tiempo de Unidad entera"))
pF = eval(input("Tiempo de Unidad flotante"))
tCB = eval(input("Tiempo de CB"))

ciclos = 0

regStatus={"F0":"0","F1":"0",
            "F2":"0","F3":"0",
            "F4":"0","F5":"0",
            "F6":"0","F7":"0","F8":"0","F9":"0","F10":"0",
            "R0":"0","R1":"0",
            "R2":"0","R3":"0",
            "R4":"0","R5":"0",
            "R6":"0","R7":"0",}
inStatus = {}

regs = {"F0":0,"F1":0,
       "F2":0,"F3":0,
       "F4":0,"F5":0,
       "F6":0,"F7":0,
       "R0":0,"R1":0,
       "R2":0,"R3":0,
       "R4":0,"R5":0,
       "R6":0,"R7":0,}

resStation = {1:[False,"","","","","","","",0,0],
              2:[False,"","","","","","","",0,0],
              3:[False,"","","","","","","",0,0],
              4:[False,"","","","","","","",0,0],
              5:[False,"","","","","","","",0,0],
              6:[False,"","","","","","","",0,0],
              7:[False,"","","","","","","",0,0],
              8:[False,"","","","","","","",0,0],
              9:[False,"","","","","","","",0,0]}


filepath = 'code.txt'  
with open(filepath) as fp:  
   line = fp.readline()
   cnt = 1
   while line:
       inStatus[cnt]=[str(line[:-1]).split(),[False,False,False]]
       instInit+=[cnt]
       line = fp.readline()
       cnt += 1

def printInStatus():
    o = list(inStatus.keys())
    o.sort()
    print("Instruction Status")
    print("[      Instruction      ] [Issue  Execute  WriteR]")
    for x in o:
        print(inStatus[x][0],inStatus[x][1])

def printRegStatus():
    o = list(regStatus.keys())
    o.sort()
    p=""
    for x in o:
        p+=str(regStatus[x])+"   "
    print("Register Status")
    print("F0  F1  F10  F2  F3  F4  F5  F6  F7  F8  F9  R1  R2  R3  R4  R5  R6  R7")
    print(p)
    
def printRegs():
    o = list(regs.keys())
    o.sort()
    p=""
    for x in o:
        p+=str(regs[x])+"   "
    print("Register Values")
    print(p)

def printResStation():
    o = list(resStation.keys())
    o.sort()
    print("Reservation Stations")
    print("[busy   op    vj    vk    qj    qk    a    sd    tEx  tCB]")
    for x in o:
        print(resStation[x])
    
def issue(nI,inst):
    if (inst[0]=="L.D"):
        updateResSta(nI,6,inst[3]+"+"+inst[2])
        updateResSta(nI,8,pE)
    elif(inst[0]=="S.D"):
        updateResSta(nI,6,inst[3]+"+"+inst[2])
        updateResSta(nI,8,pE)
        if(regStatus[inst[1]]!="0"):
            updateResSta(nI,7,regStatus[inst[1]])
    if(inst[2] in list(regStatus.keys())):
        if(regStatus[inst[2]]!="0"):
            updateResSta(nI,4,regStatus[inst[2]])
        else:
            updateResSta(nI,2,inst[2])
    else:
        updateResSta(nI,2,inst[2])
    if(inst[3] in list(regStatus.keys())):    
        if(regStatus[inst[3]]!="0"):
            updateResSta(nI,5,regStatus[inst[3]])
        else:
            updateResSta(nI,3,inst[3])
    else:
        updateResSta(nI,3,inst[2])

    updateResSta(nI,0,True)
    inStatus[nI][1][0]=True
    if(inst[0]!="S.D"):
        regStatus[inst[1]]=str(nI)
    if(inst[0]!="L.D" and inst[0]!="S.D"):
        updateResSta(nI,8,pF)
    updateResSta(nI,9,tCB)    
    updateResSta(nI,1,inst[0])

def updateResSta(nI,index,value):
    resStation[nI][index]=value

def doIssue():
    o = list(inStatus.keys())
    o.sort()
    for x in o:
        issue(x,inStatus[x][0])
            
def execute(nI,time):
    global instFinish
    updateResSta(nI,8,time-1)
    if(time-1 == 0):
        inStatus[nI][1][1]=True
        instFinish+=[nI]
    

def write(nI,t):
    updateResSta(nI,9,t-1)
    if(t-1==0):
        o = list(regStatus.keys())
        o.sort()
        for x in o:
            if (regStatus[x]==str(nI)):
                regStatus[x]="0"
        inStatus[nI][1][2]=True

def upResSat():
    o = list(resStation.keys())
    o.sort()
    rS=list(regStatus.values())
    for x in o:
        if(resStation[x][8]==0 and resStation[x][9]==0):
            resStation[x]=[False,"","","","","","","",0,0]
        else:
            if(resStation[x][4]!="" and not (resStation[x][4] in rS)):
                resStation[x][4]=""
                updateResSta(x,2,inStatus[x][0][2])
            if(resStation[x][5]!="" and not (resStation[x][5] in rS)):
                resStation[x][5]=""
                updateResSta(x,3,inStatus[x][0][3])
            if(resStation[x][7]!="" and not (resStation[x][7] in rS)):
                resStation[x][7]=""
                
                
                
     
def doWrite():
    o = list(resStation.keys())
    o.sort()
    for x in o:
        if(resStation[x][8]==0 and resStation[x][0]):
            write(x,resStation[x][9])
            break                        
    
def doExe():
    o = list(resStation.keys())
    o.sort()
    flagE=False
    flagF=False
    toExe=[]
    for x in o:
        if(resStation[x][1]=="L.D" or resStation[x][1]=="S.D" ):
            if(resStation[x][4] == "" and
               resStation[x][5] == "" and resStation[x][7] == ""
               and not flagE and resStation[x][8]!=0):
                toExe+=[[x,resStation[x][8]]]
                flagE=True
        else:
            if(resStation[x][4] == "" and
               resStation[x][5] == "" and not flagF
               and resStation[x][8]!=0):
                toExe+=[[x,resStation[x][8]]]
                flagF=True
        if(flagF and flagE):
            break
    for x in toExe:
        execute(x[0],x[1])

def finish():
    o = list(resStation.keys())
    o.sort()
    flag=True
    for x in o:
        if(resStation[x][0]):
            flag=False
            break
    return flag
def main():
    cont=0
    print("---------------------------CICLO: "+str(cont)+"-----------------------")
    doIssue()  
    printRegStatus()
    printInStatus()
    printResStation()
    cont+=1
    while(1):
        input("")
        print("---------------------------CICLO: "+str(cont)+"-----------------------")
        doWrite()
        doExe()
        upResSat()
        printRegStatus()
        printInStatus()
        printResStation()
        cont+=1
        if(finish()):
            break
    print("Ingreso de Instrucciones")
    print(instInit)
    print("Salida de Instrucciones")
    print(list(dict.fromkeys(instFinish)))
    input("Presione enter para terminar")
main()
