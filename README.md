🎮 Grid-Based Navigation Simulator (A* Pursuit + Behavior Cloning)<br>

A grid-based navigation simulator built with Python and Pygame for experimenting with classical planning algorithms and learning-based navigation agents in a controllable grid environment.<br>

The current system includes:<br>

• an A* pursuit agent that dynamically tracks the player using pathfinding  <br>
• a Behavior Cloning (BC) navigation agent under development in a separate branch (`bc-agent`)<br>

The codebase evolved from a single-file prototype into a modular simulator architecture designed for experimenting with different navigation agents.<br>

🎥 30s Gameplay Demo (A*-driven agent):<br>  
Shows two runs: an intentional failure and a successful escape. Although the developer knows the map well, a single misstep is enough for the A* agent to catch the player.<br>  
Link: https://youtube.com/shorts/KEZ5PRIL9xc?si=0C5W6CFBQtQ1kCa9<br>

⸻

🚀 How to Run the Game<br>
```bash
# Clone the repo
git clone https://github.com/danielle060821/grid-based-navigation-simulator.git
cd grid-based-navigation-simulator

# Create virtual environment
python3 -m venv .venv

# Activate venv (Mac/Linux)
source .venv/bin/activate

# Install dependencies
pip install pygame torch

# Run the game
python game.py
```
⸻

🎮 How to Play<br>

Move the player agent (spaceship) using:<br>
• W = up<br>
• A = left<br>
• S = down<br>
• D = right<br>

Objective<br>

Reach the goal location (flag) before the pursuing agent (alien) catches you.<br>

Environment Rules<br>

• The A* agent dynamically recomputes the shortest path toward the player<br>
• Independent movement cooldowns maintain fair pacing between player and agent<br>
• A step counter tracks the agent’s movement cost<br>
• The environment includes a countdown intro, win/lose conditions, and an automatic end state<br>
• The program exits automatically 3 seconds after the game ends<br>
⸻

🧠 Technical Highlights<br>

Pathfinding Agent (A*)<br>

A* pathfinding is implemented from scratch, including:<br>

• open set (priority queue)<br>
• closed set<br>
• g_score tracking with on-demand f_score computation<br>
• path reconstruction<br>

The agent performs real-time pursuit, replanning the path toward the player each step.<br>

Agent behavior is encapsulated in a dedicated AStarAgent class, enabling future extensions to multiple agents.<br>

⸻

Learning Agent (Behavior Cloning – Work in Progress)<br>

A learning-based navigation agent is currently implemented in the bc-agent branch.<br>

The BC pipeline includes:<br>

• recording player trajectories during gameplay<br>
• dataset generation (~2k state–action samples)<br>
• training a PyTorch policy network<br>

Observation space:<br>
```
dx, dy (relative position between player and goal)
walkable directions (up, down, left, right)
```
Policy network architecture:<br>
```
Input (6)
 → Linear(32)
 → ReLU
 → Linear(32)
 → ReLU
 → Output (5 actions): up, down, left, right, stay
```
Training uses cross-entropy loss to predict player actions from observations.<br>

To explore the BC implementation:<br>
```bash
git checkout bc-agent
```
⸻

Navigation Task

The simulator represents a simple grid-based navigation task.<br>

The player agent attempts to reach a goal location while avoiding interception by a pursuing agent that performs real-time path planning.<br>

The environment is intentionally small and controlled to allow experimentation with different navigation strategies (e.g., classical planning vs learning-based agents).<br>

⸻

🏗 System Architecture<br>

JSON-Based Level System<br>

Levels are defined in external JSON files containing:<br>

• grid layout<br>
• player spawn<br>
• agent spawn<br>
• goal location<br>
• background music<br>

This enables adding new levels without modifying core game logic.<br>

⸻

Game State System

The simulator uses an explicit state machine:<br>
```
Countdown → Playing → Finished
```
This separates game flow control from rendering and logic execution.<br>

⸻

Rule Evaluation

Win/lose conditions are handled by a centralized rules module, allowing future rule extensions such as:<br>

• multiple enemies<br>
• hazards<br>
• special tiles<br>

⸻

Modular Design<br>

The codebase is organized into modules with clear separation of concerns:<br>
```
agents      – autonomous entities and AI logic
rules       – win/lose conditions
renderer    – drawing and UI
audio       – background music
asserts     – level validation checks
```
This modular structure supports experimentation with multiple navigation agents within the same environment.<br>

⸻

📁 Project Structure (Simplified)<br>
```
My_Simulator/
├── README.md
├── game.py                 # Main game loop
├── game_state.py           # Game phase & state machine
├── a_star.py               # Core A* algorithm
├── agents.py               # Agent abstractions
├── rules.py                # Win / lose evaluation
├── renderer.py             # Rendering & UI
├── audio.py                # Background music
├── asserts.py              # Level validation
├── Maps/
│   └── level1.json
├── legacy/
│   └── grid_level1.py
├── assets/
│   ├── images/
│   └── audio/
└── bc-agent/               # Behavior cloning training pipeline
```
⸻

📌 Notes<br>

• Designed as a navigation simulator for experimentation, not a full game<br>
• Emphasis on algorithm implementation, modular architecture, and agent experimentation<br>
• The codebase was refactored into multiple modules to support extensibility<br>
• Future work may include reinforcement learning agents and agent performance comparisons<br>

