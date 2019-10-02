memory = [0 for i in range(32768)]
cur = 0
with open("challenge.txt", "rb") as f:
    read = f.read(2)
    while read:
        memory[cur] = int.from_bytes(read, "little")
        cur += 1
        read = f.read(2)

decrypted = []

for addr in range(6068, 30050):
    content = memory[addr]
    addr = (addr ** 2) % 32768      # 1735
    aux = content & addr            # 2129
    aux = (0x7FFF - aux) % 32768    # 2133
    content = content | addr        # 2136
    content = content & aux         # 2129

    addr2 = 16724                   # 1741

    aux = content & addr2           # 2129
    aux = (0x7FFF - aux) % 32768    # 2133
    content = content | addr2       # 2136
    content = content & aux         # 2129

    decrypted.append(content)       # 2144

cur = 0
s = []
while cur < 30050-6068-1:
    if (decrypted[cur] >= 32 and decrypted[cur] <= 127) or decrypted[cur] == 10:
        s.append(chr(decrypted[cur]))
    elif (decrypted[cur+1] >= 32 and decrypted[cur+1] <= 127):
        l = "\n[{}]> ".format(cur+6068)
        s += list(l)
    cur += 1

with open("game-strings.txt", "w") as f:
    for c in s:
        f.write(c)