import pygame
from assets import BULLET_IMAGES, SCREEN_WIDTH, SCREEN_HEIGHT

TILE_SIZE = 40
BULLET_WIDTH = TILE_SIZE // 4
BULLET_HEIGHT = TILE_SIZE // 2

DIRECTION_ANGLE = {
    (0, -1): 0,     # up
    (1, 0): -90,    # right
    (0, 1): 180,    # down
    (-1, 0): 90     # left
}

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, damage, image, walls_group, steel_walls_group):
        super().__init__()
        self.direction = direction
        self.speed = 5
        self.damage = damage
        self.walls_group = walls_group
        self.steel_walls_group = steel_walls_group

        scaled_image = pygame.transform.scale(image, (BULLET_WIDTH, BULLET_HEIGHT))
        angle = DIRECTION_ANGLE.get((int(direction.x), int(direction.y)), 0)
        self.image = pygame.transform.rotate(scaled_image, angle)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        # Перевірка зіткнення з цегляними стінами
        for wall in pygame.sprite.spritecollide(self, self.walls_group, False):
            wall.hit(self.damage)
            self.kill()
            return

        # Перевірка зіткнення з сталевими стінами
        if pygame.sprite.spritecollideany(self, self.steel_walls_group):
            self.kill()
            return

        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or 
            self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()

class PlayerBullet(Bullet):
    def __init__(self, x, y, direction, walls_group, steel_walls_group, upgraded=False):
        img = BULLET_IMAGES["upgraded"] if upgraded else BULLET_IMAGES["normal"]
        damage = 2 if upgraded else 1
        super().__init__(x, y, direction, damage, img, walls_group, steel_walls_group)

class EnemyBullet(Bullet):
    def __init__(self, x, y, direction, walls_group, steel_walls_group):
        img = BULLET_IMAGES["normal"]
        super().__init__(x, y, direction, damage=1, image=img, walls_group=walls_group, steel_walls_group=steel_walls_group)
