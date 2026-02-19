import numpy as np
import tkinter as tk
import time

CELL_SIZE = 60

# -------------------------------
# Step 1: Create the Maze
# -------------------------------
maze = np.array([
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
    [1, 1, 0, 1, 0, 1, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 1, 1],
    [0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
    [1, 1, 0, 1, 0, 1, 1, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 0, 0, 0, 1, 1, 1, 0]
])

start = (0, 0)
goal = (9, 9)

# -------------------------------
# Step 2: Define Parameters
# -------------------------------
actions = ['up', 'down', 'left', 'right']

# -------------------------------
# Step 3: Helper Functions
# -------------------------------
def is_valid(state):
    x, y = state
    if x < 0 or y < 0 or x >= maze.shape[0] or y >= maze.shape[1]:
        return False
    if maze[x][y] == 1:
        return False
    return True

def get_next_state(state, action):
    x, y = state
    if action == 'up':
        return (x - 1, y)
    if action == 'down':
        return (x + 1, y)
    if action == 'left':
        return (x, y - 1)
    if action == 'right':
        return (x, y + 1)

# -------------------------------
# Step 4: Create GUI Window
# -------------------------------
window = tk.Tk()
window.title("Autonomous Game Agent - Maze Solver")

canvas = tk.Canvas(
    window,
    width=maze.shape[1] * CELL_SIZE,
    height=maze.shape[0] * CELL_SIZE
)
canvas.pack()

# -------------------------------
# Draw Maze
# -------------------------------
def draw_maze():
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            x1 = j * CELL_SIZE
            y1 = i * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE

            if maze[i][j] == 1:
                color = "black"
            else:
                color = "white"

            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    # Start
    canvas.create_rectangle(
        start[1]*CELL_SIZE,
        start[0]*CELL_SIZE,
        start[1]*CELL_SIZE+CELL_SIZE,
        start[0]*CELL_SIZE+CELL_SIZE,
        fill="blue"
    )

    # Goal
    canvas.create_rectangle(
        goal[1]*CELL_SIZE,
        goal[0]*CELL_SIZE,
        goal[1]*CELL_SIZE+CELL_SIZE,
        goal[0]*CELL_SIZE+CELL_SIZE,
        fill="green"
    )

# -------------------------------
# Update points and feedback
# -------------------------------
score = 0
feedback_text = ""

def update_score(is_correct):
    global score, feedback_text
    if is_correct:
        score += 10
        feedback_text = "Correct Move!"
    else:
        score -= 5
        feedback_text = "Wrong Move!"
    score_label.config(text=f"Score: {score}")
    feedback_label.config(text=feedback_text)

# -------------------------------
# Move Agent based on button clicks
# -------------------------------
user_position = list(start)

def move_agent(action):
    global user_position

    # Get next state based on action
    next_state = get_next_state(tuple(user_position), action)

    if is_valid(next_state):
        user_position = list(next_state)

        # Check if move reaches goal
        if tuple(user_position) == goal:
            update_score(True)
            feedback_label.config(text="You've Reached the Goal!")
        else:
            update_score(True)
    else:
        update_score(False)

    draw_maze()

    # Draw the agent as a human symbol (e.g., a circle)
    canvas.create_oval(
        user_position[1]*CELL_SIZE+10,
        user_position[0]*CELL_SIZE+10,
        user_position[1]*CELL_SIZE+CELL_SIZE-10,
        user_position[0]*CELL_SIZE+CELL_SIZE-10,
        fill="red",
        tags="agent"
    )

# -------------------------------
# Display user input and move
# -------------------------------
# Buttons for user interaction
button_frame = tk.Frame(window)
button_frame.pack(pady=10)

up_button = tk.Button(button_frame, text="Up", command=lambda: move_agent('up'))
up_button.grid(row=0, column=1)

down_button = tk.Button(button_frame, text="Down", command=lambda: move_agent('down'))
down_button.grid(row=2, column=1)

left_button = tk.Button(button_frame, text="Left", command=lambda: move_agent('left'))
left_button.grid(row=1, column=0)

right_button = tk.Button(button_frame, text="Right", command=lambda: move_agent('right'))
right_button.grid(row=1, column=2)

# Score and feedback labels
score_label = tk.Label(window, text="Score: 0")
score_label.pack(pady=5)

feedback_label = tk.Label(window, text="")
feedback_label.pack(pady=5)

# Initial drawing of the maze
draw_maze()

window.mainloop()