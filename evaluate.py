from random_env_generator import generate_valid_mp
from agents import AStarAgent
from BC.bc_runner import BCRunner, BCMode
def generate_eval_mps(ROWS, COLS, num_episodes = 500):
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
   
def evaluate_BC_no_stay(ROWS, COLS, eval_mps, mode = BCMode.NO_STAY):
    max_steps = ROWS * COLS * 2
    success = 0
    timeout = 0
    tot_steps = 0
    for grid, start, goal in eval_mps:
        bc_runner = BCRunner(start, grid, goal, ROWS, COLS, mode)
        bc_agent = bc_runner.bc_agent
        steps = 0
        while bc_agent.pos != goal and steps < max_steps:
            # equivalent to remove cool down
            bc_runner.step(steps*1000)
            steps += 1
        if bc_agent.pos == goal:
            success += 1
            tot_steps += steps
        else:
            timeout += 1
    avrg_steps = tot_steps / success if success != 0 else None
    return success, timeout, avrg_steps
        
def evaluate_BC_with_fallback(ROWS, COLS, eval_mps, mode = BCMode.ASTAR_FALLBACK):
    max_steps = ROWS * COLS * 2
    success = 0
    timeout = 0
    tot_steps = 0
    for grid, start, goal in eval_mps:
        bc_runner = BCRunner(start, grid, goal, ROWS, COLS, mode)
        bc_agent = bc_runner.bc_agent
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
    bc_no_stay_success, bc_no_stay_timeout, bc_no_stay_avrg_steps = evaluate_BC_no_stay(15, 15, eval_mps)
    bc_fallback_success, bc_fallback_timeout, bc_fallback_avrg_steps = evaluate_BC_with_fallback(15, 15, eval_mps)
    print("Astar:")
    print("success rate:", astar_success / len(eval_mps), " timeout:", astar_timeout, " average steps:", astar_avrg_steps)
    
    print("BC (does not allow STAY action):")
    print("success rate:", bc_no_stay_success / len(eval_mps), " timeout:", bc_no_stay_timeout, " average steps:", bc_no_stay_avrg_steps)
    
    print("BC with Astar fallback:")
    print("success rate:", bc_fallback_success / len(eval_mps), " timeout:", bc_fallback_timeout, " average steps:", bc_fallback_avrg_steps)
    
        
        
        
        
    