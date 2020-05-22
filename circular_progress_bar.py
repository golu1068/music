from kivy.uix.widget import Widget
from kivy.app import App
from kivy.core.text import Label
from kivy.lang.builder import Builder
from kivy.graphics import Line, Rectangle, Color, RoundedRectangle
from kivy.clock import Clock
from collections.abc import Iterable
from math import ceil

# This constant enforces the cap argument to be one of the caps accepted by the kivy.graphics.Line class
_ACCEPTED_BAR_CAPS = {"round", "none", "square"}

# Declare the defaults for the modifiable values
_DEFAULT_THICKNESS = 20
_DEFAULT_CAP_STYLE = 'round'
_DEFAULT_PRECISION = 100
_DEFAULT_PROGRESS_COLOUR = (1, 0, 0, 1)
_DEFAULT_BACKGROUND_COLOUR = (0.26, 0.26, 0.26, 1)
_DEFAULT_MAX_PROGRESS = 20
_DEFAULT_MIN_PROGRESS = 0
_DEFAULT_WIDGET_SIZE = 200
_DEFAULT_TEXT_LABEL = Label(text="{}%", font_size=40)

# Declare the defaults for the normalisation function, these are used in the textual representation (multiplied by 100)
_NORMALISED_MAX = 1
_NORMALISED_MIN = 0


class CircularProgressBar(Widget):
    def __init__(self, my_fb,**kwargs):
        super(CircularProgressBar, self).__init__(**kwargs)
        global fb
        fb = my_fb
        # Initialise the values modifiable via the class properties
        self._thickness = _DEFAULT_THICKNESS
        self._cap_style = _DEFAULT_CAP_STYLE
        self._cap_precision = _DEFAULT_PRECISION
        self._progress_colour = _DEFAULT_PROGRESS_COLOUR
        self._background_colour = _DEFAULT_BACKGROUND_COLOUR
        self._max_progress = _DEFAULT_MAX_PROGRESS
        self._min_progress = _DEFAULT_MIN_PROGRESS
        self._widget_size = _DEFAULT_WIDGET_SIZE
        self._text_label = _DEFAULT_TEXT_LABEL

        # Initialise the progress value to the minimum - gets overridden post init anyway
        self._value = _DEFAULT_MIN_PROGRESS

        # Store some label-related values to access them later
        self._default_label_text = _DEFAULT_TEXT_LABEL.text
        self._label_size = (0, 0)

        # Create some aliases to match the progress bar method names
        self.get_norm_value = self.get_normalised_progress
        self.set_norm_value = self.set_normalised_progress

    @property
    def thickness(self):
        return self._thickness

    @thickness.setter
    def thickness(self, value):
        if type(value) != int:
            raise TypeError("Circular bar thickness only accepts an integer value, not {}!".format(type(value)))
        elif value <= 0:
            raise ValueError("Circular bar thickness must be a positive integer, not {}!".format(value))
        else:
            self._thickness = value

    @property
    def cap_style(self):
        return self._cap_style

    @cap_style.setter
    def cap_style(self, value: str):
        if type(value) != str:
            raise TypeError("Bar line cap argument must be a string, not {}!".format(type(value)))
        value = value.lower().strip()
        if value not in _ACCEPTED_BAR_CAPS:
            raise ValueError("Bar line cap must be included in {}, and {} is not!".format(_ACCEPTED_BAR_CAPS, value))
        else:
            self._cap_style = value

    @property
    def cap_precision(self):
        return self._cap_precision

    @cap_precision.setter
    def cap_precision(self, value: int):
        if type(value) != int:
            raise TypeError("Circular bar cap precision only accepts an integer value, not {}!".format(type(value)))
        elif value <= 0:
            raise ValueError("Circular bar cap precision must be a positive integer, not {}!".format(value))
        else:
            self._cap_precision = value

    @property
    def progress_colour(self):
        return self._progress_colour

    @progress_colour.setter
    def progress_colour(self, value: Iterable):
        if not isinstance(value, Iterable):
            raise TypeError("Bar progress colour must be iterable (e.g. list, tuple), not {}!".format(type(value)))
        else:
            self._progress_colour = value

    @property
    def background_colour(self):
        return self._background_colour

    @background_colour.setter
    def background_colour(self, value: Iterable):
        if not isinstance(value, Iterable):
            raise TypeError("Bar background colour must be iterable (e.g. list, tuple), not {}!".format(type(value)))
        else:
            self._background_colour = value

    @property
    def max(self):
        return self._max_progress

    @max.setter
    def max(self, value: int):
        if type(value) != int:
            raise TypeError("Maximum progress only accepts an integer value, not {}!".format(type(value)))
        elif value <= self._min_progress:
            raise ValueError("Maximum progress - {} - must be greater than minimum progress ({})!"
                             .format(value, self._min_progress))
        else:
            self._max_progress = value

    @property
    def min(self):
        return self._min_progress

    @min.setter
    def min(self, value: int):
        if type(value) != int:
            raise TypeError("Minimum progress only accepts an integer value, not {}!".format(type(value)))
        elif value > self._max_progress:
            raise ValueError("Minimum progress - {} - must be smaller than maximum progress ({})!"
                             .format(value, self._max_progress))
        else:
            self._min_progress = value
            self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: int):
        if type(value) != int:
            raise TypeError("Progress must be an integer value, not {}!".format(type(value)))
        elif self._min_progress > value or value > self._max_progress:
            raise ValueError("Progress must be between minimum ({}) and maximum ({}), not {}!"
                             .format(self._min_progress, self._max_progress, value))
        elif value != self._value:
            self._value = value
            self._draw()

    @property
    def widget_size(self):
        return self._widget_size

    @widget_size.setter
    def widget_size(self, value: int):
        if type(value) != int:
            raise TypeError("Size of this widget must be an integer value, not {}!".format(type(value)))
        elif value <= 0:
            raise ValueError("Size of this widget must be a positive integer, not {}!".format(value))
        else:
            self._widget_size = value

    @property
    def label(self):
        return self._text_label

    @label.setter
    def label(self, value: Label):
        if not isinstance(value, Label):
            raise TypeError("Label must a kivy.graphics.Label, not {}!".format(type(value)))
        else:
            self._text_label = value
            self._default_label_text = value.text

    @property
    def value_normalized(self):
        """
        Alias the for getting the normalised progress.
        Matches the property name in kivy.uix.progressbar.ProgressBar.
        :return: Current progress normalised to match the percentage constants
        """
        return self.get_normalised_progress()

    @value_normalized.setter
    def value_normalized(self, value):
        """
        Alias the for getting the normalised progress.
        Matches the property name in kivy.uix.progressbar.ProgressBar.
        :return: Current progress normalised to match the percentage constants
        """
        self.set_normalised_progress(value)

    def _refresh_text(self):
        """
        Function used to refresh the text of the progress label.
        Additionally updates the variable tracking the label's texture size
        """
        self._text_label.text = self._default_label_text.format(str(int(self.get_normalised_progress() * 100)))
        self._text_label.refresh()
        self._label_size = self._text_label.texture.size

    def get_normalised_progress(self) -> float:
        """
        Function used to normalise the progress using the MIN/MAX normalisation
        :return: Current progress normalised to match the percentage constants
        """
        return _NORMALISED_MIN + (self._value - self._min_progress) * (_NORMALISED_MAX - _NORMALISED_MIN) \
            / (self._max_progress - self._min_progress)

    def set_normalised_progress(self, norm_progress: int):
        """
        Function used to set the progress value from a normalised value, using MIN/MAX normalisation
        :param norm_progress: Normalised value to update the progress with
        """
        if type(norm_progress) != float and type(norm_progress) != int:
            raise TypeError("Normalised progress must be a float or an integer, not {}!".format(type(norm_progress)))
        elif _NORMALISED_MIN > norm_progress or norm_progress > _NORMALISED_MAX:
            raise ValueError("Normalised progress must be between the corresponding min ({}) and max ({}), {} is not!"
                             .format(_NORMALISED_MIN, _NORMALISED_MAX, norm_progress))
        else:
            self.value = ceil(self._min_progress + (norm_progress - _NORMALISED_MIN) *
                              (self._max_progress - self._min_progress) / (_NORMALISED_MAX - _NORMALISED_MIN))

    def _draw(self):
        """
        Function used to draw the progress bar onto the screen.
        The drawing process is as follows:
            1. Clear the canvas
            2. Draw the background progress line (360 degrees)
            3. Draw the actual progress line (N degrees where n is between 0 and 360)
            4. Draw the textual representation of progress in the middle of the circle
        """
        global fb
        with self.canvas.after:
            self.canvas.clear()
            self._refresh_text()

            # Draw the background progress line
#            Color(*self.background_colour)
#            Line(circle=(self.pos[0] + self._widget_size / 2, self.pos[1] + self._widget_size / 2,
#                         self._widget_size / 2 - self._thickness), width=self._thickness)
#
            # Draw the progress line
#            Color(*self.progress_colour)
#            Line(circle=(self.pos[0] + self._widget_size / 2, self.pos[1] + self._widget_size / 2,
#                         self._widget_size / 2 - self._thickness, 0, self.get_normalised_progress() * 360),
#                 width=self._thickness, cap=self._cap_style, cap_precision=self._cap_precision)

            # Center and draw the progress text
#            Color(1, 1, 1, 1)
#            Rectangle(texture=self._text_label.texture, size=self._label_size,
#                      pos=(self._widget_size / 2 - self._label_size[0] / 2 + self.pos[0],
#                           self._widget_size / 2 - self._label_size[1] / 2 + self.pos[1]),
#                           source='images/image_2.jpg')
            
            Color(1,1,1,0.8)
            Line(circle=(fb.pos[0]+fb.size[0]/2, fb.pos[1]+fb.size[0]/2,fb.size[0]/2),width=2.5)
            
            Color(0.2,0,0.2,1)
            line = Line(circle=(fb.pos[0]+fb.size[0]/2, fb.pos[1]+fb.size[0]/2,fb.size[0]/2,0,self.get_normalised_progress() * 360),
                         width=2.5, cap=self._cap_style, cap_precision=self._cap_precision)
            
#class _Example(App):
#
#    # Simple animation to show the circular progress bar in action
#    def animate(self, dt):
#        bar = self.root.children[-1]
#        if bar.value < bar.max:
#            bar.value_normalized += 0.01
#        else:
#            bar.value_normalized = 0
#
#    # Simple layout for easy example
#    def build(self):
#
#        lyt = FloatLayout()
#        cpb = CircularProgressBar()
#        lyt.add_widget(cpb)
#        # Animate the progress bar
#        Clock.schedule_interval(self.animate, 1)
#        return lyt
