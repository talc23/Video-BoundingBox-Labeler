from kivy.uix.video import Video
from kivy.properties import ListProperty, DictProperty, ObjectProperty
from BoundingBox import YoBBWidget
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from functools import partial

class DrawableVideo(Video):
    bbs = ListProperty(None)
    labelsColor = DictProperty(None)
    video_loaded = ObjectProperty(None)
    video_state_changed = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(DrawableVideo, self).__init__(**kwargs)

    def on_size(self, instance, value):
        Clock.schedule_once(self.sched_on_bbs, 0)

    def sched_on_bbs(self,dt):
        self.on_bbs(None, None)

    def on_loaded(self, inst, val):
        self.state = 'stop'
        self.video_loaded()

    def on_source(self, inst, val):
        # when source changes the move is set to play
        #on_loaded should stop it right it's loaded
        self.state = 'play'

    def on_bbs(self, instance, value):
        self.clear_widgets()
        for bb in self.bbs:
            bbWidget = YoBBWidget(labelName="")
            self.add_widget(bbWidget)
            bbWidget.update_bb(bb)
            bbWidget.set_name(bb.label)
            if bb.label in self.labelsColor:
                bbWidget.bbColor = get_color_from_hex(self.labelsColor[bb.label])
            else:
                bbWidget.bbColor = [1,1,1]

    def on_labelsColor(self, instance, value):
        self.clear_widgets()
        for bb in self.bbs:
            bbWidget = YoBBWidget(labelName="")
            self.add_widget(bbWidget)
            bbWidget.update_bb(bb)
            bbWidget.set_name(bb.label)
            if bb.label in self.labelsColor:
                bbWidget.bbColor = get_color_from_hex(self.labelsColor[bb.label])
            else:
                bbWidget.bbColor = [1,1,1]


    def stop_pressed(self):
        if self.loaded is False:
            return
        self.state = 'stop'

    def play_pause_pressed(self):
        if self.loaded is False:
            return
        if self.state is 'play':
            self.state = 'pause'
            # self.ids.playPauseButton.text = 'play'
        elif self.state is 'pause' or self.state is 'stop':
            self.state = 'play'
            # self.ids.playPauseButton.text = 'pause'