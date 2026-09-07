import pygame
import time
import random

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (213, 50, 80)

# Display setup
WIDTH = 600
HEIGHT = 400
display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

# Game constants
SNAKE_BLOCK_SIZE = 10
SNAKE_SPEED = 15
FONT_STYLE = pygame.font.SysFont("bahniScript", 25)
SCORE_FONT = pygame.font.SysFont("consola", 25)

# Snake and food coordinates
snake_list = []
snake_length = 3
food_x = round(random.randrange(0, WIDTH)/SNAKE_BLOCK_SIZE)*SNAKE_BLOCK_SIZE
food_y = round(random.randrange(0, HEIGHT)/SNAKE_BLOCK_SIZE)*SNAKE_BLOCK_SIZE

# Directions (dx, dy)
game_dx = 1
game_dy = 0
score = 0

def game_snake(snake_block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(display_surface, GREEN, [x[0], x[1], snake_block_size, snake_block_size])

def your_score(score_value):
    value = SCORE_FONT.render("Your Score: " + str(score_value), True, WHITE)
    display_surface.blit(value, [0, 0])

def your_message(msg, y_offset=WIDTH-35):
    message = FONT_STYLE.render(msg, True, RED)
    display_surface.blit(message, [WIDTH/2 - 60, y_offset])

# Game loop
game_over = False
clock_start_time = time.time()

while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        
        if event.type == pygame.KEYDOWN:
            # Restart after game over
            if game_over:
                snake_list.clear()
                score = 0
                game_dx = 1
                game_dy = 0
                
                food_x = round(random.randrange(0, WIDTH)/SNAKE_BLOCK_SIZE)*SNAKE_BLOCK_SIZE
                food_y = round(random.randrange(0, HEIGHT)/SNAKE_BLOCK_SIZE)*SNAKE_BLOCK_SIZE
            # Direction controls (prevent reversing)
            elif event.key == pygame.K_LEFT and game_dx != 1:
                game_dx = -1
                game_dy = 0
            elif event.key == pygame.K_UP and game_dy != 1:
                game_dx = 0
                game_dy = -1
            elif event.key == pygame.K_RIGHT and game_dx != -1:
                game_dx = 1
                game_dy = 0
            elif event.key == pygame.K_DOWN and game_dy != -1:
                game_dx = 0
                game_dy = 1
    
    # Display background
    display_surface.fill(BLACK)
    
    # Draw snake
    for x in snake_list:
        game_snake(SNAKE_BLOCK_SIZE, [x])
    
    # Draw food
    pygame.draw.rect(display_surface, RED, [food_x, food_y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])
    
    your_score(score)

    # Move the snake
    if time.time() - clock_start_time >= (1000/SNAKE_SPEED):
        head_x = int(snake_list[0][0] + game_dx * SNAKE_BLOCK_SIZE)
        head_y = int(snake_list[0][1] + game_dy * SNAKE_BLOCK_SIZE)
        
        # Check wall collision
        if (head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT):
            your_message("Game Over! Press ENTER to Restart")
            time.sleep(3)
            game_over = True
        
        # Check self collision
        for x in snake_list:
            if head_x == int(x[0]) and head_y == int(x[1]):
                your_message("Game Over! Press ENTER to Restart")
                time.sleep(3)
                game_over = True
        
        # Head becomes new part of the snake list
        snake_list.insert(0, [head_x, head_y])

        # Check if food consumed
        if head_x == int(food_x) and head_y == int(food_y):
            score += 1
            food_x = round(random.randrange(0, WIDTH)/SNAKE_BLOCK_SIZE)*SNAKE_BLOCK_SIZE
            food_y = round(random.randrange(0, HEIGHT)/SNAKE_BLOCK_SIZE)*SNAKE_BLOCK_SIZE
        
        # Remove the tail to maintain snake length (except when eating)
        else:
            snake_list.pop()
        
        clock_start_time = time.time()

    # Update display
    pygame.display.flip()

# Final exit message
pygame.quit()
print("Game finished.")
