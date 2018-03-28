import heapq
import json
from random import randint, shuffle


class Puzzle:
    def __init__(self, init, gen=0):
        self.grid = [[0 for _ in range(3)] for _ in range(3)]
        self.sol = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.solind = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        for i in range(3):
            for j in range(3):
                self.grid[i][j] = init[i][j]
        self.gen = gen

    def __le__(self, other):
        sh = self.heuristic()
        oh = other.heuristic()
        if sh == oh:
            return self.gen > other.gen
        return sh <= oh

    def __lt__(self, other):
        sh = self.heuristic()
        oh = other.heuristic()
        if sh == oh:
            return self.gen >= other.gen
        return sh < oh

    def swap(self, i1, j1, i2, j2):
        t = self.grid[i1][j1]
        self.grid[i1][j1] = self.grid[i2][j2]
        self.grid[i2][j2] = t

    def blank(self):
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == 0:
                    return i, j

    def left(self):
        i, j = self.blank()
        if i == 2:
            raise ValueError
        self.swap(i, j, i+1, j)
        c = Puzzle(self.grid, self.gen + 1)
        self.swap(i, j, i+1, j)
        return c

    def right(self):
        i, j = self.blank()
        if i == 0:
            raise ValueError
        self.swap(i, j, i-1, j)
        c = Puzzle(self.grid, self.gen + 1)
        self.swap(i, j, i-1, j)
        return c

    def up(self):
        i, j = self.blank()
        if j == 2:
            raise ValueError
        self.swap(i, j, i, j+1)
        c = Puzzle(self.grid, self.gen + 1)
        self.swap(i, j, i, j+1)
        return c

    def down(self):
        i, j = self.blank()
        if j == 0:
            raise ValueError
        self.swap(i, j, i, j-1)
        c = Puzzle(self.grid, self.gen + 1)
        self.swap(i, j, i, j-1)
        return c

    def is_solved(self):
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] != self.sol[i * 3 + j]:
                    return False
        return True
    """
    def conflict_r(self, t):
        r = 0
        if t == 0:
            return r
        for i in range(3):
            k = -1
            for j in range(3):
                if self.grid[i][j] == t:
                    k = j # column of tj
                    break
            if k >= 0:
                l = -1
                for j in range(3):
                    if self.sol[3 * i + j] == t:
                        l = j # column of the goal position of tj
                        break
                if l >= 0:
                    for j in range(0, k):
                        if self.grid[i][j] == 0:
                            continue
                        if (self.solind[self.grid[i][j]] // 3 == i) and (self.solind[self.grid[i][j]] % 3 > l):
                            r += 1
        return r
    
    def conflict_c(self, t):
        r = 0
        if t == 0:
            return r
        for j in range(3):
            k = -1
            for i in range(3):
                if self.grid[i][j] == t:
                    k = i # row of ti
                    break
            if k >= 0:
                l = -1
                for i in range(3):
                    if self.sol[3 * i + j] == t:
                        l = i # row of the goal position of ti
                        break
                if l >= 0:
                    for i in range(0, k):
                        if self.grid[i][j] == 0:
                            continue
                        if (self.solind[self.grid[i][j]] % 3 == j) and (self.solind[self.grid[i][j]] // 3 > l):
                            r += 1
        return r

    def conflict_t(self, t1, t2):
        if t1 == 0 or t2 == 0 or t1 == t2:
            return False
        i1 = -1
        i2 = -1
        j1 = -1
        j2 = -1
        gi1 = -1
        gi2 = -1
        gj1 = -1
        gj2 = -1
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == t1:
                    i1 = i
                    j1 = j
                    gi1 = self.solind[t1] // 3
                    gj1 = self.solind[t1] % 3
                if self.grid[i][j] == t2:
                    i2 = i
                    j2 = j
                    gi2 = self.solind[t2] // 3
                    gj2 = self.solind[t2] % 3
        if (i1 == i2 and i1 == gi1 and gi1 == gi2 and j1 > j2 and gj1 < gj2) or (j1 == j2 and j1 == gj1 and gj1 == gj2 and i1 > i2 and gi1 < gi2):
            return True
        return False


    def md(self):
        h = 0
        for i in range(3):
            for j in range(3):
                s = self.grid[i][j]
                k = self.solind[s]
                if s == 0:
                    continue
                h += (abs(k // 3 - i) + abs(k % 3 - j))
        return h
        
    """
    def heuristic(self):
        h = 0
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == 0:
                    continue
                if i != self.solind[self.grid[i][j]] // 3:
                    h += 1
                if j != self.solind[self.grid[i][j]] % 3:
                    h += 1

        return h + self.gen


def solve(puzzle):
    steps = 0
    pq = [puzzle]
    s = set()

    while True:
        curr = heapq.heappop(pq)
        #print('Step {}, current heuristic is {}, md is {} / {}'.format(steps, curr.heuristic(), curr.md(), curr.grid))
        #print('Gen is {}'.format(curr.gen))
        if curr.is_solved():
            print('solved in {} steps; Gen is {}'.format(steps, curr.gen))
            return (steps, curr.gen)

        try:
            new = curr.left()
            if not json.dumps(new.grid) in s:
                heapq.heappush(pq, new)
                s.add(json.dumps(new.grid))
        except ValueError:
            pass
        try:
            new = curr.right()
            if not json.dumps(new.grid) in s:
                heapq.heappush(pq, new)
                s.add(json.dumps(new.grid))
        except ValueError:
            pass
        try:
            new = curr.up()
            if not json.dumps(new.grid) in s:
                heapq.heappush(pq, new)
                s.add(json.dumps(new.grid))
        except ValueError:
            pass
        try:
            new = curr.down()
            if not json.dumps(new.grid) in s:
                heapq.heappush(pq, new)
                s.add(json.dumps(new.grid))
        except ValueError:
            pass

        steps += 1


def scramble():
    g = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    shuffle(g)
    c = 0
    gg = g[:]
    gg.remove(0)
    for j in range(8):
        for i in range(j+1, 8):
            if gg[j] < gg[i]:
                c += 1

    if c % 2 == 1:
        return scramble()
    l = [g[:3], g[3:6], g[6:]]
    return l


gen_list = []
step_list = []
for _ in range(101):
    puz = Puzzle(scramble())
    s = solve(puz)
    step_list.append(s[0])
    gen_list.append(s[1])

print("max of gen:  {}".format(max(gen_list)))
print("avg of gen:  {}".format(sum(gen_list) / len(gen_list)))
print("avg of step: {}".format(sum(step_list) / len(step_list)))
"""
puz = Puzzle([[2, 7, 0], [5, 4, 3], [8, 1, 6]])
solve(puz)

puz = Puzzle([[3, 4, 2], [0, 1, 5], [6, 7, 8]])
print(puz.conflict_c(0))
print(puz.conflict_c(3))
print(puz.conflict_c(6))
print(puz.conflict_c(1))
"""
