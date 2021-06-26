import random

import pygame
from pygame.locals import *
import time

size = 32
bgc = (255, 242, 140)


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.apple = pygame.image.load("Assets/apple.png").convert()
        self.x = random.randint(0, 30) * size
        self.y = random.randint(0, 14) * size

    def draw(self):
        self.parent_screen.blit(self.apple, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 30) * size
        self.y = random.randint(0, 14) * size


class Snake:
    def __init__(self, parent_screen, length):

        self.direction = 'down'
        self.parent_screen = parent_screen
        self.block = pygame.image.load("Assets/block.png").convert()

        self.length = length
        self.x = [size] * length
        self.y = [size] * length

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def draw(self):
        self.parent_screen.fill(bgc)

        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def walk(self):

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'up':
            self.y[0] -= size
        if self.direction == 'down':
            self.y[0] += size
        if self.direction == 'left':
            self.x[0] -= size
        if self.direction == 'right':
            self.x[0] += size

        self.draw()


class Game:
    def __init__(self):
        pygame.mixer.init()
        pygame.init()

        self.surface = pygame.display.set_mode((1000, 500))
        self.surface.fill((255, 242, 140))
        self.snake = Snake(self.surface, 2)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x2 <= x1 < x2 + size:
            if y2 <= y1 < y2 + size:
                return True

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            sound = pygame.mixer.Sound("Assets/pick.wav")
            pygame.mixer.Sound.play(sound)
            self.apple.move()
            self.snake.increase_length()

        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise Exception("Game over")

    def display_score(self):
        font = pygame.font.SysFont('Ariel', 30)
        score = font.render(f"SCORE: {self.snake.length - 2}", True, (0, 0, 0))
        self.surface.blit(score, (800, 10))

    def show_game_over(self):
        self.surface.fill(bgc)
        font = pygame.font.SysFont('Ariel', 30)
        line1 = font.render(f"GAME OVER | YOUR HIGH SCORE : {self.snake.length - 1}", True, (0, 0, 0))
        self.surface.blit(line1, (250, 100))
        line2 = font.render(f"PRESS ENTER TO PLAY AGAIN, ESCAPE TO EXIT", True, (0, 0, 0))
        self.surface.blit(line2, (250, 120))
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface, 2)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.07)


if __name__ == "__main__":
    game = Game()
    game.run()
