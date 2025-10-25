import pygame
from constants import *

ACTIVE_THEME = THEME_MAP[ACTIVE_THEME]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(ACTIVE_THEME['background_color'])

font = pygame.font.Font(None, 36)
text = font.render('Snake', True, ACTIVE_THEME['text_color'])
screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 50))

class GameManager:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    # Draw game menu

    # Set game state to Menu

    # Set game state to Playing

    # Set game state to Paused

    # Check for game state Game Over

    # Quit the game

    def update(self):
        pass  # Update game state here
