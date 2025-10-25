import pygame
from constants import *

# Draw game menu
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
    
# navigate menu options using W and S keys
def navigate_menu():
    selected_option = 0
    options = ['start_game', 'settings', 'quit']
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == UP_KEY:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == DOWN_KEY:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected_option]

# set selected text color to yellow
def highlight_selection(text_surface):
    highlighted_surface = text_surface.copy()
    highlighted_surface.fill((255, 255, 0), special_flags=pygame.BLEND_RGB_ADD)
    return highlighted_surface
            
# set game state to button pressed
def set_game_state(state, game_manager):
    if state == 'start_game':
        game_manager.start_game()
    elif state == 'settings':
        game_manager.open_settings()
    elif state == 'quit':
        game_manager.quit_game()

## Settings menu

# Draw settings menu with options for graphics, audio, and controls
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

    # navigate settings options using W and S keys
def navigate_settings_menu():
    selected_option = 0
    options = ['graphics', 'audio', 'controls', 'back']
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == UP_KEY:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == DOWN_KEY:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected_option]
                
    # set selected text color to yellow
def highlight_settings_selection(text_surface):
    highlighted_surface = text_surface.copy()
    highlighted_surface.fill((255, 255, 0), special_flags=pygame.BLEND_RGB_ADD)
    return highlighted_surface

# set game state to button pressed in settings menu
def set_settings_state(state, game_manager):
    if state == 'graphics':
        game_manager.open_graphics_settings()
    elif state == 'audio':
        game_manager.open_audio_settings()
    elif state == 'controls':
        game_manager.open_control_settings()
    elif state == 'back':
        game_manager.back_to_menu()

# Draw graphics settings menu
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

# navigate graphics settings options using W and S keys
def navigate_graphics_settings_menu():
    selected_option = 0
    options = ['resolution', 'fullscreen', 'back']
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == UP_KEY:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == DOWN_KEY:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected_option]

# set selected text color to yellow
def highlight_graphics_selection(text_surface):
    highlighted_surface = text_surface.copy()
    highlighted_surface.fill((255, 255, 0), special_flags=pygame.BLEND_RGB_ADD)
    return highlighted_surface

# Resolution option uses dropdown menu to select resolution from available options
# options: 10:9 aspect ratio resolutions
AVAILABLE_RESOLUTIONS = [(1200, 1080), (1000, 900), (800, 720), (600, 540), (400, 360)]

# press enter to select resolution
def set_graphics_state(state, game_manager):
    if state == 'resolution':
        game_manager.change_resolution(AVAILABLE_RESOLUTIONS)
    elif state == 'fullscreen':
        game_manager.toggle_fullscreen()
    elif state == 'back':
        game_manager.back_to_settings()

# Fullscreen option toggles between windowed and fullscreen modes when selected
def toggle_fullscreen_mode(game_manager):
    global FULLSCREEN_MODE
    FULLSCREEN_MODE = not FULLSCREEN_MODE
    game_manager.apply_graphics_settings()

# update graphics settings in constants.py to new resolution and fullscreen mode
def apply_graphics_settings(new_resolution, fullscreen_mode):
    global SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN_MODE
    SCREEN_WIDTH, SCREEN_HEIGHT = new_resolution
    FULLSCREEN_MODE = fullscreen_mode
    if FULLSCREEN_MODE:
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    else:
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.flip()

# pressing enter on Back to Settings returns to settings menu
def back_to_settings_menu(game_manager):
    game_manager.open_settings()

## Audio settings menu

# draw volume sliders with current volume level displayed
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

# update volume levels based on slider position
def set_audio_state(state, game_manager):
    if state == 'music_volume':
        game_manager.adjust_music_volume()
    elif state == 'sfx_volume':
        game_manager.adjust_sfx_volume()
    elif state == 'back':
        game_manager.back_to_settings()

## Controls settings menu

# draw current key bindings for movement and pause
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

# update key bindings based on user input
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




