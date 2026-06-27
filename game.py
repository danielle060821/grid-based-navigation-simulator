import pygame
import json
from renderer import Renderer
from audio import play_music
from game_state import Phase, GameState
from agents import AStarAgent, Player
from asserts import check_asserts
from rules import Rules, GameResult

#load level configuration
def load_level(filename):
    with open(filename) as f:
        level = json.load(f)
    return level

def run_game_mode():
    level_data = load_level("Maps/level1.json")
    #pass level data to game state
    game_state = GameState(level_data)
    """
        Initialize
    """
        
    pygame.init()
    clock = pygame.time.Clock()
    grid = level_data["grid"]
    ROWS, COLS = level_data["ROWS"], level_data["COLS"]
    renderer = Renderer(ROWS, COLS)

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
        
        #buffer time(4s)before game starts 
        if game_state.phase == Phase.COUNTDOWN:
            pr, pc = player.pos
            ar, ac = astar_agent.pos
           
            renderer.draw_static_world(grid, gr, gc, ROWS, COLS)
            renderer.draw_player(pr, pc)
            renderer.draw_astar_agent(ar,ac)
           
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
            game_state.restart = False
            
        #game in process
        elif game_state.phase == Phase.PLAYING:

            renderer.draw_static_world(grid, gr, gc, ROWS, COLS)
                
            #draw player
            player.action(grid, ROWS, COLS)
            pr, pc = player.pos
            renderer.draw_player(pr, pc)
            now = pygame.time.get_ticks()   
            
            #draw astar agent(do not need to access internal data(ex. steps, last_move))
            astar_agent.update(grid, player.pos, now)
            ar, ac = astar_agent.pos
            renderer.draw_astar_agent(ar, ac)
            
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
            renderer.draw_static_world(grid, gr, gc, ROWS, COLS)
            #redraw player to prevent being covered by goal
            pr, pc = player.pos
            ar, ac = astar_agent.pos
            renderer.draw_player(pr, pc)
            renderer.draw_astar_agent(ar, ac)
            renderer.over_text(over_text, over_color)
            
            elapsed = pygame.time.get_ticks() - game_state.phase_start_time
            if elapsed > 3000:
                game_state.running = False
            
        pygame.display.flip()
        
    pygame.quit()

if __name__ == "__main__":
    run_game_mode()