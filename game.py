import pygame
from constants import GAME_WIDTH, GAME_HEIGHT, BORDER_SIZE, CELL_SIZE
from game_manager import GameManager
from menu import Menu


def draw_border(screen, theme):
    """Draw the game border around the game area."""
    border_color = theme.get("border_color", (255, 255, 255))
    pygame.draw.rect(
        screen,
        border_color,
        (0, 0, GAME_WIDTH + 2 * BORDER_SIZE, BORDER_SIZE),
    )
    pygame.draw.rect(
        screen,
        border_color,
        (0, GAME_HEIGHT + BORDER_SIZE, GAME_WIDTH + 2 * BORDER_SIZE, BORDER_SIZE),
    )
    pygame.draw.rect(
        screen,
        border_color,
        (0, 0, BORDER_SIZE, GAME_HEIGHT + 2 * BORDER_SIZE),
    )
    pygame.draw.rect(
        screen,
        border_color,
        (GAME_WIDTH + BORDER_SIZE, 0, BORDER_SIZE, GAME_HEIGHT + 2 * BORDER_SIZE),
    )


def draw_snake(screen, snake, theme):
    """Draw the snake segments onto the given screen."""
    snake_color = theme.get("snake_color", (0, 255, 0))
    for segment in snake.segments:
        pygame.draw.rect(
            screen,
            snake_color,
            (
                BORDER_SIZE + segment.x * CELL_SIZE,
                BORDER_SIZE + segment.y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
            ),
        )


def main():
    """Start the game by showing the menu and running the manager."""
    pygame.init()
    game_manager = GameManager()
    menu = Menu(game_manager)
    menu.display_main_menu()
    game_manager.run()
    pygame.quit()


if __name__ == "__main__":
    main()