from a_Star import AStar
from BC.policy import Policy
import torch
import pygame
from enums import Move

"""
    Player(Manual)
"""
class Player:
    def __init__(self, start_pos):
        self.start = tuple(start_pos)
        self.pos = self.start
        self.PLAYER_COOLDOWN_MS = 300
        self.last_move = -self.PLAYER_COOLDOWN_MS
        
    def action(self, grid, ROWS, COLS):
        action = Move.STAY
        #player can only move 1 step per PLAYER_COOLDOWN_MS // 1000 s
        now = pygame.time.get_ticks()  
        if now - self.last_move < self.PLAYER_COOLDOWN_MS:
            return action
            
        #Player controlling keys(record player trajectory)
        #press "R" to restart the game
        keys = pygame.key.get_pressed()
        new_pr, new_pc = self.pos
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
            return action  
        
        #if not wall, can go through
        if 0 <= new_pr < ROWS and 0 <= new_pc < COLS and grid[new_pr][new_pc] == 0:
            #move
            self.pos = (new_pr, new_pc)
            self.last_move = now
            
        #at wall or grid boundary(can't move) 
        else: 
            action = Move.STAY   

        #recorder.record(obs(player_pos, goal, grid), action)    
        return action  
        
    def reset(self):
        self.pos = self.start
        self.last_move = 0
            
"""
    Astar agent
"""
class AStarAgent:
    def __init__(self, start_pos):
        self.start = tuple(start_pos)
        self.pos = self.start
        self.steps = 0
        self.ASTAR_COOLDOWN_MS = 330
        self.last_move = -self.ASTAR_COOLDOWN_MS
        self.astar_agent = AStar()
             
    def update(self, grid, player_pos, now):
        #Astar agent can only move 1 step per AGENT_COOLDOWN_MS // 1000s
        if now - self.last_move <= self.ASTAR_COOLDOWN_MS:
            return
        else:
            #cooldown over, reset last_move(time)
            self.last_move = now
            
        path = self.astar_agent.get_shortest_path(grid, self.pos, player_pos)
        #only walk one step at a time(0 is start, 1 is the next step because i wrote came_from = {Start: None} in a_Star.py)
        #steps that have been used
        #if agent is only 1 step away from player or already chased player(or path does not exist)
        if not path or len(path) < 2:
            return 
        next_pos = path[1]     
        if next_pos != self.pos:
            self.steps += 1
            self.pos = next_pos
    
    def reset(self):
        self.pos = self.start
        self.steps = 0
        self.last_move = 0

"""
    BC agent
"""
class BCAgent:
    def __init__(self, start_pos):
        self.start = tuple(start_pos)
        self.pos = self.start
        self.BC_COOLDOWN_MS = 300
        self.steps = 0
        self.last_move = -self.BC_COOLDOWN_MS
        self.model = Policy()
        self.model.load_state_dict(torch.load("BC/model.pth", map_location="cpu"))
        #change to evalution mode(not training)
        self.model.eval()
        
    #get direction(not position)
    def action(self, state, now):
        state = torch.tensor(state).float().unsqueeze(0)
        
        if now - self.last_move < self.BC_COOLDOWN_MS:
            return Move.STAY
        else:
            self.last_move = now
            with torch.no_grad():
                logits = self.model(state)
                action = torch.argmax(logits, dim=1).item()
                print("state:", state)
                print("logits:", logits)
                #record steps
                if action != Move.STAY:
                    self.steps += 1
            return action
    
    def move(self, action, grid, ROWS, COLS):
            r, c = self.pos
            if action == Move.UP:
                r -= 1
            elif action == Move.DOWN:
                r += 1
            elif action == Move.LEFT:
                c -= 1
            elif action == Move.RIGHT:
                c += 1
            #if not wall, can go through
            if 0 <= r < ROWS and 0 <= c < COLS and grid[r][c] == 0:
                #move
                self.pos = (r, c)    
            #at wall or grid boundary(can't move) 
            else: 
                return
                
    
    def reset(self):
        self.pos = self.start
        self.steps = 0
        self.last_move = 0
        
        