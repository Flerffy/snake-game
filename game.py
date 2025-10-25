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

# Draw the snake in the center of the game area

# 