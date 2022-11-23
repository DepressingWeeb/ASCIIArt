import cv2
import pygame
from pygame.locals import *
import numpy as np
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class ASCIIArtGenerator:
    def __init__(self, path, font_size=5, rows=100):
        self.light = ' `.-\':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@'
        self.font_size = font_size
        pygame.init()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('SpaceMono-Regular.ttf', font_size)
        self.char_dict = {char: self.font.render(char, True, BLACK) for char in self.light}
        self.cap = cv2.VideoCapture(path)
        self.rows, self.cols = rows, int((int(self.cap.get(3)) / int(self.cap.get(4))) * rows)
        self.FPS = int(self.cap.get(5))
        self.ascii_video = np.zeros((int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)), self.rows, self.cols), str)
        self.preprocessing()
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0);
        self.SCREEN = pygame.display.set_mode((self.cols * font_size, self.rows * font_size))

    def draw(self, frame_number=0):
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                self.SCREEN.blit(self.char_dict[self.ascii_video[frame_number][i][j]],
                                 (j * self.font_size, i * self.font_size))

        pass

    def preprocessing(self):
        frame_current = 0
        frame_total = int(self.cap.get(7))
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (self.cols, self.rows), interpolation=cv2.INTER_CUBIC)
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            self.generate_ascii_matrix(gray, frame_current)
            self.progress_bar(frame_current, frame_total, 30)
            frame_current += 1

    def generate_ascii_matrix(self, gray, frame):
        f = lambda x: self.light[(255 - x) * len(self.light) // 256]
        self.ascii_video[frame] = np.vectorize(f)(gray)
        pass

    @staticmethod
    def progress_bar(current, total, progress_bar_length):
        percentage = (current * 100) / total
        step = 100 / progress_bar_length
        number_display = percentage // step
        s = ''.join(['#' if i < number_display else '.' for i in range(progress_bar_length)])
        print(f'\r{s} {current}/{total}', end='')

    def run(self):
        frame_current = 0
        total_frame = self.cap.get(7)
        while frame_current < total_frame:
            self.SCREEN.fill(WHITE)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            self.draw(frame_current)
            ret, frame = self.cap.read()
            cv2.imshow('frame', frame)
            pygame.display.update()
            frame_current += 1
            self.clock.tick(self.FPS)

        pass
