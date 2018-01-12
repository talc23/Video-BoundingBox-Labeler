from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.logger import Logger
from kivy.properties import BooleanProperty, ObjectProperty,\
    ListProperty, DictProperty, StringProperty
from widgets.Dialogs import LoadDialog
from kivy.app import App

import os

class DrawableVideoPlayer(BoxLayout):
    add_bb = ObjectProperty(None)
    bbs = ListProperty(None)
    labelsColor = DictProperty(None)
    videoSource = StringProperty("")
    video_loaded = ObjectProperty(None)
    isVideoLoaded    = BooleanProperty(False)
    load_movie = ObjectProperty(None)
    workAreaPath = StringProperty(None)

    def __init__(self, **kwargs):
        super(DrawableVideoPlayer, self).__init__(**kwargs)
        self.savedDataIndex = 0
        self.videoSliderPressed = False

    def load_movie(self):
        Logger.debug("Load Movie released")
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self.activePopup = Popup(title='Choose file to load...', content=content,
                                    size_hint=(0.9, 0.9))
        self.activePopup.open()

    def load(self, path, filename):
        fullPath = os.path.join(path, filename[0])
        self.videoSource = fullPath
        # self.ids.videoplayer.state = 'play'
        # self.ids.videoslider.disabled=False
        self.dismiss_popup()

    def dismiss_popup(self):
        self.activePopup.dismiss()
        self.activePopup = None

    def video_loaded(self, loaded):
        self.isVideoLoaded = loaded

    def on_bbs(self, instance, value):
        self.ids.videoplayer.bbs = self.bbs

    def on_position(self, value):
        if self.videoSliderPressed is False:
            self.ids.videoSlider.value = value

    def video_duration_changed(self, value):
        self.ids.videoSlider.max = value

    def video_slider_released(self, touch, value):
        if self.videoSliderPressed:
            self.ids.videoplayer.seek(value)
            self.videoSliderPressed = False

    def video_slider_pressed(self, touch):
        if self.ids.videoSlider.disabled is True:
            return
        if 'pos' in touch.profile:
            if self.ids.videoSlider.collide_point(touch.pos[0], touch.pos[1]) is False:
                return
        self.videoSliderPressed = True

    def video_state_changed(self, instance, value):
        print('video_state_changed' + value)
        self.video_state = value


    def save_screen(self):
        if self.ids.videoplayer.loaded:
            savePath = App.get_running_app().config.get('Settings', 'Folder')
            imageFileName =  savePath + r'\image'+ str(self.savedDataIndex)+ '.png'
            bbFileName    = savePath + r'\image'+ str(self.savedDataIndex)+ '.txt'
            bbData = ''
            if self.ids.videoplayer.texture.save(imageFileName):
                self.savedDataIndex += 1
                for bb in self.bbs:
                   bbData += bb.get_yolo_repr() + '\n'
                if len(bbData) != 0:
                    bbFile = open(bbFileName, 'w')
                    bbFile.write(bbData)
                    bbFile.close()
