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
        sol = list(range(9))
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] != sol[i * 3 + j]:
                    return False
        return True

    def heuristic(self):
        h = 0
        sol = list(range(9))
        for i in range(3):
            for j in range(3):
                k = 3 * i + j
                s = self.grid[i][j]
                h += (abs(k // 3 - s // 3) + abs(k % 3 - s % 3))
        return h + self.gen


def solve(puzzle):
    steps = 0
    pq = [puzzle]
    s = set()

    while True:
        curr = heapq.heappop(pq)
        # print('Step {}, current heuristic is {} / {}'.format(steps, curr.heuristic(), curr.grid))
        # print('Gen is {}'.format(curr.gen))
        if curr.is_solved():
            print('solved in {} steps'.format(steps))
            return curr.gen

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
    g = list(range(9))
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


step_list = []
for _ in range(101):
    puz = Puzzle(scramble())
    step_list.append(solve(puz))

print(max(step_list))
print(sum(step_list) / len(step_list))
