import sys
import utils

registers = [0 for i in range(8)]
stack = []
inputBuffer = utils.InputBuffer("savefile.txt")
memory = utils.loadMemory("challenge.bin")

def getVal(x): return registers[getReg(x)] if 32768 <= x <= 32775 else x
def getReg(x): return x-32768

def memoryHack():
    # Disable "$7 == 0" self-check
    memory[521] = 21
    memory[522] = 21
    memory[523] = 21
    
    # Change $7 to the Ackermann key found
    registers[7] = 25734

    # Remove "confirmation mechanism" call
    memory[5489] = 21
    memory[5490] = 21

    # Remove "$0 == 6" check after "confirmation mechanism"
    memory[5491] = 21
    memory[5492] = 21
    memory[5493] = 21
    memory[5494] = 21

    return memory

def runProgram(filename):
    memoryHack()

    PC = 0
    while True:
        if memory[PC] == 0: # halt
            return
        elif memory[PC] == 1: # set a b
            registers[getReg(memory[PC+1])] = getVal(memory[PC+2])
            PC += 3
        elif memory[PC] == 2: # push a
            stack.append(getVal(memory[PC+1]))
            PC += 2
        elif memory[PC] == 3: # pop a
            registers[getReg(memory[PC+1])] = stack.pop()
            PC += 2
        elif memory[PC] == 4: # eq a b c
            if getVal(memory[PC+2]) == getVal(memory[PC+3]):
                registers[getReg(memory[PC+1])] = 1
            else:
                registers[getReg(memory[PC+1])] = 0
            PC += 4
        elif memory[PC] == 5: # gt a b c
            if getVal(memory[PC+2]) > getVal(memory[PC+3]):
                registers[getReg(memory[PC+1])] = 1
            else:
                registers[getReg(memory[PC+1])] = 0
            PC += 4
        elif memory[PC] == 6: # jmp a
            PC = memory[PC+1]
        elif memory[PC] == 7: # jt a b
            if getVal(memory[PC+1]) != 0:
                PC = memory[PC+2]
            else:
                PC += 3
        elif memory[PC] == 8: # jf a b
            if getVal(memory[PC+1]) == 0:
                PC = memory[PC+2]
            else:
                PC += 3
        elif memory[PC] == 9: # add a b c
            registers[getReg(memory[PC+1])] = (getVal(memory[PC+2]) + getVal(memory[PC+3])) % 32768
            PC += 4
        elif memory[PC] == 10: # mult a b c
            registers[getReg(memory[PC+1])] = (getVal(memory[PC+2]) * getVal(memory[PC+3])) % 32768
            PC += 4
        elif memory[PC] == 11: # mod a b c
            registers[getReg(memory[PC+1])] = getVal(memory[PC+2]) % getVal(memory[PC+3])
            PC += 4
        elif memory[PC] == 12: # and a b c
            registers[getReg(memory[PC+1])] = getVal(memory[PC+2]) & getVal(memory[PC+3])
            PC += 4
        elif memory[PC] == 13: # or a b c
            registers[getReg(memory[PC+1])] = getVal(memory[PC+2]) | getVal(memory[PC+3])
            PC += 4
        elif memory[PC] == 14: # not a b
            registers[getReg(memory[PC+1])] = 0x7FFF - getVal(memory[PC+2])
            PC += 3
        elif memory[PC] == 15: # rmem a b
            registers[getReg(memory[PC+1])] = memory[getVal(memory[PC+2])]
            PC += 3
        elif memory[PC] == 16: # wmem a b
            prev = memory[getVal(memory[PC+1])]
            memory[getVal(memory[PC+1])] = getVal(memory[PC+2])
            PC += 3
        elif memory[PC] == 17: # call a
            stack.append(PC+2)
            PC = getVal(memory[PC+1])
        elif memory[PC] == 18: # ret
            if stack:
                PC = stack.pop()
            else:
                return
        elif memory[PC] == 19: # out a
            print(chr(getVal(memory[PC+1])), end="")
            PC += 2
        elif memory[PC] == 20: # in
            inputBuffer.input()
            read = inputBuffer.read()
            
            if memory[PC+1] >= 32768:
                registers[getReg(memory[PC+1])] = ord(read[0])
            else:
                memory[memory[PC+1]] = ord(read[0])
            PC += 2
        elif memory[PC] == 21: # noop
            PC += 1
        else:
            print("ERROR -> Addr#{}: {}".format(PC, memory[PC]))
            return

def main():
    utils.disassembler("challenge.bin", "challenge.asm")
    runProgram("challenge.bin")

if __name__ == "__main__":
    main()