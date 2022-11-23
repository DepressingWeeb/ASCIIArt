import cv2
import pygame
from pygame.locals import *
import numpy as np
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class ASCIIArtGeneratorCam:
    def __init__(self, font_size=5, rows=100):
        self.light = ' `.-\':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@'
        self.font_size = font_size
        pygame.init()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('SpaceMono-Regular.ttf', font_size)
        self.char_dict = {char: self.font.render(char, True, BLACK) for char in self.light}
        self.cap = cv2.VideoCapture(0)
        self.rows, self.cols = rows, int((int(self.cap.get(3)) / int(self.cap.get(4))) * rows)
        self.FPS = int(self.cap.get(5))
        self.SCREEN = pygame.display.set_mode((self.cols * font_size, self.rows * font_size))

    def draw(self, ascii_frame):
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                self.SCREEN.blit(self.char_dict[ascii_frame[i][j]],
                                 (j * self.font_size, i * self.font_size))

        pass

    def generate_ascii_matrix(self, gray):
        f=lambda x: self.light[(255 - x) * len(self.light) // 256]
        return np.vectorize(f)(gray)

    def run(self):
        while True:
            self.SCREEN.fill(WHITE)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            ret,frame=self.cap.read()
            frame = cv2.resize(frame, (self.cols, self.rows), interpolation=cv2.INTER_CUBIC)
            self.draw(self.generate_ascii_matrix(cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)))
            cv2.imshow('frame',frame)
            pygame.display.update()
            self.clock.tick(self.FPS)

        pass
