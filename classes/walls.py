#walls.py

import pygame
from assets import WALL_IMAGE, WALL_DAMAGED_IMAGE, STEEL_WALL_IMAGE, sounds

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size):
        super().__init__()
        # Масштабуємо зображення під tile_size
        self.full_image = pygame.transform.scale(WALL_IMAGE, (tile_size, tile_size))
        self.damaged_image = pygame.transform.scale(WALL_DAMAGED_IMAGE, (tile_size, tile_size))
        self.image = self.full_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.max_health = 2
        self.health = self.max_health

    def hit(self, damage = 1):
        if self.health > 0:
            self.health -= damage
            sounds["play"]("hit_wall")

        if self.health <= 0:
            sounds["play"]("wall_break")
            self.kill()

    def update(self):
        if self.health <= 0:
            self.kill()
        elif self.health <= self.max_health / 2:
            self.image = self.damaged_image


class SteelWall(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size):
        super().__init__()
        self.image = pygame.transform.scale(STEEL_WALL_IMAGE, (tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def hit(self):
        sounds["play"]("hit_metal")
