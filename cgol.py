import pygame
import sys
import numpy as np
import random

HEIGHT = 40
WIDTH = 40
BORN = (3,)
SURVIVE = (3, 2,)
SPARSITY = 0.5

SCREEN_SIZE = 400
CELL_SIZE = SCREEN_SIZE // max(HEIGHT, WIDTH)
PREVIEW_STEPS = 1


space = np.zeros((HEIGHT, WIDTH))

def populate(space: list[list], sparsity: float):
    for h in range(HEIGHT):
        for w in range(WIDTH):
            if random.random() > sparsity:
                space[h][w] = 1

# 0 = dead, 1 = survive, 2 = born
def check_survive(space: list[list], place: tuple) -> int:
    ncount = count_neighbors(space, place)
    if space[place[0]][place[1]] == 0:
        if ncount in BORN:
            return 2
        else:
            return 0
    else:
        if ncount in SURVIVE:
            return 1
        else:
            return 0


def count_neighbors(space: list[list], place: tuple) -> int:
    c = 0
    for ud in [-1,0,1]:
        for lr in [-1,0,1]:
            if ud == 0 and lr == 0:
                continue
            if 0 <= place[0] + ud <= HEIGHT - 1 and 0 <= place[1] + lr <= WIDTH - 1:
                c += space[place[0] + ud][place[1] + lr]
 
    return c

def gametick(space: list[list]):
    new_space = step(space)
    space += new_space

def step(space):
    new_space = np.zeros_like(space)
    for h in range(HEIGHT):
        for w in range(WIDTH):
            state = check_survive(space, (h,w))
            if state == 0 and space[h][w] == 1:
                new_space[h][w] = -1
            if state == 2 and space[h][w] == 0:
                new_space[h][w] = 1
    return new_space

auto = False
preview = True

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE,SCREEN_SIZE))

clock = pygame.time.Clock()


def render_future(space, depth, w, h):
    if depth > PREVIEW_STEPS:
        return
    a = pygame.Rect(w*(CELL_SIZE+1) -1 + np.floor(CELL_SIZE*(1/2 - 1/depth)),
                h*(CELL_SIZE+1) -1 + np.floor(CELL_SIZE*(1/2 - 1/depth)), CELL_SIZE//depth, CELL_SIZE//depth)
    changes = step(space)
    for h in range(HEIGHT):
            for w in range(WIDTH):
                if changes[h][w] == -1:
                    pygame.draw.rect(screen, (200, 200, 255), a)
                elif changes[h][w] == 1:
                    pygame.draw.rect(screen, (255, 255, 255), a)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
                mpos = pygame.mouse.get_pos()
                space[mpos[1]//(CELL_SIZE+1)][mpos[0]//(CELL_SIZE+1)] = not space[mpos[1]//(CELL_SIZE+1)][mpos[0]//(CELL_SIZE+1)]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not auto:
                    gametick(space)
            if event.key == pygame.K_a:
                auto = not auto
            if event.key == pygame.K_p:
                preview = not preview
            if event.key == pygame.K_r:
                space = np.zeros((HEIGHT, WIDTH))
                populate(space, SPARSITY)
            if event.key == pygame.K_k:
                space = np.zeros((HEIGHT, WIDTH))

            

    screen.fill((0,0,0))

    pygame.draw.rect(screen, (200, 200, 255), pygame.Rect(0, 0, WIDTH * (CELL_SIZE+1), HEIGHT * (CELL_SIZE+1)))

    if auto:
        gametick(space)


    for h in range(HEIGHT):
        for w in range(WIDTH):
            if space[h][w] == 1:
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(w*(CELL_SIZE+1), h*(CELL_SIZE+1), CELL_SIZE, CELL_SIZE))

    if preview:
        changes = step(space)
        for h in range(HEIGHT):
            for w in range(WIDTH):
                if changes[h][w] == -1:
                    pygame.draw.rect(screen, (200, 200, 255), pygame.Rect(
                        w*(CELL_SIZE+1) -1 + CELL_SIZE//3, h*(CELL_SIZE+1) -1 + CELL_SIZE//3, CELL_SIZE*2//3, CELL_SIZE*2//3))
                elif changes[h][w] == 1:
                    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(
                        w*(CELL_SIZE+1) -1 + CELL_SIZE//3, h*(CELL_SIZE+1) -1 + CELL_SIZE//3, CELL_SIZE*2//3, CELL_SIZE*2//3))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()