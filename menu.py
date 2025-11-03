import pygame
from constants import *


# Keep functional drawing helpers but provide a Menu wrapper class so
# `game.py` can construct a Menu instance and call `display_main_menu()`.

def draw_menu(screen):
    screen.fill(ACTIVE_THEME['background_color'])
    font = pygame.font.Font(None, 48)
    title_text = font.render(GAME_TITLE, True, ACTIVE_THEME['text_color'])
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

    menu_font = pygame.font.Font(None, 36)
    start_text = menu_font.render('1. Start Game', True, ACTIVE_THEME['text_color'])
    settings_text = menu_font.render('2. Settings', True, ACTIVE_THEME['text_color'])
    quit_text = menu_font.render('3. Quit', True, ACTIVE_THEME['text_color'])
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 250))
    screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 300))
    pygame.display.flip()


def navigate_menu():
    selected_option = 0
    options = ['start_game', 'settings', 'quit']
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == UP_KEY:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == DOWN_KEY:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected_option]


def highlight_selection(text_surface):
    highlighted_surface = text_surface.copy()
    highlighted_surface.fill((255, 255, 0), special_flags=pygame.BLEND_RGB_ADD)
    return highlighted_surface


def set_game_state(state, game_manager):
    if state == 'start_game':
        game_manager.start_game()
    elif state == 'settings':
        game_manager.open_settings()
    elif state == 'quit':
        game_manager.quit_game()


def draw_settings_menu(screen):
    screen.fill(ACTIVE_THEME['background_color'])
    font = pygame.font.Font(None, 48)
    title_text = font.render('Settings', True, ACTIVE_THEME['text_color'])
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

    settings_font = pygame.font.Font(None, 36)
    graphics_text = settings_font.render('1. Graphics', True, ACTIVE_THEME['text_color'])
    audio_text = settings_font.render('2. Audio', True, ACTIVE_THEME['text_color'])
    controls_text = settings_font.render('3. Controls', True, ACTIVE_THEME['text_color'])
    back_text = settings_font.render('4. Back to Menu', True, ACTIVE_THEME['text_color'])
    screen.blit(graphics_text, (SCREEN_WIDTH // 2 - graphics_text.get_width() // 2, 250))
    screen.blit(audio_text, (SCREEN_WIDTH // 2 - audio_text.get_width() // 2, 300))
    screen.blit(controls_text, (SCREEN_WIDTH // 2 - controls_text.get_width() // 2, 350))
    screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, 400))
    pygame.display.flip()


def navigate_settings_menu():
    selected_option = 0
    options = ['graphics', 'audio', 'controls', 'back']
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'back'
            if event.type == pygame.KEYDOWN:
                if event.key == UP_KEY:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == DOWN_KEY:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected_option]


def highlight_settings_selection(text_surface):
    highlighted_surface = text_surface.copy()
    highlighted_surface.fill((255, 255, 0), special_flags=pygame.BLEND_RGB_ADD)
    return highlighted_surface


def set_settings_state(state, game_manager):
    if state == 'graphics':
        game_manager.open_graphics_settings()
    elif state == 'audio':
        game_manager.open_audio_settings()
    elif state == 'controls':
        game_manager.open_control_settings()
    elif state == 'back':
        game_manager.back_to_menu()


def draw_graphics_settings_menu(screen):
    screen.fill(ACTIVE_THEME['background_color'])
    font = pygame.font.Font(None, 48)
    title_text = font.render('Graphics Settings', True, ACTIVE_THEME['text_color'])
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

    settings_font = pygame.font.Font(None, 36)
    resolution_text = settings_font.render('1. Resolution', True, ACTIVE_THEME['text_color'])
    fullscreen_text = settings_font.render('2. Fullscreen Mode', True, ACTIVE_THEME['text_color'])
    back_text = settings_font.render('3. Back to Settings', True, ACTIVE_THEME['text_color'])
    screen.blit(resolution_text, (SCREEN_WIDTH // 2 - resolution_text.get_width() // 2, 250))
    screen.blit(fullscreen_text, (SCREEN_WIDTH // 2 - fullscreen_text.get_width() // 2, 300))
    screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, 350))
    pygame.display.flip()


def navigate_graphics_settings_menu():
    selected_option = 0
    options = ['resolution', 'fullscreen', 'back']
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'back'
            if event.type == pygame.KEYDOWN:
                if event.key == UP_KEY:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == DOWN_KEY:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected_option]


def highlight_graphics_selection(text_surface):
    highlighted_surface = text_surface.copy()
    highlighted_surface.fill((255, 255, 0), special_flags=pygame.BLEND_RGB_ADD)
    return highlighted_surface


# Resolution option uses dropdown menu to select resolution from available options
# options: 10:9 aspect ratio resolutions
AVAILABLE_RESOLUTIONS = [(1200, 1080), (1000, 900), (800, 720), (600, 540), (400, 360)]


def set_graphics_state(state, game_manager):
    if state == 'resolution':
        # choose first available as a fallback
        game_manager.change_resolution(AVAILABLE_RESOLUTIONS)
    elif state == 'fullscreen':
        game_manager.toggle_fullscreen()
    elif state == 'back':
        game_manager.back_to_settings()


def toggle_fullscreen_mode(game_manager):
    # prefer using GameManager.toggle_fullscreen which updates display
    game_manager.toggle_fullscreen()


def apply_graphics_settings(new_resolution, fullscreen_mode):
    # convenience helper that uses pygame directly; menu uses GameManager methods
    global SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN_MODE
    SCREEN_WIDTH, SCREEN_HEIGHT = new_resolution
    FULLSCREEN_MODE = fullscreen_mode
    if FULLSCREEN_MODE:
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    else:
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.flip()


def back_to_settings_menu(game_manager):
    game_manager.open_settings()


def draw_audio_settings_menu(screen, music_volume, sfx_volume):
    screen.fill(ACTIVE_THEME['background_color'])
    font = pygame.font.Font(None, 48)
    title_text = font.render('Audio Settings', True, ACTIVE_THEME['text_color'])
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

    settings_font = pygame.font.Font(None, 36)
    music_text = settings_font.render(f'1. Music Volume: {int(music_volume * 100)}%', True, ACTIVE_THEME['text_color'])
    sfx_text = settings_font.render(f'2. SFX Volume: {int(sfx_volume * 100)}%', True, ACTIVE_THEME['text_color'])
    back_text = settings_font.render('3. Back to Settings', True, ACTIVE_THEME['text_color'])
    screen.blit(music_text, (SCREEN_WIDTH // 2 - music_text.get_width() // 2, 250))
    screen.blit(sfx_text, (SCREEN_WIDTH // 2 - sfx_text.get_width() // 2, 300))
    screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, 350))
    pygame.display.flip()


def set_audio_state(state, game_manager):
    if state == 'music_volume':
        game_manager.adjust_music_volume()
    elif state == 'sfx_volume':
        game_manager.adjust_sfx_volume()
    elif state == 'back':
        game_manager.back_to_settings()


def draw_control_settings_menu(screen, up_key, down_key, left_key, right_key, pause_key):
    screen.fill(ACTIVE_THEME['background_color'])
    font = pygame.font.Font(None, 48)
    title_text = font.render('Control Settings', True, ACTIVE_THEME['text_color'])
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

    settings_font = pygame.font.Font(None, 36)
    up_text = settings_font.render(f'1. Up: {pygame.key.name(up_key)}', True, ACTIVE_THEME['text_color'])
    down_text = settings_font.render(f'2. Down: {pygame.key.name(down_key)}', True, ACTIVE_THEME['text_color'])
    left_text = settings_font.render(f'3. Left: {pygame.key.name(left_key)}', True, ACTIVE_THEME['text_color'])
    right_text = settings_font.render(f'4. Right: {pygame.key.name(right_key)}', True, ACTIVE_THEME['text_color'])
    pause_text = settings_font.render(f'5. Pause: {pygame.key.name(pause_key)}', True, ACTIVE_THEME['text_color'])
    back_text = settings_font.render('6. Back to Settings', True, ACTIVE_THEME['text_color'])
    screen.blit(up_text, (SCREEN_WIDTH // 2 - up_text.get_width() // 2, 200))
    screen.blit(down_text, (SCREEN_WIDTH // 2 - down_text.get_width() // 2, 250))
    screen.blit(left_text, (SCREEN_WIDTH // 2 - left_text.get_width() // 2, 300))
    screen.blit(right_text, (SCREEN_WIDTH // 2 - right_text.get_width() // 2, 350))
    screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, 400))
    screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, 450))
    pygame.display.flip()


def set_control_state(state, game_manager):
    if state == 'up_key':
        game_manager.rebind_key('up')
    elif state == 'down_key':
        game_manager.rebind_key('down')
    elif state == 'left_key':
        game_manager.rebind_key('left')
    elif state == 'right_key':
        game_manager.rebind_key('right')
    elif state == 'pause_key':
        game_manager.rebind_key('pause')
    elif state == 'back':
        game_manager.back_to_settings()


class Menu:
    """Small Menu wrapper so callers can use an object and avoid
    depending on top-level functions directly.
    """

    def __init__(self, game_manager):
        self.game_manager = game_manager

    def display_main_menu(self):
        # Interactive main menu: redraws on selection change and responds to
        # both WASD and arrow keys. Press Enter to select.
        options = [
            ("Start Game", 'start_game'),
            ("Settings", 'settings'),
            ("Quit", 'quit'),
        ]
        selected = 0
        screen = self.game_manager.screen
        clock = getattr(self.game_manager, 'clock', pygame.time.Clock())
        # Use the constants for title/option font sizes
        title_font = pygame.font.Font(None, MENU_TITLE_FONT_SIZE)
        menu_font = pygame.font.Font(None, MENU_OPTION_FONT_SIZE)

        while self.game_manager.running and self.game_manager.state == GAME_STATES['MENU']:
            # Use the pre-created fonts from above (sizes come from constants)
            # Prepare and compute option rects so we can check mouse events

            # Precompute option rectangles (including padding) for mouse hit testing
            option_rects = []
            y = 250
            for i, (label, _) in enumerate(options):
                text_surf = menu_font.render(label, True, ACTIVE_THEME['text_color'])
                x = SCREEN_WIDTH // 2 - text_surf.get_width() // 2
                # hit-rect uses small padding but we won't draw a background rectangle;
                # this keeps mouse targeting slightly forgiving while highlighting only text.
                rect = pygame.Rect(x - 6, y - 4, text_surf.get_width() + 12, text_surf.get_height() + 6)
                option_rects.append(rect)
                y += MENU_OPTION_FONT_SIZE + 10

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_manager.quit_game()
                    return
                # keyboard navigation
                if event.type == pygame.KEYDOWN:
                    if event.key in (UP_KEY, pygame.K_w, pygame.K_UP):
                        selected = (selected - 1) % len(options)
                    elif event.key in (DOWN_KEY, pygame.K_s, pygame.K_DOWN):
                        selected = (selected + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        label, action = options[selected]
                        set_game_state(action, self.game_manager)
                        if action in ('start_game', 'quit'):
                            return

                # mouse movement: highlight hovered option
                if event.type == pygame.MOUSEMOTION:
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint(event.pos):
                            selected = i
                            break

                # mouse click: select option
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint(event.pos):
                            label, action = options[i]
                            set_game_state(action, self.game_manager)
                            if action in ('start_game', 'quit'):
                                return

            # draw menu with highlight
            screen.fill(ACTIVE_THEME['background_color'])
            title_text = title_font.render(GAME_TITLE, True, ACTIVE_THEME['text_color'])
            screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

            # draw options using the precomputed rects; highlight by changing text color only
            y = 250
            for i, (label, _) in enumerate(options):
                text_color = ACTIVE_THEME['text_color']
                if i == selected:
                    text_surf = menu_font.render(label, True, (255, 255, 0))
                else:
                    text_surf = menu_font.render(label, True, text_color)
                x = SCREEN_WIDTH // 2 - text_surf.get_width() // 2
                screen.blit(text_surf, (x, y))
                y += MENU_OPTION_FONT_SIZE + 10

            pygame.display.flip()
            clock.tick(FPS)




