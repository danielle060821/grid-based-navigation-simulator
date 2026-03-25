from enum import Enum, IntEnum, auto

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
    