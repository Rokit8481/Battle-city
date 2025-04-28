class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Battle City")
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = False  # чи йде гра зараз

        # Ігрові об'єкти
        self.player = None
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.map = GameMap()

    def new(self):
        # Створення нового рівня
        self.player = PlayerTank(300, 500)
        self.map.create_base(300, 550)

        # Створити ворогів
        for i in range(5):
            enemy = EnemyTank(100 * i, 0)
            self.enemies.add(enemy)

        self.playing = True
        self.run()

    def run(self):
        while self.playing:
            self.clock.tick(60)  # 60 FPS
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
                    # Створити кулю
                    bullet = Bullet(self.player.rect.centerx, self.player.rect.centery, self.player.direction)
                    self.bullets.add(bullet)

        self.player.handle_keys(keys)

    def update(self):
        self.player.update()
        self.enemies.update()
        self.bullets.update()
        self.map.update()

        # Перевірка колізій кулі з ворогами
        for bullet in self.bullets:
            hit_enemies = pygame.sprite.spritecollide(bullet, self.enemies, True)
            if hit_enemies:
                bullet.kill()

        # Перевірка чи вороги дійшли до бази
        for enemy in self.enemies:
            if pygame.sprite.spritecollideany(enemy, self.map.bases):
                for base in self.map.bases:
                    base.take_damage()
                enemy.kill()

        # Програш якщо база знищена
        if not self.map.bases:
            self.playing = False
            self.show_game_over_screen()

        # Перемога якщо всі вороги вбиті
        if not self.enemies:
            self.playing = False
            self.show_win_screen()

    def draw(self):
        self.screen.fill((0, 0, 0))  # Чорний фон
        self.screen.blit(self.player.image, self.player.rect)
        self.enemies.draw(self.screen)
        self.bullets.draw(self.screen)
        self.map.draw(self.screen)
        pygame.display.flip()

    def show_start_screen(self):
        self.screen.fill((0, 0, 0))
        self.draw_text("BATTLE CITY", 50, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        self.draw_text("Натисни ENTER щоб почати", 30, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.draw_text("Натисни ESC для виходу", 30, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)
        pygame.display.flip()
        self.wait_for_key()

    def show_game_over_screen(self):
        self.screen.fill((0, 0, 0))
        self.draw_text("Ти програв!", 50, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        self.draw_text("Натисни ENTER щоб повернутися в меню", 30, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        pygame.display.flip()
        self.wait_for_key()

    def show_win_screen(self):
        self.screen.fill((0, 0, 0))
        self.draw_text("Перемога!", 50, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        self.draw_text("Натисни ENTER щоб повернутися в меню", 30, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(15)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # ENTER
                        waiting = False
                    if event.key == pygame.K_ESCAPE:  # ESC
                        waiting = False
                        self.running = False

    def draw_text(self, text, size, x, y):
        font = pygame.font.SysFont("arial", size)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
