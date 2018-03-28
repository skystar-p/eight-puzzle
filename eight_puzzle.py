import heapq
import json
from random import randint, shuffle


class Puzzle:
    def __init__(self, init, gen=0):
        self.grid = [[0 for _ in range(3)] for _ in range(3)]
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
        sol = [1, 2, 3, 8, 0, 4, 7, 6, 5]
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] != sol[i * 3 + j]:
                    return False
        return True

    def heuristic(self):
        h = 0
        h2 = 0
        sol = [1, 2, 3, 8, 0, 4, 7, 6, 5]
        solind = [4, 0, 1, 2, 5, 8, 7, 6, 3]
        for i in range(3):
            for j in range(3):
                s = self.grid[i][j]
                k = solind[s]
                if s == 0:
                    continue
                h += (abs(k // 3 - i) + abs(k % 3 - j))
        
        if self.grid[1][1] != 0:
            h2 += 1
        l1 = [(self.grid[0][0], self.grid[0][1]), 
                (self.grid[0][1], self.grid[0][2]),
                (self.grid[0][2], self.grid[1][2]),
                (self.grid[1][2], self.grid[2][2]),
                (self.grid[2][2], self.grid[2][1]),
                (self.grid[2][1], self.grid[2][0]),
                (self.grid[2][0], self.grid[1][0])]
        l2 = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8)]
        for p in l1:
            try:
                l2.index(p)
            except ValueError:
                h2 += 2
        h = h + 3 * h2
        
        return h + self.gen


def solve(puzzle):
    steps = 0
    pq = [puzzle]
    s = set()

    while True:
        curr = heapq.heappop(pq)
        #print('Step {}, current heuristic is {} / {}'.format(steps, curr.heuristic(), curr.grid))
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
    g = [1, 2, 3, 8, 0, 4, 7, 6, 5]
    shuffle(g)
    c = 0
    gg = g[:]
    gg.remove(0)
    for j in range(8):
        for i in range(j+1, 8):
            if gg[j] < gg[i]:
                c += 1

    if c % 2 == 0:
        return scramble()
    l = [g[:3], g[3:6], g[6:]]
    return l


gen_list = []
step_list = []
for _ in range(511):
    puz = Puzzle(scramble())
    s = solve(puz)
    step_list.append(s[0])
    gen_list.append(s[1])

print("max of gen:  {}".format(max(gen_list)))
print("avg of gen:  {}".format(sum(gen_list) / len(gen_list)))
print("avg of step: {}".format(sum(step_list) / len(step_list)))
"""
puz = Puzzle([[0, 1, 3], [8, 2, 4], [7, 6, 5]])
solve(puz)
"""
