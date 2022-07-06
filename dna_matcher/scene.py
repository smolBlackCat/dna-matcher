import pygame.constants as constants
import pygame.draw as draw
import pygame.rect as rect
import pygame.surface as surface
import pygame.time as time

from . import effects, interface, utils


class Scene:
    """A base object for the creation of scenes in a screen."""

    def __init__(self, screen):
        """Initialises the Scene object.

        Args:

            screen:
                The Surface object where this scene will be drawn.
        """

        self.screen = screen
        self.screen_rect = screen.get_rect()

        # This variable is only filled when this scene is added to a
        # scene manager instance.
        self.scene_manager = None

        self.particles_groups = []

    def draw_particles(self):
        for particles_group in self.particles_groups:
            particles_group.draw(self.screen)

    def update_particles(self):
        for particles_group in self.particles_groups:
            if len(particles_group) == 0:
                self.particles_groups.remove(particles_group)
            particles_group.update()

    def draw(self):
        """It draws the components of this scene in the screen."""

        pass

    def update(self):
        """It updates the components everytime in the loop."""

        pass

    def update_on_event(self, event):
        """It updates the components if a event occur.

        Args:

            event:
                This is an object passed by the iteration, that is
                responsible for iterating all events
                (pygame.event.get()).
        """

        pass


class DebugScene(Scene):
    """Simple scene class that displays a white background. Mainly
    used to debug new stuff.
    """

    def __init__(self, screen):
        super().__init__(screen)

        self.bg = surface.Surface(self.screen.get_size())
        self.bg.fill((200, 200, 200))

        self.rect = self.bg.get_rect()
        self.rect.center = self.screen_rect.center

        # Do whatever you want here
        self.test_rect = rect.Rect(0, 0, 10, 10)
        self.test_rect.center = self.screen_rect.center

    def draw(self):
        self.screen.blit(self.bg, self.rect)
        draw.rect(self.screen, (0, 0, 180), self.test_rect)


class IntroScene(Scene):
    """A scene that shows the logo of the creator of the game."""

    END_INTRO = constants.USEREVENT + 1

    def __init__(self, screen):
        super().__init__(screen)

        self.logo_icon = interface.Label(
            screen, utils.load_image("game_intro/moura_cat.png"))
        self.logo_title = interface.Label(
            screen, utils.load_image("game_intro/logo_title.png"))

        self.logo_icon.rect.centerx = self.screen_rect.centerx
        self.logo_icon.rect.centery = self.screen_rect.centery

        self.logo_title.rect.centerx = self.screen_rect.centerx
        self.logo_title.rect.centery = self.screen_rect.centery + 74

        time.set_timer(IntroScene.END_INTRO, 3000, 1)

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.logo_icon.draw()
        self.logo_title.draw()

    def update_on_event(self, event):
        if event.type == IntroScene.END_INTRO:
            print("changing view")
            self.scene_manager.change_view(
                "main_menu",
                effects.FadeTransition(
                    self.screen, self.scene_manager, "main_menu",
                    (0, 0, 0), 4))


class SceneManager:
    """Manages the scenes in the main thread of the running game."""

    def __init__(self):
        """Initialises the scene manager object."""

        self.views = dict()
        self.on_transition = False
        self.fx_object = None
        self.current_view = None

    def add(self, view_name, scene_object):
        """Adds a view to the scene manager.

        Args:

            view_name:
                A name to the view. It will be used for example when
                a scene change is requested.

            scene_object:
                A object that contains all the components to be drawn
                on the screen.
        """

        scene_object.scene_manager = self
        self.views[view_name] = scene_object

    def show(self):
        """Shows the current view. This function may not have only
        one behavior
        """

        self.views[self.current_view].draw()
        if self.on_transition:
            self.fx_object.animate()

    def update(self):
        """It updates the components of the current scene in loop."""

        if not self.on_transition:
            self.views[self.current_view].update()

    def update_on_event(self, event):
        """It updates scenes based on events being read by the for
        loop.

        Args:

            event:
                A pygame Event object. This args is the event in the
                for loop, that is responsible for reading each
                event.
        """

        if not self.on_transition:
            self.views[self.current_view].update_on_event(event)

    def _change_view(self, view_name):
        """It changes the current view directly."""

        self.current_view = view_name

    def change_view(self, view_name, fx=None):
        """It changes the current scene with a special effect or
        not.

        Args:

            view_name:
                The codename of the view to be the new current_view.

            fx:
                A class that is responsible for a transition of
                views. When none, the view is changed abruptly
        """

        if view_name != self.current_view:
            if fx is not None:
                self.fx_object = fx
                self.on_transition = True
            else:
                # Changes the view abruptly.
                self._change_view(view_name)

    def initial_view(self, view_name):
        """Sets the initial view for the scene manager."""

        self.current_view = view_name
