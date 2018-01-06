from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty, StringProperty

class BottomControlPanel(StackLayout):
    load_movie = ObjectProperty(None)
    play_pause_pressed = ObjectProperty(None)
    stop_pressed = ObjectProperty(None)
    video_state = StringProperty(None)
    def __init__(self, **kwargs):
        super(BottomControlPanel,self).__init__(**kwargs)

    def on_video_state(self, instance, value):
        if value is 'play':
            self.ids.playPauseButton.text = 'pause'
        else:
            self.ids.playPauseButton.text = 'play'
