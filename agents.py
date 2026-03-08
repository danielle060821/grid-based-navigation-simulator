from a_Star import AStar
from BC.policy import Policy
import torch

#matches main loop
STAY = 4
"""
    Astar agent
"""
class AStarAgent:
    def __init__(self, start_pos):
        self.start_pos = tuple(start_pos)
        self.pos = self.start_pos
        self.steps = 0
        self.ASTAR_COOLDOWN_MS = 330
        self.last_move = 0
        self.astar_agent = AStar()
             
    def update(self, grid, player_pos, now):
        #Astar agent can only move 1 step per AGENT_COOLDOWN_MS // 1000s
        if now - self.last_move <= self.ASTAR_COOLDOWN_MS:
            return self.pos, self.steps, self.last_move
        else:
            #cooldown over, reset last_move(time)
            self.last_move = now
            
        path = self.astar_agent.get_shortest_path(grid, self.pos, player_pos)
        #only walk one step at a time(0 is start, 1 is the next step because i wrote came_from = {Start: None} in a_Star.py)
        #steps that have been used
        #if agent is only 1 step away from player or already chased player(or path does not exist)
        if not path or len(path) < 2:
            return self.pos, self.steps, self.last_move     
        if path[1] != self.pos:
            self.steps += 1
            self.pos = path[1]
        return self.pos, self.steps, now
    
    def reset(self):
        self.pos = self.start_pos
        self.steps = 0
        self.last_move = 0

"""
    BC agent
"""
class BCAgent:
    def __init__(self):
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
            return STAY
        else:
            self.last_move = now
            with torch.no_grad():
                logits = self.model(state)
                dir = torch.argmax(logits, dim=1).item()
                #print("state:", state)
                #print("logits:", logits)
                #record steps
                if dir != STAY:
                    self.steps += 1
            return dir
        
        