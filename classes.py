"""game classes, for:
make, calculate and show pipe, bird, score, background and floor
"""
from random import randrange
from constant import pygame, BEST_SCORE
from constant import WINDOW_HEIGHT, FLOOR_HEIGHT, PIPE_GAP
from constant import world, bird_images, numbers_img, scoreboard_img


class Score:
    """Score class for
    add score,
    and draw the score and best score
    """
    numbers = numbers_img
    scoreboard = scoreboard_img

    def __init__(self):
        self.score_number = 0

    def add_score(self):
        """add the value to score number
        """
        self.score_number += 1

    def draw(self, window):
        """draw the score and best score

        Args:
            window (pygame surface): display of the game
        """
        global BEST_SCORE
        if self.score_number >= 0:
            if self.score_number > BEST_SCORE:
                BEST_SCORE = self.score_number
            score = str(self.score_number)
            best = str(BEST_SCORE)

            window.blit(self.scoreboard, (16, 16))

            for index, num in enumerate(score[::-1]):
                number = self.numbers[int(num)]
                window.blit(number, (self.scoreboard.get_width() -
                            20 - (index * number.get_width()), 50))

            for index, num in enumerate(best[::-1]):
                number = self.numbers[int(num)]
                window.blit(number, (self.scoreboard.get_width() -
                            20 - (index * number.get_width()), 90))


class Pipe:
    """Pipe class for
    set pipes height,
    move and draw pipes
    and check collide the bird to pipes
    """
    PIPE_BOTTOM = world['pipe']
    PIPE_TOP = pygame.transform.flip(world['pipe'], False, True)
    GAP = PIPE_GAP
    velocity = 5

    def __init__(self, x_pos):
        self.x_pos = x_pos
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.passed = False
        self.set_height()

    def set_height(self):
        """calculate the random height for pipes
        """
        self.height = randrange(50, 400)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        """move the pipes with velocity number
        """
        self.x_pos -= self.velocity

    def draw(self, window):
        """draw the pipes in screen

        Args:
            window (pygame surface): display of the game
        """
        window.blit(self.PIPE_TOP, (self.x_pos, self.top))
        window.blit(self.PIPE_BOTTOM, (self.x_pos, self.bottom))

    def collide(self, bird: object) -> bool:
        """check collide the bird to pipes

        Args:
            bird (object): bird class

        Returns:
            bool: True for collide and false for not collide
        """
        bird_mask = pygame.mask.from_surface(bird.img)
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x_pos - bird.x_pos, self.top - round(bird.y_pos))
        bottom_offset = (self.x_pos - bird.x_pos, self.bottom - round(bird.y_pos))

        t_point = bird_mask.overlap(top_mask, top_offset)
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)

        if b_point or t_point:
            return True
        return False


class Bird:
    """Bird class for
    bird jump,
    change tilt
    check crashed,
    move the bird(change bird position),
    set state of bird image(idle, ascend, descend)
    draw the bird in screen
    and get mask(for collide in Pipe model)
    """
    img = bird_images['idle']
    crashed = False
    FLAPS_ANIMATION_TIME = 5
    ROTATE_VEL = 10

    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.tilt = 0
        self.tick = 0
        self.frame_index = 0
        self.velacity = 0
        self.height = self.y_pos

    def jump(self):
        """jump the bird in screen
        """
        self.velacity = -8
        self.tick = 0
        self.height = self.y_pos

    def tilt_bird(self, displacement):
        """tilt the bird

        Args:
            displacement (int): displacement of bird
        """
        if displacement < 0 or self.y_pos < self.height + 50:
            self.tilt = max(self.tilt, 25)
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATE_VEL

    def check_crashed(self):
        """check for crashed bird, if it falls or goes up a lot
        """
        if self.y_pos + self.img.get_height() >= WINDOW_HEIGHT - FLOOR_HEIGHT:
            self.crashed = True

        if self.y_pos < - self.img.get_height() / 4:
            self.crashed = True

    def move(self):
        """move bird in screen with displacement value
        """
        self.tick += 1
        displacement = self.velacity * (self.tick) + 1.5 * self.tick ** 2
        if displacement >= 16:
            displacement = (displacement/abs(displacement)) * 16

        self.y_pos += displacement

        self.tilt_bird(displacement)
        self.check_crashed()

    def set_state(self):
        """set state of bird(idle, ascend, descend)
        with FLAPS_ANIMATION_TIME and frame_index variable"""
        self.frame_index += 1
        if self.crashed:
            self.img = bird_images['idle']
        elif self.frame_index < self.FLAPS_ANIMATION_TIME:
            self.img = bird_images['ascend']
        elif self.frame_index < self.FLAPS_ANIMATION_TIME * 2:
            self.img = bird_images['idle']
        elif self.frame_index < self.FLAPS_ANIMATION_TIME * 3:
            self.img = bird_images['descend']
        else:
            self.frame_index = 0

    def draw(self, window):
        """draw the bird with it states
        """
        self.set_state()
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        window.blit(rotated_image, (self.x_pos, self.y_pos))


class Background:
    """Background class for,
    move and draw backgrounds
    """
    img = world['background']
    width = img.get_width()
    height = img.get_height()
    velocity = 1

    def __init__(self):
        self.background_x1 = 0
        self.background_x2 = self.width

    def move(self):
        """move backgrounds with velocity
        """
        self.background_x1 -= self.velocity
        self.background_x2 -= self.velocity

        if self.background_x1 + self.width < 0:
            self.background_x1 = self.background_x2 + self.width
        if self.background_x2 + self.width < 0:
            self.background_x2 = self.background_x1 + self.width

    def draw(self, window):
        """draw backgrounds in screen

        Args:
            window (pygame surface): game display
        """
        window.blit(self.img, (self.background_x1, 0))
        window.blit(self.img, (self.background_x2, 0))


class Floor:
    """Floor class for,
    move and draw floors
    """
    img = world['floor']
    width = img.get_width()
    height = img.get_height()
    velocity = 5

    def __init__(self):
        self.floor_x1 = 0
        self.floor_x2 = self.width

    def move(self):
        """move floor in screen with velocity
        """
        self.floor_x1 -= self.velocity
        self.floor_x2 -= self.velocity

        if self.floor_x1 + self.width < 0:
            self.floor_x1 = self.floor_x2 + self.width
        if self.floor_x2 + self.width < 0:
            self.floor_x2 = self.floor_x1 + self.width

    def draw(self, window):
        """draw floors in screen

        Args:
            window (pygame surface): game display
        """
        window.blit(self.img, (self.floor_x1, WINDOW_HEIGHT - FLOOR_HEIGHT))
        window.blit(self.img, (self.floor_x2, WINDOW_HEIGHT - FLOOR_HEIGHT))
