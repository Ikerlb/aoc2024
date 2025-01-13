from sys import stdin

def parse_instructions(instr):
    res = []
    instr = "".join(instr.splitlines())
    for c in instr:
        
        if c == "<":
            res.append((0, -1))
        elif c == "v":
            res.append((1, 0))
        elif c == ">":
            res.append((0, 1))
        else:
            res.append((-1, 0))
    return res

def format_dir(dr, dc):
    if (dr, dc) == (0, 1):
        return ">"
    if (dr, dc) == (1, 0):
        return "v"
    if (dr, dc) == (-1, 0):
        return "^"
    return "<"

class Grid:
    def __init__(self, grid):
        self.n = len(grid)
        self.m = len(grid[0])
        self.objs = {}
        self.robot = None
        self._parse(grid)
        
    def _parse(self, grid):
        n, m = len(grid), len(grid[0])
        for r in range(n):
            for c in range(m):
                ch = grid[r][c]    
                if ch == "]":
                    continue
                elif ch == "#":
                    coords = [(r, c)]
                    self.add(coords, Wall(coords))
                elif ch == "O":
                    coords = [(r, c)]
                    self.add(coords, Box(coords))
                elif ch == "[" and c + 1 < m and grid[r][c + 1] == "]":
                    coords = [(r, c), (r, c + 1)]
                    self.add(coords, Box(coords))
                elif ch == "@": 
                    coords = [(r, c)]
                    robot = Robot(coords)
                    self.add(coords, robot)
                    self.robot = robot

    def can_move(self, dr, dc):
        r, c = self.robot.coords[0]
        s = [(r, c)]
        seen = set(s)
        while s:
            #print(s, seen)
            r, c = s.pop()
            if type(self.objs[(r, c)]) is Wall:
                return False
            nr, nc = r + dr, c + dc
            if (nr, nc) in self.objs:
                for r, c in self.objs[(nr, nc)].coords:
                    if (r, c) not in seen:
                        seen.add((r, c))
                        s.append((r, c))    
        return True
            

    # does this really mean no wall was hit?
    def move(self, dr, dc):
        if not self.can_move(dr, dc):
            return False
        r, c = self.robot.coords[0]            
        s = [(r, c)]
        seen = set(s)
        to_move = set()
        while s:
            r, c = s.pop()
            if (r, c) in self.objs:
                to_move.add(self.objs[(r, c)])
            nr, nc = r + dr, c + dc
            if (nr, nc) in self.objs:
                for r, c in self.objs[(nr, nc)].coords:
                    if (r, c) not in seen:
                        seen.add((r, c))
                        s.append((r, c))    


        # then move on objects
        # to avoid double moving
        for obj in to_move:
            for r, c in obj.coords:
                self.objs.pop((r, c))
            # do move
            obj.move(dr, dc)    

        for obj in to_move:
            for r, c in obj.coords:
                self.objs[(r, c)] = obj
        return True

        
    def add(self, coords, obj):
        for tup in coords:
            self.objs[tup] = obj


    def gps(self):
        return sum(obj.gps() for obj in set(self.objs.values()))

    def __repr__(self):
        res, chrs = [], {}
        for obj in self.objs.values():
            for tup, ch in obj.coords_chars():
                chrs[tup] = ch
        
        for r in range(self.n):
            row = []
            for c in range(self.m):
                if (r, c) in chrs:
                    row.append(chrs[(r, c)])
                else:
                    row.append(".")
            res.append("".join(row))
        return "\n".join(res)

class GridObject:
    def __init__(self, coords):
        self.coords = coords

    def gps(self):
        return 0

    def __contains__(self, tup):
        return tup in self.coords

    def move(self, dr, dc):
        self.coords = [(r + dr, c + dc) for r, c in self.coords]

    def __repr__(self):
        return f"{type(self)}{self.coords}"


class Wall(GridObject):
    def __init__(self, coords):
        super().__init__(coords)

    # coords of wall should
    # only have a single char
    def coords_chars(self):
        yield self.coords[0], "#"


    
class Box(GridObject):
    def __init__(self, coords):
        super().__init__(coords)

    def coords_chars(self):
        if len(self.coords) > 1:
            yield from zip(self.coords, "[]")
        else:
            yield self.coords[0], "O"

    def gps(self):
        r, c = self.coords[0]
        return r * 100 + c

class Robot(GridObject):
    def __init__(self, coords):
        super().__init__(coords)

    def coords_chars(self):
        yield self.coords[0], "@"

def augment(grid):
    res = []
    for r in grid:
        row = [] 
        for c in r:
            if c == "#":
                row.extend("##")
            elif c == "@":
                row.extend("@.")
            elif c == ".":
                row.extend("..")
            else:
                row.extend("[]")
        res.append(row)
    return res

txt = "".join(stdin)
grid_txt, instructions_txt = txt.split("\n\n")
grid = [list(row) for row in grid_txt.splitlines()]
instructions = parse_instructions(instructions_txt)

def simulate(grid, instructions):
    #print(grid)
    for (dr, dc) in instructions:
        grid.move(dr, dc)
        #print(f"Move {format_dir(dr, dc)}:")
        #print(grid)
    return grid.gps()

#p1
print(simulate(Grid(grid), instructions))
#p2
print(simulate(Grid(augment(grid)), instructions))
