import pygame
from enums import Phase, GameResult, Move

#used auto instead of numbers to avoid unexpected confusion since there are multiple classes.
#numbers are also useless in this case.

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
  
    #reset game
    def reset_game(self):
        self.restart = False
        self.phase = Phase.COUNTDOWN
        #remember to reset game result too!
        self.result = GameResult.NONE
        
    def set_phase(self, new_phase):
        self.phase = new_phase
        self.phase_start_time = pygame.time.get_ticks()
        