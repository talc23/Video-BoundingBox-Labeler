from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.properties import ObjectProperty, ListProperty, DictProperty, StringProperty
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.videoplayer import VideoPlayer
from kivy.logger import Logger
import os
from YoVideoPlayer import YoVideoPlayer
from Panels import RightControlPanel
from BoundingBox import BoundingBox
from Colors import colors
from kivy.config import Config
import random
Config.set('graphics', 'fullscreen', 'auto')

class YoLabelerScreen(BoxLayout):
    add_label = ObjectProperty(None)
    add_bb = ObjectProperty(None)
    delete_label = ObjectProperty(None)
    assign_label = ObjectProperty(None)
    bbs = ListProperty(None)
    labels = ListProperty(None)
    labelsColor = DictProperty(None)

    availableColors = [colors.YELLOW, colors.BLUE, colors.GREEN, colors.PINK, colors.PURPLE]#, colors.WHITE]

    def __init__(self, **kwargs):
        super(YoLabelerScreen, self).__init__(**kwargs)
        self.AvailableColorIdx = list(range(0, len(self.availableColors)))

    def on_bbs(self, instance, value):
        self.ids.rightControlPanel.bbs = self.bbs
        self.ids.videoWidget.bbs = self.bbs

    def on_labels(self, instance, value):
        for label in self.labels:
            if label not in self.labelsColor.keys():
                if len(self.AvailableColorIdx) > 0:
                    idx = self.AvailableColorIdx.pop()
                    self.labelsColor[label] = self.availableColors[idx]
        self.ids.rightControlPanel.labels = self.labels

class YoLabelerApp(App):

    def __init__(self, **kwargs):
        super(YoLabelerApp, self).__init__(**kwargs)
        self.bbs = []
        self.labels = {}
        self.screen = None
        self.bbCounter = 0
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self.root)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def build(self):
        self.screen = YoLabelerScreen(add_label=self.add_label,
                                      delete_label=self.delete_label,
                                      add_bb= self.add_bbWidget,
                                      assign_label = self.assign_label)
        return self.screen

    def _keyboard_closed(self):
        if self._keyboard:
            self._keyboard.unbind(on_key_down=self._on_keyboard_down)
            self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'd':
            self.add_label('car')
            self.add_label('person')

            self.bbs.clear()
            bb = BoundingBox(0.35535714285714287, 0.32592592592592595, 0.44375, 1.0094650205761317, 0)
            self.add_bb(bb)
            bb2 = BoundingBox(0.12857142857142848, 0.28971193415637864, 0.8089285714285714, 0.7559670781893005, 1)
            self.add_bb(bb2)
            bb3 = BoundingBox(0.21964285714285714, 0.15617283950617286, 0.42232142857142857, 0.5601851851851852, 2)
            self.add_bb(bb3)
            self.add_bb(BoundingBox(0.14285714285714285, 0.18106995884773658, 0.6785714285714286, 0.4753086419753087, 3))
            self.add_bb(BoundingBox(0.1625, 0.27839506172839523, 0.12767857142857142, 0.7367283950617285, 4))
            self.assign_label(bb2, 'person')
            self.assign_label(bb, 'car')
            self.assign_label(bb3, 'person')
            self.assign_label(bb3, 'car')
            self._keyboard.unbind(on_key_down=self._on_keyboard_down)
            self._keyboard = None
        return True

    def assign_label(self, bb, label):
        print('assign_label bb:{} To label:{}'.format(str(bb), str(label)))
        bb.assign_label(label)
        self.screen.bbs = []
        self.screen.bbs = self.bbs


    def delete_label(self, newLabel):
        if newLabel is not "":
            if newLabel in self.labels.keys():
                print('delete Label='  + newLabel)
                self.labels.pop(newLabel)
                self.screen.labels = self.labels.keys()
            else:
                print(newLabel + 'is not defined')

    def add_bbWidget(self, bbWidget):
        if bbWidget.is_legal_size():
            bb = BoundingBox(bbWidget._width, bbWidget._height, bbWidget._centerX, bbWidget._centerY, self.bbCounter)
            self.add_bb(bb)

    def add_bb(self, bb):
        self.bbs.append(bb)
        self.bbCounter+=1
        self.screen.bbs = self.bbs

    def add_label(self, newLabel):
        if newLabel is not "":
            if newLabel not in self.labels.keys():
                self.labels[newLabel] = newLabel
                self.screen.labels = self.labels.keys()
            else:
                print(newLabel + 'is already defined')

if __name__ == '__main__':
    yoLabelerApp = YoLabelerApp()
    yoLabelerApp.run()

