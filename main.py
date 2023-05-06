"""Most Important imports
    - pygame is to load the game and its mechanics
    - random is necessary when generating random gapes between the pipes
    - sys is to fully close the window when the game is closed"""

import pygame
import random
import sys


pygame.init()
"""
----------------- CONSTANTS -----------------
"""
# Window
WIDTH = 600
HEIGHT = 750
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))   # Let the window be a display of size 500x500

# Sizes
BIRD_WIDTH = 80
BIRD_HEIGHT = 56
PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP = 175
GROUND_HEIGHT = 100

# Photos
BACKGROUND = pygame.transform.scale(pygame.image.load("Sources/BG/background_1.png"),  (900, HEIGHT))
GROUND = pygame.transform.scale(pygame.image.load("Sources/ground.png"), (WIDTH, GROUND_HEIGHT))
BIRD_IMAGE = pygame.transform.scale(pygame.image.load("Sources/BIRD/bird_1.png"), (BIRD_WIDTH, BIRD_HEIGHT))
PIPE_UPWARD = pygame.transform.scale(pygame.image.load("Sources/Pipe/pipe_1.png"), (PIPE_WIDTH, PIPE_HEIGHT))
PIPE_DOWNWARD = pygame.transform.flip(PIPE_UPWARD, True, True)

# Positions
BIRD_X = 50
BIRD_Y = 50
PIPE_X = 450
PIPE_Y = 500
TOLERANCE = 100
x_distance = 0

# Speed
BIRD_VELOCITY = 0
TERMINAL_SPEED = 10
ATTRACTION_OF_GRAVITY = 0.4
JUMP_SPEED = -7
PIPE_SPEED = 4

# Score
SCORE = 0
pygame.font.init()
FONT = pygame.font.SysFont("Bree Serif", 100, True)
FONT_1 = pygame.font.SysFont("Bree Serif", 75, True)
BLACK_MARGIN = 10

# Sounds
JUMP_SOUND = pygame.mixer.Sound("Sources/jump.wav")
HIT_SOUND = pygame.mixer.Sound("Sources/hit.wav")
SCORE_SOUND = pygame.mixer.Sound("Sources/score.wav")
BG_MUSIC = pygame.mixer.Sound("Sources/background_music.mp3")


"""
----------------- FUNCTIONS -----------------
"""


# Functions to draw
def draw_bird(x, y):
    WINDOW.blit(BIRD_IMAGE, (x, y))


def draw_pipes(pipes):
    for pipe in pipes:
        # Draw the first pipe (on the ground)
        WINDOW.blit(PIPE_UPWARD, (pipe[0], pipe[1]))
        # Draw the second pipe (from the sky)
        WINDOW.blit(PIPE_DOWNWARD, (pipe[0], pipe[1]-PIPE_HEIGHT-PIPE_GAP))


def main_draw(bird_x, bird_y, pipes):
    # Draw the background on the window
    WINDOW.blit(BACKGROUND, (0, 0))

    # Draw the bird & pipes
    draw_bird(bird_x, bird_y)
    draw_pipes(pipes)

    # Draw the Ground
    WINDOW.blit(GROUND, (0, HEIGHT - GROUND_HEIGHT))

    # Draw the Score
    score_text = FONT.render(f"{SCORE}", True, "black")
    WINDOW.blit(score_text, (10, 10))

    HS = check_high_score(SCORE)
    HS_text = FONT_1.render(f"{HS}", True, "black")
    WINDOW.blit(HS_text, (10, 10+score_text.get_height()))

    # UPDATE THE DISPLAY
    pygame.display.update()


# Handling movement function
def move_pipes(pipes):
    global SCORE
    for pipe in pipes:
        pipe[0] -= PIPE_SPEED
        if pipe[0]+PIPE_WIDTH < 0:
            pipes.remove(pipe)
        if pipe[0] == BIRD_X:
            SCORE += 1
            pygame.mixer.Sound.play(SCORE_SOUND)

            pygame.mixer.music.stop()


def check_collision(pipes):
    gap_start_y = pipes[0][1]
    gap_end_y = gap_start_y - PIPE_GAP
    gap_start_x = pipes[0][0]
    gap_end_x = gap_start_x + PIPE_WIDTH
    if gap_start_x < BIRD_X+BIRD_WIDTH and gap_end_x > BIRD_X:
        if not(gap_end_y-15 < BIRD_Y and BIRD_Y+BIRD_HEIGHT < gap_start_y+15):
            pygame.mixer.Sound.play(HIT_SOUND)
            pygame.mixer.music.stop()
            return True
    if BIRD_Y+BIRD_HEIGHT >= HEIGHT-GROUND_HEIGHT:
        pygame.mixer.Sound.play(HIT_SOUND)
        pygame.mixer.music.stop()
        return True


# Method for displaying the lost message
def lost():
    # Set the loosing text message
    lost_text = FONT.render("YOU LOST!", True, "white")

    # Set the position & dimensions
    x = WIDTH / 2 - lost_text.get_width() / 2-BLACK_MARGIN
    y = HEIGHT / 2 - lost_text.get_height() / 2-BLACK_MARGIN
    width = lost_text.get_width()+BLACK_MARGIN*2
    height = lost_text.get_height()+BLACK_MARGIN*2

    # Set the black rectangle behind the text message
    black_rect = pygame.Rect(x, y, width, height)

    # Draw the rectangle & text
    pygame.draw.rect(WINDOW, "black", black_rect, 0, 10)
    WINDOW.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(1000)


# Checks if the current score is higher than the high score
def check_high_score(score):
    file_r = open("HighScore.txt", "r")
    high_score = int(file_r.read())
    file_r.close()
    if score > high_score:
        file_w = open("HighScore.txt", "w")
        file_w.write(str(score))
        file_w.close()
    return high_score


# Main Function
def main():
    while True:
        # Get the global variables
        global BIRD_X, BIRD_Y, x_distance, BIRD_VELOCITY, PIPE_X, PIPE_Y, SCORE
        BIRD_X = 50
        BIRD_Y = 50
        SCORE = 0

        # Initializing the setup
        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        starting = False
        check_high_score(SCORE)

        # Get the clock to set game speed
        clock = pygame.time.Clock()

        # Making a list of pipes
        pipes = [[450, 500]]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pygame.mixer.Sound.play(JUMP_SOUND)
                pygame.mixer.music.stop()
                starting = True

        if starting:

            while True:
                # Check for all the events in the game first
                for event in pygame.event.get():
                    # If the window is closed then close the game
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        BIRD_VELOCITY = JUMP_SPEED
                        BIRD_Y += BIRD_VELOCITY
                        pygame.mixer.Sound.play(JUMP_SOUND)
                        pygame.mixer.music.stop()

                # Make sure the bird is between the boundaries
                if BIRD_Y+BIRD_HEIGHT < HEIGHT-GROUND_HEIGHT:
                    # This if statement simulates the terminal velocity of the bird (can't go faster than 5.5)
                    if BIRD_VELOCITY < TERMINAL_SPEED:
                        # This addition makes a similar effect to gravity
                        BIRD_VELOCITY += ATTRACTION_OF_GRAVITY
                    BIRD_Y += BIRD_VELOCITY
                    # print(BIRD_VELOCITY)

                while len(pipes) < 5:
                    gap_height = random.randint(PIPE_GAP+TOLERANCE, HEIGHT-GROUND_HEIGHT-TOLERANCE)
                    for pipe in pipes:
                        x_distance = pipe[0] + 300
                    pipes.append([x_distance, gap_height])

                # After handling all the events draw the objects
                main_draw(BIRD_X, BIRD_Y, pipes)
                hit = check_collision(pipes)
                # hit = False
                move_pipes(pipes)

                if hit:
                    lost()
                    check_high_score(SCORE)
                    break

                # Control Game Speed
                clock.tick(60)


# Make sure this code is being executed from the main
if __name__ == "__main__":
    main()
