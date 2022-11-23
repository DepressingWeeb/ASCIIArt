import cv2
import pygame
from pygame.locals import *
import numpy as np
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class ASCIIArtGeneratorColoredCam:
    def __init__(self, font_size=5, rows=100, n_bits_color=12):
        # ' `.-\':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@'
        self.light = '@'
        self.font_size = font_size
        self.n_bits_color = n_bits_color
        self.arr = np.empty((self.n_bits_color + 1, self.n_bits_color + 1, self.n_bits_color + 1, len(self.light)),
                            dtype=pygame.Surface)
        pygame.init()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('SpaceMono-Regular.ttf', font_size)
        self.char_dict = {self.light[i]: i for i in range(len(self.light))}
        self.cap = cv2.VideoCapture(0)
        self.rows, self.cols = rows, int((int(self.cap.get(3)) / int(self.cap.get(4))) * rows)
        self.FPS = int(self.cap.get(5))
        self.step = 255 / n_bits_color
        self.init_color()
        self.SCREEN = pygame.display.set_mode((self.cols * font_size, self.rows * font_size))

    def init_color(self):
        step = 255 / self.n_bits_color
        total = (self.n_bits_color + 1) ** 3
        current = 0
        for i in range(0, self.n_bits_color + 1):
            for j in range(0, self.n_bits_color + 1):
                for k in range(0, self.n_bits_color + 1):
                    self.arr[i, j, k] = [self.font.render(char, True, (int(i * step), int(j * step), int(k * step))) for
                                         char in self.light]
                    self.progress_bar(current, total, 10, 'Init color palette')
                    current += 1
        print()

    def draw(self, ascii_frame):
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                r, g, b = ascii_frame[i][j]
                self.SCREEN.blit(self.arr[int(r / self.step), int(g / self.step), int(b / self.step), 0],
                                 (j * self.font_size, i * self.font_size))

    @staticmethod
    def progress_bar(current, total, progress_bar_length, phase):
        percentage = (current * 100) / total
        step = 100 / progress_bar_length
        number_display = percentage // step
        s = ''.join(['#' if i < number_display else '.' for i in range(progress_bar_length)])
        print(f'\r{phase} : {s} {current}/{total}', end='')

    def run(self):
        frame_current = 0
        while True:
            self.SCREEN.fill(WHITE)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            ret, frame = self.cap.read()
            frame = cv2.resize(frame, (self.cols, self.rows), interpolation=cv2.INTER_CUBIC)
            self.draw(frame)
            cv2.imshow('frame', frame)
            pygame.display.update()
            frame_current += 1
            self.clock.tick(self.FPS)
        pass
