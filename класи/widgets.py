import pygame


class Label:


    def __init__(self, screen, pos, text, font_size, font_color):
        self.screen = screen
        self.text = text
        self.pos = pos
        self.font_size = font_size
        self.font_color = font_color

        self.label: pygame.font.Font = pygame.font.Font(
            None, font_size).render(text, True, font_color)
        self.rect: pygame.Rect = \
            self.label.get_rect(center=pos)
        self._pos = pos


    def draw(self):
        self.screen.blit(self.label, self.rect)


class Button(Label):


    def __init__(self, screen, pos, text, font_size, font_color):
        super().__init__(screen, pos, text, font_size, font_color)
        self.__clicked = False


    def click(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.__clicked = True
                return False

        if event.type == pygame.MOUSEBUTTONUP:
            if self.__clicked and \
                self.rect.collidepoint(event.pos):
                self.__clicked = False
                return True


def main():
    'приклад'
    pygame.init()
    screen_size = (600, 600)
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    button = Button(screen, (300, 250), 'Hello', 40, (250, 250, 0))
    fps = 60

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if button.click(event):
                print('Ok')

        screen.fill((120, 200, 144))

        button.draw()
        clock.tick(fps)
        pygame.display.update()


if __name__ == '__main__':
    main()
