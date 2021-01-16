import pygame
import random
import os

WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)

pygame.init()

# initialization
BOARD_WIDTH = 400
COLS = 10
DISTANCE = BOARD_WIDTH // COLS
ROWS = 20
BOARD_HEIGHT = DISTANCE * ROWS
board = [0] * COLS * ROWS

# load picture
blocks = []
files = os.listdir('images')
for pic in files:
    blocks.append(pygame.transform.scale(pygame.image.load('images\\' + pic), (DISTANCE, DISTANCE)))

# initialize matrix shape
SHAPE_I = [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]

SHAPE_S = [0, 2, 2, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

SHAPE_J = [0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0]

SHAPE_T = [0, 0, 0, 0, 4, 4, 4, 0, 0, 4, 0, 0, 0, 0, 0, 0]

SHAPE_Z = [5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0]

SHAPE_L = [0, 0, 6, 0, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0]

SHAPE_O = [7, 7, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

shape_list = [SHAPE_I, SHAPE_J, SHAPE_L, SHAPE_O, SHAPE_S, SHAPE_Z, SHAPE_T]

# initialize screen
screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
pygame.display.set_caption('Tetris')

# initialize music background
pygame.mixer.music.load('audio\\tetris.mp3')
pygame.mixer.music.play(loops=-1)

speed = 1000
score = 0
level = 1
temp = 0

# falling event
block_down = pygame.USEREVENT + 1
pygame.time.set_timer(block_down, speed)


class Block:
    shape: list
    row: int = 0
    column: int = 4
    
    def __init__(self, shape):
        self.shape = shape
    
    def show(self):
        for i, color in enumerate(self.shape):
            if color > 0:
                x = (self.column + i % 4) * DISTANCE
                y = (self.row + i // 4) * DISTANCE
                screen.blit(blocks[color - 1], (x, y))
                
    def update(self, r, c):
        if self.check(self.row + r, self.column + c):
            self.row += r
            self.column += c
            return True
        return False
    
    # <to be continue>
    def fast_fall(self):
        pass
        
    def rotate(self):
        save_shape = self.shape.copy()
        for i , color in enumerate(save_shape):
            self.shape[(2 - (i % 4)) * 4 + (i // 4)] = color
        if not self.check(self.row, self.column):
            self.shape = save_shape.copy()
    
    # Check if collided or not: return True if it can move, return False if it can't move 
    def check(self, r, c):
        for i, color in enumerate(self.shape):
            if color > 0:
                rs = r + i // 4
                cs = c + i % 4
                if cs < 0 or rs >= ROWS or cs >= COLS or board[rs * COLS + cs] > 0:
                    return False
        return True


def draw_on_board():
    for i, color in enumerate(block.shape):
        if color > 0:
            board[(block.row + i // 4) * COLS + (block.column + i % 4)] = color

    
def delete_rows():
    full_rows = 0
    for row in range(ROWS):
        for col in range(COLS):
            if board[row * COLS + col] == 0:
                break
        else:
            del board[row * COLS: row * COLS + col]
            board[0:0] = [0] * COLS
            full_rows += 1
    return full_rows ** 2 * 100

def show_score_level():
    text_surface = pygame.font.SysFont('consolas', 40, 1, 0).render(f'{score}', False, (WHITE))
    screen.blit(text_surface, (BOARD_WIDTH // 2 - text_surface.get_width() // 2, 5))

    text_surface = pygame.font.SysFont('consolas', 20, 1, 0).render(f'Level: {level}', False, (WHITE))
    screen.blit(text_surface, (BOARD_WIDTH // 2 - text_surface.get_width() // 2, 55))
    
def game_over():
    for column in range(COLS): 
            if board[column] > 0:
                screen.fill(BLACK)
                font = pygame.font.SysFont("comicsansms", 40)
                text = font.render("Game Over!", True, (255, 0, 0))      
                screen.blit(text, (BOARD_WIDTH // 2 - text.get_width() // 2, 200))

block = Block(random.choice(shape_list))       

# MAIN GAME LOOP
running = True

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == block_down:
            if not block.update(1, 0):
                draw_on_board()
                score += delete_rows()
                # LEVEL UP!!
                if score // 1000 >= level and score > 0 and temp != score:
                    speed = int(0.75 * speed)
                    pygame.time.set_timer(block_down, speed)
                    level = score // 1000 + 1
                    temp = score
                # CREAT NEW BLOCK
                block = Block(random.choice(shape_list))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                block.update(1, 0)
            if event.key == pygame.K_LEFT:
                block.update(0, -1)
            if event.key == pygame.K_RIGHT:
                block.update(0, 1)
            if event.key == pygame.K_UP:
                block.rotate()
    
    screen.fill(BLACK)    
    
    block.show()
    
    show_score_level()

    for i, color in enumerate(board):
        if color > 0:
            x = i % COLS * DISTANCE
            y = i * 2 // ROWS * DISTANCE
            screen.blit(blocks[color - 1], (x, y))
        game_over()
        
    
    pygame.display.flip()
    pygame.display.update()
pygame.quit()
