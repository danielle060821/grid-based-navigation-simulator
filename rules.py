from game_state import GameResult

"""
    Game Rule
"""
class Rules():
    def __init__(self, goal):
        self.goal = goal
        self.result = GameResult.NONE
            
    def astar_caught_player(self, player_pos, astar_pos):
        if astar_pos == player_pos and player_pos != self.goal:
            return True
        return False
    
    def player_reaches_goal(self, player_pos, astar_pos):
        if player_pos == self.goal and astar_pos != player_pos:
            return True
        return False
    
    #pack all the rules to be used this in the game loop
    def evaluate(self, player_pos, astar_pos):
        #if already checked(already has a result), no need to check again
        if self.result != GameResult.NONE:
            return self.result       
        if self.astar_caught_player(player_pos, astar_pos):
            self.result = GameResult.LOSE   
        elif self.player_reaches_goal(player_pos, astar_pos):
            self.result = GameResult.WIN
        return self.result

    def reset(self):
        self.result = GameResult.NONE
        return self.result