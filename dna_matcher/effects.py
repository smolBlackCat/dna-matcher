import pygame.surface as surface


class Transition:
    """Base class that is responsible for creating smooth
    transitions.
    """

    def __init__(self, screen, scene_manager, next_view):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.scene_manager = scene_manager
        self.next_view = next_view

    def animate(self):
        pass

    def clean(self):
        """Always called in the end of the animate method."""

        self.scene_manager.on_transition = False
        self.fx_object = None


class FadeTransition(Transition):
    """Class responsible for manipulating the Surface in a way that
    the screens is fading.
    """

    def __init__(self, screen, scene_manager, next_view, fade_colour,
                 speed_factor=2):
        super().__init__(screen, scene_manager, next_view)
        self.scene_manager = scene_manager

        # Fade elements
        self.fade_bg = surface.Surface(screen.get_size())
        self.fade_bg.set_alpha(0)
        self.fade_bg.fill(fade_colour)
        self.rect = self.fade_bg.get_rect()
        self.rect.center = self.screen_rect.center

        # Fade params
        self.on_fade = True
        self.alpha = 0
        self.factor = speed_factor
        self.backwards = False
        self.c = 0

    def animate(self):
        """It fades the screen to the next view."""

        if self.on_fade:
            if self.c == 1:
                self.scene_manager.change_view(self.next_view)

            self.alpha += self.factor
            if (self.alpha > 255 and not self.backwards) \
                    or (self.alpha < 0 and self.backwards):
                self.backwards = not self.backwards
                self.factor *= -1
                self.c += 1

            self.fade_bg.set_alpha(self.alpha)
            self.screen.blit(self.fade_bg, self.rect)

            if self.c == 2:
                self.on_fade = False
        else:
            self.clean()


def floating_animation(*args):
    """Simulates a floating object with a given sprite rect.

    It utilises only three arguments: a component object, that is
    custom object like Label and Button, y_limit_bottom and
    y_limit_top respectively.
    """

    component = args[0]
    y_limit_bottom = args[1]
    y_limit_top = args[2]

    if component.rect.bottom >= y_limit_bottom \
            or component.rect.top <= y_limit_top:
        component.yspeed *= -1
    component.rect.y += component.yspeed
