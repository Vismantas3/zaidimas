import pygame
import os

pygame.init()

class character(pygame.sprite.Sprite):
    def __init__(self, PC, flip, char_type, x, y, scale, speed, animation_fps, health):
        self.PC = PC
        self.rect = pygame.Rect((x, y, 80, 180))
        pygame.sprite.Sprite.__init__(self)
        self.WIDTH = 576
        self.HEIGHT = 324
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.walk = False
        self.flip = flip
        self.animation_fps = animation_fps
        self.vel_y = 0
        self.jump = False
        self.attacking = False
        self.attack_counter = 0
        self.hit = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.health = health
        self.update_time = pygame.time.get_ticks()

        self.hurt_duration = 0

        #uzkrauti visus paveiksliukus
        animation_types = ['Idle', 'Run', 'Jump', 'Attack', 'Hurt', 'Dead', 'Run+Attack', 'Jump+Attack']
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
        self.walk = False

        #mygtuku paspaudimai
        if self.PC == 1: #Pirmo zaidejo nustatymai
            key = pygame.key.get_pressed()
            if key[pygame.K_a]:
                dx = -self.speed
                self.walk = True
            if key[pygame.K_d]:
                dx = self.speed
                self.walk = True
            # suolis
            if key[pygame.K_w] and self.alive and self.jump == False:
                self.vel_y = -16
                self.jump = True


            # puolimas
            if key[pygame.K_SPACE] and self.attack_counter == 0:
                self.attack(surface, target)

            #nepulti, kol yra laikomas mygtukas
            if not key[pygame.K_SPACE]:
                self.attack_counter = 0

        if self.PC == 2: #antro zaidejo nustatymai
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                dx = -self.speed
                self.walk = True
            if key[pygame.K_RIGHT]:
                dx = self.speed
                self.walk = True
            # suolis
            if key[pygame.K_UP] and self.alive and self.jump == False:
                self.vel_y = -16
                self.jump = True

            # puolimas
            if key[pygame.K_RCTRL] and self.attack_counter == 0:
                self.attack(surface, target)

            # nepulti, kol yra laikomas mygtukas
            if not key[pygame.K_RCTRL]:
                self.attack_counter = 0




        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > self.WIDTH:
            dx = self.WIDTH - self.rect.right



        # atnaujinti zaidejo pozicija
        self.rect.x += dx
        self.rect.y += dy



        # gravitacija
        self.vel_y += gravity
        dy += self.vel_y
        self.rect.y += dy



        # stoveti ant grindinio
        if self.rect.bottom + dy > self.HEIGHT - 30:
            dy = self.HEIGHT - 30 - self.rect.bottom
            self.jump = False
            self.rect.y += dy


        #kad visa laika ziuretu vienas i kita
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True



    def update_animation(self):
        #animacija
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(5)
        elif self.walk and self.attacking:
            self.update_action(3)  # Use the "Run+Attack" animation
        elif self.walk and not self.jump:
            self.update_action(1)  # Use the "Run" animation
        elif self.jump:
            self.update_action(2)  # Use the "Jump" animation
        elif self.hit:
            self.update_action(4)  # Use the "Hurt" animation
        elif self.attacking:
            self.update_action(3)  # Use the "Attack" animation
        elif self.jump and self.attacking:
            self.update_action(7)  # Use the "Jump+Attack" animation
        else:
            self.update_action(0)  # Use the "Idle" animation



        #animacijos greitis
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]
        #pamatyti, ar pakankamai pra4jo laiko nuo senos animacijos
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += int(self.animation_fps)
        #kada baigiasi animacijos kadru sarasas, pradedama is naujo
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                if self.action == 3:
                    self.attacking = False
                if self.action == 4:
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
        img = pygame.transform.flip(self.image, self.flip, False)
        self.screen.blit(img, self.rect)

    def attack(self, surface, target):
        self.attacking = True
        self.attack_counter += 1
        if self.PC == 1:
            attacking_rect = pygame.Rect(self.rect.centerx - (0.4 * self.rect.width * self.flip), self.rect.y, 0.5 * self.rect.width, self.rect.height)
        elif self.PC == 2:
            attacking_rect = pygame.Rect(self.rect.centerx - (0.4 * self.rect.width * self.flip), self.rect.y, 0.5 * self.rect.width, self.rect.height)
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
