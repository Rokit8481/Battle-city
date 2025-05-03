import pygame
from assets import TITLE_IMAGE


WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Label:
    def __init__(self, screen, pos, text, font_size, font_color):
        self.screen = screen
        self.font = pygame.font.SysFont("arial", font_size, bold=True)
        self.label = self.font.render(text, True, font_color)
        self.rect = self.label.get_rect(center=pos)

    def draw(self):
        self.screen.blit(self.label, self.rect)


class Button:
    def __init__(self, screen, pos, size, text, font_size, font_color, bg_color=(70, 70, 70), hover_color=(100, 100, 100)):
        self.screen = screen
        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = pos
        self.text = text
        self.font = pygame.font.SysFont("arial", font_size, bold=True)
        self.font_color = font_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.clicked = False

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.bg_color
        pygame.draw.rect(self.screen, color, self.rect, border_radius=8)
        pygame.draw.rect(self.screen, WHITE, self.rect, 2, border_radius=8)
        text_surface = self.font.render(self.text, True, self.font_color)
        self.screen.blit(text_surface, text_surface.get_rect(center=self.rect.center))

    def click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.clicked = True
            return False
        if event.type == pygame.MOUSEBUTTONUP and self.clicked and self.rect.collidepoint(event.pos):
            self.clicked = False
            return True
        return False


class Screens:
    def __init__(self, screen, game_reference=None):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.selected_level = 1
        self.game = game_reference

    def wait_for_key(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type in [pygame.KEYUP, pygame.MOUSEBUTTONUP]:
                    return
            self.clock.tick(self.fps)

    def show_next_level_screen(self, level):
        # This method will handle showing the next level screen
        level_up_btn = Button(self.screen, (self.screen.get_width() // 2, 300), (250, 50), f"Наступний рівень ({level})", 30, WHITE)
        menu_btn = Button(self.screen, (self.screen.get_width() // 2, 370), (250, 50), "МЕНЮ", 30, WHITE)
        quit_btn = Button(self.screen, (self.screen.get_width() // 2, 440), (250, 50), "ВИХІД", 30, WHITE)
        buttons = [level_up_btn, menu_btn, quit_btn]
        label = Label(self.screen, (self.screen.get_width() // 2, 200), "ПЕРЕМОГА!", 50, GREEN)

        while True:
            self.screen.fill(BLACK)
            self.draw_title_image()
            label.draw()
            self._draw_buttons(buttons)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if level_up_btn.click(event):
                    if self.game:
                        self.game.new(level)  # Pass the next level to start it
                    return
                if menu_btn.click(event):
                    self.show_start_screen()
                    return
                if quit_btn.click(event):
                    pygame.quit()
                    exit()
            self.clock.tick(self.fps)


    def draw_title_image(self):
        title_image = pygame.transform.scale(TITLE_IMAGE["title"], (500, 150))
        title_rect = title_image.get_rect(center=(self.screen.get_width() // 2, 120))
        self.screen.blit(title_image, title_rect)

    def show_start_screen(self):
        start_btn = Button(self.screen, (self.screen.get_width() // 2, 300), (250, 60), "ГРАТИ", 36, WHITE)
        level_btn = Button(self.screen, (self.screen.get_width() // 2, 380), (250, 50), "ВИБІР РІВНЯ", 30, GRAY)
        exit_btn = Button(self.screen, (self.screen.get_width() // 2, 460), (250, 50), "ВИХІД", 30, GRAY)
        buttons = [start_btn, level_btn, exit_btn]

        while True:
            self.screen.fill(BLACK)
            self.draw_title_image()
            self._draw_buttons(buttons)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if start_btn.click(event):
                    if self.game:
                        self.game.new(self.selected_level)
                    return
                if level_btn.click(event):
                    self.show_level_selection()
                if exit_btn.click(event):
                    pygame.quit()
                    exit()
            self.clock.tick(self.fps)

    def show_level_selection(self):
        selected_level = 1
        buttons = []
        for i in range(10):
            x = 160 + (i % 5) * 130
            y = 200 + (i // 5) * 80
            buttons.append((Button(self.screen, (x, y), (100, 50), f"Рівень {i+1}", 24, WHITE), i + 1))

        back_btn = Button(self.screen, (self.screen.get_width() // 2, 400), (200, 50), "НАЗАД", 30, GRAY)

        while True:
            self.screen.fill(BLACK)
            self.draw_title_image()

            for btn, _ in buttons:
                btn.draw()
            back_btn.draw()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pygame.quit()
                    exit()
                for btn, level in buttons:
                    if btn.click(event):
                        self.selected_level = level
                        return
                if back_btn.click(event):
                    return
            self.clock.tick(self.fps)

    def show_game_over_screen(self):
        self._show_result_screen("ПОРАЗКА", RED)

    def show_win_screen(self):
        self._show_result_screen("ПЕРЕМОГА", GREEN)

    def _show_result_screen(self, title_text, color):
        play_again_btn = Button(self.screen, (self.screen.get_width() // 2, 300), (250, 50), "ГРАТИ ЩЕ", 30, WHITE)
        menu_btn = Button(self.screen, (self.screen.get_width() // 2, 370), (250, 50), "МЕНЮ", 30, WHITE)
        quit_btn = Button(self.screen, (self.screen.get_width() // 2, 440), (250, 50), "ВИХІД", 30, WHITE)
        buttons = [play_again_btn, menu_btn, quit_btn]
        label = Label(self.screen, (self.screen.get_width() // 2, 200), title_text, 50, color)

        while True:
            self.screen.fill(BLACK)
            self.draw_title_image()
            label.draw()
            self._draw_buttons(buttons)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if play_again_btn.click(event):
                    if self.game:
                        self.game.new(self.selected_level)
                    return
                if menu_btn.click(event):
                    self.show_start_screen()
                    return
                if quit_btn.click(event):
                    pygame.quit()
                    exit()
            self.clock.tick(self.fps)

    def _draw_buttons(self, buttons):
        for btn in buttons:
            btn.draw()
