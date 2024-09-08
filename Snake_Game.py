from tkinter import *
import random

GAME_WIDTH = 700
GAME_HEIGHT = 500
SPEED = 50
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = "#0fc717"
FOOD_COLOR = "#ff0000"
BACKGROUND_COLOR = "#000000"


score = 0
direction = 'down'
game_running = False
main_window = None 
game_instance_window = None 

def easy():
    global GAME_HEIGHT, GAME_WIDTH, SPEED, SPACE_SIZE
    GAME_WIDTH = 1000
    GAME_HEIGHT = 700
    SPEED = 100
    SPACE_SIZE = 20  
    start_game()

def medium():
    global GAME_HEIGHT, GAME_WIDTH, SPEED, SPACE_SIZE
    GAME_WIDTH = 700
    GAME_HEIGHT = 700
    SPEED = 50
    SPACE_SIZE = 25 
    start_game()

def hard():
    global GAME_HEIGHT, GAME_WIDTH, SPEED, SPACE_SIZE
    GAME_WIDTH = 500
    GAME_HEIGHT = 500
    SPEED = 50
    SPACE_SIZE = 30 
    start_game()

def start_game():
    global game_instance_window, canvas, label, snake, food, score, direction, game_running

    score = 0
    direction = 'down'

    if game_instance_window is not None:
        game_instance_window.destroy()
    
    game_instance_window = Toplevel()
    game_instance_window.title("Snake Game")
    game_instance_window.resizable(False, False)

    label = Label(game_instance_window, text="Score:{}".format(score), font=("consolas", 40))
    label.pack()

    canvas = Canvas(game_instance_window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
    canvas.pack()

    update_game_window() 

    game_instance_window.bind('<Left>', lambda event: change_direction('left'))
    game_instance_window.bind('<Right>', lambda event: change_direction('right'))
    game_instance_window.bind('<Up>', lambda event: change_direction('up'))
    game_instance_window.bind('<Down>', lambda event: change_direction('down'))
    
    game_instance_window.focus_set()

    snake = Snake()
    food = Food()

    next_turn(snake, food)  

def update_game_window():
    global game_instance_window

    canvas.config(width=GAME_WIDTH, height=GAME_HEIGHT)

    window_width = GAME_WIDTH
    window_height = GAME_HEIGHT
    screen_width = game_instance_window.winfo_screenwidth()
    screen_height = game_instance_window.winfo_screenheight()

    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    game_instance_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    game_instance_window.update()

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        
        for i in range(BODY_PARTS):
            self.coordinates.append([0, 0])
         
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        self.randomize_position()
    
    def randomize_position(self):
        while True:
            x = random.randint(0, (GAME_WIDTH - SPACE_SIZE) // SPACE_SIZE) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT - SPACE_SIZE) // SPACE_SIZE) * SPACE_SIZE
            if not any([x == part[0] and y == part[1] for part in snake.coordinates]):
                break
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    global direction
    
    x, y = snake.coordinates[0]
    
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
        
    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)
    
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food() 
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collision(snake):
        game_over()
    else:
        game_instance_window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    if (new_direction == 'left') and (direction != 'right'):
        direction = new_direction
    elif (new_direction == 'right') and (direction != 'left'):
        direction = new_direction
    elif (new_direction == 'up') and (direction != 'down'):
        direction = new_direction
    elif (new_direction == 'down') and (direction != 'up'):
        direction = new_direction

def check_collision(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def game_over():
    global game_running

    canvas.delete(ALL)
    
    canvas.create_text(canvas.winfo_width() / 2,
                       canvas.winfo_height() / 2,
                       font=("consolas", 70),
                       text="GAME OVER",
                       fill="red", tag="gameover")
    
    game_running = False
    game_instance_window.after(1000, close_game_window)

def close_game_window():
    global game_instance_window
    if game_instance_window:
        game_instance_window.destroy()
        game_instance_window = None

def create_main_window():
    global main_window
    main_window = Tk()
    main_window.title("Snake Game")
    main_window.resizable(False, False)

    label1 = Label(main_window, text="Select Difficulty", font=("consolas", 25))
    label1.pack()

    button1 = Button(main_window, text="EASY", command=easy, font=("consolas", 25), bg="#000000", fg="red", width=20)
    button1.pack()
    button2 = Button(main_window, text="MEDIUM", command=medium, font=("consolas", 25), bg="#000000", fg="red", width=20)
    button2.pack()
    button3 = Button(main_window, text="HARD", command=hard, font=("consolas", 25), bg="#000000", fg="red", width=20)
    button3.pack()

    main_window.mainloop()

create_main_window()
