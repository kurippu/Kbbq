import pygame

class Smoke(pygame.sprite.Sprite):
    def __init__(self,
                 groups: pygame.sprite.Group,
                 pos: list[int],
                 direction: pygame.math.Vector2,
                 speed: int):
        super().__init__(groups)
        self.image = pygame.image.load("smoke.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction
        self.speed = speed
    
    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed