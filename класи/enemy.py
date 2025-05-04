import pygame, random
from assets import ENEMY_IMAGES, SCREEN_WIDTH, SCREEN_HEIGHT, sounds
from bullets import EnemyBullet

class EnemyTank(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size, player, enemy_bullets_group, walls_group, steel_walls_group, enemies_group, enemy_type="normal"):
        super().__init__()
        self.tile_size = tile_size
        self.player = player
        self.enemy_bullets = enemy_bullets_group
        self.walls_group = walls_group
        self.steel_walls_group = steel_walls_group
        self.enemies_group = enemies_group

        self.enemy_type = enemy_type
        self.speed = 2 if enemy_type == "fast" else 1
        self.health = 3 if enemy_type == "armored" else 1

        original_images = ENEMY_IMAGES[enemy_type]
        self.images = {
            dir_name: pygame.transform.scale(img, (tile_size, tile_size))
            for dir_name, img in original_images.items()
        }

        self.direction = pygame.Vector2(0, 1)
        self.direction_name = "down"
        self.image = self.images[self.direction_name]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.rect.inflate_ip(-10, -10)

        self.last_shot = pygame.time.get_ticks()
        self.shot_cooldown = 2500
        self.last_dir_change = pygame.time.get_ticks()
        self.dir_change_interval = 1000

    def update(self):
        now = pygame.time.get_ticks()
        target = self.player
        if not target: 
            return

        moved = self.try_move_towards_target(target)
        if not moved and now - self.last_dir_change >= self.dir_change_interval:
            self.random_direction()
            self.last_dir_change = now

        self.image = self.images[self.direction_name]
        self.try_shoot(target)

    def try_move_towards_target(self, target):
        dx = target.rect.centerx - self.rect.centerx
        dy = target.rect.centery - self.rect.centery
        moved_x = moved_y = False

        if dx != 0:
            step_x = self.speed if dx > 0 else -self.speed
            if not self.check_collision(step_x, 0):
                self.move(step_x, 0, "right" if step_x > 0 else "left")
                moved_x = True

        if dy != 0:
            step_y = self.speed if dy > 0 else -self.speed
            if not self.check_collision(0, step_y):
                self.move(0, step_y, "down" if step_y > 0 else "up")
                moved_y = True

        return moved_x or moved_y

    def random_direction(self):
        dirs = [(0,-1,"up"), (0,1,"down"), (-1,0,"left"), (1,0,"right")]
        random.shuffle(dirs)
        for dx, dy, dir_name in dirs:
            if not self.check_collision(dx * self.speed, dy * self.speed):
                self.move(dx * self.speed, dy * self.speed, dir_name)
                break

    def move(self, dx, dy, dir_name):
        self.direction = pygame.Vector2(dx, dy)
        self.direction_name = dir_name
        new_rect = self.rect.move(dx, dy)
        if (0 <= new_rect.left <= SCREEN_WIDTH - new_rect.width and 
            0 <= new_rect.top <= SCREEN_HEIGHT - new_rect.height):
            self.rect = new_rect

    def check_collision(self, dx, dy):
        test_rect = self.rect.move(dx, dy)
        for group in (self.walls_group, self.steel_walls_group, self.enemies_group):
            for sprite in group:
                if sprite != self and test_rect.colliderect(sprite.rect):
                    return True
        return False

    def try_shoot(self, target):
        now = pygame.time.get_ticks()
        if now - self.last_shot < self.shot_cooldown:
            return

        tx, ty = target.rect.center
        ex, ey = self.rect.center

        if abs(tx - ex) < 10:
            direction = pygame.Vector2(0, 1 if ty > ey else -1)
            self.direction = direction
            self.direction_name = "down" if ty > ey else "up"
            bullet = EnemyBullet(ex, ey, direction, self.walls_group, self.steel_walls_group)
            self.enemy_bullets.add(bullet)
            self.last_shot = now
            sounds["play"]("shoot")
            return

        if abs(ty - ey) < 10:
            direction = pygame.Vector2(1 if tx > ex else -1, 0)
            self.direction = direction
            self.direction_name = "right" if tx > ex else "left"
            bullet = EnemyBullet(ex, ey, direction, self.walls_group, self.steel_walls_group)
            self.enemy_bullets.add(bullet)
            self.last_shot = now
            sounds["play"]("shoot")

    def hit(self, damage):
        self.health -= damage
        sounds["play"]("hit_tank")  # Звук при попаданні в танк

        if self.health <= 0:
            self.kill()  # Вилучення танка після знищення
