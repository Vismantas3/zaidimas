import pygame
from infiniteBG import background
from player import character

pygame.init()

clock = pygame.time.Clock()
fps = 60
WIDTH = 576
HEIGHT = 324

#zaidimo kintamieji
intro_count = 3
fight = "FIGHT"
fight_counter = 300
last_count_update = pygame.time.get_ticks()


screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Game")

RED = (255, 0, 0)
GREEN= (0, 255, 0)
BLACK = (0, 0, 0)

#fonas
bg = background(0)

#fiksuota kovotoju pozicija
player_x = WIDTH / 4
player_y = 251
player2_x = WIDTH / 4 * 3
player2_y = 253

#sriftas
count_font = pygame.font.Font('World Conflict .ttf', 80)

#rasymo funkcija
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, BLACK, (x - 1, y - 1, 252, 22))
    pygame.draw.rect(screen, RED, (x, y, 250, 20))
    pygame.draw.rect(screen, GREEN, (x, y, 100 * ratio, 20) )

#zaidimo loop

#characters
player = character(1, False, "knight", player_x,player_y, 1, 5, 1, 250)
player2 = character(2, True, "black_werewolf", player2_x,player2_y, 1, 5, 2, 250)

run = True
while run:

    clock.tick(fps)
    #fono iskvietimas
    bg.draw_bg()



    #gyvybes
    draw_health_bar(player.health, 20, 20)
    draw_health_bar(player2.health,300, 20)

    #intro skaiciavimas
    if intro_count <= 0:
        player.move(screen, player2)
        player2.move(screen, player)
        if fight_counter > 0:
            draw_text(str('FIGHT'), count_font, RED, WIDTH / 2 - 140, HEIGHT / 3 - 40)
            fight_counter -= 1
    else:

        draw_text(str(intro_count), count_font, RED, WIDTH / 2 -40, HEIGHT / 3 - 40)
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()
            print(intro_count + 1)


    player.draw(screen)
    player2.draw(screen)




    player.update_animation()
    player2.update_animation()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False



    pygame.display.update()
pygame.quit()