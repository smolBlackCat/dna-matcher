import pygame.constants as constants
import pygame.draw as draw
import pygame.surface as surface
import pygame.time as time

from . import app, effects, interface, utils


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
        self.bg.fill((20, 20, 20))

        self.rect = self.bg.get_rect()
        self.rect.center = self.screen_rect.center

        self.load_sample1_label = interface.Label.from_text(screen, "No \"DNA\" sample selected yet.", (255, 255, 255), 18, 30, 1)
        self.load_sample1_label.rect.bottomleft = self.screen_rect.bottomleft
        self.load_sample1_label.rect.x += 10
        self.load_sample1_label.rect.y = 610
        self.load_sample1_button = interface.Button(screen,
            utils.load_image("matcher_view/load1_button_on.png"),
            utils.load_image("matcher_view/load1_button_off.png"),
            utils.load_image("matcher_view/load1_button_clicked.png"),
            lambda: self.load([100, 500], 0))
        self.load_sample1_button.rect.bottomleft = self.screen_rect.bottomleft
        self.load_sample1_button.rect.x += 10
        self.load_sample1_button.rect.y -= 10

        self.load_sample2_label = interface.Label.from_text(screen, "No \"DNA\" sample selected.", (255, 255, 255), 18, 30, 1)
        self.load_sample2_label.rect.bottomright = self.screen_rect.bottomright
        self.load_sample2_label.rect.x -= 10
        self.load_sample2_label.rect.y = self.load_sample1_label.rect.y
        self.load_sample2_button = interface.Button(screen,
            utils.load_image("matcher_view/load2_button_on.png"),
            utils.load_image("matcher_view/load2_button_off.png"),
            utils.load_image("matcher_view/load2_button_clicked.png"),
            lambda: self.load([784, 1127], 1))
        self.load_sample2_button.rect.bottomright = self.screen_rect.bottomright
        self.load_sample2_button.rect.x -= 10
        self.load_sample2_button.rect.y -= 10

        self.match_button = interface.Button(screen,
            utils.load_image("matcher_view/match_button_on.png"),
            utils.load_image("matcher_view/match_button_off.png"),
            utils.load_image("matcher_view/match_button_clicked.png"))
        self.match_button.rect.center = self.screen_rect.center
        self.match_button.rect.y = 620
        self.match_label = interface.Label.from_text(screen, "Fill all the sample's boxes", (255, 255, 255), 18, 30, 1)
        self.match_label.rect.centerx = self.screen_rect.centerx
        self.match_label.rect.top = self.match_button.rect.bottom
        self.match_label.rect.y += 10

        self.dna_samples = [None, None]

    def load(self, x_boundaries, index):
        path = app.fd("Select your sample")
        if path is None:
            return
        self.dna_samples[index] = app.DNA(self.screen, x_boundaries, path)

        if (not index):
            self.load_sample1_label.update_text("Ready and loaded")
        else:
            self.load_sample2_label.update_text("Ready and loaded")

    def draw(self):
        self.screen.blit(self.bg, self.rect)

        # Dividing lines
        draw.line(self.screen, (0, 102, 255), (640, 0), (640, 600), width=4)
        draw.line(self.screen, (0, 102, 255), (0, 600), (1280, 600), width=4)
        draw.line(self.screen, (0, 102, 255), (360, 600), (360, 768), width=4)
        draw.line(self.screen, (0, 102, 255), (965, 600), (965, 768), width=4)

        for dna in self.dna_samples:
            try:
                dna.draw()
            except AttributeError:
                continue

        # Buttons and Labels drawning.
        self.load_sample1_label.draw()
        self.load_sample1_button.draw()
        self.load_sample2_label.draw()
        self.load_sample2_button.draw()
        self.match_button.draw()
        self.match_label.draw()

    def update(self):
        self.load_sample1_button.update()
        self.load_sample2_button.update()
        self.match_button.update()

        if self.dna_samples[0] and self.dna_samples[1]:
            self.match_label.update_text("You are all free now.")
        
        for dna in self.dna_samples:
            try:
                dna.update()
            except AttributeError:
                continue

    def update_on_event(self, event):
        self.load_sample1_button.update_on_event(event)
        self.load_sample2_button.update_on_event(event)
        self.match_button.update_on_event(event)


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
                    (0, 0, 0), 24))


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
