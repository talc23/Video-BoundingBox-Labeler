from kivy.uix.video import Video
from kivy.properties import ListProperty, DictProperty, ObjectProperty
from data.BoundingBox import YoBBWidget
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from cfg.Colors import colors

class DrawableVideo(Video):
    bbs = ListProperty(None)
    labelsColor = DictProperty(None)
    video_loaded = ObjectProperty(None)
    video_state_changed = ObjectProperty(None)
    add_bb = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(DrawableVideo, self).__init__(**kwargs)
        self.activeLabel = None

    def on_size(self, instance, value):
        Clock.schedule_once(self.sched_on_bbs, 0)

    def sched_on_bbs(self,dt):
        self.on_bbs(None, None)

    def on_loaded(self, inst, val):
        self.state = 'stop'
        self.video_loaded(val)

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

    def on_touch_down(self, touch):
        if 'pos' not in touch.profile:
            return False
        else:
            if self.collide_point(touch.pos[0], touch.pos[1]) is False:
                return False
        if 'button' in touch.profile:
            isLeftButton = (touch.button == 'left')
            if isLeftButton:
                self.currentLabelLeftTop = touch.pos
                self.currentLabelPivot = touch.pos
                self.activeLabel = YoBBWidget()
                self.add_widget(self.activeLabel)
                self.activeLabel.bbColor=get_color_from_hex(colors.YELLOW)

    def on_touch_move(self, touch):
        if self.activeLabel is None:
            return
        if 'pos' in touch.profile:
            if self.collide_point(touch.pos[0], touch.pos[1]) is False:
                touchX = touch.pos[0]
                touchY = touch.pos[1]
                if (touch.pos[0]<self.pos[0]):
                    touchX=self.pos[0]
                elif (touch.pos[0]>self.pos[0]+self.size[0]):
                    touchX = self.pos[0]+self.size[0]
                if (touch.pos[1]<self.pos[1]):
                    touchY =self.pos[1]
                elif (touch.pos[1]>self.pos[1]+self.size[1]):
                    touchY = self.pos[1]+self.size[1]

                touch.pos = (touchX ,touchY)
            if self.currentLabelPivot is not None:
                xMin = min(self.currentLabelPivot[0], touch.pos[0])
                xMax = max(self.currentLabelPivot[0], touch.pos[0])
                yMin = min(self.currentLabelPivot[1], touch.pos[1])
                yMax = max(self.currentLabelPivot[1], touch.pos[1])

                self.currentLabelLeftTop = (xMin, yMin)
                self.currentLabelSize = (xMax-xMin, yMax-yMin)
                self.activeLabel.update(self.currentLabelLeftTop, self.currentLabelSize)

    def on_touch_up(self, touch):
        if self.activeLabel is not None:
            self.add_bb(self.activeLabel)
            self.remove_widget(self.activeLabel)
        self.currentLabelLeftTop = None
        self.currentLabelPivot = None
        self.activeLabel = None
