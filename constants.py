import pygame
# Constants stored for game configuration and settings

## Configurable game settings

# Graphics settings
# Screen resolution (Default 1000x900)
SCREEN_WIDTH = 1000  # Width of the game window in pixels
SCREEN_HEIGHT = 900  # Height of the game window in pixels

# Windowed  (True by default)
WINDOWED_MODE = True  # True for windowed mode, False for fullscreen

# Fullscreen mode (False by default)
FULLSCREEN_MODE = False  # True for fullscreen mode, False for windowed

# Color Scheme (Light or Dark; Default Dark)
COLOR_SCHEME = 'Dark'  # Options: 'Light', 'Dark'

# Color values for Dark Theme
class DARK_THEME_COLORS:
    'background'== (30, 30, 30),
    'snake'== (0, 255, 0),
    'food'== (255, 0, 0),
    'border'== (255, 255, 255)

# Color values for Light Theme
class LIGHT_THEME_COLORS: 
    'background'== (220, 220, 220),
    'snake'== (0, 100, 0),
    'food'== (200, 0, 0),
    'border'== (0, 0, 0)

THEME_MAP = {
    'Dark': DARK_THEME_COLORS,
    'Light': LIGHT_THEME_COLORS
}
ACTIVE_THEME ='Dark'

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
GAME_WIDTH = 800  # Width of the game area in pixels
GAME_HEIGHT = 800  # Height of the game area in pixels

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