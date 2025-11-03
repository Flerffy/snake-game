import pygame
import time
import threading
import traceback
from game_manager import GameManager
from menu import Menu


def _post_return_key(delay=0.8):
    """Wait `delay` seconds then post a RETURN keydown so the menu selects
    the default option and returns. This avoids the test blocking for input.
    """
    time.sleep(delay)
    ev = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})
    pygame.event.post(ev)


def smoke():
    print("[smoke] pygame.init()")
    pygame.init()
    print("[smoke] creating GameManager...")
    gm = GameManager()
    print("[smoke] GameManager created")
    menu = Menu(gm)
    print("[smoke] Menu created")

    # Start a background thread to post a RETURN after a short delay so the
    # menu returns and the test can continue.
    print("[smoke] starting helper thread to post RETURN key")
    t = threading.Thread(target=_post_return_key, args=(0.8,), daemon=True)
    t.start()

    try:
        print("[smoke] calling menu.display_main_menu()")
        # Display main menu (should return when the posted RETURN is delivered)
        menu.display_main_menu()
        print("[smoke] returned from display_main_menu()")

        # Run a couple of frames of the game loop to ensure no immediate errors
        start = time.time()
        frame = 0
        while gm.running and time.time() - start < 2.0:
            frame += 1
            print(f"[smoke] frame {frame}")
            gm.handle_events()
            gm.update()
            gm.draw()
            gm.clock.tick(30)

        print("Smoke test finished")
    except Exception as e:
        traceback.print_exc()
        print("SMOKE TEST FAILURE:", repr(e))
    finally:
        print("[smoke] pygame.quit()")
        pygame.quit()


if __name__ == "__main__":
    smoke()
