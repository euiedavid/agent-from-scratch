"""
Snake Game Functions Module
Contains game logic, drawing functions, and event handling.
"""

# Import pygame
import pygame

# Import constants from the main module
from .. import Constants

def game_snake(snake_block_size, snake_list):
    """Draw the snake on the screen."""
    for x in snake_list:
        pygame.draw.rect(display_surface, GREEN, [x[0], x[1], snake_block_size, snake_block_size])


def your_score(score_value):
    """Display current score at the top left corner."""
    value = Constants.SCORE_FONT.render("Your Score: " + str(score_value), True, WHITE)
    display_surface.blit(value, [0, 0])


def your_message(msg, y_offset=Constants.SCREEN_WIDTH-35):
    """Display a message centered at the bottom of the screen."""
    message = Constants.FONT_STYLE.render(msg, True, RED)
    display_surface.blit(message, [Constants.SCREEN_WIDTH/2 - 60, y_offset])


# Initialize pygame once for module-level setup
pygame.init()
