import pygame
from game_manager import GameManager
from menu import Menu


def main():
    """Temporary clean entrypoint: initialize and run the GameManager via Menu."""
    pygame.init()
    game_manager = GameManager()
    menu = Menu(game_manager)
    menu.display_main_menu()
    game_manager.run()
    pygame.quit()


if __name__ == "__main__":
    main()
