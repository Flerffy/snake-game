import pygame
from constants import *
from objects import Snake, Food
from sounds import play_sfx, init_sounds


class GameManager:
    """Responsible for initializing pygame, holding the main screen and
    providing safe method stubs that the menu calls. The implementations are
    intentionally minimal so the menu can call these without raising
    AttributeError while you build full game logic."""

    def __init__(self):
        # initialize pygame display and clock
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()

        # initialize sounds early to avoid first-play hiccup
        try:
            init_sounds()
        except Exception:
            pass

        # runtime state
        self.running = True
        self.state = GAME_STATES['MENU']
        self.theme = ACTIVE_THEME
        self.fullscreen = FULLSCREEN_MODE

        # gameplay objects (created when a game starts)
        self.snake = None
        self.food = None
        self.score = 0
        # movement timing (ms)
        self.move_delay = int(1000 / max(1, SNAKE_SPEED))
        self._last_move_time = 0

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            # route keyboard input during gameplay
            if event.type == pygame.KEYDOWN and self.state == GAME_STATES['PLAYING']:
                # ensure snake exists before calling its methods (static analyzers may warn)
                if self.snake:
                    if event.key in (UP_KEY, pygame.K_w, pygame.K_UP):
                        self.snake.change_direction(DIRECTIONS['UP'])
                    elif event.key in (DOWN_KEY, pygame.K_s, pygame.K_DOWN):
                        self.snake.change_direction(DIRECTIONS['DOWN'])
                    elif event.key in (LEFT_KEY, pygame.K_a, pygame.K_LEFT):
                        self.snake.change_direction(DIRECTIONS['LEFT'])
                    elif event.key in (RIGHT_KEY, pygame.K_d, pygame.K_RIGHT):
                        self.snake.change_direction(DIRECTIONS['RIGHT'])
                if event.key == PAUSE_KEY:
                    self.state = GAME_STATES['PAUSED']
            elif event.type == pygame.KEYDOWN and self.state == GAME_STATES['PAUSED']:
                if event.key == PAUSE_KEY:
                    self.state = GAME_STATES['PLAYING']
            elif event.type == pygame.KEYDOWN and self.state == GAME_STATES['GAME_OVER']:
                # Allow returning to main menu from Game Over with the Pause/ESC key
                if event.key == PAUSE_KEY:
                    self.back_to_menu()

    def update(self):
        # game update logic
        if self.state != GAME_STATES['PLAYING']:
            return

        now = pygame.time.get_ticks()
        if now - self._last_move_time < self.move_delay:
            return
        self._last_move_time = now

        # move snake
        if self.snake:
            self.snake.move()

            # check wall collisions
            head = self.snake.head
            if (head.x < BORDER_SIZE or head.y < BORDER_SIZE or
                head.x >= BORDER_SIZE + GAME_WIDTH or head.y >= BORDER_SIZE + GAME_HEIGHT):
                try:
                    play_sfx('low_beep', volume=SFX_VOLUME)
                except Exception:
                    pass
                self.state = GAME_STATES['GAME_OVER']
                return

            # check self collision
            if self.snake.check_self_collision():
                try:
                    play_sfx('low_beep', volume=SFX_VOLUME)
                except Exception:
                    pass
                self.state = GAME_STATES['GAME_OVER']
                return

            # check food collision
            if self.food:
                p = getattr(self.food, 'position', None)
                if p is not None and head.x == p.x and head.y == p.y:
                    self.score += 1
                    self.snake.grow()
                    self.food.respawn(self.snake.segments)
                    # play food-eaten sound (best-effort)
                    try:
                        # use centralized sounds manager
                        play_sfx('beep', volume=SFX_VOLUME)
                    except Exception:
                        # don't let sound errors disrupt the game
                        pass

    def draw(self):
        # clear background
        self.screen.fill(self.theme.get('background_color', (0, 0, 0)))

        # compute area offset to center the game area inside the window
        if CENTER_GAME_AREA:
            area_x = (SCREEN_WIDTH - (GAME_WIDTH + 2 * BORDER_SIZE)) // 2
            area_y = (SCREEN_HEIGHT - (GAME_HEIGHT + 2 * BORDER_SIZE)) // 2
        else:
            area_x = 0
            area_y = 0

        # draw based on state
        if self.state == GAME_STATES['MENU']:
            # menu drawing handled by Menu class; keep background only
            pass
        elif self.state == GAME_STATES['PLAYING']:
            # draw border
            border_color = self.theme.get('border_color', (255, 255, 255))
            # top
            pygame.draw.rect(self.screen, border_color, (area_x, area_y, GAME_WIDTH + 2 * BORDER_SIZE, BORDER_SIZE))
            # bottom
            pygame.draw.rect(self.screen, border_color, (area_x, area_y + GAME_HEIGHT + BORDER_SIZE, GAME_WIDTH + 2 * BORDER_SIZE, BORDER_SIZE))
            # left
            pygame.draw.rect(self.screen, border_color, (area_x, area_y, BORDER_SIZE, GAME_HEIGHT + 2 * BORDER_SIZE))
            # right
            pygame.draw.rect(self.screen, border_color, (area_x + GAME_WIDTH + BORDER_SIZE, area_y, BORDER_SIZE, GAME_HEIGHT + 2 * BORDER_SIZE))

            # draw food
            if self.food:
                p = getattr(self.food, 'position', None)
                if p is not None:
                    food_color = self.theme.get('food_color', (255, 0, 0))
                    pygame.draw.rect(self.screen, food_color, (area_x + p.x, area_y + p.y, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(self.screen, (0, 0, 0), (area_x + p.x, area_y + p.y, CELL_SIZE, CELL_SIZE), 1)

            # draw snake
            if self.snake:
                snake_color = self.theme.get('snake_color', (0, 255, 0))
                for seg in self.snake.segments:
                    pygame.draw.rect(self.screen, snake_color, (area_x + seg.x, area_y + seg.y, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(self.screen, (0, 0, 0), (area_x + seg.x, area_y + seg.y, CELL_SIZE, CELL_SIZE), 1)

            # draw score
            font = pygame.font.SysFont(None, 36)
            text_color = self.theme.get('text_color', (255, 255, 255))
            score_surf = font.render(f"Score: {self.score}", True, text_color)
            self.screen.blit(score_surf, (area_x + BORDER_SIZE + 10, area_y + BORDER_SIZE + 10))

        elif self.state == GAME_STATES['PAUSED']:
            # draw pause overlay
            overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (area_x + BORDER_SIZE, area_y + BORDER_SIZE))
            font = pygame.font.SysFont(None, 72)
            text_color = self.theme.get('text_color', (255, 255, 255))
            pause_surf = font.render("PAUSED", True, text_color)
            pause_rect = pause_surf.get_rect(center=(area_x + BORDER_SIZE + GAME_WIDTH // 2, area_y + BORDER_SIZE + GAME_HEIGHT // 2))
            self.screen.blit(pause_surf, pause_rect)

        elif self.state == GAME_STATES['GAME_OVER']:
            overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (area_x + BORDER_SIZE, area_y + BORDER_SIZE))
            font = pygame.font.SysFont(None, 72)
            text_color = self.theme.get('text_color', (255, 255, 255))
            game_over_surf = font.render("GAME OVER", True, text_color)
            game_over_rect = game_over_surf.get_rect(center=(area_x + BORDER_SIZE + GAME_WIDTH // 2, area_y + BORDER_SIZE + GAME_HEIGHT // 2 - 40))
            self.screen.blit(game_over_surf, game_over_rect)
            score_font = pygame.font.SysFont(None, 48)
            score_surf = score_font.render(f"Final Score: {self.score}", True, text_color)
            score_rect = score_surf.get_rect(center=(area_x + BORDER_SIZE + GAME_WIDTH // 2, area_y + BORDER_SIZE + GAME_HEIGHT // 2 + 40))
            self.screen.blit(score_surf, score_rect)

        pygame.display.flip()

    # ---- Methods the menu expects (safe stubs) ----
    def start_game(self):
        # initialize gameplay state
        self.snake = Snake()
        self.food = Food()
        # ensure food not on snake
        self.food.respawn(self.snake.segments)
        self.score = 0
        self._last_move_time = pygame.time.get_ticks()
        self.state = GAME_STATES['PLAYING']

    def open_settings(self):
        self.state = GAME_STATES['PAUSED']

    def quit_game(self):
        self.running = False

    def change_resolution(self, resolution):
        # resolution may be a tuple (w, h) or a list of options; choose first tuple
        if isinstance(resolution, (list, tuple)) and len(resolution) and isinstance(resolution[0], tuple):
            w, h = resolution[0]
        elif isinstance(resolution, tuple) and len(resolution) == 2:
            w, h = resolution
        else:
            return
        # update display surface
        self.screen = pygame.display.set_mode((w, h), pygame.FULLSCREEN if self.fullscreen else 0)

    def apply_graphics_settings(self, new_resolution, fullscreen_mode=False):
        self.fullscreen = bool(fullscreen_mode)
        flags = pygame.FULLSCREEN if self.fullscreen else 0
        w, h = new_resolution
        self.screen = pygame.display.set_mode((w, h), flags)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        flags = pygame.FULLSCREEN if self.fullscreen else 0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)

    def back_to_menu(self):
        # Reset gameplay state and return to main menu
        self.state = GAME_STATES['MENU']
        self.snake = None
        self.food = None
        self.score = 0
        self._last_move_time = 0

        # Open the Menu so the player sees the main menu UI immediately.
        # Import locally to avoid circular imports at module level.
        try:
            from menu import Menu
        except Exception:
            return
        menu = Menu(self)
        menu.display_main_menu()

    def open_graphics_settings(self):
        # placeholder
        self.state = GAME_STATES['PAUSED']

    def open_audio_settings(self):
        # placeholder
        self.state = GAME_STATES['PAUSED']

    def open_control_settings(self):
        # placeholder
        self.state = GAME_STATES['PAUSED']

    def back_to_settings(self):
        self.state = GAME_STATES['PAUSED']

    def adjust_music_volume(self, level=None):
        # placeholder: if level provided, clamp and set; otherwise no-op
        if level is not None:
            level = max(0.0, min(1.0, float(level)))

    def adjust_sfx_volume(self, level=None):
        if level is not None:
            level = max(0.0, min(1.0, float(level)))

    def rebind_key(self, identifier):
        # placeholder for rebinding control keys
        return
