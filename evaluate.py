from random_env_generator import generate_valid_mp
from agents import AStarAgent
from BC.bc_runner import BCRunner
def generate_eval_mps(ROWS, COLS, num_episodes = 100):
    eval_mps = []
    for _ in range(num_episodes):
        eval_mps.append(generate_valid_mp(ROWS, COLS))
    return eval_mps
    
def evaluate_Astar(ROWS, COLS, eval_mps):
    max_steps = ROWS * COLS * 2
    success = 0
    timeout = 0
    tot_steps = 0
    for grid, start, goal in eval_mps:
        astar_agent = AStarAgent(start)
        astar_agent.ASTAR_COOLDOWN_MS = 0
        steps = 0
        while astar_agent.pos != goal and steps < max_steps:
            astar_agent.update(grid, goal, steps * 1000)
            steps += 1
        if astar_agent.pos == goal:
            success += 1
            tot_steps += steps
        else:
            timeout += 1
    avrg_steps = tot_steps / success if success != 0 else None
    return success, timeout, avrg_steps
   
        
def evaluate_BC(ROWS, COLS, eval_mps):
    max_steps = ROWS * COLS * 2
    success = 0
    timeout = 0
    tot_steps = 0
    for grid, start, goal in eval_mps:
        bc_runner = BCRunner(start, grid, goal, ROWS, COLS)
        bc_agent = bc_runner.bc_agent
        bc_agent.BC_COOLDOWN_MS = 0
        steps = 0
        while bc_agent.pos != goal and steps < max_steps:
            bc_runner.step(steps*1000)
            steps += 1
        if bc_agent.pos == goal:
            success += 1
            tot_steps += steps
        else:
            timeout += 1
    avrg_steps = tot_steps / success if success != 0 else None
    return success, timeout, avrg_steps

if __name__ == '__main__':
    eval_mps = generate_eval_mps(15, 15)
    astar_success, astar_timeout, astar_avrg_steps = evaluate_Astar(15, 15, eval_mps)
    bc_success, bc_timeout, bc_avrg_steps = evaluate_BC(15, 15, eval_mps)
    print("Astar:")
    print("success rate:", astar_success / len(eval_mps), " timeout:", astar_timeout, " average steps:", astar_avrg_steps)
    print("BC:")
    print("success rate:", bc_success / len(eval_mps), " timeout:", bc_timeout, " average steps:", bc_avrg_steps)
    
        
        
        
        
    