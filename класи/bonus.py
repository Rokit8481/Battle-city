
# Бонус для гравця
class Bonus(pygame.sprite.Sprite):
    def __init__(self, x, y, bonus_type):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.type = bonus_type  # Наприклад: "shield", "speed", "extra_life"

        # Кольори бонусів для зручності
        if bonus_type == "shield":
            self.image.fill((0, 255, 255))  # Бірюзовий
        elif bonus_type == "speed":
            self.image.fill((255, 0, 255))  # Фіолетовий
        elif bonus_type == "extra_life":
            self.image.fill((255, 255, 255))  # Білий
        else:
            self.image.fill((128, 128, 128))  # Сірий (невідомий бонус)

    def apply_bonus(self, player):
        if self.type == "shield":
            player.shield = True
        elif self.type == "speed":
            player.speed_boost = True
        elif self.type == "extra_life":
            player.lives += 1
