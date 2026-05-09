import sys

input_file=sys.argv[1]
output_file=sys.argv[2]

pc_s=0x00000000
pc_e=0x000000FF

stk_s=0b00000000000000000000000100000000
stk_e=0b00000000000000000000000101111111
stk_sp=0b00000000000000000000000101111100

mem_s=0x00010000
mem_e=0x0001007F

VIRTUAL_HALT="00000000000000000000000001100011"

inp_r={
    '00000': 0b00000000000000000000000000000000,
    '00001': 0b00000000000000000000000000000000,
    '00010': 0b00000000000000000000000101111100,
    '00011': 0b00000000000000000000000000000000,
    '00100': 0b00000000000000000000000000000000,
    '00101': 0b00000000000000000000000000000000,
    '00110': 0b00000000000000000000000000000000,
    '00111': 0b00000000000000000000000000000000,
    '01000': 0b00000000000000000000000000000000,
    '01001': 0b00000000000000000000000000000000,
    '01010': 0b00000000000000000000000000000000,
    '01011': 0b00000000000000000000000000000000,
    '01100': 0b00000000000000000000000000000000,
    '01101': 0b00000000000000000000000000000000,
    '01110': 0b00000000000000000000000000000000,
    '01111': 0b00000000000000000000000000000000,
    '10000': 0b00000000000000000000000000000000,
    '10001': 0b00000000000000000000000000000000,
    '10010': 0b00000000000000000000000000000000,
    '10011': 0b00000000000000000000000000000000,
    '10100': 0b00000000000000000000000000000000,
    '10101': 0b00000000000000000000000000000000,
    '10110': 0b00000000000000000000000000000000,
    '10111': 0b00000000000000000000000000000000,
    '11000': 0b00000000000000000000000000000000,
    '11001': 0b00000000000000000000000000000000,
    '11010': 0b00000000000000000000000000000000,
    '11011': 0b00000000000000000000000000000000,
    '11100': 0b00000000000000000000000000000000,
    '11101': 0b00000000000000000000000000000000,
    '11110': 0b00000000000000000000000000000000,
    '11111': 0b00000000000000000000000000000000
}

stk_mem={}

for addr in range(stk_s,stk_e+1,4):
    stk_mem[addr]=0

data_mem={}

for addr in range(mem_s,mem_e+1,4):
    data_mem[addr]=0

def mem_type(addr):

    if (addr%4!=0):
        print (f"misaligned memory address {hex(addr)} in line {int(PC/4)+1}")
        exit()

    if(stk_s<=addr<=stk_e):
        return "stack"
    
    if(mem_s<=addr<=mem_e):
        return "data"
    
    print (f"invalid memory address {hex(addr)} in line {int(PC/4)+1}")

    exit()

def main(instr,opcode):

    if opcode == '0110011':
        return R_type(instr)
    
    elif opcode == '0000011' or opcode == '0010011' or opcode == '1100111':
        return I_type(instr)
    
    elif opcode == '1100011':
        return B_type(instr)
    
    elif opcode == '0100011':
        return sw(instr)
    
    elif opcode == '1101111':
        return J_type(instr)
    
    elif opcode == '0110111':
        return lui(instr)
    
    elif opcode == '0010111':
        return auipc(instr)
    
    else:
        print(f"invalid opcode in line {i+1}")
        exit()

def dec_to_bin(val):
    return format(val & 0xFFFFFFFF, '032b')

def bin_to_dec(bin):

    if bin[0] == '1':  
        return -((1 << len(bin)) - int(bin, 2))
    
    else:
        return int(bin, 2)
    
def unsigned(val):
    return val&0xFFFFFFFF

def signed(val):

    val=val&0xFFFFFFFF

    if val& (1<<31):
       return val-(1<<32)
    
    return val

def signextend(val, bits):

    if val & (1 << (bits - 1)):
        val -= (1 << bits)

    return val

def auipc(instr):

    imm=instr[0:20]
    imm_val=int(imm,2)

    if imm[0]=='1':
        imm_val-=(1<<20)

    imm_val=imm_val<<12
    rd=instr[20:25]
    inp_r[rd]=unsigned(PC+imm_val)

    return PC+4

def lui(instr):

    imm=instr[0:20]
    imm_val=int(imm, 2)

    if imm[0]=='1':  
        imm_val-=(1<<20)

    imm_val=imm_val<<12
    rd=instr[20:25]
    inp_r[rd]=unsigned(imm_val)

    return PC+4

def sw(instr):

    if (instr[17:20]!="010"):
        print(f"invalid S-type instruction in line {int(PC/4)+1}")
        exit()

    imm=instr[0:7]+instr[20:25]
    imm_val=int(imm,2)

    if imm[0]=='1':
        imm_val-=(1 << 12)

    rs2=instr[7:12]
    addr=unsigned(inp_r[instr[12:17]]+imm_val)

    if mem_type(addr)=="stack":
        stk_mem[addr]=unsigned(inp_r[rs2])

    elif mem_type(addr)=="data":
        data_mem[addr]=unsigned(inp_r[rs2])

    return PC+4

def B_type(instr):
    instr = instr.strip()
    funct3 = instr[17:20]
    
    rs1 = instr[12:17]
    rs2 = instr[7:12]
    r1 = inp_r[rs1]
    r2 = inp_r[rs2]

    imm_bin = instr[0] + instr[24] + instr[1:7] + instr[20:24] + '0'
    imm_val = bin_to_dec(imm_bin)

    if funct3 == '000': 

        if r1 == r2:
            return PC + imm_val
        
        else:
            return PC + 4
                
    elif funct3 == '001': 

        if r1 != r2:
            return PC + imm_val
        
        else:
            return PC + 4         
    elif funct3 == '100':   

        if signed(r1) < signed(r2):
            return PC + imm_val
        
        else:
            return PC + 4 
        
    elif funct3 == '101':   

        if signed(r1) >= signed(r2):
            return PC + imm_val
        
        else:
            return PC + 4 
        
    elif funct3 == '110':    

        if (r1 & 0xFFFFFFFF) < (r2 & 0xFFFFFFFF):
            return PC + imm_val 
        
        else: 
            return PC + 4
        
    elif funct3 == '111': 

        if (r1 & 0xFFFFFFFF) >= (r2 & 0xFFFFFFFF):
            return PC + imm_val
         
        else:
            return PC + 4
        
    else:

        print(f"Invalid B-type instruction in line {int(PC//4)+1} ")
        exit()
    
def R_type(bin):

    func7=bin[0:7]
    func3=bin[17:20]

    if(func7=="0100000" and func3=="000"):
        #sub
        inp_r[bin[20:25]]=unsigned(inp_r[bin[12:17]]-inp_r[bin[7:12]])

    elif(func7=="0000000" and func3=="000"):
        #add
        inp_r[bin[20:25]]=unsigned(inp_r[bin[7:12]]+inp_r[bin[12:17]])

    elif(func7=="0000000" and func3=="001"):
        #sll
        inp_r[bin[20:25]]=unsigned(inp_r[bin[12:17]]<<(inp_r[bin[7:12]]&0b11111))

    elif(func7=="0000000" and func3=="010"):
        #slt
        if(signed(inp_r[bin[12:17]])<signed(inp_r[bin[7:12]])):

            inp_r[bin[20:25]]=0b00000000000000000000000000000001
        else:
            inp_r[bin[20:25]]=0b00000000000000000000000000000000

    elif(func7=="0000000" and func3=="011"):
        #sltu
        if(unsigned(inp_r[bin[12:17]])<unsigned(inp_r[bin[7:12]])):
            inp_r[bin[20:25]]=0b00000000000000000000000000000001
        else:
            inp_r[bin[20:25]]=0b00000000000000000000000000000000

    elif(func7=="0000000" and func3=="100"):
        #xor
        inp_r[bin[20:25]]=unsigned(inp_r[bin[12:17]]^inp_r[bin[7:12]])
    elif(func7=="0000000" and func3=="101"):
        #srl
        inp_r[bin[20:25]]=unsigned(inp_r[bin[12:17]]>>unsigned(inp_r[bin[7:12]]&0b11111))

    elif(func7=="0000000" and func3=="110"):
        #or
        inp_r[bin[20:25]]=inp_r[bin[12:17]]|inp_r[bin[7:12]]

    elif(func7=="0000000" and func3=="111"):
        #and
        inp_r[bin[20:25]]=inp_r[bin[12:17]]&inp_r[bin[7:12]]

    else:
        print(f"invalid R-type instruction in line {int(PC/4)+1}")
        exit()

    return PC+4

def I_type(s):

    opcode=s[25:]
    rd=s[20:25]
    rs1=s[12:17]
    func3=s[17:20]

    if (opcode=="0000011" and func3=="010"): #lw

        imm=signextend(int(s[:12],2),12)
        addr=unsigned(inp_r[rs1]+imm)

        if mem_type(addr)=="stack":
            val=stk_mem[addr]
        elif mem_type(addr)=="data":
            val=data_mem[addr]
        else:
            val=0

        inp_r[rd]=unsigned(val)
        inp_r['00000']=0 
        
        return PC+4
    
    elif (opcode=="0010011" and (func3=="000" or func3=="011")): #addi or sltiu
        funct3=s[17:20]

        if funct3=="000": #addi
            imm=signextend(int(s[0:12],2),12)
            inp_r[rd]=unsigned(inp_r[rs1]+imm)

        elif funct3=="011": #sltiu
            imm=signextend(int(s[0:12],2),12)

            if (inp_r[rs1] & 0xFFFFFFFF)<(imm & 0xFFFFFFFF):
                inp_r[rd]=1
            else:
                inp_r[rd]=0

        inp_r['00000']=0 
        return PC+4

    elif (opcode=="1100111" and func3=="000"): #jalr

        imm = signextend(int(s[0:12], 2), 12)
        nextpc = PC + 4
        PC1 = (unsigned(inp_r[rs1] + imm) // 2) * 2
        inp_r[rd] = unsigned(nextpc)
        inp_r['00000'] = 0

        return PC1
    
    else:
        print(f"invalid I-type instruction in line {(PC//4)+1}")
        exit()

def J_type(s):

    rd=s[20:25]

    imm = s[0] + s[12:20] + s[11] + s[1:11] + "0"
    immfinal= signextend(int(imm, 2), 21)
    nextpc=PC+4

    PC1=unsigned(PC+immfinal)
    inp_r[rd]=unsigned(nextpc)
    inp_r['00000']=0

    return PC1

def mem_print(f2):
    j = 0

    for i in sorted(data_mem.keys()):
        if j == 32:
            break
        f2.write("0x" + format(i, '08X') + ":" + "0b" + dec_to_bin(data_mem[i]) + "\n")
        j += 1 

def reg_print(f2,PC):
    f2.write("0b"+dec_to_bin(PC) + " ")

    for i in range(32):
        reg = format(i, '05b')   
        f2.write("0b"+dec_to_bin(inp_r[reg]) + " ")
    f2.write("\n")

with open(input_file, "r") as f1, open(output_file, "w") as f2:
    
    ll=f1.readlines()
    PC=pc_s
    i=0
    run=0
    maxr=100000
    l1=[x.strip() for x in ll if x.strip()]

    if(len(l1)==0):
        print("empty instruction file")
        exit()

    while(len(l1)>0):
        if l1[-1]=="":
            l1.pop()
        else:
            break

    if(len(l1)==0):
        print("empty instruction file")
        exit()

    if(len(l1)>64):
        print("instruction memory overflow")
        exit()

    if VIRTUAL_HALT not in l1:
        print("missing virtual halt")
        exit()

    # if l1[-1]!=VIRTUAL_HALT:
    #     print("virtual halt is not used as last instruction")
    #     exit()

    while (i < len(l1)):
        run+=1

        if run>maxr :
            print("possible infinite loop")
            exit()

        if(PC<pc_s or PC>pc_e):
            print(f"PC out of the range in line{i+1}")
            exit()
            
        if(PC%4 !=0):
            print(f"misaligned PC in line {i+1}")
            exit()

        instr = l1[i]

        if(len(instr)!=32):
            print(f"invalid instruction in line {i+1}")
            exit()

        for j in instr:
            if (j!="0" and j!="1"):
                print(f"invalid input in line {i+1}")
                exit()

        if (instr == VIRTUAL_HALT):
            reg_print(f2, PC)
            break

        op = instr[25:32]
        PC = main(instr, op)
        inp_r['00000'] = 0b00000000000000000000000000000000

        if(inp_r["00010"]<stk_s or inp_r["00010"]>stk_e):
            print((f"stack pointer out of range at line {i+1}"))
            exit()

        if(inp_r["00010"] % 4 !=0):
            print(f"misaligned stack pointer at line {i+1}")
            exit()

        if(PC<pc_s or PC>pc_e or PC>(len(l1)-1)*4):
            print(f"PC out of the range in line{i+1}")
            exit()

        if(PC%4 !=0):
            print(f"misaligned PC in line {i+1}")
            exit()

        reg_print(f2, PC)
        temp=i
        i = PC // 4
        
        if(i<0 or  i>=len(ll)):
            print(f"PC is outside the instruction list in line no {temp+1}")
            exit()

    mem_print(f2)
