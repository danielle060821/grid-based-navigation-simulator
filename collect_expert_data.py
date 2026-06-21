import random
from enums import Move
from random_env_generator import generate_valid_mp
from agents import AStarAgent
from BC.trajectory_recoreder import TrajectoryRecorder
from BC.features import obs

def expert_data(ROWS, COLS, save_path, episodes = 1000):
    max_steps = ROWS * COLS * 2
    recorder = TrajectoryRecorder(save_path)
    recorder.reset(save_path)
    for episode in range(episodes):
        grid, start, goal = generate_valid_mp(ROWS, COLS)
        #astar to generate expert data for bc
        expert = AStarAgent(start)
        #expert data(remove cooldown time to reduce stay)
        expert.ASTAR_COOLDOWN_MS = 0
        step = 0
        while expert.pos != goal and step <= max_steps:
            expert_obs = obs(expert.pos, goal, grid, ROWS, COLS)
            prev_r, prev_c = expert.pos
            expert.update(grid, goal, step*1000)
            er, ec = expert.pos
            if er < prev_r:
                expert_action = Move.UP
            elif er > prev_r:
                expert_action = Move.DOWN
            elif ec < prev_c:
                expert_action = Move.LEFT
            elif ec > prev_c:
                expert_action = Move.RIGHT
            else:
                expert_action = Move.STAY

            #record data: only keep 1% of "STAY" data when recording, to prevent agent from only learning "STAY"
            if expert_action == Move.STAY:
                if random.random() < 0.01:
                    recorder.record(expert_obs, expert_action, episode, step)
                        
            else:
                recorder.record(expert_obs, expert_action, episode, step)
            step += 1
        print("episode: ", episode, " finished at: ", expert.pos, " goal: ", goal, " steps: ", step )
if __name__ == "__main__":
    expert_data(15, 15, "dataset_expert.jsonl")
                
        