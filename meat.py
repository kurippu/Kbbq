import pygame

class Meat(pygame.sprite.Sprite):
    def __init__(self, group):
        meat_images = [
        pygame.image.load('Meat.png').convert_alpha(),
        pygame.image.load('meat2.webp').convert_alpha(),
        pygame.image.load('almost_cooked_meat1.png').convert_alpha(),
        pygame.image.load('cooked_meat_1.png').convert_alpha(),
        pygame.image.load('burnt_meat_!.png').convert_alpha
        ]

        super().__init__(group)
        self.state = 0
        self.x = -50
        self.y = -50
        self.image = meat_images[self.state]
        self.image = pygame.transform.scale(self.image, (240, 240))
        self.rect = self.image.get_rect(topleft=(self.x + 100, self.y + 100))
        self.rect.width = self.image.get_width() // 2
        self.rect.height = self.image.get_height() // 2
        self.is_dragging = False
        self.offset_x = 0
        self.offset_y = 0

    def change_state(self):
        meat_images = [
        pygame.image.load('Meat.png').convert_alpha(),
        pygame.image.load('meat2.webp').convert_alpha(),
        pygame.image.load('almost_cooked_meat1.png').convert_alpha(),
        pygame.image.load('cooked_meat_1.png').convert_alpha(),
        pygame.image.load('burnt_meat_!.png').convert_alpha
        ]

        self.state += 1
        self.image = meat_images[self.state]

    def update(self, mousex, mousey):
        if self.is_dragging:
            self.x = mousex - self.offset_x
            self.y = mousey - self.offset_y
            self.rect.center = (self.x, self.y)

    def start_drag(self, mousex, mousey):
        self.is_dragging = True
        self.offset_x = mousex - self.rect.centerx
        self.offset_y = mousey - self.rect.centery
    
    def stop_drag(self):
        self.is_dragging = False