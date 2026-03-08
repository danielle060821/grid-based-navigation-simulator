import pygame
from enum import Enum, IntEnum, auto

#used auto instead of numbers to avoid unexpected confusion since there are multiple classes.
#numbers are also useless in this case.
class Phase(Enum):
    INIT = auto()
    COUNTDOWN = auto()
    PLAYING = auto()
    FINISHED = auto()
class GameResult(Enum):
    NONE = auto()
    WIN = auto()
    LOSE = auto()
class Move(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3 
    STAY = 4     
    
class GameState:
    def __init__(self, level_data):
        self.running = True
        self.phase = Phase.INIT
        self.phase_start_time = pygame.time.get_ticks()
        self.result = None
        self.finish_time = None
        self.restart = False
        self.grid = level_data["grid"]
        self.ROWS, self.COLS = level_data["map_size"]
        self.goal = level_data["goal"]
        
        #player
        self.player_start = tuple(level_data["player_start"])
        self.player_pos = self.player_start
        self.PLAYER_COOLDOWN_MS = 300
        #make sure the player can move when the frame first starts
        self.player_last_move = -self.PLAYER_COOLDOWN_MS
        
        #astar
        self.astar_start = tuple(level_data["astar_start"])
        self.astar_pos = self.astar_start
        
        #bc
        self.bc_start = tuple(level_data["bc_start"])
        self.bc_pos = self.bc_start
    
    """ 
    Player is manual
    """ 
    def player_action(self):
        action = Move.STAY
        #player can only move 1 step per PLAYER_COOLDOWN_MS // 1000 s
        now = pygame.time.get_ticks()  
        if now - self.player_last_move < self.PLAYER_COOLDOWN_MS:
            return self.player_pos, self.player_last_move,self.restart, action
            
        #Player controlling keys(record player trajectory)
        #press "R" to restart the game
        keys = pygame.key.get_pressed()
        pr, pc = self.player_pos
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
            return self.player_pos, self.player_last_move, self.restart, action  
        
        #if not wall, can go through
        if 0 <= new_pr < self.ROWS and 0 <= new_pc < self.COLS and self.grid[new_pr][new_pc] == 0:
            #move
            self.player_pos = (new_pr, new_pc)
            self.player_last_move = now
            
        #at wall or grid boundary(can't move) 
        else: 
            action = Move.STAY   
    
        #recorder.record(obs(player_pos, goal, grid), action)    
        return self.player_pos, self.player_last_move,self.restart, action    
 
    #reset game
    def reset_game(self):
        self.player_last_move = -300
        self.player_pos = self.player_start
        self.astar_pos = self.astar_start
        self.bc_pos = self.bc_start
        self.restart = False
        self.phase = Phase.COUNTDOWN
        #remember to reset game result too!
        self.result = GameResult.NONE
        return self.player_pos
    
    def move_based_on_dir(self, pos, dir):
        pr, pc = pos
        if dir == Move.UP:
            pr -= 1
        elif dir == Move.DOWN:
            pr += 1
        elif dir == Move.LEFT:
            pc -= 1
        elif dir == Move.RIGHT:
            pc += 1
        return (pr, pc)
    
    def move(self, pos, dir):
        return self.move_based_on_dir(pos, dir)

    def get_bc_state(self, player_pos):
        gr, gc = self.goal
        pr, pc = player_pos
        dr = gr - pr
        dc = gc - pc
        
        #initialize all directions to walkable
        up = 1
        down = 1
        left = 1
        right = 1
        #check boundary/wall
        if pr - 1 < 0 or self.grid[pr-1][pc] == 1:
            up = 0
        if pr + 1 >= self.ROWS or self.grid[pr+1][pc] == 1:
            down = 0
        if pc - 1 < 0 or self.grid[pr][pc-1] == 1:
            left = 0
        if pc + 1 >= self.COLS or self.grid[pr][pc+1] == 1:
            right = 0   
        return (dr, dc, up, down, left, right)
        
    def set_phase(self, new_phase):
        self.phase = new_phase
        self.phase_start_time = pygame.time.get_ticks()
        