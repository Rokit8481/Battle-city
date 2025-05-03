# game.py
import pygame
pygame.init()  

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
from assets import TERRAIN_IMAGE
from player import PlayerTank
from enemy import EnemyTank
from bullets import PlayerBullet
from map import GameMap
from level1 import level_map

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
        pygame.display.set_caption("Battle City")
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = False

        # Фон (ґрунт на весь екран)
        self.background = pygame.transform.scale(TERRAIN_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.player = None
        self.enemies = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.map = GameMap(level_map)

    def new(self):
        # Запускаємо нову гру/рівень
        self.all_sprites = pygame.sprite.Group()
        self.enemies.empty()
        self.player_bullets.empty()
        self.enemy_bullets.empty()

        # Створюємо гравця
        spawn_col, spawn_row = 1, 1
        x = spawn_col*self.map.tile_size + self.map.x_offset
        y = spawn_row*self.map.tile_size + self.map.y_offset
        self.player = PlayerTank(x, y, 30)
        self.all_sprites.add(self.player)

        # Створюємо ворогів
        for i in range(5):
            col = 2 + i*2
            row = 0
            ex = col*self.map.tile_size + self.map.x_offset
            ey = row*self.map.tile_size + self.map.y_offset
            enemy = EnemyTank(
                ex, ey,
                30,
                player=self.player,
                enemy_bullets_group=self.enemy_bullets,
                walls_group=self.map.walls,
                steel_walls_group=self.map.steel_walls,
                enemies_group=self.enemies,
                enemy_type="normal"
                
            )
            self.enemies.add(enemy)

        self.playing = True
        self.run()

    def run(self):
        # Основний цикл гри
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def events(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Створюємо кулю гравця
                    bullet = PlayerBullet(
                        self.player.rect.centerx, self.player.rect.centery, 
                        self.player.direction, upgraded=self.player.upgraded
                    )
                    self.player_bullets.add(bullet)

        # Обробка руху гравця
        self.player.handle_keys(keys, self.map.walls, self.map.steel_walls)

    def update(self):
        self.player.update()
        self.map.update()
        self.enemies.update()
        self.player_bullets.update()
        self.enemy_bullets.update()

        # Колізії бонусів
        collided_bonuses = pygame.sprite.spritecollide(self.player, self.map.bonuses, dokill=True)
        for bonus in collided_bonuses:
            bonus.apply_bonus(self.player)

        # Колізії куль і ворогів/стін – оптимізовано через groupcollide
        hits = pygame.sprite.groupcollide(self.player_bullets, self.enemies, True, False)
        for bullet, enemies_hit in hits.items():
            for enemy in enemies_hit:
                enemy.hit(bullet.damage)

        # Зіткнення куль гравця зі стінами
        wall_hits = pygame.sprite.groupcollide(self.player_bullets, self.map.walls, True, False)
        for bullet, walls_hit in wall_hits.items():
            for wall in walls_hit:
                wall.hit()

        # Кулі ворога вражають стіни
        if pygame.sprite.groupcollide(self.enemy_bullets, self.map.walls, True, False):
            # Якщо зіткнення, тут можна оновити health стіни
            pass
        # Якщо влучили в сталеву стіну – просто знищити кулю
        if pygame.sprite.groupcollide(self.enemy_bullets, self.map.steel_walls, True, False):
            pass

        # Вороги влучили в гравця
        if pygame.sprite.spritecollide(self.player, self.enemy_bullets, True):
            if not self.player.shield:
                self.player.lives -= 1
            if self.player.lives <= 0:
                self.end_game("Game Over")

        # Якщо усі вороги знищені – гравець переміг
        if not self.enemies:
            self.end_game("You Win")

    def end_game(self, result):
        self.playing = False
        if result == "Game Over":
            self.show_game_over_screen()
        else:
            self.show_win_screen()

    def draw(self):
        self.screen.blit(self.background, (0,0))
        self.map.draw(self.screen)
        self.enemies.draw(self.screen)
        self.player_bullets.draw(self.screen)
        self.enemy_bullets.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        pygame.display.flip()

    # Методи для відображення екранів меню/результату (не показані повністю)
    def show_start_screen(self): ...
    def show_game_over_screen(self): ...
    def show_win_screen(self): ...
    def wait_for_key(self): ...
    def draw_text(self, text, size, x, y): ...

if __name__ == "__main__":
    game = Game()
    game.new()
    pygame.quit()
