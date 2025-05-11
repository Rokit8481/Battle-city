#player.py

import pygame
from assets import PLAYER_IMAGES, SCREEN_WIDTH, SCREEN_HEIGHT, sounds

class PlayerTank(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size):
        super().__init__()
        self.tile_size = tile_size
        self.images_normal = {
            "up":    pygame.transform.scale(PLAYER_IMAGES["up"], (tile_size, tile_size)),
            "down":  pygame.transform.scale(PLAYER_IMAGES["down"], (tile_size, tile_size)),
            "left":  pygame.transform.scale(PLAYER_IMAGES["left"], (tile_size, tile_size)),
            "right": pygame.transform.scale(PLAYER_IMAGES["right"], (tile_size, tile_size)),
        }
        self.images_upgraded = {
            "up":    pygame.transform.scale(PLAYER_IMAGES["upgraded_up"], (tile_size, tile_size)),
            "down":  pygame.transform.scale(PLAYER_IMAGES["upgraded_down"], (tile_size, tile_size)),
            "left":  pygame.transform.scale(PLAYER_IMAGES["upgraded_left"], (tile_size, tile_size)),
            "right": pygame.transform.scale(PLAYER_IMAGES["upgraded_right"], (tile_size, tile_size)),
        }
        self.images_shield = { 
            "up":    pygame.transform.scale(PLAYER_IMAGES["upgraded_up"], (tile_size, tile_size)),
            "down":  pygame.transform.scale(PLAYER_IMAGES["upgraded_down"], (tile_size, tile_size)),
            "left":  pygame.transform.scale(PLAYER_IMAGES["upgraded_left"], (tile_size, tile_size)),
            "right": pygame.transform.scale(PLAYER_IMAGES["upgraded_right"], (tile_size, tile_size)),
        }
        self.images_fast = {
            "up":    pygame.transform.scale(PLAYER_IMAGES["fast_up"], (tile_size, tile_size)),
            "down":  pygame.transform.scale(PLAYER_IMAGES["fast_down"], (tile_size, tile_size)),
            "left":  pygame.transform.scale(PLAYER_IMAGES["fast_left"], (tile_size, tile_size)),
            "right": pygame.transform.scale(PLAYER_IMAGES["fast_right"], (tile_size, tile_size)),
        }


        self.upgraded = False
        self.speed_boost = False
        self.shield = False
        self.direction = pygame.Vector2(0, 1)
        self.direction_name = "down"
        self.image = self.images_normal[self.direction_name]   
        self.rect = self.image.get_rect(topleft=(x, y)) 

        self.step = tile_size // 10
        self.speed = self.step

        self.lives = 3
        self.bonus_durations = {
            "shield": 3750,  
            "bullet_upgrade": 2575, 
            "speed": 2750, 
        }
        self.active_bonuses = []

    def change_speed(self, speed_boost):
        self.speed_boost = speed_boost
        if self.speed_boost:
            self.speed = self.step * 1.5
        else:
            self.speed = self.step

    def hit(self, damage):
        self.health -= damage
        sounds["play"]("hit_tank")

    def add_bonus(self, bonus_type):
        now = pygame.time.get_ticks()

        if bonus_type == "extra_life":
            self.lives += 1
            return

        for i, (b_type, _) in enumerate(self.active_bonuses):
            if b_type == bonus_type:
                self.active_bonuses[i] = (bonus_type, now)
                break
        else:
            self.active_bonuses.append((bonus_type, now))

        if bonus_type == "speed":
            self.change_speed(True)
        elif bonus_type == "shield":
            self.shield = True
        elif bonus_type == "upgrade":
            self.upgraded = True

    def update(self):
        now = pygame.time.get_ticks()
        to_remove = []

        for bonus_type, start in self.active_bonuses:
            duration = self.bonus_durations.get(bonus_type, 0)
            if now - start > duration:
                if bonus_type == "upgrade":
                    self.upgraded = False
                elif bonus_type == "shield":
                    self.shield = False
                elif bonus_type == "speed":
                    self.speed_boost = False
                to_remove.append((bonus_type, start))

        for b in to_remove:
            self.active_bonuses.remove(b)

        if self.shield:
            self.image = self.images_shield[self.direction_name]
        elif self.upgraded:
            self.image = self.images_upgraded[self.direction_name]
        elif self.speed_boost:
            self.image = self.images_fast[self.direction_name]
        else:
            self.image = self.images_normal[self.direction_name]
        
        self.rect.size = self.image.get_size()



    def handle_keys(self, keys, walls, steel_walls):
        dx = dy = 0
        moved = False

        if keys[pygame.K_a]:
            dx = -self.speed
            self.direction = pygame.Vector2(-1, 0)
            self.direction_name = "left"
            moved = True
        elif keys[pygame.K_d]:
            dx = self.speed
            self.direction = pygame.Vector2(1, 0)
            self.direction_name = "right"
            moved = True
        elif keys[pygame.K_w]:
            dy = -self.speed
            self.direction = pygame.Vector2(0, -1)
            self.direction_name = "up"
            moved = True
        elif keys[pygame.K_s]:
            dy = self.speed
            self.direction = pygame.Vector2(0, 1)
            self.direction_name = "down"
            moved = True

        # Звук руху
        if moved:
            sounds["play"]("move")
        else:
            sounds["stop"]("move")  

        original_pos = self.rect.topleft
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT: self.rect.bottom = SCREEN_HEIGHT

        if (pygame.sprite.spritecollide(self, walls, False) or 
            pygame.sprite.spritecollide(self, steel_walls, False)):
            self.rect.topleft = original_pos


