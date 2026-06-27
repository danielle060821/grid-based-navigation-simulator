import sys
import os

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

import pygame
from renderer import Renderer
from audio import play_music
from game_state import Phase, GameState
from random_env_generator import generate_valid_mp
from bc_runner import BCRunner

def run_bc_demo(ROWS, COLS):
    grid, start, goal = generate_valid_mp(ROWS, COLS)
    level_data = {
        "level_name": "Random BC Demo",
        "grid": grid,
        "bc_start": list(start),
        "map_size":[ROWS, COLS], 
        "goal": list(goal),
        "music": "assets/audio/Space_Game_Music.mp3"
    }
    game_state = GameState(level_data)
    """
        Initialize
    """
        
    pygame.init()
    clock = pygame.time.Clock()
    grid = level_data["grid"]
    renderer = Renderer(15, 15)
    level_name = level_data.get("level_name", "Space Game")
    renderer.set_caption(level_name) 
    
    #background music
    play_music(level_data["music"])
    #goal
    goal = tuple(level_data["goal"])
    gr, gc = goal
    
    #bc
    bc_runner = BCRunner(start, grid, goal, ROWS, COLS)
    bc_agent = bc_runner.bc_agent
    INITIAL_COUNTDOWN_MS = 3000
    GO_MS = 1000
    over_text = None
    over_color = None
    max_steps = ROWS * COLS * 2

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
        renderer.display_steps("BC Duck", bc_agent.steps)
        
        #buffer time(4s)before game starts 
        if game_state.phase == Phase.COUNTDOWN:
            br, bc = bc_agent.pos
            renderer.draw_static_world(grid, gr, gc, ROWS, COLS)
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
            grid, start, goal = generate_valid_mp(ROWS, COLS)
            gr, gc = goal
            bc_runner = BCRunner(start, grid, goal, ROWS, COLS)
            bc_agent = bc_runner.bc_agent
            game_state.restart = False
            
        #game in process
        elif game_state.phase == Phase.PLAYING:

            renderer.draw_static_world(grid, gr, gc, ROWS, COLS)
                
            now = pygame.time.get_ticks()   
            
            bc_runner.step(now)
                
            # print("obs:", observation)
            # print("action:", bc_action)
            # print("pos:", bc_agent.pos)
            
            #draw bc agent
            br, bc = bc_agent.pos
            renderer.draw_bc_agent(br, bc)
            
            #bc reaches goal
            if bc_agent.pos == goal:
                game_state.set_phase(Phase.FINISHED)
                over_text = "BC Win!"
                over_color = (23, 199, 29)
            elif bc_agent.steps >= max_steps:
                game_state.set_phase(Phase.FINISHED)
                over_text = "Time Out!"
                over_color = (255, 0, 0)
        #delay 3 seconds after finish
        elif game_state.phase == Phase.FINISHED:
            renderer.draw_static_world(grid, gr, gc, ROWS, COLS)
            br, bc = bc_agent.pos
            renderer.draw_bc_agent(br, bc)
            renderer.over_text(over_text, over_color)
            
            elapsed = pygame.time.get_ticks() - game_state.phase_start_time
            if elapsed > 3000:
                game_state.running = False
            
        pygame.display.flip()
        
    pygame.quit()

if __name__ == "__main__":
    run_bc_demo(15, 15)
    
    
    
    