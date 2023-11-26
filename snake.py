from tkinter import *
import random

# Game configuration constants
GAME_WIDTH = 1000
GAME_HEIGHT = 1000
SPEED = 100  # Game speed (lower is faster)
SPACE_SIZE = 40
BODY_PARTS = 3  # Initial number of snake body parts
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

# Snake class
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        # Initialize the snake's body coordinates
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        # Create the snake's body on the canvas
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

# Food class
class Food:
    def __init__(self):
        # Randomly place the food on the canvas
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

# Function to perform game actions in each frame
def next_turn(snake, food):
    x, y = snake.coordinates[0]

    # Move the snake in the current direction
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # Add the new head of the snake
    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    # Check if the snake has eaten the food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        # Remove the snake's tail (move the snake)
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Check for collisions with walls or self
    if check_collisions(snake):
        game_over()
    else:
        # Continue the game after a short delay
        window.after(SPEED, next_turn, snake, food)

# Function to change the direction of the snake
def change_direction(new_direction):
    global direction
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

# Function to check if the snake has collided with the game boundaries or itself
def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

# Function to end the game
def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")

# Set up the main window
window = Tk()
window.title("Snake game")
window.resizable(False, False)

# Initialize score and direction
score = 0
direction = 'down'

# Create a label to display the score
label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

# Create a canvas for the game
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Force window update to calculate sizes
window.update()

# Get window dimensions and screen dimensions
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate position for centering the window
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

# Set window geometry for centering
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Bind arrow keys to the change_direction function
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Create the snake and food objects
snake = Snake()
food = Food()

# Start the game loop
next_turn(snake, food)

# Start the Tkinter main loop
window.mainloop()

