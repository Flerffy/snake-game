import pygame
from constants import *
from objects import *
from utils import *
from game_manager import GameManager
from menu import Menu

# initialize game and open to Main Menu
def main():
    pygame.init()
    game_manager = GameManager()
    menu = Menu(game_manager)
    menu.display_main_menu()
    game_manager.run()
    pygame.quit()
if __name__ == "__main__":
    main()

# Once game is started, the game loop is handled here, game states are managed by game_manager.py

# Draw the game border around the game area
def draw_border(screen, theme):
    border_color = theme.get('border_color', (255, 255, 255))
    pygame.draw.rect(screen, border_color, 
                     (0, 0, GAME_WIDTH + 2 * BORDER_SIZE, BORDER_SIZE))  # Top
    pygame.draw.rect(screen, border_color, 
                     (0, GAME_HEIGHT + BORDER_SIZE, GAME_WIDTH + 2 * BORDER_SIZE, BORDER_SIZE))  # Bottom
    pygame.draw.rect(screen, border_color, 
                     (0, 0, BORDER_SIZE, GAME_HEIGHT + 2 * BORDER_SIZE))  # Left
    pygame.draw.rect(screen, border_color, 
                     (GAME_WIDTH + BORDER_SIZE, 0, BORDER_SIZE, GAME_HEIGHT + 2 * BORDER_SIZE))  # Right

# Draw the snake in the center of the game area
def draw_snake(screen, snake, theme):
    snake_color = theme.get('snake_color', (0, 255, 0))
    for segment in snake.segments:
        pygame.draw.rect(screen, snake_color, 
                         (segment.x, segment.y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, (0, 0, 0), 
                         (segment.x, segment.y, CELL_SIZE, CELL_SIZE), 1)  #
        
# Draw a food item at a random position within the game area
def draw_food(screen, food, theme):
    food_color = theme.get('food_color', (255, 0, 0))
    pygame.draw.rect(screen, food_color, 
                     (food.position.x, food.position.y, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, (0, 0, 0), 
                     (food.position.x, food.position.y, CELL_SIZE, CELL_SIZE), 1)  #

# Draw the current score at the top-left corner of the screen
def draw_score(screen, score, theme):
    font = pygame.font.SysFont(None, 36)
    text_color = theme.get('text_color', (255, 255, 255))
    score_surf = font.render(f"Score: {score}", True, text_color)
    screen.blit(score_surf, (BORDER_SIZE + 10, BORDER_SIZE + 10))


# Draw the pause overlay when the game is paused
def draw_pause_overlay(screen, theme):
    overlay_color = (0, 0, 0, 150)  # semi-transparent black
    overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
    overlay.fill(overlay_color)
    screen.blit(overlay, (BORDER_SIZE, BORDER_SIZE))

    font = pygame.font.SysFont(None, 72)
    text_color = theme.get('text_color', (255, 255, 255))
    pause_surf = font.render("PAUSED", True, text_color)
    pause_rect = pause_surf.get_rect(center=(BORDER_SIZE + GAME_WIDTH // 2, BORDER_SIZE + GAME_HEIGHT // 2))
    screen.blit(pause_surf, pause_rect)

# Draw the game over overlay when the game ends
# The game over overlay shows "GAME OVER" and the final score in the center of the screen.
# It uses a semi-transparent black overlay to dim the game area.
def draw_game_over_overlay(screen, score, theme):
    overlay_color = (0, 0, 0, 150)  # semi-transparent black
    overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
    overlay.fill(overlay_color)
    screen.blit(overlay, (BORDER_SIZE, BORDER_SIZE))

    font = pygame.font.SysFont(None, 72)
    text_color = theme.get('text_color', (255, 255, 255))
    game_over_surf = font.render("GAME OVER", True, text_color)
    game_over_rect = game_over_surf.get_rect(center=(BORDER_SIZE + GAME_WIDTH // 2, BORDER_SIZE + GAME_HEIGHT // 2 - 40))
    screen.blit(game_over_surf, game_over_rect)

    score_font = pygame.font.SysFont(None, 48)
    score_surf = score_font.render(f"Final Score: {score}", True, text_color)
    score_rect = score_surf.get_rect(center=(BORDER_SIZE + GAME_WIDTH // 2, BORDER_SIZE + GAME_HEIGHT // 2 + 40))
    screen.blit(score_surf, score_rect)
def draw(self):
        # simple clear using theme to avoid import-time drawing
        self.screen.fill(self.theme.get('background_color', (0, 0, 0)))
        pygame.display.flip()

