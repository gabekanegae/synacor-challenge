class InputBuffer:
    def __init__(self, savefile=None):
        if savefile:
            self.data = loadSave(savefile)
        else:
            self.data = []
        self.cur = 0

    def read(self):
        if len(self.data) <= self.cur:
            return None

        char = self.data[self.cur]
        self.cur += 1
        return char

    def input(self):
        if len(self.data) == 0 or len(self.data) <= self.cur:
            print(">>> ", end="")
            self.data += list(input() + "\n")

def loadSave(filename):
    s = []

    with open(filename) as f:
        for l in f:
            s += list(l.strip()) + ["\n"]
    
    return s

def loadMemory(filename):
    memory = [0 for i in range(32768)]
    cur = 0
    with open(filename, "rb") as f:
        read = f.read(2)
        while read:
            memory[cur] = int.from_bytes(read, "little")
            cur += 1
            read = f.read(2)

    return memory

def disassembler(filenameBIN, filenameASM):
    opCodes = ["halt", "set", "push", "pop", "eq",
           "gt", "jmp", "jt", "jf", "add",
           "mult", "mod", "and", "or",
           "not", "rmem", "wmem", "call",
           "ret", "out", "in", "noop"]

    opAmts = [0, 2, 1, 1, 3, 3, 1, 2, 2, 3, 3,
              3, 3, 3, 2, 2, 2, 1, 0, 1, 1, 0]

    memory = loadMemory(filenameBIN)

    with open(filenameASM, "w") as f:
        end = len(memory)
        cur = 0
        while cur < end:
            op = int(memory[cur])
            cur += 1
            if op <= 21:
                f.write("{:>5}: {}".format(cur-1, opCodes[op]))
                for i in range(opAmts[op]):
                    arg = int(memory[cur])
                    if arg >= 32768 and arg <= 32775: # Registers
                        arg = "$" + str(arg-32768)
                    elif op == 19 and arg >= 32 and arg <= 126: # Char
                        arg = str(arg) + "   \t# '" + chr(arg) + "'"
                    f.write(" {}".format(arg)) # Integers
                    cur += 1
                f.write("\n")
            else: # Not an instruction, just a memory value
                f.write("{:>5}: {}\n".format(cur-1, op))