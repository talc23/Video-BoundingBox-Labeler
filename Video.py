from kivy.uix.video import Video
from kivy.properties import ListProperty
from YoLabel import YoBBWidget
from kivy.clock import Clock
from functools import partial

class DrawableVideo(Video):
    bbs = ListProperty(None)
    def __init__(self, **kwargs):
        super(DrawableVideo, self).__init__(**kwargs)

    def on_size(self, instance, value):
        Clock.schedule_once(self.sched_on_bbs, 0)

    def sched_on_bbs(self,dt):
        self.on_bbs(None, None)

    def on_bbs(self, instance, value):
        self.clear_widgets()
        for bb in self.bbs:
            bbWidget = YoBBWidget(labelName="")
            self.add_widget(bbWidget)
            bbWidget.update_bb(bb)



