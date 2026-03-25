import numpy as np

"""
    observation for bc
"""
#obs: need dx, dy and up_walkable, down...,left...,right...
def obs(bc_pos, goal, grid, ROWS, COLS):
    up_walkable = True
    down_walkable = True
    left_walkable = True
    right_walkable = True
    br, bc = bc_pos
    gr, gc = goal
    dr = gr - br
    dc = gc - bc
    
    #check if position is valid first, avoid out of bounds error
    if br + 1 >= ROWS or grid[br + 1][bc] == 1:
        up_walkable = False
    if br - 1 < 0 or grid[br - 1][bc] == 1:
        down_walkable = False
    if bc - 1 < 0 or grid[br][bc - 1] == 1:
        left_walkable = False
    if bc + 1 >= COLS or grid[br][bc + 1] == 1:
        right_walkable = False       
    obs = np.array([dr, dc, int(up_walkable), int(down_walkable), int(left_walkable), int(right_walkable)])
    return obs   
