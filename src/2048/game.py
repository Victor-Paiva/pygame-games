import pygame
import random
import sys
import time
from tile import Tile
from colors import COLORS

class Game:
    def __init__(self, size, dim=4, best=0, filename='best.txt'):
        self.size = size
        self.real_size = size[0], size[1] + 100
        self.full_size = size[0], size[1] + 200
        self.dim = dim
        self.side = size[0] // dim
        self.board = [[Tile((j, i), 0, self.side) for i in range(self.dim)] for j in range(self.dim)]
        self.filename = filename
        self.best = best
        self.score = 0

    def get_available_tiles(self):
        available = []
        for i in range(self.dim):
            for j in range(self.dim):
                if self.board[i][j].value == 0:
                    available.append((i, j))

        return available

    def compare(self, previous):
        for i in range(self.dim):
            for j in range(self.dim):
                if previous[i][j] != self.board[i][j].value:
                    return True
        return False

    def update_best(self):
        if self.score > self.best:
            with open(self.filename, 'w') as f:
                f.write(str(self.score))
            self.best = self.score

    def setup(self, label, tiles=2, prob=0.7):
        pygame.init()
        pygame.font.init()
        win = pygame.display.set_mode(self.full_size)
        pygame.display.set_caption(label)

        for _ in range(tiles):
            self.insert_tile() 

        return win

    def insert_tile(self, prob=0.7):
        r, c = random.choice(self.get_available_tiles())
        self.board[r][c].update_value(1 if random.random() < prob else 2)

    def draw_tiles(self):
        for i in range(self.dim):
            for j in range(self.dim):
                self.board[i][j].show(self.surface)

    def draw_grid(self):
        for i in range(self.dim):
            pygame.draw.line(self.surface, COLORS['lines'], (0, i*self.side), (self.size[0], i*self.side), 4)
            for j in range(self.dim):
                pygame.draw.line(self.surface, COLORS['lines'], (j*self.side, 0), (j*self.side, self.size[1]), 4)

        pygame.draw.line(self.surface, COLORS['lines'], (0, self.dim*self.side-2), (self.size[0], self.dim*self.side-2), 4)
        pygame.draw.line(self.surface, COLORS['lines'], (self.dim*self.side-2, 0), (self.dim*self.side-2, self.size[1]), 4)
    
    def draw_score(self, height=70, width=105, n_height=40, n_width=120):
        x_score = self.size[0] // 4 - width // 2
        x_best = 3 * self.size[0] // 4 - width // 2
        x_reset = self.size[0] // 2 - n_width // 2
        y = self.size[1] + (self.real_size[1] - self.size[1]) // 2 - height // 2
        y_reset = self.real_size[1] + (self.full_size[1] - self.real_size[1]) // 2 - n_height // 2

        pygame.draw.rect(self.surface, COLORS['lines'], (x_score, y, width, height), 0)
        pygame.draw.rect(self.surface, COLORS['score_label'], (x_score, y, width, height), 3)
        pygame.draw.rect(self.surface, COLORS['lines'], (x_best, y, width, height), 0)
        pygame.draw.rect(self.surface, COLORS['score_label'], (x_best, y, width, height), 3)
        self.reset_button = pygame.draw.rect(self.surface, COLORS['new_game'], (x_reset, y_reset, n_width, n_height), 0)
        pygame.draw.rect(self.surface, COLORS['score_label'], (x_reset, y_reset, n_width, n_height), 3)
        
        font = pygame.font.SysFont('arialrounded', 10)
        s_label = font.render('SCORE', 1, COLORS['score_label'])
        self.surface.blit(s_label, (x_score + width // 2 - s_label.get_width() // 2, y + 5))
        b_label = font.render('BEST', 1, COLORS['score_label'])
        self.surface.blit(b_label, (x_best + width // 2 - b_label.get_width() // 2, y + 5))

        font = pygame.font.SysFont('arialrounded', 30)
        s_label = font.render(str(self.score), 1, COLORS['score'])
        self.surface.blit(s_label, (x_score + width // 2 - s_label.get_width() // 2, y + height // 2 - s_label.get_height() // 2 + 5))
        b_label = font.render(str(max(self.best, self.score)), 1, COLORS['score'])
        self.surface.blit(b_label, (x_best + width // 2 - b_label.get_width() // 2, y + height // 2 - s_label.get_height() // 2 + 5))
        
        font = pygame.font.SysFont('arialrounded', 20)
        n_label = font.render('New Game', 1, COLORS['score'])
        self.surface.blit(n_label, (x_reset + n_width // 2 - n_label.get_width() // 2, y_reset + n_height // 2 - n_label.get_height() // 2))

    def draw_window(self):
        self.surface.fill((COLORS['background']))
        self.draw_tiles()
        self.draw_grid()
        self.draw_score()

    def move(self, direction):
        ranges = {
            'left': (range(self.dim), range(self.dim - 1)),
            'right': (range(self.dim), range(self.dim - 1, 0, -1)),
            'up': (range(self.dim), range(self.dim)),
            'down': (range(self.dim), range(self.dim - 1, 0, -1))
        }

        for i in ranges[direction][0]:
            for j in ranges[direction][1]:
                done = False
                ranges_2 = {
                    'left': range(j + 1, self.dim),
                    'right': range(j - 1, -1, -1),
                    'up': range(j + 1, self.dim),
                    'down': range(j - 1, -1, -1)
                }
                if direction == 'left' or direction == 'right':
                    for k in ranges_2[direction]:
                        if self.board[i][j].value == 0 and self.board[i][k].value != 0:
                            self.board[i][j].update_value(self.board[i][k].value)
                            self.board[i][k].update_value(0)
                        
                        elif self.board[i][j].value != 0 and not done:
                            if self.board[i][j].value == self.board[i][k].value:
                                self.board[i][j].update_value(self.board[i][j].value + 1)
                                self.board[i][k].update_value(0)
                                self.score += 2 ** self.board[i][j].value
                                done = True
                            elif self.board[i][k].value != 0:
                                done = True
                else:
                    for k in ranges_2[direction]:
                        if self.board[j][i].value == 0 and self.board[k][i].value != 0:
                            self.board[j][i].update_value(self.board[k][i].value)
                            self.board[k][i].update_value(0)
                        
                        elif self.board[j][i].value != 0 and not done:
                            if self.board[j][i].value == self.board[k][i].value:
                                self.board[j][i].update_value(self.board[j][i].value + 1)
                                self.board[k][i].update_value(0)
                                self.score += 2 ** self.board[j][i].value
                                done = True
                            elif self.board[k][i].value != 0:
                                done = True
    def run(self):
        self.surface = self.setup('2048')

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.update_best()
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    old = [[0 for x in range(self.dim)] for x in range(self.dim)]
                    for i in range(self.dim):
                        for j in range(self.dim):
                            old[i][j] = self.board[i][j].value

                    if event.key == pygame.K_LEFT:
                        self.move('left')
                    elif event.key == pygame.K_RIGHT:
                        self.move('right')
                    elif event.key == pygame.K_UP:
                        self.move('up')
                    elif event.key == pygame.K_DOWN:
                        self.move('down')

                    if self.compare(old):
                        self.insert_tile()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.reset_button.collidepoint(pos):
                        self.update_best()
                        time.sleep(0.2)
                        self.__init__(self.size, dim=self.dim, best=self.best, filename=self.filename)
                        self.run()

            self.draw_window()
            pygame.display.update()