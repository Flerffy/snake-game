import pygame
# Constants stored for game configuration and settings

## Configurable game settings

# Graphics settings
# Screen resolution: derived from game area below (can be overridden)
# If you want a different window size, set SCREEN_WIDTH / SCREEN_HEIGHT here.
SCREEN_WIDTH = None
SCREEN_HEIGHT = None

# Windowed  (True by default)
WINDOWED_MODE = True  # True for windowed mode, False for fullscreen

# Fullscreen mode (False by default)
FULLSCREEN_MODE = False  # True for fullscreen mode, False for windowed

# Default theme name (used to build the active theme dict)
DEFAULT_THEME_NAME = 'Dark'  # Options: 'Light', 'Dark'

# Theme color dictionaries (use explicit keys expected by the UI)
DARK_THEME = {
    'background_color': (30, 30, 30),
    'text_color': (255, 255, 255),
    'snake_color': (0, 255, 0),
    'food_color': (255, 0, 0),
    'border_color': (255, 255, 255),
}

LIGHT_THEME = {
    'background_color': (220, 220, 220),
    'text_color': (0, 0, 0),
    'snake_color': (0, 100, 0),
    'food_color': (200, 0, 0),
    'border_color': (0, 0, 0),
}

THEME_MAP = {
    'Dark': DARK_THEME,
    'Light': LIGHT_THEME,
}

# The active theme is the resolved dict for the selected theme name
ACTIVE_THEME = THEME_MAP[DEFAULT_THEME_NAME]

# Menu / UI sizes (tweakable)
MENU_TITLE_FONT_SIZE = 40
MENU_OPTION_FONT_SIZE = 28

# Center the game area inside the window (adds margins) when True
CENTER_GAME_AREA = True

# Audio settings
# Music Volume
MUSIC_VOLUME = 1.0  # Music volume level (0.0 to 1.0)

# Sound Effects Volume
SFX_VOLUME = 1.0  # Sound effects volume level (0.0 to 1.0)

# Control settings
UP_KEY = pygame.K_w  # Key for moving up
DOWN_KEY = pygame.K_s  # Key for moving down
LEFT_KEY = pygame.K_a  # Key for moving left
RIGHT_KEY = pygame.K_d  # Key for moving right
PAUSE_KEY = pygame.K_ESCAPE  # Key for pausing the game

## Hard Game Constants

GAME_TITLE = "Snake Game"
# Snake movement speed
SNAKE_SPEED = 15  # Speed of the snake in the game

# Initial snake length
INITIAL_SNAKE_LENGTH = 3  # Starting length of the snake

# Game area dimensions
# Reduce the playable area by ~25% to avoid overly large windows on small screens.
# This keeps the game visible and leaves room for window controls.
GAME_WIDTH = 600  # Width of the game area in pixels (was 800)
GAME_HEIGHT = 600  # Height of the game area in pixels (was 800)

# Game area border
BORDER_SIZE = 5  # Size of the border around the game area in pixels

# Size of each grid cell
CELL_SIZE = 20  # Size of each cell in the game grid in pixels

# Frames per second
FPS = 30  # Frames per second for the game loop

# Directions
DIRECTIONS = {
    'UP': (0, -1),
    'DOWN': (0, 1),
    'LEFT': (-1, 0),
    'RIGHT': (1, 0)
}

# Game States
GAME_STATES = {
    'MENU': 0,
    'PLAYING': 1,
    'PAUSED': 2,
    'GAME_OVER': 3
}

# If SCREEN_WIDTH / SCREEN_HEIGHT were not set earlier, derive them to tightly
# fit the game area plus borders. This keeps the window from being excessively
# large by default while still allowing override at the top of this file.
# Add a bit of horizontal padding so the game area doesn't touch the window
# edges and there's space left/right for UI or window controls.
SIDE_PADDING = int(GAME_WIDTH * 0.25)  # ~25% extra horizontal space

if SCREEN_WIDTH is None:
    SCREEN_WIDTH = GAME_WIDTH + 2 * BORDER_SIZE + SIDE_PADDING
if SCREEN_HEIGHT is None:
    SCREEN_HEIGHT = GAME_HEIGHT + 2 * BORDER_SIZE