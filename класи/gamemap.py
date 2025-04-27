# Карта гри
class GameMap:
    def __init__(self):
        self.walls = pygame.sprite.Group()
        self.bases = pygame.sprite.Group()
        self.bonuses = pygame.sprite.Group()

    def create_wall(self, x, y):
        wall = Wall(x, y)
        self.walls.add(wall)

    def create_base(self, x, y):
        base = Base(x, y)
        self.bases.add(base)

    def create_bonus(self, x, y, bonus_type):
        bonus = Bonus(x, y, bonus_type)
        self.bonuses.add(bonus)

    def draw(self, screen):
        self.walls.draw(screen)
        self.bases.draw(screen)
        self.bonuses.draw(screen)

    def update(self):
        self.bonuses.update()

# Стінка (щоб карта працювала)
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((139, 69, 19))  # Коричнева стіна
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)