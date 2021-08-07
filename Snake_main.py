import random
import pygame as py
from pygame import Vector2

# Initialising pygame
py.init()

class Fruit:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = py.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)
        #py.draw.rect(screen, (126, 166, 114), fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

        # Initialising the snake graphics
        self.head_up = py.image.load('head_up.png').convert_alpha()
        self.head_down = py.image.load('head_down.png').convert_alpha()
        self.head_left = py.image.load('head_left.png').convert_alpha()
        self.head_right = py.image.load('head_right.png').convert_alpha()

        self.tail_up = py.image.load('tail_up.png').convert_alpha()
        self.tail_down = py.image.load('tail_down.png').convert_alpha()
        self.tail_left = py.image.load('tail_left.png').convert_alpha()
        self.tail_right = py.image.load('tail_right.png').convert_alpha()

        self.body_vertical = py.image.load('body_vertical.png').convert_alpha()
        self.body_horizontal = py.image.load('body_horizontal.png').convert_alpha()

        self.body_tr = py.image.load('body_tr.png').convert_alpha()
        self.body_tl = py.image.load('body_tl.png').convert_alpha()
        self.body_br = py.image.load('body_br.png').convert_alpha()
        self.body_bl = py.image.load('body_bl.png').convert_alpha()

        # Initialising the snake crunch sound
        self.crunch_sound = py.mixer.Sound('Sound_crunch.wav')

    def draw_snake(self):

        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            snake_rect = py.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, snake_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, snake_rect)
            else:
                prev_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block

                if prev_block.x == next_block.x:
                    screen.blit(self.body_vertical, snake_rect)
                elif prev_block.y == next_block.y:
                    screen.blit(self.body_horizontal, snake_rect)
                else:
                    if prev_block.x == -1 and next_block.y == -1 or prev_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, snake_rect)
                    elif prev_block.x == -1 and next_block.y == 1 or prev_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, snake_rect)
                    elif prev_block.x == 1 and next_block.y == -1 or prev_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, snake_rect)
                    elif prev_block.x == 1 and next_block.y == 1 or prev_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, snake_rect)

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]

        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]

        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[: -1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]

class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        # Drawing grass
        self.draw_grass()

        # Drawing the Fruit
        self.fruit.draw_fruit()

        # Drawing the Snake
        self.snake.draw_snake()

        # Drawing the score
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x <= cell_number:
            self.game_over()
        elif not 0 <= self.snake.body[0].y <= cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = py.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                        py.draw.rect(screen, grass_color, grass_rect)

            if row % 2 != 0:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = py.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                        py.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score = str(len(self.snake.body) - 3)
        score_text = score_font.render(("The score is: " + score), True, (56, 74, 12))
        screen.blit(score_text, (0, 0))

cell_size = 40
cell_number = 20

# Initializing the screen.
screen = py.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = py.time.Clock()
apple = py.image.load('apple_1.png').convert_alpha()

# Initialising game font
score_font = py.font.Font('PoetsenOne-Regular.ttf', 25)

# Initialising background music
py.mixer.music.load('XPT5HRY-video-game.mp3')
py.mixer.music.play(-1)

# Run variable
running = True

# Initialising fruit
fruit = Fruit()

# Initialising Snake
snake = Snake()

# Moving the snake
SCREEN_UPDATE = py.USEREVENT
py.time.set_timer(SCREEN_UPDATE, 150)

# Initialising the main_game
main_game = Main()

# Main game loop
while running:

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == py.KEYDOWN:
            if event.key == py.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == py.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == py.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == py.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)

    screen.fill((175, 215, 70))

    main_game.draw_elements()
    py.display.update()

    # Controlling the Frame rate of the game.
    clock.tick(60)
