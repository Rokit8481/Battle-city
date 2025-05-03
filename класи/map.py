# map.py
import pygame
from walls import Wall, SteelWall
from bonus import Bonus
from assets import TERRAIN_IMAGE, SCREEN_WIDTH, SCREEN_HEIGHT
from level1 import level_map  # дані рівня

class GameMap:
    def __init__(self, level_map):
        self.walls = pygame.sprite.Group()
        self.steel_walls = pygame.sprite.Group()
        self.bonuses = pygame.sprite.Group()
        self.level_map = level_map
        self.tile_size = 40  # розмір клітинки
        self.rows = len(level_map)
        self.cols = len(level_map[0])
        self.map_width = self.cols * self.tile_size
        self.map_height = self.rows * self.tile_size
        self.x_offset = (SCREEN_WIDTH - self.map_width)//2
        self.y_offset = (SCREEN_HEIGHT - self.map_height)//2

        # Підготовка тайлу ґрунту
        self.grass_tile = pygame.transform.scale(TERRAIN_IMAGE, (self.tile_size, self.tile_size))
        self.load_map()

    def load_map(self):
        for row_idx, row in enumerate(self.level_map):
            for col_idx, tile in enumerate(row):
                x = col_idx * self.tile_size + self.x_offset
                y = row_idx * self.tile_size + self.y_offset
                if tile == "W":
                    self.walls.add(Wall(x, y, self.tile_size))
                elif tile == "S":
                    self.steel_walls.add(SteelWall(x, y, self.tile_size))  
                elif tile == "G":
                    self.bonuses.add(Bonus(x, y, "shield"))
                elif tile == "T":
                    self.bonuses.add(Bonus(x, y, "bullet_upgrade"))
                elif tile == "L":
                    self.bonuses.add(Bonus(x, y, "extra_life"))
                elif tile == "D":
                    self.bonuses.add(Bonus(x, y, "speed"))

    def draw(self, screen):
        # Малюємо ґрунт
        for row in range(self.rows):
            for col in range(self.cols):
                x = col*self.tile_size + self.x_offset
                y = row*self.tile_size + self.y_offset
                screen.blit(self.grass_tile, (x, y))
        # Малюємо елементи
        self.walls.draw(screen)
        self.steel_walls.draw(screen)
        self.bonuses.draw(screen)
        # (опційно) малюнок сітки
        self.draw_grid(screen)

    def update(self):
        self.walls.update()
        self.bonuses.update()

    def draw_grid(self, screen):
        # Показати сітку клітин (для відладки)
        for x in range(self.x_offset, self.x_offset + self.map_width, self.tile_size):
            pygame.draw.line(screen, (100,100,100), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(self.y_offset, self.y_offset + self.map_height, self.tile_size):
            pygame.draw.line(screen, (100,100,100), (0, y), (SCREEN_WIDTH, y))
