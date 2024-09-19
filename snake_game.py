from tkinter import *
import random
import pygame

# basic
GAME_WIDTH = 800
GAME_HEIGHT = 800
SPEED = 65

# player
SPACE_SIZE = 50
BODY_PARTS = 3

# colour
SNAKE_COLOR = "#DEB9E4"
FOOD_COLOR = "#C4B4D4"
BG_COLOR = "#473574"


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake"
            )
            self.squares.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food"
        )

pygame.mixer.init()

# sound effects
bg_sound = pygame.mixer.Sound("space_adventure.mp3")
eat_sound = pygame.mixer.Sound("eat.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")

# bg music
bg_sound.play(loops=-1)

def next_turn():
    global food  # declare food as global

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])

    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR
    )
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text=f"Score: {score}")
        canvas.delete("food")
        food = Food()
        eat_sound.play() 
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions():
        game_over()
    else:
        window.after(SPEED, next_turn)


def switch_direction(new_direction):
    global direction

    if new_direction == "left":
        if direction != "right":
            direction = new_direction
    elif new_direction == "right":
        if direction != "left":
            direction = new_direction
    elif new_direction == "up":
        if direction != "down":
            direction = new_direction
    elif new_direction == "down":
        if direction != "up":
            direction = new_direction


def check_collisions():
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2,
        font=("consolas", 70),
        text="GAME OVER",
        fill="red",
        tag="gameover",
    )
    game_over_sound.play()


def restart_game(event):
    global score, direction, snake, food

    score = 0
    direction = "down"
    label.config(text=f"Score: {score}")

    # Clear the canvas
    canvas.delete(ALL)

    # reanimate the snake and food
    snake = Snake()
    food = Food()

    # game loop
    next_turn()

# main ()
def main(): 
    global canvas, label, snake, food, direction, score, bg_sound, eat_sound, game_over_sound

window = Tk()
window.title("Classic Snake Game")
window.resizable(False, False)

score = 0
direction = "down"

label = Label(window, text=f"Score: {score}", font=("consolas", 34))
label.pack()

canvas = Canvas(window, bg=BG_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

snake = Snake()
food = Food()

# bind the space bar key to the restart function
window.bind("<space>", restart_game)

# control
window.bind("<Left>", lambda event: switch_direction("left"))
window.bind("<Right>", lambda event: switch_direction("right"))
window.bind("<Up>", lambda event: switch_direction("up"))
window.bind("<Down>", lambda event: switch_direction("down"))

next_turn()

window.mainloop()


if __name__ == "__main__":
    main()