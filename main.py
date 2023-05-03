"""Most Important imports
    - pygame is to load the game and its mechanics
    - random is necessary when generating random gapes between the pipes
    - sys is to fully close the window when the game is closed"""
import pygame
import random
import sys

"""
----------------- CONSTANTS -----------------
"""
# Window
WIDTH = 900
HEIGHT = 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))   # Let the window be a display of size 500x500

# Sizes
BIRD_WIDTH = 75
BIRD_HEIGHT = 60
PIPE_WIDTH = 20

# Photos
BACKGROUND = pygame.transform.scale(pygame.image.load("Sources/background.png"), (WIDTH, HEIGHT))
BIRD_IMAGE = pygame.transform.scale(pygame.image.load("Sources/bird.png"), (BIRD_WIDTH, BIRD_HEIGHT))
PIPE_IMAGE = pygame.image.load("Sources/pipe.png")



"""
----------------- FUNCTIONS -----------------
"""


# Functions to draw
def draw_bird(x, y):
    pygame.draw.rect(WINDOW, "black", pygame.Rect(50, 50, BIRD_WIDTH, BIRD_HEIGHT))

    WINDOW.blit(BIRD_IMAGE, (50, 50))


def draw_pipes():
    pass


def main_draw():
    # Draw the background on the window
    WINDOW.blit(BACKGROUND, (0, 0))

    # Draw the bird & pipes
    draw_bird()
    draw_pipes()

    # UPDATE THE DISPLAY
    pygame.display.update()


# Main Function
def main():
    # Initializing the setup
    pygame.init()
    pygame.display.set_caption("Flappy Bird")

    # Start with running true to make sure the game runs in the beginning (Loop starts)
    running = True
    # Start the game as the bird is not hit
    hit = False

    while running:
        # Check for all the events in the game first
        for event in pygame.event.get():
            # If the window is closed then close the game
            if event.type == pygame.QUIT:
                running = False
                break

        # After handling all the events draw the objects
        main_draw()


# Make sure this code is being executed from the main
if __name__ == "__main__":
    main()

