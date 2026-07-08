# Grid-Based Navigation Simulator

A Python-based navigation simulator featuring both a real-time interactive game and a hybrid navigation agent that combines learning (Behavior Cloning) and algorithmic planning (A*).

## Demo
▶️ [🎮 Game Mode(Watch Demo on YouTube)](https://youtube.com/shorts/hbPkSqb0V5U?si=l3zwWbpXMcCj4Su4)

▶️ [🧪 Hybrid Navigation Mode(Watch Demo on YouTube)](https://youtube.com/shorts/kqObUgraAOg?si=0PpGFdVwAle4QEF6)

---
## Motivation

A* pathfinding finds the optimal path, but it requires complete map information — it needs to “see” the entire grid before planning. In real-world robotics, however, maintaining an accurate global map is often difficult, while local observations are much easier to obtain.

This project explores a hybrid navigation approach where a learned policy handles most navigation using only local observations, while A* is used only as a fallback when needed. The goal is not to replace A* completely, but to reduce how often the system depends on a global planner while still maintaining reliable navigation.

## Hybrid Navigation Architecture

```text
              Local Observation
                     │
                     ▼
        Learned Policy (Behavior Cloning)
                     │
             ┌───────┴────────┐
             │                │
         Normal         Stuck for 6 steps
             │                │
             ▼                ▼
        Next Action      Expert Planner (A*)
             │                │
             └───────┬────────┘
                     ▼
              Continue Navigation
```
The learned policy handles routine navigation using only local observations, while the expert planner is invoked only when recovery is needed.

## Modes

### 🎮 Game Mode (`game.py`)
Control a player with WASD keys while an A* agent pursues you in real time. Maps are loaded from JSON config files — swap maps without touching any code.

### 🧪 Hybrid Navigation Mode (`BC/bc_demo.py`)
Watch the hybrid navigation agent navigate randomized grid maps. The learned policy performs most navigation, while A* is used only as a fallback when needed. The demo showcases successful runs, recovery cases, and failure cases.

---

## Experiment Results
Evaluated on 500 randomly generated valid maps with 20% wall density. All methods were tested on the same map set for a fair comparison. The hybrid agent achieved an 87% success rate while requiring expert intervention for only about 4% of navigation steps.

| Method | Success Rate | Avg Steps | Timeouts | Expert Steps |
|--------|-------------:|----------:|----------:|-------------:|
| A* (Expert) | 100% | 11.19 | 0 | 100% |
| BC (without STAY) | 66% | 10.80 | 172 | 0% |
| Hybrid Agent | **87%** | 12.73 | 65 | **4.1%** |

The learned policy sometimes oscillated near obstacles, causing navigation failures. To improve robustness, a 2-step A* fallback was triggered after the policy remained stuck for 6 consecutive steps. This increased the success rate from 66% to 87%.


**Note:** A* has access to the full map throughout navigation, while the learned policy only receives local observations. The hybrid system calls the expert planner only when recovery is needed, allowing the learned policy to make the vast majority (96%) of navigation decisions independently.

---

## Requirements
- Python 3.11+

## Get Started

```bash
# Clone the repository
git clone https://github.com/danielle060821/grid-based-navigation-simulator.git

# Enter the project directory
cd grid-based-navigation-simulator

# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment (macOS/Linux)
source .venv/bin/activate

# Install project dependencies
python3 -m pip install -r requirements.txt

# Run the game
python3 game.py

# Run the hybrid navigation demo
python3 BC/bc_demo.py
```

## Project Structure
```
grid-based-navigation-simulator/
├── game.py                  # Interactive game mode
├── a_Star.py                # A* pathfinding implementation
├── agents.py                # Agent class definitions
├── game_state.py            # Game state management
├── renderer.py              # Pygame rendering
├── rules.py                 # Game rules and logic
├── enums.py                 # Shared enumerations
├── random_env_generator.py  # Randomized map generation
├── evaluate.py              # Evaluation pipeline
├── Maps/
│   └── level1.json          # JSON map configs
├── BC/
│   ├── bc_demo.py           # Hybrid navigation demo
│   ├── bc_train.py          # Model training
│   ├── collect_expert_data.py
│   ├── features.py          # Observation space design
│   ├── policy.py            # Neural network policy
│   ├── trajectory_recorder.py
│   ├── hybrid_controller.py # A* fallback controller
│   └── dataset_expert.json  # Training data
├── experiments/
│   ├── experiments.md       # Experiment log
│   ├── pure_bc.json
│   ├── bc_no_stay.json
│   └── bc_astar_override.json
├── assets/
│   ├── audio/
│   └── images/
├── audio.py
└── requirements.txt
```

## Tech Stack
Python · PyTorch · Pygame · Git
