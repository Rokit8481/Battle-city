# assets.py

import pygame

pygame.mixer.init()

import threading

_image_cache = {}

def load_image(path):
    if path not in _image_cache:
        _image_cache[path] = pygame.image.load(path).convert_alpha()
    return _image_cache[path]

SCREEN_WIDTH = 960

SCREEN_HEIGHT = 720

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

TITLE_IMAGE = {
    "title":    load_image("sprites/title_bg.png")
} 

BULLET_IMAGES = {
    "normal": load_image("sprites/bullet_normal.png"),
    "upgraded": load_image("sprites/bullet_upgraded.png"),
    "normal_icon": load_image("sprites/icon_bullet_normal.png"),
    "upgraded_icon": load_image("sprites/icon_bullet_upgraded.png")
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


_raw_sounds = {
    'background': pygame.mixer.Sound('sounds/background.wav'),  
    'move': pygame.mixer.Sound('sounds/move.wav'),
    'shoot': pygame.mixer.Sound('sounds/shoot.wav'),
    'hit_tank': pygame.mixer.Sound('sounds/hit_tank.wav'),
    'hit_wall': pygame.mixer.Sound('sounds/hit_wall.wav'),
    'hit_metal': pygame.mixer.Sound('sounds/hit_metal.wav'),
    'bonus': pygame.mixer.Sound('sounds/bonus.wav'),
    'wall_break': pygame.mixer.Sound('sounds/wall_break.wav'),
}

SOUND_DURATIONS = {
    'move': 300,
    'shoot': 200,
    'hit_tank': 200,
    'hit_wall': 200,
    'hit_metal': 300,
    'bonus': 400,
    'wall_break': 500,
}

VOLUMES = {
    'move': 0.100,
    'shoot': 0.050,
    'hit_tank': 0.150,
    'hit_wall': 0.075,
    'hit_metal': 0.2,
    'background': 0.175,
    'bonus': 0.100,
    'wall_break': 0.125
    }

for name, sound in _raw_sounds.items():
    vol = VOLUMES.get(name, 1.0)
    sound.set_volume(vol)

def play_sound(name, loops=0):
    if name not in _raw_sounds:
        return
    sound = _raw_sounds[name]
    sound.play(loops=loops) 

    duration = SOUND_DURATIONS.get(name, None)
    if duration:
        def stop_sound():
            pygame.time.wait(duration) 
            sound.stop()
        threading.Thread(target=stop_sound, daemon=True).start()


sounds = {
    'play': play_sound,
    'raw': _raw_sounds,  
}