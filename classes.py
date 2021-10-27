from constant import *


class Score:
    numbers = numbers_img
    scoreboard = scoreboard_img

    def __init__(self):
        self.score_number = 0

    def add_score(self):
        self.score_number += 1

    def draw(self, window):
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
    img = world['pipe']
    GAP = PIPE_GAP
    velocity = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_BOTTOM = self.img
        self.PIPE_TOP = pygame.transform.flip(self.img, False, True)

        self.passed = False

        self.set_height()

    def set_height(self):
        self.height = randrange(50, 400)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.velocity

    def draw(self, window):
        window.blit(self.PIPE_TOP, (self.x, self.top))
        window.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird, window):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        t_point = bird_mask.overlap(top_mask, top_offset)
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)

        if b_point or t_point:
            return True
        if bird.y < -10:
            return True
        return False


class Bird:
    img = bird_images['idle']
    crashed = False
    FLAPS_ANIMATION_TIME = 5
    ROTATE_VEL = 10

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick = 0
        self.frame_index = 0
        self.velacity = 0
        self.height = self.y

    def jump(self):
        self.velacity = -8
        self.tick = 0
        self.height = self.y

    def move(self):
        self.tick += 1
        displacement = self.velacity * (self.tick) + 1.5 * self.tick ** 2
        if displacement >= 16:
            displacement = (displacement/abs(displacement)) * 16

        self.y += displacement

        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < 25:
                self.tilt = 25
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATE_VEL

        if self.y + self.img.get_height() >= WINDOW_HEIGHT - FLOOR_HEIGHT:
            self.crashed = True

    def draw(self, window):
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

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        window.blit(rotated_image, (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Background:
    img = world['background']
    width = img.get_width()
    height = img.get_height()
    velocity = 1

    def __init__(self):
        self.x1 = 0
        self.x2 = self.width

    def move(self):
        self.x1 -= self.velocity
        self.x2 -= self.velocity

        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width
        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self, window):
        window.blit(self.img, (self.x1, 0))
        window.blit(self.img, (self.x2, 0))


class Floor:
    img = world['floor']
    width = img.get_width()
    height = img.get_height()
    velocity = 5

    def __init__(self):
        self.x1 = 0
        self.x2 = self.width

    def move(self):
        self.x1 -= self.velocity
        self.x2 -= self.velocity

        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width
        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self, window):
        window.blit(self.img, (self.x1, WINDOW_HEIGHT - FLOOR_HEIGHT))
        window.blit(self.img, (self.x2, WINDOW_HEIGHT - FLOOR_HEIGHT))
