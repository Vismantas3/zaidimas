import pygame
import os

pygame.init()

class character(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, health):
        self.rect = pygame.Rect((x, y, 80, 180))
        pygame.sprite.Sprite.__init__(self)
        self.WIDTH = 576
        self.HEIGHT = 324
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.vel_y = 0
        self.jump = False
        self.attacking = False
        self.hit = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.health = health
        self.update_time = pygame.time.get_ticks()

        self.hurt_duration = 0

        #uzkrauti visus paveiksliukus
        animation_types = ['Run', 'Jump', 'Attack', 'Hurt', 'Dead', 'Run+Attack', 'Idle']
        for animation in animation_types:
            temp_list = []
            #suskaiciuoja failu kieki
            num_of_frames = len(os.listdir(f'{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'{self.char_type}/{animation}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, surface, target):
        #default judesio kintamieji
        dx = 0
        dy = 0
        gravity = 0.75

        #mygtuku paspaudimai
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            dx = -self.speed
        if key[pygame.K_RIGHT]:
            dx = self.speed

        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > self.WIDTH:
            dx = self.WIDTH - self.rect.right

        # atnaujinti zaidejo pozicija
        self.rect.x += dx
        self.rect.y += dy

        #suolis
        if key[pygame.K_UP] and self.alive and self.jump == False:
            self.vel_y = -11
            self.jump = True

        # gravitacija
        self.vel_y += gravity
        dy += self.vel_y
        self.rect.y += dy



        # stoveti ant grindinio
        if self.rect.bottom + dy > self.HEIGHT - 30:
            dy = self.HEIGHT - 30 - self.rect.bottom
            self.jump = False
            self.rect.y += dy

        # puolimas
        if key[pygame.K_SPACE] and self.attacking == False:
            self.attack(surface, target)


    def update_animation(self):
        #animacija
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(4)
        elif self.jump:
            self.update_action(1) #suolis
        elif self.hit:
            self.update_action(3)
        elif self.attacking:
            self.update_action(2)
        else:
            self.update_action(0) #begimas

        #animacijos greitis
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]
        #pamatyti, ar pakankamai pra4jo laiko nuo senos animacijos
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #kada baigiasi animacijos kadru sarasas, pradedama is naujo
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                if self.action == 2:
                    self.attacking = False
                if self.action == 3:
                    self.action = 0
                    self.hit = False
                    self.attacking = False








    def update_action(self, new_action):
        #tikrinti, ar naujas veiksmas yra kitos nuo praejusio
        if new_action != self.action:
            self.action = new_action
            #atnaujinti animacijos nustatymus
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def draw(self, surface):
        self.screen.blit(self.image, self.rect)

    def attack(self, surface, target):
        self.attacking = True
        attacking_rect = pygame.Rect(self.rect.centerx, self.rect.y, self.rect.width, self.rect.height)
        if attacking_rect.colliderect(target.rect):
            target.health -= 10
            target.hit = True

        pygame.draw.rect(surface, (0, 255, 0), attacking_rect)





# run = True
# while run:
#
#     clock.tick(fps)
#
#     draw_bg()
#
#     player.update_animation()
#     player.draw(screen)
#
#
#     #atnaujinti zaidejo veiksmus
#
#
#     for event in pygame.event.get():
#         #quit game code
#         if event.type == pygame.QUIT:
#             run = False
#
#         #keyboard presses
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_ESCAPE:
#                 run = False
#             #judesys
#
#
#
#
#
#         #keyboard button release
#         if event.type == pygame.KEYUP:
#             if event.key == pygame.K_LEFT:
#                 moving_left = False
#             if event.key == pygame.K_RIGHT:
#                 moving_right = False
#
#
#
#
#     pygame.display.update()
