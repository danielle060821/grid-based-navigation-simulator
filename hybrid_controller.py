from a_Star import AStar
class HybridController:
    def __init__(self, override_steps = 2, windowLen = 6):
        self.windowLen = windowLen
        self.recent_pos = []
        self.astar = AStar()
        self.override_steps = override_steps
        self.remaining_steps = 0
        self.astar_path = []
    
    def isStuck(self, pos):
        self.recent_pos.append(pos)
        if len(self.recent_pos) > self.windowLen:
            self.recent_pos.pop(0)
        unique_pos = set(self.recent_pos)
        return len(self.recent_pos) == self.windowLen and len(unique_pos) <= 2
    
    def startOverride(self, pos, grid, goal):
        path = self.astar.get_shortest_path(grid, pos, goal)
        if not path or len(path) <= 1:
            self.remaining_steps = 0
            self.astar_path = []
            return
        self.astar_path = path[1:]
        #make sure no index out of bounds
        self.remaining_steps = min(self.override_steps, len(self.astar_path))
        
    def isOverriding(self):
        return self.remaining_steps > 0 and len(self.astar_path) > 0
    
    def getToNextPos(self):
        if not self.isOverriding():
            return None
        nxt = self.astar_path.pop(0)
        self.remaining_steps -= 1
        return nxt
    
        
        
        
        