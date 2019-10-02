import random

class Graph:
    def __init__(self, nodeAmt, symbols):
        self.nodeAmt = nodeAmt
        self.edges = [[0 for i in range(self.nodeAmt)] for i in range(self.nodeAmt)]
        self.symbols = symbols

    def addEdge(self, a, b):
        self.edges[a][b] = 1

    def getNeighbors(self, a):
        neighbors = []
        for i in range(self.nodeAmt):
            if self.edges[a][i] == 1:
                neighbors.append(i)
        return neighbors

    def solve(self, s, e):
        while True:
            path = [self.symbols[s]]
            curPos = s
            total = int(self.symbols[s])
            while True:
                if total <= 0 or total >= 32768: break
                if len(path) >= 13: break

                if not self.getNeighbors(curPos): break
                nextPos = random.choice(self.getNeighbors(curPos))
                
                if not self.getNeighbors(nextPos): break
                nextNextPos = random.choice(self.getNeighbors(nextPos))
                
                nextFloor, nextNextFloor = self.symbols[nextPos], self.symbols[nextNextPos]
                if nextFloor == "-":
                    total -= int(nextNextFloor)
                    path.append(nextFloor)
                    path.append(nextNextFloor)
                elif nextFloor == "+":
                    total += int(nextNextFloor)
                    path.append(nextFloor)
                    path.append(nextNextFloor)
                elif nextFloor == "*":
                    total *= int(nextNextFloor)
                    path.append(nextFloor)
                    path.append(nextNextFloor)

                if nextNextPos == e and total == 30:
                    print("".join(path) + " = " + str(total))
                    return

                curPos = nextNextPos
            #     print("".join(path) + " = " + str(total))
            # print("Invalid path! Starting from scratch...")

symbols = ["*", "8", "-", "1",
           "4", "*", "11", "*",
           "+", "4", "-", "18",
           "22", "-", "9", "*"]

edgesH = [(0,1), (1,2), (2,3), (4,5), (5,6), (6,7),
          (8,9), (9,10), (10,11), (12,13), (13,14), (14,15)]
edgesV = [(0,4), (4,8), (8,12), (1,5), (5,9), (9,13),
          (2,6), (6,10), (10,14), (3,7), (7,11), (11,15)]

edgesHInverted = [(b, a) for (a, b) in edgesH]
edgesVInverted = [(b, a) for (a, b) in edgesV]

edges = edgesH + edgesV + edgesHInverted + edgesVInverted

edges.remove((8, 12))
edges.remove((13, 12))
edges.remove((3, 2))
edges.remove((3, 7))

g = Graph(16, symbols)
for e in edges:
    if e != (8, 12) and e != (13, 12) and e != (3, 2) and e != (3, 7):
        g.addEdge(e[0], e[1])

g.solve(12, 3)

# 22+4-11*4-18-11-1 = 30
# NEENWSEEWNNE