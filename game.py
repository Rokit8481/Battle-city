# game.py
import pygame
pygame.init()  

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
UI_PANEL_HEIGHT = 100
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + UI_PANEL_HEIGHT)) 
from assets import TERRAIN_IMAGE, BONUS_IMAGES, BULLET_IMAGES
from player import PlayerTank
from enemy import EnemyTank
from bullets import PlayerBullet
from map import GameMap
from level1 import level_map

class Game:
    def __init__(self):
        pygame.init()
        self.screen = screen
        pygame.display.set_caption("Battle City")
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = False

        # Фон (ґрунт на весь екран)
        self.background = pygame.transform.scale(TERRAIN_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT + UI_PANEL_HEIGHT))


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
        for (ex, ey) in self.map.get_enemy_spawns():
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
                    self.player.direction,
                    self.map.walls,
                    self.map.steel_walls,
                    upgraded=self.player.upgraded  # тільки якщо це справжній апгрейд
                    )

                    self.player_bullets.add(bullet)

        # Обробка руху гравця
        self.player.handle_keys(keys, self.map.walls, self.map.steel_walls)

    def draw_ui(self):
        panel_y = SCREEN_HEIGHT
        pygame.draw.rect(self.screen, (40, 40, 40), (0, panel_y, SCREEN_WIDTH, 100))  # сірий фон

        # Життя
        heart_icon = pygame.transform.scale(BONUS_IMAGES["heart"], (30, 30))
        self.screen.blit(heart_icon, (10, panel_y + 10))
        self.draw_text(f"x {self.player.lives}", 24, 50, panel_y + 15)

        # Бонуси
        x_start = 150
        bonuses = ["shield", "bullet_upgrade", "speed"]
        for i, bonus in enumerate(bonuses):
            if any(b[0] == bonus for b in self.player.active_bonuses):
                icon = pygame.transform.scale(BONUS_IMAGES[bonus], (30, 30))
                self.screen.blit(icon, (x_start + i * 40, panel_y + 10))

        # Показ рівня куль
        bullet_icon = BULLET_IMAGES["upgraded"] if self.player.upgraded else BULLET_IMAGES["normal"]
        bullet_icon = pygame.transform.scale(bullet_icon, (30, 30))
        self.screen.blit(bullet_icon, (SCREEN_WIDTH - 80, panel_y + 10))
        self.draw_text("BULLET", 16, SCREEN_WIDTH - 85, panel_y + 45)


    def update(self):
        self.player.update()
        self.map.update()
        self.map.walls.update()  
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
        wall_hits = pygame.sprite.groupcollide(self.enemy_bullets, self.map.walls, True, False)
        for bullet, walls_hit in wall_hits.items():
            for wall in walls_hit:
                wall.hit(bullet.damage)

        # Кулі ворога вражають стіни
        wall_hits = pygame.sprite.groupcollide(self.enemy_bullets, self.map.walls, True, False)
        for bullet, walls_hit in wall_hits.items():
            for wall in walls_hit:
                wall.hit(bullet.damage)
        # Якщо влучили в сталеву стіну – просто знищити кулю
        pygame.sprite.groupcollide(self.enemy_bullets, self.map.steel_walls, True, False)

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
        self.draw_ui()
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
