# Гравець
class PlayerTank(Tank):
    def __init__(self, x, y):
        super().__init__(x, y, (0, 255, 0))  # Зелений танк

    def handle_keys(self, keys):
        if keys[pygame.K_LEFT]:
            self.move(-1, 0)
            self.direction = pygame.Vector2(-1, 0)
        if keys[pygame.K_RIGHT]:
            self.move(1, 0)
            self.direction = pygame.Vector2(1, 0)
        if keys[pygame.K_UP]:
            self.move(0, -1)
            self.direction = pygame.Vector2(0, -1)
        if keys[pygame.K_DOWN]:
            self.move(0, 1)
            self.direction = pygame.Vector2(0, 1)
