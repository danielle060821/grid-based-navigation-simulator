import pygame
import json
import numpy as np
from enum import IntEnum
from renderer import Renderer
from audio import play_music
from game_state import Phase, GameState
from agents import AStarAgent
from asserts import check_asserts
from rules import Rules, GameResult
from trajectory_recoreder import TrajectoryRecorder

#load level configuration
def load_level(filename):
    with open(filename) as f:
        level = json.load(f)
    return level

level_data = load_level("Maps/level1.json")

"""
    Initialize
"""
    
pygame.init()
clock = pygame.time.Clock()
grid = level_data["grid"]
renderer = Renderer()
ROWS, COLS = renderer.ROWS, renderer.COLS

#set caption for the current level 
#set "Space Game" as caption when level name is not found, avoid unexpected behaviour 
level_name = level_data.get("level_name", "Space Game")
renderer.set_caption(level_name) 

#background music
play_music(level_data["music"])   

#player    
start = tuple(level_data["player_start"])
player_pos = start

#goal
goal = tuple(level_data["goal"])

#astar agent
astar_start = tuple(level_data["astar_start"])
astar_agent = AStarAgent(astar_start)

#open dataset by trajectory recorder
#path = "dataset.jsonl"
#recorder = TrajectoryRecorder(path)

sr, sc = start
gr, gc = goal
asr,asc = astar_start

#check rules
rules = Rules(goal)

INITIAL_COUNTDOWN_MS = 3000
GO_MS = 1000
over_text = None
over_color = None

PLAYER_COOLDOWN_MS = 300
restart = False
#make sure the player can move when the frame first starts
player_last_move = -PLAYER_COOLDOWN_MS
class Move(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3 
    STAY = 4  

#avoid potential bugs
check_asserts(ROWS, COLS, grid, start, goal, astar_start)

""" 
    Player is manual
""" 
#reset game
def reset_game(player_start, astar_start):
    global player_last_move, restart
    player_pos = player_start
    astar_agent.pos = astar_start
    player_last_move = -PLAYER_COOLDOWN_MS
    restart = False
    state.set_phase(Phase.COUNTDOWN)
    #remember to reset game result too!
    rules.result = GameResult.NONE
    
    return player_pos
    
def player_action(player_pos, player_last_move, restart):
    
    action = Move.STAY
    #player can only move 1 step per PLAYER_COOLDOWN_MS // 1000 s
    now = pygame.time.get_ticks()  
    if now - player_last_move < PLAYER_COOLDOWN_MS:
           return player_pos, player_last_move,restart
         
    #Player controlling keys(record player trajectory)
    #press "R" to restart the game
    keys = pygame.key.get_pressed()
    action = Move.STAY
    pr, pc = player_pos
    new_pr, new_pc = pr, pc
    if keys[pygame.K_w]:
            new_pr -= 1
            action = Move.UP
    elif keys[pygame.K_s]:
            new_pr += 1
            action = Move.DOWN
    elif keys[pygame.K_a]:
            new_pc -= 1
            action = Move.LEFT
    elif keys[pygame.K_d]:
            new_pc += 1
            action = Move.RIGHT
    else:
        #stay(did not press any key)
        #recorder.record(obs(player_pos, goal, grid), action)    
        return player_pos, player_last_move, restart  
     
    #if not wall, can go through
    if 0 <= new_pr < ROWS and 0 <= new_pc < COLS and grid[new_pr][new_pc] == 0:
        #move
        player_pos = (new_pr, new_pc)
        player_last_move = now
        
    #at wall or grid boundary(can't move) 
    else: 
        action = Move.STAY   
  
    #recorder.record(obs(player_pos, goal, grid), action)    
    return player_pos, player_last_move,restart

"""
Trajectory recording
"""
#obs: need dx, dy and up_walkable, down...,left...,right...
def obs(player_pos, goal, grid):
    up_walkable = True
    down_walkable = True
    left_walkable = True
    right_walkable = True
    pr, pc = player_pos
    gr, gc = goal
    dr = gr - pr
    dc = gc - pc
    
    #check if position is valid first, avoid out of bounds error
    if pr + 1 >= ROWS or grid[pr + 1][pc] == 1:
        up_walkable = False
    if pr - 1 < 0 or grid[pr - 1][pc] == 1:
        down_walkable = False
    if pc - 1 < 0 or grid[pr][pc - 1] == 1:
        left_walkable = False
    if pc + 1 >= COLS or grid[pr][pc + 1] == 1:
        right_walkable = False       
    obs = np.array([dr, dc, up_walkable, down_walkable, left_walkable, right_walkable])
    return obs   
                  
"""
    Game loop
""" 
state = GameState()
state.set_phase(Phase.COUNTDOWN)
while state.running:
    #60 frames/s
    clock.tick(60)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state.running = False
            #restart game
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            restart = True
               
    #cover the previous step
    renderer.draw_background() 
    
    #display steps    
    renderer.display_steps(astar_agent.steps)
    
    #buffer time(4s)before game starts 
    if state.phase == Phase.COUNTDOWN:
        renderer.draw_static_world(grid, gr, gc)
        renderer.draw_player(sr, sc)
        renderer.draw_astar_agent(asr,asc)
        now = pygame.time.get_ticks()
        elapsed = now - state.phase_start_time
        if elapsed < INITIAL_COUNTDOWN_MS:
            #count down: 3 -> 2 -> 1
            remaining = (INITIAL_COUNTDOWN_MS - elapsed + 999) // 1000
            renderer.set_countdown(remaining)
        elif elapsed - INITIAL_COUNTDOWN_MS < GO_MS:
            renderer.game_start_text()
        else:
            state.set_phase(Phase.PLAYING) 
            
    #restart game
    elif restart == True:    
        player_pos = reset_game(start, astar_start)
                
    #game in process
    elif state.phase == Phase.PLAYING:

        renderer.draw_static_world(grid, gr, gc)
            
        #draw player
        player_pos, player_last_move, restart = player_action(player_pos, player_last_move, restart)
    
        pr, pc = player_pos
        renderer.draw_player(pr, pc)
        now = pygame.time.get_ticks()   
        
        #draw astar agent(do not need to access internal data(ex. steps, last_move))
        astar_pos, _, _ = astar_agent.update(grid, player_pos, now)
        ar, ac = astar_pos
        renderer.draw_astar_agent(ar, ac)
        result = rules.evaluate(player_pos, astar_pos)
        
        #player lost(game loop does not care about why lose. lose is lose)
        if result == GameResult.LOSE:
            state.set_phase(Phase.FINISHED)
            over_text = "You Lost!"
            over_color = (255, 0, 0)
            
        #player wins
        elif result == GameResult.WIN:
            state.set_phase(Phase.FINISHED)
            over_text = "You Win!"
            over_color = (23, 199, 29)
    
    #delay 3 seconds after finish
    elif state.phase == Phase.FINISHED:
        pr, pc = player_pos
        ar,ac = astar_agent.pos
        renderer.draw_static_world(grid, gr, gc)
        #redraw player to prevent being covered by goal
        renderer.draw_player(pr, pc)
        renderer.draw_astar_agent(ar, ac)
        renderer.over_text(over_text, over_color)
        
        elapsed = pygame.time.get_ticks() - state.phase_start_time
        if elapsed > 3000:
            state.running = False
        
    pygame.display.flip()
    
pygame.quit()