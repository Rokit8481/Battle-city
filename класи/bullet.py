class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 255, 0))  # Жовта куля
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.rect.x += self.direction.x * BULLET_SPEED
        self.rect.y += self.direction.y * BULLET_SPEED

        # Видалити кулю, якщо вона виходить за межі екрана
        if not (0 <= self.rect.x <= SCREEN_WIDTH and 0 <= self.rect.y <= SCREEN_HEIGHT):
            self.kill()
