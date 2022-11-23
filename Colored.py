import cv2
import pygame
from pygame.locals import *
import numpy as np
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class ASCIIArtGeneratorColored:
    def __init__(self, path, font_size=5, rows=100, n_bits_color=255):
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
        self.cap = cv2.VideoCapture(path)
        self.rows, self.cols = rows, int((int(self.cap.get(3)) / int(self.cap.get(4))) * rows)
        self.FPS = int(self.cap.get(5))
        self.step = 255 / n_bits_color
        self.ascii_video_color = np.zeros((int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)), self.rows, self.cols, 3),
                                          np.ubyte)
        self.preprocessing()
        if n_bits_color <= 46:
            self.ascii_video_color_step = (lambda x: np.ubyte(np.round(x / self.step)))(self.ascii_video_color)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0);
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

    def draw(self, frame_number=0):
        temp_surface = pygame.Surface((self.cols * self.font_size, self.rows * self.font_size))
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                r, g, b = self.ascii_video_color[frame_number][i][j]
                gray_val = int(r * 0.3 + g * 0.59 + b * 0.11)
                rendered = self.font.render(self.light[(255 - gray_val) * len(self.light) // 256], True,
                                            (round(r / self.step) * self.step, round(g / self.step) * self.step,
                                             round(b / self.step) * self.step))
                temp_surface.blit(rendered, (j * self.font_size, i * self.font_size))

        cv2.imwrite(f"Frames/{frame_number}.jpg",
                    cv2.rotate(pygame.surfarray.pixels3d(temp_surface), cv2.ROTATE_90_CLOCKWISE))
        pass

    def preprocessing(self):
        total_frame = int(self.cap.get(7))
        if self.n_bits_color <= 46:
            self.init_color()
        frame_current = 0
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (self.cols, self.rows), interpolation=cv2.INTER_CUBIC)
            self.ascii_video_color[frame_current] = frame
            self.progress_bar(frame_current, total_frame, 10, 'Preprocessing')
            frame_current += 1
        if self.n_bits_color >= 47:
            print()
            self.get_frames()

    def get_frames(self):
        frame_current = 0
        total_frame = int(self.cap.get(7))
        while frame_current < total_frame:
            self.draw(frame_current)
            self.progress_bar(frame_current, total_frame, 10, 'Get frames')
            frame_current += 1

    def draw_font(self, frame_number):
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                r, g, b = self.ascii_video_color_step[frame_number][i][j]
                self.SCREEN.blit(self.arr[r, g, b, 0], (j * self.font_size, i * self.font_size))

    @staticmethod
    def progress_bar(current, total, progress_bar_length, phase):
        percentage = (current * 100) / total
        step = 100 / progress_bar_length
        number_display = percentage // step
        s = ''.join(['#' if i < number_display else '.' for i in range(progress_bar_length)])
        print(f'\r{phase} : {s} {current}/{total}', end='')

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
            if self.n_bits_color >= 47:
                self.SCREEN.blit(pygame.image.load(f"Frames/{frame_current}.jpg"), (0, 0))
            else:
                self.draw_font(frame_current)
            ret, frame = self.cap.read()
            cv2.imshow('frame', frame)
            pygame.display.update()
            frame_current += 1
            self.clock.tick(self.FPS)
        pass
