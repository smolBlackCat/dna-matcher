"""Pong game main function."""

import pygame

from . import scene, utils


def main() -> None:
    """Main Program."""

    pygame.init()

    # Pygame setup
    SCREEN_SIZE = (600, 400)

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SCREEN_SIZE)

    pygame.display.set_caption("DNA Matcher")
    pygame.display.set_icon(utils.load_image("icon.png"))

    # Game setup
    scene_manager = scene.SceneManager()
    intro_scene = scene.IntroScene(screen)
    debug_scene = scene.DebugScene(screen)
    scene_manager.add("game_intro", intro_scene)
    scene_manager.add("main_menu", debug_scene)
    scene_manager.initial_view("game_intro")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            scene_manager.update_on_event(event)

        # Game loop
        scene_manager.show()
        scene_manager.update()

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
