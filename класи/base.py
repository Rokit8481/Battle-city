# База гравця
class Base(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((60, 60))
        self.image.fill((0, 0, 255))  # Синій колір
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.health = 3  # Базово 3 життя

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.destroy()

    def destroy(self):
        self.kill()
        print("Базу знищено!")
