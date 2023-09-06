import pygame
from infiniteBG import background
from player import character

pygame.init()

clock = pygame.time.Clock()
fps = 60
WIDTH = 576
HEIGHT = 324


screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Game")

RED = (255, 0, 0)
GREEN= (0, 255, 0)
BLACK = (0, 0, 0)

#fonas
bg = background(0)

def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, BLACK, (x - 1, y - 1, 252, 22))
    pygame.draw.rect(screen, RED, (x, y, 250, 20))
    pygame.draw.rect(screen, GREEN, (x, y, 100 * ratio, 20) )

#zaidimo loop

#characters
player = character(1, False, "knight", 200,294, 1, 5, 1, 250)
player2 = character(2, True, "black_werewolf", 400,277, 1, 5, 2, 250)

run = True
while run:

    clock.tick(fps)
    #fono iskvietimas
    bg.draw_bg()

    #gyvybes
    draw_health_bar(player.health, 20, 20)
    draw_health_bar(player2.health,300, 20)

    player.move(screen, player2)
    player2.move(screen, player)

    player.update_animation()
    player2.update_animation()
    player.draw(screen)
    player2.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False



    pygame.display.update()
pygame.quit()