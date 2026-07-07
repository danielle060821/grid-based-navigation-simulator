# Grid-Based Navigation Simulator

A Python simulator with two modes: a real-time interactive game and a machine learning experiment pipeline comparing A* pathfinding with a learned navigation policy (Behavior Cloning).

## Demo
▶️ [🎮Game mode(Watch Demo on YouTube)](https://youtube.com/shorts/hbPkSqb0V5U?si=l3zwWbpXMcCj4Su4)

▶️ [🧪Experiment mode(Watch Demo on YouTube)](https://youtube.com/shorts/kqObUgraAOg?si=0PpGFdVwAle4QEF6)

---
## Motivation

A* pathfinding finds the optimal path, but it requires complete map information — 
it needs to "see" the entire grid before planning. Real-world navigation (robotics, 
autonomous agents) often doesn't have this luxury: agents typically only perceive 
their local surroundings.

This project explores whether a learned policy, using only local observations, 
can approximate the performance of a fully-informed A* planner  (used here as the expert to generate training data)— and what happens 
when that learned policy fails.

## Modes

### 🎮 Game Mode (`game.py`)
Control a player with WASD keys while an A* agent pursues you in real time. Maps are loaded from JSON config files — swap maps without touching any code.

### 🧪 Experiment Mode (`BC/bc_demo.py`)
Watch a trained Behavior Cloning agent navigate randomized grid maps from start to goal. Visualizes successful runs, failure cases, and A* fallback behavior side by side.

---

## Experiment Results
Evaluated on 500 randomly generated valid maps with 20% wall density. All methods were tested on the same map set for a fair comparison.

| Method | Success Rate | Avg Steps | Timeouts |
|--------|-------------|-----------|----------|
| A* (Expert) | 100% | 11.19 | 0 |
| BC (without STAY action) | 66% | 10.80 | 172 |
| BC + A* Fallback | 87% | 12.73 | 65 |

The learned policy sometimes oscillated near obstacles; adding a 2-step A* fallback when stuck for 6 steps improved success rate from 66% to 87%.

Note: A* has full map visibility, while the BC policy only observes local 
surroundings — these numbers reflect a fundamentally different information 
constraint, not just a weaker model.

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

# Run the Behavior Cloning demo
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
│   ├── bc_demo.py           # Behavior Cloning demo
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
