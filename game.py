import pygame
import json
#import random
from renderer import Renderer
from audio import play_music
from game_state import Phase, GameState
from agents import AStarAgent, BCAgent, Player
from asserts import check_asserts
from rules import Rules, GameResult
#from BC.trajectory_recoreder import TrajectoryRecorder
from BC.features import obs

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
gr, gc = goal
#player
player = Player(tuple(level_data["player_start"]))
#astar
astar_agent = AStarAgent(tuple(level_data["astar_start"]))
#bc
bc_agent = BCAgent(tuple(level_data["bc_start"]))

#open dataset by trajectory recorder
path = "dataset.jsonl"
#recorder = TrajectoryRecorder(path)
#recorder.reset(path)

#check rules
rules = Rules(goal)

INITIAL_COUNTDOWN_MS = 3000
GO_MS = 1000
over_text = None
over_color = None

#avoid potential bugs
check_asserts(ROWS, COLS, grid, player.start, goal, astar_agent.start)

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
        pr, pc = player.pos
        ar, ac = astar_agent.pos
        br, bc = bc_agent.pos
        renderer.draw_static_world(grid, gr, gc)
        renderer.draw_player(pr, pc)
        renderer.draw_astar_agent(ar,ac)
        renderer.draw_bc_agent(br, bc)
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
        game_state.reset_game()  
        result = rules.reset()
        player.reset()
        astar_agent.reset()
        bc_agent.reset()
           
    #game in process
    elif game_state.phase == Phase.PLAYING:

        renderer.draw_static_world(grid, gr, gc)
            
        #draw player
        player_action = player.action(grid, ROWS, COLS)
        pr, pc = player.pos
        renderer.draw_player(pr, pc)
        now = pygame.time.get_ticks()   
        
        #draw astar agent(do not need to access internal data(ex. steps, last_move))
        astar_agent.update(grid, player.pos, now)
        ar, ac = astar_agent.pos
        renderer.draw_astar_agent(ar, ac)
        
        #draw bc agent
        observation = obs(bc_agent.pos, goal, grid, ROWS, COLS)
        bc_action = bc_agent.action(observation, now)
        bc_agent.move(bc_action, grid, ROWS, COLS)
        br, bc = bc_agent.pos
        renderer.draw_bc_agent(br, bc)
        
        #record data: only keep 1% of "STAY" data when recording, to prevent agent from only learning "STAY"
        """if bc_action == Move.STAY:
            if random.random() < 0.01:
                recorder.record(observation, bc_action)    
        else:
            recorder.record(observation, bc_action)
        """   
        result = rules.evaluate(player.pos, astar_agent.pos)
    
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
        renderer.draw_static_world(grid, gr, gc)
        #redraw player to prevent being covered by goal
        pr, pc = player.pos
        ar, ac = astar_agent.pos
        br, bc = bc_agent.pos
        renderer.draw_player(pr, pc)
        renderer.draw_astar_agent(ar, ac)
        renderer.draw_bc_agent(br, bc)
        renderer.over_text(over_text, over_color)
        
        elapsed = pygame.time.get_ticks() - game_state.phase_start_time
        if elapsed > 3000:
            game_state.running = False
        
    pygame.display.flip()
    
pygame.quit()