# Reinforcement Learning for Optimizing Engineering Designs

## Overview
This experiment demonstrates how **Reinforcement Learning (RL)** can be used for two engineering optimization tasks:

1. **Energy Consumption Optimization** — learn which machine power action to take at different load levels.
2. **Robot Guidance and Navigation** — train a robot to move from a starting cell to a goal in a grid world.

The implementation is provided in a Jupyter Notebook and uses **Q-learning**, a model-free reinforcement learning algorithm.

## Objectives
- Understand how an agent learns by receiving rewards and penalties.
- Learn a suitable machine power action for each load level.
- Train a simulated robot to reach a goal while minimizing unnecessary movement.
- Visualize the robot's movement through a grid.

## Technologies Used
- Python
- NumPy
- Matplotlib
- `random` and `time` (Python standard library)
- Jupyter Notebook

## Project Structure
```text
.
└── E10_Implementation_Reinforced Learning for optimizing engineering designs (2).ipynb
```

## Task 1: Energy Consumption Optimization

### Concept
The agent selects an operating action based on the current machine load. The reward table provides feedback for each state-action combination.

**States (machine load):**
- Low
- Medium
- High

**Actions:**
- Reduce power
- Maintain power
- Increase power

### Q-learning settings
| Parameter | Value | Meaning |
|---|---:|---|
| Learning rate (`alpha`) | 0.1 | How quickly new information updates the Q-table |
| Discount factor (`gamma`) | 0.9 | Importance of future rewards |
| Exploration rate (`epsilon`) | 0.2 | Chance of trying a random action |
| Training episodes | 1,000 | Number of learning iterations |

The notebook initializes a Q-table, selects actions using an epsilon-greedy strategy, calculates rewards, and updates the Q-values. It then prints the Q-table and the best action for each machine load.

The notebook's stated example policy is:
| Machine load | Best action |
|---|---|
| Low | Reduce power |
| Medium | Maintain power |
| High | Increase power |

*Note: Q-values are learned during execution and can vary because the code uses random choices.*

## Task 2: Robot Guidance and Navigation

### Concept
A simulated robot moves on a 5 × 5 grid from the start cell `(0, 0)` to the goal cell `(4, 4)`. The Q-learning agent learns which movement to choose at each cell.

**Available actions:**
- Right
- Left
- Down
- Up

**Reward system:**
- `+100` when the robot reaches the goal.
- `-1` for other moves, encouraging the robot to reach the goal with fewer steps.

### Q-learning settings
| Parameter | Value |
|---|---:|
| Learning rate (`alpha`) | 0.1 |
| Discount factor (`gamma`) | 0.9 |
| Exploration rate (`epsilon`) | 0.2 |
| Training episodes | 300 |

The Q-table stores values for each grid cell and possible movement. After training, Matplotlib displays the robot's movement toward the goal.

**Important:** The current grid-world code does not define any obstacles, so it demonstrates goal navigation rather than obstacle avoidance. It also does not impose a maximum number of steps per episode or during visualization; if the learned policy fails to reach the goal, execution may continue for a long time.

## How to Run

1. Download or clone this project and open the `.ipynb` file in Jupyter Notebook, JupyterLab, or VS Code.
2. Make sure Python is installed.
3. Install the required packages:
   ```bash
   pip install numpy matplotlib notebook
   ```
4. Open the notebook and run the cells from top to bottom.
5. Review the printed Q-table and best policy for Task 1.
6. Observe the Matplotlib animation for Task 2.

## Expected Output
- A learned Q-table for machine energy optimization.
- A printed best action for each machine load.
- A message indicating that robot training is completed.
- A grid visualization showing the robot's movement toward the goal.
- A message when the robot reaches the goal.

Because the notebook uses random action selection, numeric Q-values and the exact learned behavior may differ between runs.

## Conclusion
This experiment illustrates how reinforcement learning can support engineering optimization. Q-learning uses rewards and penalties to learn machine power-control actions and robot navigation decisions. The example provides a basic foundation for more advanced systems that include realistic energy measurements, obstacles, and additional constraints.

## Future Improvements
- Add obstacles to the robot's grid and penalize collisions.
- Set a maximum number of steps per episode to prevent endless loops.
- Set random seeds for more reproducible results.
- Evaluate energy consumption with realistic simulated or measured data.
- Compare Q-learning results across different learning rates and exploration settings.
