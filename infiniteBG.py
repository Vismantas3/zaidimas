import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60




pygame.display.set_caption("Side Scroller")



class background(pygame.sprite.Sprite):
    def __init__(self, scroll):
        pygame.sprite.Sprite.__init__(self)
        self.WIDTH = 576
        self.HEIGHT = 324
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        self.scroll = scroll
        self.bg_images = []
        self.bg_width = 0

        for i in range(1, 8):
            self.bg_image = pygame.image.load(f"forest/forest_{i}.png").convert_alpha()
            self.bg_images.append(self.bg_image)
        self.bg_width = self.bg_images[0].get_width()

    # def draw_bg(self):
    #     for item in self.bg_images:
    #         self.screen.blit(item,(0, 0))


    def draw_bg(self):
        for x in range(20):
            speed = 1
            for i in self.bg_images:
                self.screen.blit(i, ((x * self.bg_width) - self.scroll * speed, 0))
                speed += 0.1



# run = True
# while run:
#     clock.tick(fps)
#
#     draw_bg()
#
#     #get keypresses
#     key = pygame.key.get_pressed()
#     if key[pygame.K_LEFT] and scroll > 0:
#         scroll -= 5
#     if key[pygame.K_RIGHT] and scroll < 3000:
#         scroll += 5
#
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False

    # pygame.display.update()
pygame.quit()