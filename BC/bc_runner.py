from BC.hybrid_controller import HybridController
from agents import BCAgent
from BC.features import obs
from enums import BCMode
class BCRunner:
    def __init__(self, start, grid, goal, ROWS, COLS, mode):
        self.hybrid_controller = HybridController()
        self.bc_agent = BCAgent(start)
        self.grid = grid
        self.goal = goal
        self.ROWS = ROWS
        self.COLS = COLS
        self.last_move_time = 0
        self.mode = mode
    def step(self, now):
        if now - self.last_move_time < self.bc_agent.BC_COOLDOWN_MS:
            return
        self.last_move_time = now
        if self.mode == BCMode.ASTAR_FALLBACK:
            #temporarily take over by astar if stuck
            if self.hybrid_controller.isOverriding():
                self.bc_agent.pos = self.hybrid_controller.getToNextPos()
            else:
                if self.hybrid_controller.isStuck(self.bc_agent.pos):
                    self.hybrid_controller.startOverride(self.bc_agent.pos, self.grid, self.goal)
                    if self.hybrid_controller.isOverriding():
                        self.bc_agent.pos = self.hybrid_controller.getToNextPos()
            
                else:
                    observation = obs(self.bc_agent.pos, self.goal, self.grid, self.ROWS, self.COLS)
                    bc_action = self.bc_agent.action(observation, now)
                    self.bc_agent.move(bc_action, self.grid, self.ROWS, self.COLS)
            self.bc_agent.steps += 1 
        elif self.mode == BCMode.NO_STAY:
            observation = obs(self.bc_agent.pos, self.goal, self.grid, self.ROWS, self.COLS)
            bc_action = self.bc_agent.action(observation, now)
            self.bc_agent.move(bc_action, self.grid, self.ROWS, self.COLS)
            self.bc_agent.steps += 1 
            
        