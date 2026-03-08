import pygame
import json
import numpy as np
from renderer import Renderer
from audio import play_music
from game_state import Phase, GameState
from agents import AStarAgent, BCAgent
from asserts import check_asserts
from rules import Rules, GameResult
from BC.trajectory_recoreder import TrajectoryRecorder

#load level configuration
def load_level(filename):
    with open(filename) as f:
        level = json.load(f)
    return level

level_data = load_level("Maps/level1.json")
#pass level data to game state
game_state = GameState(level_data)

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

#goal
goal = tuple(level_data["goal"])
#player
start = tuple(level_data["player_start"])
player_pos = start
#astar
astar_start = tuple(level_data["astar_start"])
astar_agent = AStarAgent(astar_start)
astar_pos = astar_start
#bc
bc_start = tuple(level_data["bc_start"])
bc_pos = bc_start
bc_agent = BCAgent()

#open dataset by trajectory recorder
#path = "dataset.jsonl"
#recorder = TrajectoryRecorder(path)

sr, sc = start
gr, gc = goal
asr,asc = astar_start
bcsr, bcsc = bc_start

#check rules
rules = Rules(goal)

INITIAL_COUNTDOWN_MS = 3000
GO_MS = 1000
over_text = None
over_color = None

#avoid potential bugs
check_asserts(ROWS, COLS, grid, start, goal, astar_start)

#bc pos
def get_bc_pos(bc_pos, last_pos, now):
    last_pos = bc_pos
    state = game_state.get_bc_state(bc_pos)
    dir = bc_agent.action(state, now)
    pos = game_state.move(bc_pos, dir)
    pr, pc = pos

    if grid[pr][pc] == 1:
        return last_pos
    else:
        last_pos = pos
        return pos

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
    obs = np.array([dr, dc, int(up_walkable), int(down_walkable), int(left_walkable), int(right_walkable)])
    return obs   

"""
    Game loop
""" 
game_state.set_phase(Phase.COUNTDOWN)
while game_state.running:
    #60 frames/s
    clock.tick(60)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state.running = False
            #restart game
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            game_state.restart = True
               
    #cover the previous step
    renderer.draw_background() 
    
    #display steps    
    renderer.display_steps("AStar Alien", astar_agent.steps)
    renderer.display_steps("BC Duck", bc_agent.steps)
    
    #buffer time(4s)before game starts 
    if game_state.phase == Phase.COUNTDOWN:
        renderer.draw_static_world(grid, gr, gc)
        renderer.draw_player(sr, sc)
        renderer.draw_astar_agent(asr,asc)
        renderer.draw_bc_agent(bcsr, bcsc)
        now = pygame.time.get_ticks()
        elapsed = now - game_state.phase_start_time
        if elapsed < INITIAL_COUNTDOWN_MS:
            #count down: 3 -> 2 -> 1
            remaining = (INITIAL_COUNTDOWN_MS - elapsed + 999) // 1000
            renderer.set_countdown(remaining)
        elif elapsed - INITIAL_COUNTDOWN_MS < GO_MS:
            renderer.game_start_text()
        else:
            game_state.set_phase(Phase.PLAYING) 
            
    #restart game
    elif game_state.restart == True:    
        player_pos = game_state.reset_game()
                
    #game in process
    elif game_state.phase == Phase.PLAYING:

        renderer.draw_static_world(grid, gr, gc)
            
        #draw player
        player_pos, player_last_move, restart, _ = game_state.player_action()
    
        pr, pc = player_pos
        renderer.draw_player(pr, pc)
        now = pygame.time.get_ticks()   
        
        #draw astar agent(do not need to access internal data(ex. steps, last_move))
        astar_pos, _, _ = astar_agent.update(grid, player_pos, now)
        ar, ac = astar_pos
        renderer.draw_astar_agent(ar, ac)
        
        #draw bc agent
        bc_pos = get_bc_pos(bc_pos, bc_pos, now)
        bcr, bcc = bc_pos
        renderer.draw_bc_agent(bcr, bcc)
        
        result = rules.evaluate(player_pos, astar_pos)
        
        #player lost(game loop does not care about why lose. lose is lose)
        if result == GameResult.LOSE:
            game_state.set_phase(Phase.FINISHED)
            over_text = "You Lost!"
            over_color = (255, 0, 0)
            
        #player wins
        elif result == GameResult.WIN:
            game_state.set_phase(Phase.FINISHED)
            over_text = "You Win!"
            over_color = (23, 199, 29)
    
    #delay 3 seconds after finish
    elif game_state.phase == Phase.FINISHED:
        pr, pc = player_pos
        ar,ac = astar_pos
        bcr, bcc = bc_pos
        renderer.draw_static_world(grid, gr, gc)
        #redraw player to prevent being covered by goal
        renderer.draw_player(pr, pc)
        renderer.draw_astar_agent(ar, ac)
        renderer.draw_bc_agent(bcr, bcc)
        renderer.over_text(over_text, over_color)
        
        elapsed = pygame.time.get_ticks() - game_state.phase_start_time
        if elapsed > 3000:
            game_state.running = False
        
    pygame.display.flip()
    
pygame.quit()