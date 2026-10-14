import random
import numpy as np
from flask import Flask, render_template_string, request

app = Flask(__name__)

# HTML Template with Interactive Form UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>RL Engineering Optimization & Navigation Dashboard</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 30px; background: #f0f2f5; color: #333; }
        h1 { text-align: center; color: #1a73e8; margin-bottom: 30px; }
        .container { display: flex; flex-direction: column; gap: 30px; max-width: 900px; margin: 0 auto; }
        .card { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
        h2 { color: #202124; margin-top: 0; font-size: 20px; border-bottom: 2px solid #e8eaed; padding-bottom: 10px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; font-weight: 600; margin-bottom: 5px; color: #5f6368; }
        select, input { padding: 8px 12px; width: 100%; max-width: 300px; border: 1px solid #dadce0; border-radius: 6px; font-size: 14px; }
        button { background: #1a73e8; color: white; border: none; padding: 10px 20px; font-size: 14px; font-weight: 600; border-radius: 6px; cursor: pointer; margin-top: 10px; }
        button:hover { background: #1557b0; }
        .result-box { background: #e8f0fe; border-left: 4px solid #1a73e8; padding: 12px; margin-top: 15px; border-radius: 0 6px 6px 0; font-size: 15px; }
        table { border-collapse: collapse; margin-top: 15px; width: 100%; max-width: 500px; }
        th, td { border: 1px solid #e8eaed; padding: 10px; text-align: center; }
        th { background-color: #f8f9fa; color: #202124; }
        .grid { display: grid; grid-template-columns: repeat(5, 50px); gap: 4px; margin-top: 15px; }
        .cell { width: 50px; height: 50px; background: #f1f3f4; display: flex; align-items: center; justify-content: center; font-weight: bold; border-radius: 4px; font-size: 12px; color: #5f6368; }
        .robot { background: #1a73e8 !important; color: white !important; }
        .goal { background: #34a853 !important; color: white !important; }
        .path-text { font-family: monospace; background: #f8f9fa; padding: 10px; border-radius: 6px; margin-top: 10px; border: 1px solid #e8eaed; }
        .row-inputs { display: flex; gap: 15px; max-width: 400px; }
    </style>
</head>
<body>
    <h1>Reinforcement Learning Dashboard</h1>
    
    <div class="container">
        <!-- MODULE 1: Energy Consumption Optimization -->
        <div class="card">
            <h2>1. Energy Consumption Optimization (Q-Learning)</h2>
            <form method="POST">
                <input type="hidden" name="form_type" value="energy">
                <div class="form-group">
                    <label for="machine_load">Select Current Machine Load:</label>
                    <select name="machine_load" id="machine_load">
                        {% for s in states %}
                        <option value="{{ s }}" {% if selected_load == s %}selected{% endif %}>{{ s }} Load</option>
                        {% endfor %}
                    </select>
                </div>
                <button type="submit">Optimize Energy Action</button>
            </form>

            {% if energy_result %}
            <div class="result-box">
                <strong>Recommended Action:</strong> For <strong>{{ energy_result.state }}</strong> load, the optimal policy recommends to <strong>{{ energy_result.action }}</strong> power.
            </div>
            {% endif %}

            <h3>Trained Q-Table</h3>
            <table>
                <tr>
                    <th>Load / Action</th>
                    {% for action in actions %}
                    <th>{{ action }}</th>
                    {% endfor %}
                </tr>
                {% for i in range(states|length) %}
                <tr>
                    <td><strong>{{ states[i] }}</strong></td>
                    {% for j in range(actions|length) %}
                    <td>{{ q_table[i][j] }}</td>
                    {% endfor %}
                </tr>
                {% endfor %}
            </table>
        </div>

        <!-- MODULE 2: Robot Navigation -->
        <div class="card">
            <h2>2. Robot Navigation (Grid World)</h2>
            <form method="POST">
                <input type="hidden" name="form_type" value="robot">
                <div class="row-inputs">
                    <div class="form-group" style="flex:1;">
                        <label for="start_x">Start Row (0-4):</label>
                        <input type="number" name="start_x" id="start_x" min="0" max="4" value="{{ start_x }}">
                    </div>
                    <div class="form-group" style="flex:1;">
                        <label for="start_y">Start Col (0-4):</label>
                        <input type="number" name="start_y" id="start_y" min="0" max="4" value="{{ start_y }}">
                    </div>
                </div>
                <div class="row-inputs">
                    <div class="form-group" style="flex:1;">
                        <label for="goal_x">Goal Row (0-4):</label>
                        <input type="number" name="goal_x" id="goal_x" min="0" max="4" value="{{ goal_x }}">
                    </div>
                    <div class="form-group" style="flex:1;">
                        <label for="goal_y">Goal Col (0-4):</label>
                        <input type="number" name="goal_y" id="goal_y" min="0" max="4" value="{{ goal_y }}">
                    </div>
                </div>
                <button type="submit">Calculate Navigation Path</button>
            </form>

            <div class="path-text"><strong>Computed Path:</strong> {{ path }}</div>

            <h3>Grid World Simulation (5x5)</h3>
            <div class="grid">
                {% for i in range(grid_size) %}
                    {% for j in range(grid_size) %}
                        {% set current_coord = (i, j) %}
                        <div class="cell {% if current_coord == (goal_x, goal_y) %}goal{% elif current_coord == path[-1] %}robot{% endif %}">
                            ({{ i }},{{ j }})
                        </div>
                    {% endfor %}
                {% endfor %}
            </div>
            <p style="font-size: 13px; color: #5f6368; margin-top: 10px;">
                <span style="display:inline-block; width:12px; height:12px; background:#1a73e8; border-radius:2px; margin-right:4px;"></span> Robot Final Position &nbsp;&nbsp;
                <span style="display:inline-block; width:12px; height:12px; background:#34a853; border-radius:2px; margin-right:4px;"></span> Goal Position
            </p>
        </div>
    </div>
</body>
</html>
"""


def train_energy_ql():
  states = ["Low", "Medium", "High"]
  actions_energy = ["Reduce", "Maintain", "Increase"]
  Q_energy = np.zeros((len(states), len(actions_energy)))
  alpha, gamma, epsilon = 0.1, 0.9, 0.2
  rewards = np.array([[5, 2, -1], [3, 4, 0], [-2, 2, 5]])

  for _ in range(1000):
    state = random.randint(0, 2)
    action = (
        random.randint(0, 2)
        if random.uniform(0, 1) < epsilon
        else np.argmax(Q_energy[state])
    )
    reward = rewards[state][action]
    next_state = random.randint(0, 2)
    Q_energy[state][action] += alpha * (
        reward + gamma * np.max(Q_energy[next_state]) - Q_energy[state][action]
    )
  return Q_energy, states, actions_energy


def train_robot_ql(start, goal, grid_size=5):
  Q_robot = np.zeros((grid_size, grid_size, 4))
  actions_robot = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up
  alpha, gamma, epsilon = 0.1, 0.9, 0.2

  for _ in range(300):
    state = start
    while state != goal:
      action = (
          random.randint(0, 3)
          if random.uniform(0, 1) < epsilon
          else np.argmax(Q_robot[state[0], state[1]])
      )
      move = actions_robot[action]
      new_state = (
          max(0, min(grid_size - 1, state[0] + move[0])),
          max(0, min(grid_size - 1, state[1] + move[1])),
      )
      r = 100 if new_state == goal else -1
      Q_robot[state[0], state[1], action] += alpha * (
          r
          + gamma * np.max(Q_robot[new_state[0], new_state[1]])
          - Q_robot[state[0], state[1], action]
      )
      state = new_state

  # Evaluate/run path from start to goal
  path = [start]
  state = start
  steps = 0
  while state != goal and steps < 30:
    action = np.argmax(Q_robot[state[0], state[1]])
    move = actions_robot[action]
    state = (
        max(0, min(grid_size - 1, state[0] + move[0])),
        max(0, min(grid_size - 1, state[1] + move[1])),
    )
    path.append(state)
    steps += 1
  return path, grid_size


@app.route("/", methods=["GET", "POST"])
def index():
  Q_energy, states, actions_energy = train_energy_ql()
  q_table_rounded = Q_energy.round(2).tolist()

  # Default inputs
  selected_load = "Low"
  energy_result = None

  start_x, start_y = 0, 0
  goal_x, goal_y = 4, 4
  path, grid_size = train_robot_ql((start_x, start_y), (goal_x, goal_y))

  if request.method == "POST":
    form_type = request.form.get("form_type")

    if form_type == "energy":
      selected_load = request.form.get("machine_load", "Low")
      state_idx = states.index(selected_load)
      best_action_idx = np.argmax(Q_energy[state_idx])
      energy_result = {
          "state": selected_load,
          "action": actions_energy[best_action_idx],
      }

    elif form_type == "robot":
      try:
        start_x = int(request.form.get("start_x", 0))
        start_y = int(request.form.get("start_y", 0))
        goal_x = int(request.form.get("goal_x", 4))
        goal_y = int(request.form.get("goal_y", 4))
      except ValueError:
        start_x, start_y, goal_x, goal_y = 0, 0, 4, 4

      start = (max(0, min(4, start_x)), max(0, min(4, start_y)))
      goal = (max(0, min(4, goal_x)), max(0, min(4, goal_y)))
      path, grid_size = train_robot_ql(start, goal)

  if not energy_result:
    state_idx = states.index(selected_load)
    energy_result = {
        "state": selected_load,
        "action": actions_energy[np.argmax(Q_energy[state_idx])],
    }

  return render_template_string(
      HTML_TEMPLATE,
      states=states,
      actions=actions_energy,
      q_table=q_table_rounded,
      selected_load=selected_load,
      energy_result=energy_result,
      start_x=start_x,
      start_y=start_y,
      goal_x=goal_x,
      goal_y=goal_y,
      path=path,
      grid_size=grid_size,
  )


if __name__ == "__main__":
  app.run(debug=True)