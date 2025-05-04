# bonus.py

import pygame
from assets import BONUS_IMAGES

class Bonus(pygame.sprite.Sprite):
    def __init__(self, x, y, bonus_type):
        super().__init__()
        self.type = bonus_type
        self.image = BONUS_IMAGES.get(bonus_type, pygame.Surface((30,30)))
        self.image = pygame.transform.scale(self.image, (20,20))
        self.rect = self.image.get_rect(center=(x + 20, y + 20))

    def apply_bonus(self, player):
        if self.type == "shield" and not any(b[0] == "shield" for b in player.active_bonuses):
            player.add_bonus("shield")
        elif self.type == "bullet_upgrade" and not any(b[0] == "upgrade" for b in player.active_bonuses):
            player.add_bonus("upgrade")
        elif self.type == "speed" and not any(b[0] == "speed" for b in player.active_bonuses):
            player.add_bonus("speed")
        elif self.type == "extra_life":  
            player.lives += 1
