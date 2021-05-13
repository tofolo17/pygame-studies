from random import randint

import pygame

# Initializing pygame
pygame.init()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Global variables
width = height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()


# Functions
def score(snake_blocks):
    points = pygame.font.SysFont("Times New Roman", 15).render(str(snake_blocks), True, white)
    screen.blit(points, [int(10), int(10)])


def on_grid_random():
    x = randint(10, 390)
    return x // 10 * 10


def snake_builder(xy_snake, h=0):
    for xy in xy_snake:
        pygame.draw.rect(screen, white, [xy[0], xy[1], 10, 10])
    if h:
        return pygame.draw.rect(screen, white, [xy_snake[-1][0], xy_snake[-1][1], 10, 10])


def message(txt, cor):
    msg = pygame.font.SysFont("", 20).render(txt, True, cor)
    screen.blit(msg, [int(100), int(100)])


# Game loop
def replay():
    # Loop variables
    game_over = False
    game_close = False
    snake_len = 1
    speed_cont = 10
    snake_list = list()
    speed_x = speed_y = 0
    pos_x = on_grid_random()
    pos_y = on_grid_random()
    pos_x_apple = on_grid_random()
    pos_y_apple = on_grid_random()

    while not game_over:
        while game_close:

            # Final score
            screen.fill(black)
            message(f"{len(snake_list)} points! P - Play again / E - Exit", red)
            pygame.display.update()

            # Checking permanence
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_p:
                        replay()

        # Detecting events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                # Commands
                if event.key == pygame.K_UP and speed_y != 10:
                    speed_x = 0
                    speed_y = -10
                elif event.key == pygame.K_DOWN and speed_y != -10:
                    speed_x = 0
                    speed_y = 10
                elif event.key == pygame.K_LEFT and speed_x != 10:
                    speed_x = -10
                    speed_y = 0
                elif event.key == pygame.K_RIGHT and speed_x != -10:
                    speed_x = 10
                    speed_y = 0

        # Borders
        if pos_x + 10 > width:
            pos_x = 0
        if pos_x < 0:
            pos_x = width - 10
        if pos_y + 10 > height:
            pos_y = 0
        if pos_y < 0:
            pos_y = height - 10

        # URM
        pos_x += speed_x
        pos_y += speed_y
        screen.fill(black)

        # Apple spawner
        apple = pygame.draw.rect(screen, red, [pos_x_apple, pos_y_apple, 10, 10])

        # Snake builder
        snake_head = [pos_x, pos_y]
        snake_list.append(snake_head)

        # Snake existence conditions
        if len(snake_list) > snake_len:
            del snake_list[0]
        for snake_tail in snake_list[:-1]:
            if snake_tail == snake_head:
                game_close = True

        # Functional
        snake_builder(snake_list)
        score(snake_len - 1)
        pygame.display.update()

        # Snake body and velocity increase
        if snake_builder(snake_list, True).colliderect(apple):
            snake_len += 1
            collision = True
            while collision:
                pos_x_apple = on_grid_random()
                pos_y_apple = on_grid_random()
                collision = False
                for xy in snake_list:
                    part = pygame.Rect(xy[0], xy[1], 17, 17)
                    if part.collidepoint(pos_x_apple, pos_y_apple):
                        collision = True
                        break
            speed_cont += snake_len * 0.01
        clock.tick(speed_cont)

    # Exit
    pygame.quit()


replay()
