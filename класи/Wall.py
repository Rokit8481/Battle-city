import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, full_image, damaged_image):
        super().__init__()
        self.full_image = full_image        # Картинка коли стіна ціла
        self.damaged_image = damaged_image  # Картинка коли стіна пошкоджена
        self.image = self.full_image
        self.rect = self.image.get_rect(topleft=(x, y))

        self.max_health = 100               # Максимальне здоров'я
        self.health = self.max_health

    def hit(self, damage=50):
        if self.health > 0:
            self.health -= damage

    def update(self):
        if self.health <= 0:
            self.kill()                     # Якщо хп 0 або менше - стіну знищуємо
        elif self.health <= self.max_health / 2:
            self.image = self.damaged_image  # Якщо менше половини хп - змінюємо текстуру

class SteelWall(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image                  # У сталевої стіни одна картинка
        self.rect = self.image.get_rect(topleft=(x, y))

    def hit(self, damage=50):
        pass                                # Сталева стіна не пошкоджується

    def update(self):
        pass                                # Сталева стіна не змінюється
