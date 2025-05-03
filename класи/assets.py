# assets.py
import pygame

# Кеш для зображень
_image_cache = {}

def load_image(path):
    if path not in _image_cache:
        _image_cache[path] = pygame.image.load(path).convert_alpha()
    return _image_cache[path]

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
# Заздалегідь підвантажуємо всі потрібні ресурси
PLAYER_IMAGES = {
    "up":    load_image("sprites/player_up.png"),
    "down":  load_image("sprites/player_down.png"),
    "left":  load_image("sprites/player_left.png"),
    "right":  load_image("sprites/player_right.png"),

    "upgraded_up":    load_image("sprites/player_upgrade_up.png"),
    "upgraded_down":    load_image("sprites/player_upgrade_down.png"),
    "upgraded_left":    load_image("sprites/player_upgrade_left.png"),
    "upgraded_right":    load_image("sprites/player_upgrade_right.png"),

    "fast_up":      load_image("sprites/player_fast_up.png"),
    "fast_down":    load_image("sprites/player_fast_down.png"),
    "fast_left":    load_image("sprites/player_fast_left.png"),
    "fast_right":   load_image("sprites/player_fast_right.png")
}
ENEMY_IMAGES = {
    "normal": {
        "up":   load_image("sprites/enemy_normal_up.png"),
        "down":  load_image("sprites/enemy_normal_down.png"),
        "left":  load_image("sprites/enemy_normal_left.png"),
        "right":  load_image("sprites/enemy_normal_right.png")
    },
}
BULLET_IMAGES = {
    "normal": load_image("sprites/bullet_normal.png"),
    "upgraded": load_image("sprites/bullet_upgraded.png")
}
WALL_IMAGE = load_image("sprites/wall.png")
WALL_DAMAGED_IMAGE = load_image("sprites/wall_damaged.png")
STEEL_WALL_IMAGE = load_image("sprites/steel_wall.png")
BONUS_IMAGES = {
    "heart":         load_image("sprites/heart_icon.png"),
    "shield":        load_image("sprites/bonus_shield.png"),
    "bullet_upgrade":load_image("sprites/bonus_bullet_upgrade.png"),
    "extra_life":    load_image("sprites/bonus_extra_life.png"),
    "speed":         load_image("sprites/bonus_speed.png")
}
TERRAIN_IMAGE = load_image("sprites/floor.png")
