# assets.py

import pygame

pygame.mixer.init()

_sound_channels = {}
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


raw_sounds = {
    'background': pygame.mixer.Sound('sounds/background.wav'),  
    'move': pygame.mixer.Sound('sounds/move.wav'),
    'shoot': pygame.mixer.Sound('sounds/shoot.wav'),
    'hit_tank': pygame.mixer.Sound('sounds/hit_tank.wav'),
    'hit_wall': pygame.mixer.Sound('sounds/hit_wall.wav'),
    'hit_metal': pygame.mixer.Sound('sounds/hit_metal.wav'),
    'bonus': pygame.mixer.Sound('sounds/bonus.wav'),
    'wall_break': pygame.mixer.Sound('sounds/wall_break.wav'),
}



VOLUMES = {
    'move': 0.090,
    'shoot': 0.050,
    'hit_tank': 0.075,
    'hit_wall': 0.075,
    'hit_metal': 0.075,
    'background': 0.175,
    'bonus': 0.075,
    'wall_break': 0.100
    }

for name, sound in raw_sounds.items():
    vol = VOLUMES.get(name, 1.0)
    sound.set_volume(vol)

def play_sound(name, loops=0, force=False):
    if name not in raw_sounds:
        return

    sound = raw_sounds[name]

    if name == 'move':
        if name not in _sound_channels:
            _sound_channels[name] = pygame.mixer.find_channel()
        channel = _sound_channels[name]
        if channel is not None and not channel.get_busy():
            channel.play(sound, loops=-1)
    else:
        sound.play(loops=loops)

def stop_sound(name):
    channel = _sound_channels.get(name)
    if channel and channel.get_busy():
        channel.stop()



sounds = {
    'play': play_sound,
    'stop': stop_sound,
    'raw': raw_sounds
}