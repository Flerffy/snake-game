import pygame
import json
import os
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    GAME_TITLE,
    FPS,
    MUSIC_VOLUME,
    SFX_VOLUME,
    UP_KEY,
    DOWN_KEY,
    LEFT_KEY,
    RIGHT_KEY,
    PAUSE_KEY,
    GAME_STATES,
    ACTIVE_THEME,
    FULLSCREEN_MODE,
    SNAKE_SPEED,
    BORDER_SIZE,
    GAME_WIDTH,
    GAME_HEIGHT,
    CELL_SIZE,
    DIRECTIONS,
    CENTER_GAME_AREA,
)
from objects import Snake, Food
from sounds import play_sfx, init_sounds, set_bgm_volume, set_sfx_volume


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

        # audio state (kept on GameManager so Menu can read/update them)
        self.music_volume = MUSIC_VOLUME
        self.sfx_volume = SFX_VOLUME

        # key bindings (defaults from constants) — stored here so they can be rebound
        self.keys = {
            'up': UP_KEY,
            'down': DOWN_KEY,
            'left': LEFT_KEY,
            'right': RIGHT_KEY,
            'pause': PAUSE_KEY,
        }

        # settings file path
        self._settings_path = os.path.join(os.path.dirname(__file__), 'settings.json')
        # load saved settings if present
        try:
            self.load_settings()
        except Exception:
            pass

        try:
            set_bgm_volume(self.music_volume)
            set_sfx_volume(self.sfx_volume)
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
                    if event.key == self.keys.get('up'):
                        self.snake.change_direction(DIRECTIONS['UP'])
                    elif event.key == self.keys.get('down'):
                        self.snake.change_direction(DIRECTIONS['DOWN'])
                    elif event.key == self.keys.get('left'):
                        self.snake.change_direction(DIRECTIONS['LEFT'])
                    elif event.key == self.keys.get('right'):
                        self.snake.change_direction(DIRECTIONS['RIGHT'])
                if event.key == self.keys.get('pause'):
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
            # check for wall collisions (split expressions for readability)
            hit_left = head.x < BORDER_SIZE
            hit_top = head.y < BORDER_SIZE
            hit_right = head.x >= (BORDER_SIZE + GAME_WIDTH)
            hit_bottom = head.y >= (BORDER_SIZE + GAME_HEIGHT)
            if hit_left or hit_top or hit_right or hit_bottom:
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
            top_rect = (area_x, area_y, GAME_WIDTH + 2 * BORDER_SIZE, BORDER_SIZE)
            pygame.draw.rect(self.screen, border_color, top_rect)
            # bottom
            bottom_rect = (area_x, area_y + GAME_HEIGHT + BORDER_SIZE, GAME_WIDTH + 2 * BORDER_SIZE, BORDER_SIZE)
            pygame.draw.rect(self.screen, border_color, bottom_rect)
            # left
            left_rect = (area_x, area_y, BORDER_SIZE, GAME_HEIGHT + 2 * BORDER_SIZE)
            pygame.draw.rect(self.screen, border_color, left_rect)
            # right
            right_rect = (area_x + GAME_WIDTH + BORDER_SIZE, area_y, BORDER_SIZE, GAME_HEIGHT + 2 * BORDER_SIZE)
            pygame.draw.rect(self.screen, border_color, right_rect)

            # draw food
            if self.food:
                p = getattr(self.food, 'position', None)
                if p is not None:
                    food_color = self.theme.get('food_color', (255, 0, 0))
                    fx = area_x + p.x
                    fy = area_y + p.y
                    pygame.draw.rect(self.screen, food_color, (fx, fy, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(self.screen, (0, 0, 0), (fx, fy, CELL_SIZE, CELL_SIZE), 1)

            # draw snake
            if self.snake:
                snake_color = self.theme.get('snake_color', (0, 255, 0))
                for seg in self.snake.segments:
                    sx = area_x + seg.x
                    sy = area_y + seg.y
                    pygame.draw.rect(self.screen, snake_color, (sx, sy, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(self.screen, (0, 0, 0), (sx, sy, CELL_SIZE, CELL_SIZE), 1)

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
            pause_cx = area_x + BORDER_SIZE + GAME_WIDTH // 2
            pause_cy = area_y + BORDER_SIZE + GAME_HEIGHT // 2
            pause_rect = pause_surf.get_rect(center=(pause_cx, pause_cy))
            self.screen.blit(pause_surf, pause_rect)

        elif self.state == GAME_STATES['GAME_OVER']:
            overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (area_x + BORDER_SIZE, area_y + BORDER_SIZE))
            font = pygame.font.SysFont(None, 72)
            text_color = self.theme.get('text_color', (255, 255, 255))
            game_over_surf = font.render("GAME OVER", True, text_color)
            game_over_cx = area_x + BORDER_SIZE + GAME_WIDTH // 2
            game_over_cy = area_y + BORDER_SIZE + GAME_HEIGHT // 2
            game_over_rect = game_over_surf.get_rect(center=(game_over_cx, game_over_cy - 40))
            self.screen.blit(game_over_surf, game_over_rect)
            score_font = pygame.font.SysFont(None, 48)
            score_surf = score_font.render(f"Final Score: {self.score}", True, text_color)
            score_rect = score_surf.get_rect(center=(game_over_cx, game_over_cy + 40))
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
        # if level provided, clamp and set the music volume
        if level is not None:
            level = max(0.0, min(1.0, float(level)))
            self.music_volume = level
            try:
                set_bgm_volume(self.music_volume)
            except Exception:
                pass
            try:
                self.save_settings()
            except Exception:
                pass
        return self.music_volume

    def adjust_sfx_volume(self, level=None):
        if level is not None:
            level = max(0.0, min(1.0, float(level)))
            self.sfx_volume = level
            try:
                set_sfx_volume(self.sfx_volume)
            except Exception:
                pass
            try:
                self.save_settings()
            except Exception:
                pass
        return self.sfx_volume

    # Settings persistence
    def load_settings(self):
        if not os.path.exists(self._settings_path):
            return
        try:
            with open(self._settings_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # apply stored settings if present
            self.music_volume = float(data.get('music_volume', self.music_volume))
            self.sfx_volume = float(data.get('sfx_volume', self.sfx_volume))
            # keys may be stored as numbers
            keys = data.get('keys', {})
            for k in ('up', 'down', 'left', 'right', 'pause'):
                if k in keys:
                    try:
                        self.keys[k] = int(keys[k])
                    except Exception:
                        pass
            # resolution/fullscreen
            res = data.get('resolution')
            if isinstance(res, list) and len(res) == 2:
                try:
                    self.change_resolution((int(res[0]), int(res[1])))
                except Exception:
                    pass
            fs = data.get('fullscreen')
            if isinstance(fs, bool):
                self.fullscreen = fs
        except Exception:
            # ignore corrupt settings
            pass

    def save_settings(self):
        data = {
            'music_volume': self.music_volume,
            'sfx_volume': self.sfx_volume,
            'keys': {k: int(v) for k, v in self.keys.items()},
            'resolution': [SCREEN_WIDTH, SCREEN_HEIGHT],
            'fullscreen': bool(self.fullscreen),
        }
        try:
            with open(self._settings_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def rebind_key(self, identifier):
        # identifier is expected to be one of 'up','down','left','right','pause'
        # The actual new key should be set by Menu via direct call to this method
        # with an integer key value. To support older callsites, accept either
        # a string (key name) -> no-op, or a tuple/list/number -> set mapping.
        if identifier is None:
            return
        # If user passed a mapping dict, merge
        if isinstance(identifier, dict):
            for k, v in identifier.items():
                if k in self.keys:
                    try:
                        self.keys[k] = int(v)
                    except Exception:
                        pass
            try:
                self.save_settings()
            except Exception:
                pass
            return
        # otherwise no direct action here; Menu will call set and save
        return
