# Grid-Based Navigation Simulator

A Python simulator with two modes: a real-time interactive game and an ML experiment pipeline comparing A* pathfinding against a learned agent.

## Demo
▶️ [🎮Game mode(Watch Demo on YouTube)](https://youtube.com/shorts/hbPkSqb0V5U?si=l3zwWbpXMcCj4Su4)

▶️ [🧪Experiment mode(Watch Demo on YouTube)](https://youtube.com/shorts/kqObUgraAOg?si=0PpGFdVwAle4QEF6)

---

## Modes

### 🎮 Game Mode (`game.py`)
Control a player with WASD keys while an A* agent pursues you in real time. Maps are loaded from JSON config files — swap maps without touching any code.

### 🧪 Experiment Mode (`bc_demo.py`)
Watch a trained ML-based agent navigate randomized grid maps from start to goal. Visualizes success, failure, and A* override behavior side by side.

---

## Experiment Results

| Method | Success Rate | Avg Steps | Timeouts |
|--------|-------------|-----------|----------|
| A* (Oracle) | 100% | 11.74 | 0 |
| BC Baseline | 60% | 8.62 | 40 |
| BC (No STAY) | 63% | 9.35 | 37 |
| BC + A* Override | 89% | 13.38 | 11 |

Evaluated across 100 randomized maps (20% wall density). The ML agent frequently oscillated near obstacles; adding a 2-step A* override when stuck improved success rate from 60% to 89%.

---

## Getting Started

```bash
# Clone the repo
git clone https://github.com/danielle060821/grid-based-navigation-simulator.git
cd grid-based-navigation-simulator

# Create virtual environment
python3 -m venv .venv

# Activate (Mac/Linux)
source .venv/bin/activate

# Install dependencies
pip install pygame torch

# Run game mode
python game.py

# Run experiment mode
python bc_demo.py
```
## Project Structure
```
My_Simulator/
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
│   ├── bc_demo.py           # ML experiment entry point
│   ├── bc_train.py          # Model training
│   ├── collect_expert_data.py
│   ├── features.py          # Observation space design
│   ├── policy.py            # BC policy
│   ├── trajectory_recorder.py
│   ├── hybrid_controller.py # A* override fallback
│   └── dataset_expert.json  # Training data
├── experiments/
│   ├── experiments.md       # Experiment log
│   ├── pure_bc.json
│   ├── bc_no_stay.json
│   └── bc_astar_override.json
└── assets/
├── images/
└── audio/
```

## Tech Stack
Python · PyTorch · Pygame
