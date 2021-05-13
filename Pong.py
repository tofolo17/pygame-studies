import os
from random import choice, randint

import pygame

# Cores
black = (0, 0, 0)
white = (255, 255, 255)

# Initializing and centering
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

# Global variables
factor = []
width = 1000
height = 500
start = False
imprecision = 1
points_r = points_l = 0
clock = pygame.time.Clock()
pygame.display.set_caption('A really bad Pong')
screen = pygame.display.set_mode((width, height))
for x in range(1, 10):
    factor.append(randint(1, 10))


# Functions
def screen_text(text, x_coord, y_coord, color, size, r=False):
    msg = pygame.font.SysFont('verdana', size - 10).render(str(text), True, color)
    screen.blit(msg, msg.get_rect(center=(int(x_coord), int(y_coord))))
    if r:
        return msg.get_rect(center=(x_coord, y_coord))


def back_to():
    get_back = screen_text('Back', 40, 20, white, 30, True)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if get_back.collidepoint(event.pos):
                    game_intro()


# Main Menu
def game_intro():
    # Temporary variables
    global points_l, points_r, start, imprecision
    intro = True
    start = False
    imprecision = 1
    points_r = points_l = 0
    screen.fill(white)
    screen_text('A really bad Pong', 300, 200, black, 30)
    bt1 = screen_text('single player', 400, 300, black, 25, True)
    bt2 = screen_text('multi player', 400, 330, black, 25, True)

    # Analysing events
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if bt1.collidepoint(event.pos):
                        intro = False
                        mode = 0
                        game_loop(mode)
                    elif bt2.collidepoint(event.pos):
                        intro = False
                        mode = 1
                        game_loop(mode)
        pygame.display.update()


# Game loop
def game_loop(game_mode):
    side = choice([-1, 1])
    pos_x_ball = int(width / 2)
    pos_y_ball = int(height / 2)
    pos_y_foot1 = pos_y_foot2 = 200
    speed_y_ball = speed_x_ball = 7
    game_over = game_pause = game_finish = False
    global points_l, points_r, start, imprecision

    while not game_over:

        # Point screen
        while game_pause:
            screen_text('SPACE to continue.', width / 2, height / 2, white, 30)
            pygame.display.update()

            # Checking permanence
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_loop(game_mode)
            back_to()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Victory screen
        while game_finish:
            screen_text(
                'The player on the right won.' if points_r == 5 else 'The player on the left won.',
                width / 2,
                height / 2,
                white, 30
            )
            screen_text('SPACE to continue or B to main menu.', width / 2, height - 200, white, 30)
            pygame.display.update()

            # Checking permanence
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        points_r = points_l = 0
                        game_loop(game_mode)
                    if event.key == pygame.K_b:
                        game_intro()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Moving pads
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_UP]:
            pos_y_foot1 += -9
        if pressed_keys[pygame.K_DOWN]:
            pos_y_foot1 += 9
        # Multiplayer
        if game_mode == 1:
            if pressed_keys[pygame.K_w]:
                pos_y_foot2 += -9
            if pressed_keys[pygame.K_s]:
                pos_y_foot2 += 9

        # Starting the game
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            start = True

        # Single player
        if game_mode == 0:
            # Bot imprecision
            dist = pos_y_ball - pos_y_foot2 - 50
            pos_y_foot2 += (dist / imprecision)

        # Pad position delimiter
        if pos_y_foot1 < 0:
            pos_y_foot1 = 0
        if pos_y_foot1 > height - 100:
            pos_y_foot1 = height - 100
        if pos_y_foot2 < 0:
            pos_y_foot2 = 0
        if pos_y_foot2 > height - 100:
            pos_y_foot2 = height - 100

        # Graphics
        bounds = pygame.Rect(0, 0, 1000, 500)
        foot2 = pygame.Rect(30, int(pos_y_foot2), 15, 100)
        foot1 = pygame.Rect(width - 45, int(pos_y_foot1), 15, 100)
        right_side2 = pygame.draw.line(screen, white, (45, int(pos_y_foot2)), (45, int(pos_y_foot2) + 15), 1)
        left_side2 = pygame.draw.line(screen, white, (45, int(pos_y_foot2) + 75), (45, int(pos_y_foot2) + 100), 1)
        right_side = pygame.draw.line(screen, white, (width - 45, pos_y_foot1), (width - 45, pos_y_foot1 + 15), 1)
        left_side = pygame.draw.line(screen, white, (width - 45, pos_y_foot1 + 80), (width - 45, pos_y_foot1 + 100), 1)

        # It finally starts
        if start:
            pos_x_ball += -speed_x_ball * side
            pos_y_ball += -speed_y_ball

        # Filling screen
        screen.fill(black)
        pygame.draw.rect(screen, black, bounds, 1)
        ball = pygame.draw.circle(screen, white, (int(pos_x_ball), int(pos_y_ball)), 10, 0)

        # Direction, speed and randomness
        if pos_y_ball + 10 > bounds.bottom or pos_y_ball - 10 < bounds.top:
            speed_y_ball = -speed_y_ball
        if ball.colliderect(foot1):
            if side == -1:
                speed_x_ball = -speed_x_ball - 0.5
            else:
                speed_x_ball = -speed_x_ball + 0.5
            imprecision = choice(factor)
        if ball.colliderect(foot2):
            if side == -1:
                speed_x_ball = - speed_x_ball + 0.5
            else:
                speed_x_ball = - speed_x_ball - 0.5
            imprecision = choice(factor)
        if ball.colliderect(right_side) or ball.colliderect(left_side) \
                or ball.colliderect(right_side2) or ball.colliderect(left_side2):
            speed_y_ball = -speed_y_ball

        # Verifying points
        if pos_x_ball + 10 > bounds.right:
            points_l += 1
            if points_l == 5:
                game_finish = True
            else:
                game_pause = True
        if pos_x_ball - 10 < bounds.left:
            points_r += 1
            if points_r == 5:
                game_finish = True
            else:
                game_pause = True

        # Sprites and FPS
        pygame.draw.line(screen, white, (int(width / 2), 0), (int(width / 2), height), 1)
        pygame.draw.rect(screen, white, foot1, 1)
        pygame.draw.rect(screen, white, foot2, 1)
        screen_text(points_l, width / 2 - 20, 20, white, 30)
        screen_text(points_r, width / 2 + 20, 20, white, 30)
        back_to()
        clock.tick(60)
        pygame.display.update()


game_intro()
