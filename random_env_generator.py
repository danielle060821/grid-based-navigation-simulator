import random
from collections import deque
#make sure there is a path by using bfs, make sure start and goal dont overlap, and make sure start and goal is not wall
def mp_valid(grid, start, goal, ROWS, COLS):
    if start == goal:
        return False
    sr, sc = start
    gr, gc = goal
    if grid[sr][sc] == 1 or grid[gr][gc] == 1:
        return False
    q = deque([start])
    visited = set([start])
    while q:
        r, c = q.popleft()
        if (r, c) == goal:
            return True
        for nr, nc in [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]:
            if 0 <= nr < ROWS and 0 <= nc < COLS and (nr, nc) not in visited:
                if grid[nr][nc] == 0:
                    q.append((nr, nc))
                    visited.add((nr, nc))
    return False

#grid
def generate_grid(ROWS, COLS, obstacle_prob = 0.2):
    grid = []
    for _ in range(ROWS):
        row = []
        for _ in range(COLS):
            if random.random() < obstacle_prob:
                row.append(1)
            else:
                row.append(0)
        grid.append(row)
    return grid
        
#make sure the position generated is not wall
def generate_pos(grid, ROWS, COLS):
    while True:
        r = random.randint(0, ROWS - 1)
        c = random.randint(0, COLS - 1)
        if grid[r][c] == 0:
            return (r, c)

#final function being used by main
def generate_valid_mp(ROWS, COLS):
    while True:
        grid = generate_grid(ROWS, COLS, obstacle_prob = 0.2)
        start = generate_pos(grid, ROWS, COLS)
        goal = generate_pos(grid, ROWS, COLS)
        if mp_valid(grid, start, goal, ROWS, COLS):
            return grid, start, goal
        
    

