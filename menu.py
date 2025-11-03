import pygame
from constants import (
    ACTIVE_THEME,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    MENU_TITLE_FONT_SIZE,
    MENU_OPTION_FONT_SIZE,
    GAME_TITLE,
    FPS,
    GAME_STATES,
    UP_KEY,
    DOWN_KEY,
    MUSIC_VOLUME,
    SFX_VOLUME,
)

# If the project does not expose a list of supported resolutions, provide a
# small sensible default list so the graphics settings screen can function.
AVAILABLE_RESOLUTIONS = [
    (SCREEN_WIDTH, SCREEN_HEIGHT),
    (800, 600),
    (1024, 768),
]


class Menu:
    """Single, clean Menu implementation used by the game.

    The Menu only calls public GameManager methods and reads a few public
    attributes (screen, keys, running, state). It contains the main menu and
    settings screens (graphics, audio, controls).
    """

    def __init__(self, game_manager):
        self.game_manager = game_manager

    def _render_center(self, surf, text, y, font, color=None):
        color = color or ACTIVE_THEME["text_color"]
        ts = font.render(text, True, color)
        surf.blit(ts, (SCREEN_WIDTH // 2 - ts.get_width() // 2, y))

    def display_main_menu(self):
        options = [("Start Game", "start_game"), ("Settings", "settings"), ("Quit", "quit")]
        selected = 0
        screen = self.game_manager.screen
        clock = getattr(self.game_manager, "clock", pygame.time.Clock())
        title_font = pygame.font.Font(None, MENU_TITLE_FONT_SIZE)
        menu_font = pygame.font.Font(None, MENU_OPTION_FONT_SIZE)

        while self.game_manager.running and self.game_manager.state == GAME_STATES["MENU"]:
            # build option rects for mouse hit testing
            option_rects = []
            y = 250
            for label, _ in options:
                text_surf = menu_font.render(label, True, ACTIVE_THEME["text_color"])
                x = SCREEN_WIDTH // 2 - text_surf.get_width() // 2
                rect = pygame.Rect(x - 6, y - 4, text_surf.get_width() + 12, text_surf.get_height() + 6)
                option_rects.append(rect)
                y += MENU_OPTION_FONT_SIZE + 10

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_manager.quit_game()
                    return
                if event.type == pygame.KEYDOWN:
                    gm_keys = getattr(self.game_manager, "keys", {})
                    up_key = gm_keys.get("up", UP_KEY)
                    down_key = gm_keys.get("down", DOWN_KEY)
                    if event.key in (up_key, pygame.K_w, pygame.K_UP):
                        selected = (selected - 1) % len(options)
                    elif event.key in (down_key, pygame.K_s, pygame.K_DOWN):
                        selected = (selected + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        _, action = options[selected]
                        if action == "settings":
                            self.display_settings_menu()
                        elif action == "start_game":
                            self.game_manager.start_game()
                            return
                        elif action == "quit":
                            self.game_manager.quit_game()
                            return
                if event.type == pygame.MOUSEMOTION:
                    for i, r in enumerate(option_rects):
                        if r.collidepoint(event.pos):
                            selected = i
                            break
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, r in enumerate(option_rects):
                        if r.collidepoint(event.pos):
                            _, action = options[i]
                            if action == "settings":
                                self.display_settings_menu()
                            elif action == "start_game":
                                self.game_manager.start_game()
                                return
                            elif action == "quit":
                                self.game_manager.quit_game()
                                return

            # draw
            screen.fill(ACTIVE_THEME["background_color"])
            self._render_center(screen, GAME_TITLE, 100, title_font)
            y = 250
            for i, (label, _) in enumerate(options):
                color = (255, 255, 0) if i == selected else ACTIVE_THEME["text_color"]
                self._render_center(screen, label, y, menu_font, color)
                y += MENU_OPTION_FONT_SIZE + 10

            pygame.display.flip()
            clock.tick(FPS)

    def display_settings_menu(self):
        """Settings menu with Graphics / Audio / Controls / Back."""
        options = [("Graphics", "graphics"), ("Audio", "audio"), ("Controls", "controls"), ("Back", "back")]
        selected = 0
        screen = self.game_manager.screen
        clock = getattr(self.game_manager, "clock", pygame.time.Clock())
        title_font = pygame.font.Font(None, MENU_TITLE_FONT_SIZE)
        menu_font = pygame.font.Font(None, MENU_OPTION_FONT_SIZE)

        while self.game_manager.running and self.game_manager.state == GAME_STATES["MENU"]:
            option_rects = []
            y = 250
            for label, _ in options:
                text_surf = menu_font.render(label, True, ACTIVE_THEME["text_color"])
                x = SCREEN_WIDTH // 2 - text_surf.get_width() // 2
                rect = pygame.Rect(x - 6, y - 4, text_surf.get_width() + 12, text_surf.get_height() + 6)
                option_rects.append(rect)
                y += MENU_OPTION_FONT_SIZE + 10

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_manager.quit_game()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key in (UP_KEY, pygame.K_w, pygame.K_UP):
                        selected = (selected - 1) % len(options)
                    elif event.key in (DOWN_KEY, pygame.K_s, pygame.K_DOWN):
                        selected = (selected + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        _, action = options[selected]
                        if action == "graphics":
                            self.display_graphics_settings()
                        elif action == "audio":
                            self.display_audio_settings()
                        elif action == "controls":
                            self.display_control_settings()
                        elif action == "back":
                            return
                if event.type == pygame.MOUSEMOTION:
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint(event.pos):
                            selected = i
                            break
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint(event.pos):
                            _, action = options[i]
                            if action == "graphics":
                                self.display_graphics_settings()
                            elif action == "audio":
                                self.display_audio_settings()
                            elif action == "controls":
                                self.display_control_settings()
                            elif action == "back":
                                return

            # draw settings list
            screen.fill(ACTIVE_THEME["background_color"])
            self._render_center(screen, "Settings", 100, title_font)
            y = 250
            for i, (label, _) in enumerate(options):
                color = (255, 255, 0) if i == selected else ACTIVE_THEME["text_color"]
                self._render_center(screen, label, y, menu_font, color)
                y += MENU_OPTION_FONT_SIZE + 10

            pygame.display.flip()
            clock.tick(FPS)

    def display_audio_settings(self):
        screen = self.game_manager.screen
        clock = getattr(self.game_manager, "clock", pygame.time.Clock())
        title_font = pygame.font.Font(None, MENU_TITLE_FONT_SIZE)
        menu_font = pygame.font.Font(None, MENU_OPTION_FONT_SIZE)

        music = getattr(self.game_manager, "music_volume", MUSIC_VOLUME)
        sfx = getattr(self.game_manager, "sfx_volume", SFX_VOLUME)
        options = ["music", "sfx", "back"]
        selected = 0

        # slider geometry
        slider_width = 320
        slider_height = 8
        slider_x = SCREEN_WIDTH // 2 - slider_width // 2
        music_y = 260
        sfx_y = 310

        dragging = False
        drag_target = None  # 'music' | 'sfx' | None

        def draw_slider(vol, y, highlight=False):
            # bar
            bar_rect = pygame.Rect(slider_x, y, slider_width, slider_height)
            pygame.draw.rect(screen, (100, 100, 100), bar_rect)
            # fill
            fill_rect = pygame.Rect(slider_x, y, int(vol * slider_width), slider_height)
            pygame.draw.rect(screen, (50, 200, 50), fill_rect)
            # knob
            knob_x = slider_x + int(vol * slider_width)
            knob_rect = pygame.Rect(knob_x - 8, y - 6, 16, 20)
            pygame.draw.rect(screen, (220, 220, 220) if not highlight else (255, 255, 0), knob_rect)
            return bar_rect, knob_rect

        while self.game_manager.running and self.game_manager.state == GAME_STATES["MENU"]:
            # prepare a Back button rect for mouse hit-testing
            back_text = menu_font.render("Back", True, ACTIVE_THEME["text_color"])
            back_x = SCREEN_WIDTH // 2 - back_text.get_width() // 2
            back_y = 370
            back_rect = pygame.Rect(back_x - 6, back_y - 4, back_text.get_width() + 12,
                                    back_text.get_height() + 6)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_manager.quit_game()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key in (UP_KEY, pygame.K_w, pygame.K_UP):
                        selected = (selected - 1) % len(options)
                    elif event.key in (DOWN_KEY, pygame.K_s, pygame.K_DOWN):
                        selected = (selected + 1) % len(options)
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        if options[selected] == "music":
                            music = max(0.0, music - 0.05)
                            self.game_manager.adjust_music_volume(music)
                        elif options[selected] == "sfx":
                            sfx = max(0.0, sfx - 0.05)
                            self.game_manager.adjust_sfx_volume(sfx)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        if options[selected] == "music":
                            music = min(1.0, music + 0.05)
                            self.game_manager.adjust_music_volume(music)
                        elif options[selected] == "sfx":
                            sfx = min(1.0, sfx + 0.05)
                            self.game_manager.adjust_sfx_volume(sfx)
                    elif event.key == pygame.K_RETURN:
                        if options[selected] == "back":
                            return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    # check knobs and bars
                    m_bar, m_knob = draw_slider(music, music_y)
                    s_bar, s_knob = draw_slider(sfx, sfx_y)
                    if m_knob.collidepoint((mx, my)) or m_bar.collidepoint((mx, my)):
                        dragging = True
                        drag_target = "music"
                        # set immediately
                        rel = max(0, min(1, (mx - slider_x) / slider_width))
                        music = rel
                        self.game_manager.adjust_music_volume(music)
                    elif s_knob.collidepoint((mx, my)) or s_bar.collidepoint((mx, my)):
                        dragging = True
                        drag_target = "sfx"
                        rel = max(0, min(1, (mx - slider_x) / slider_width))
                        sfx = rel
                        self.game_manager.adjust_sfx_volume(sfx)
                    elif back_rect.collidepoint((mx, my)):
                        # clicked Back
                        return
                if event.type == pygame.MOUSEMOTION and dragging:
                    mx, my = event.pos
                    rel = max(0, min(1, (mx - slider_x) / slider_width))
                    if drag_target == "music":
                        music = rel
                        self.game_manager.adjust_music_volume(music)
                    elif drag_target == "sfx":
                        sfx = rel
                        self.game_manager.adjust_sfx_volume(sfx)
                if event.type == pygame.MOUSEMOTION and not dragging:
                    # highlight selection when hovering knobs/bars/back
                    mx, my = event.pos
                    # compute bar/knob rects (no drawing) for hit testing
                    m_bar_rect = pygame.Rect(slider_x, music_y, slider_width, slider_height)
                    m_knob_rect = pygame.Rect(slider_x + int(music * slider_width) - 8, music_y - 6, 16, 20)
                    s_bar_rect = pygame.Rect(slider_x, sfx_y, slider_width, slider_height)
                    s_knob_rect = pygame.Rect(slider_x + int(sfx * slider_width) - 8, sfx_y - 6, 16, 20)
                    if m_bar_rect.collidepoint((mx, my)) or m_knob_rect.collidepoint((mx, my)):
                        selected = 0
                    elif s_bar_rect.collidepoint((mx, my)) or s_knob_rect.collidepoint((mx, my)):
                        selected = 1
                    elif back_rect.collidepoint((mx, my)):
                        selected = 2
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    dragging = False
                    drag_target = None

            screen.fill(ACTIVE_THEME["background_color"])
            self._render_center(screen, "Audio Settings", 100, title_font)

            # draw sliders and labels
            music_label = f"Music: {int(music * 100)}%"
            sfx_label = f"SFX: {int(sfx * 100)}%"
            self._render_center(screen, music_label, music_y - 30, menu_font,
                                (255, 255, 0) if selected == 0 else None)
            self._render_center(screen, sfx_label, sfx_y - 30, menu_font,
                                (255, 255, 0) if selected == 1 else None)

            m_bar_rect, m_knob_rect = draw_slider(music, music_y, highlight=(selected == 0))
            s_bar_rect, s_knob_rect = draw_slider(sfx, sfx_y, highlight=(selected == 1))

            # draw back option
            self._render_center(screen, "Back", 370, menu_font, (255, 255, 0) if selected == 2 else None)

            pygame.display.flip()
            clock.tick(FPS)

    def display_graphics_settings(self):
        screen = self.game_manager.screen
        clock = getattr(self.game_manager, "clock", pygame.time.Clock())
        title_font = pygame.font.Font(None, MENU_TITLE_FONT_SIZE)
        menu_font = pygame.font.Font(None, MENU_OPTION_FONT_SIZE)

        # compute a current-resolution tuple safely and use it to find an index
        if hasattr(self.game_manager, "screen") and getattr(self.game_manager.screen, "get_height", None):
            cur_h = self.game_manager.screen.get_height()
        else:
            cur_h = SCREEN_HEIGHT
        current = (SCREEN_WIDTH, cur_h)
        try:
            idx = AVAILABLE_RESOLUTIONS.index(current)
        except Exception:
            idx = 0

        options = ["resolution", "fullscreen", "back"]
        selected = 0

        while self.game_manager.running and self.game_manager.state == GAME_STATES["MENU"]:
            # build option rects for mouse hit-testing
            option_rects = []
            y = 250
            labels = [
                f"Resolution: {AVAILABLE_RESOLUTIONS[idx][0]}x{AVAILABLE_RESOLUTIONS[idx][1]}",
                f"Fullscreen: {getattr(self.game_manager, 'fullscreen', False)}",
                "Back",
            ]
            for label in labels:
                surf = menu_font.render(label, True, ACTIVE_THEME["text_color"])
                rect = pygame.Rect(SCREEN_WIDTH // 2 - surf.get_width() // 2 - 6,
                                   y - 4,
                                   surf.get_width() + 12,
                                   surf.get_height() + 6)
                option_rects.append(rect)
                y += MENU_OPTION_FONT_SIZE + 10

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_manager.quit_game()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key in (UP_KEY, pygame.K_w, pygame.K_UP):
                        selected = (selected - 1) % len(options)
                    elif event.key in (DOWN_KEY, pygame.K_s, pygame.K_DOWN):
                        selected = (selected + 1) % len(options)
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        if options[selected] == "resolution":
                            idx = (idx - 1) % len(AVAILABLE_RESOLUTIONS)
                            self.game_manager.change_resolution(AVAILABLE_RESOLUTIONS[idx])
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        if options[selected] == "resolution":
                            idx = (idx + 1) % len(AVAILABLE_RESOLUTIONS)
                            self.game_manager.change_resolution(AVAILABLE_RESOLUTIONS[idx])
                    elif event.key == pygame.K_RETURN:
                        if options[selected] == "fullscreen":
                            self.game_manager.toggle_fullscreen()
                        elif options[selected] == "back":
                            return
                if event.type == pygame.MOUSEMOTION:
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint(event.pos):
                            selected = i
                            break
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint((mx, my)):
                            # map clicked index to option
                            opt = options[i]
                            if opt == "resolution":
                                idx = (idx + 1) % len(AVAILABLE_RESOLUTIONS)
                                self.game_manager.change_resolution(AVAILABLE_RESOLUTIONS[idx])
                            elif opt == "fullscreen":
                                self.game_manager.toggle_fullscreen()
                            elif opt == "back":
                                return
                            break
                    else:
                        # fallback: check y positions in case rect construction mismatched
                        # compute expected Ys (same layout as drawing)
                        y_positions = [250, 300, 350]
                        for i, y_pos in enumerate(y_positions):
                            h = MENU_OPTION_FONT_SIZE
                            if y_pos - h <= my <= y_pos + h:
                                opt = options[i]
                                if opt == "resolution":
                                    idx = (idx + 1) % len(AVAILABLE_RESOLUTIONS)
                                    self.game_manager.change_resolution(AVAILABLE_RESOLUTIONS[idx])
                                elif opt == "fullscreen":
                                    self.game_manager.toggle_fullscreen()
                                elif opt == "back":
                                    return
                                break

            screen.fill(ACTIVE_THEME["background_color"])
            self._render_center(screen, "Graphics Settings", 100, title_font)
            res_label = f"Resolution: {AVAILABLE_RESOLUTIONS[idx][0]}x{AVAILABLE_RESOLUTIONS[idx][1]}"
            self._render_center(screen, res_label, 250, menu_font, (255, 255, 0) if selected == 0 else None)
            fullscreen_label = f"Fullscreen: {getattr(self.game_manager, 'fullscreen', False)}"
            self._render_center(screen, fullscreen_label, 300, menu_font,
                                (255, 255, 0) if selected == 1 else None)
            self._render_center(screen, "Back", 350, menu_font, (255, 255, 0) if selected == 2 else None)

            pygame.display.flip()
            clock.tick(FPS)

    def display_control_settings(self):
        screen = self.game_manager.screen
        clock = getattr(self.game_manager, "clock", pygame.time.Clock())
        menu_font = pygame.font.Font(None, MENU_OPTION_FONT_SIZE)
        controls = ["up", "down", "left", "right", "pause", "back"]
        selected = 0
        listening = False

        while self.game_manager.running and self.game_manager.state == GAME_STATES["MENU"]:
            # build option rects for mouse hit-testing
            option_rects = []
            y = 200
            for i, ctl in enumerate(controls):
                display_label = "Back" if ctl == "back" else ctl.capitalize()
                surf = menu_font.render(display_label, True, ACTIVE_THEME["text_color"])
                rect = pygame.Rect(SCREEN_WIDTH // 2 - surf.get_width() // 2 - 6,
                                   y - 4,
                                   surf.get_width() + 12,
                                   surf.get_height() + 6)
                option_rects.append(rect)
                y += MENU_OPTION_FONT_SIZE + 8

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_manager.quit_game()
                    return
                if event.type == pygame.KEYDOWN:
                    if listening:
                        if selected < len(controls) - 1:
                            control = controls[selected]
                            self.game_manager.keys[control] = event.key
                            try:
                                self.game_manager.save_settings()
                            except Exception:
                                pass
                        listening = False
                    else:
                        up_key = getattr(self.game_manager, "keys", {}).get("up", UP_KEY)
                        down_key = getattr(self.game_manager, "keys", {}).get("down", DOWN_KEY)
                        if event.key in (up_key, pygame.K_w, pygame.K_UP):
                            selected = (selected - 1) % len(controls)
                        elif event.key in (down_key, pygame.K_s, pygame.K_DOWN):
                            selected = (selected + 1) % len(controls)
                        elif event.key == pygame.K_RETURN:
                            if controls[selected] == "back":
                                return
                            listening = True
                if event.type == pygame.MOUSEMOTION and not listening:
                    # highlight hovered option
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint(event.pos):
                            selected = i
                            break
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint((mx, my)):
                            # clicked this control
                            if controls[i] == "back":
                                return
                            # start listening to rebind this control
                            selected = i
                            listening = True
                            break

            # draw
            screen.fill(ACTIVE_THEME["background_color"])
            title_font = pygame.font.Font(None, MENU_TITLE_FONT_SIZE)
            self._render_center(screen, "Control Settings (Enter to rebind)", 100, title_font)
            y = 200
            for i, ctl in enumerate(controls):
                if ctl == "back":
                    # For the Back entry show just 'Back' centered (no number/colon/value)
                    text = "Back"
                else:
                    label = ctl.capitalize()
                    keyval = self.game_manager.keys.get(ctl, None)
                    value = pygame.key.name(keyval) if keyval is not None else "None"
                    text = f"{i+1}. {label}: {value}"
                color = (255, 255, 0) if i == selected else ACTIVE_THEME["text_color"]
                surf = menu_font.render(text, True, color)
                screen.blit(surf, (SCREEN_WIDTH // 2 - surf.get_width() // 2, y))
                y += MENU_OPTION_FONT_SIZE + 8

            if listening:
                info = menu_font.render("Press a key to bind...", True, (200, 200, 0))
                screen.blit(info, (SCREEN_WIDTH // 2 - info.get_width() // 2, y + 10))
            pygame.display.flip()
            clock.tick(FPS)
