"""main of flappybird game
"""
from constant import pygame, WINDOW, WINDOW_WIDTH
from constant import clock, GAME_TICK, MAINMENU_ACTIVE
from constant import toolkit, messages, buttons
from classes import Score, Pipe, Bird, Background, Floor


def gameover():
    """For when the player loses the game
    """
    WINDOW.blit(messages['game_title'],
                (WINDOW_WIDTH / 2 - messages['game_title'].get_width() / 2,
                 100)
                )
    WINDOW.blit(messages['gameover'],
                (WINDOW_WIDTH / 2 - messages['gameover'].get_width() / 2,
                 180)
                )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        toolkit.button(buttons['play'],
                       WINDOW_WIDTH / 2 - buttons['play'].get_width() / 2,
                       350,
                       run)

        pygame.display.update()
        clock.tick(30)


def mainmenu():
    """Main menu to start the game
    """
    WINDOW.blit(messages['game_title'],
                (WINDOW_WIDTH / 2 - messages['game_title'].get_width() / 2,
                 100)
                )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        toolkit.button(buttons['play'],
                       WINDOW_WIDTH / 2 - buttons['play'].get_width() / 2,
                       300,
                       close_mainmenu)

        pygame.display.update()
        clock.tick(30)


def close_mainmenu():
    """Close main menu and start the game
    """
    global MAINMENU_ACTIVE
    MAINMENU_ACTIVE = False
    run()


def run():
    """This is the base function of the game,
    where all processes are controlled
    """
    score = Score()
    background = Background()
    floor = Floor()
    bird = Bird(40, 100)
    pipes = [Pipe(WINDOW_WIDTH+100)]

    while True:
        clock.tick(GAME_TICK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        if pygame.mouse.get_pressed()[0] == 1:
            bird.jump()

        if bird.crashed:
            toolkit.update_display(background, pipes, bird, floor)
            gameover()
        else:
            background.move()
            floor.move()
            bird.move()
            add_pipe = False
            for pipe in pipes:
                pipe.move()
                if pipe.collide(bird):
                    toolkit.update_display(background, pipes, bird, floor)
                    gameover()
                if not pipe.passed and pipe.x_pos < bird.x_pos:
                    pipe.passed = True
                    add_pipe = True

        if add_pipe:
            score.add_score()
            if len(pipes) > 1:
                pipes.pop(0)
            pipes.append(Pipe(WINDOW_WIDTH))

        if MAINMENU_ACTIVE:
            toolkit.update_display(background, floor)
            mainmenu()

        toolkit.update_display(background, pipes, bird, floor, score)


if __name__ == '__main__':
    run()
