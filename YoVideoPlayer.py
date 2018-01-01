from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.logger import Logger
from kivy.utils import get_color_from_hex
from Video import DrawableVideo
from Panels import BottomControlPanel
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, ListProperty, DictProperty, StringProperty
from Colors import colors


from BoundingBox import YoBBWidget

import os

class YoVideoPlayer(BoxLayout):
    add_bb = ObjectProperty(None)
    bbs = ListProperty(None)
    labelsColor = DictProperty(None)
    videoSource = StringProperty("")
    video_loaded = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(YoVideoPlayer, self).__init__(**kwargs)
        self.activeLabel = None
        self.workingAreaPath = r'C:\Labeler'
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

    def video_loaded(self):
        print('video_loaded')
        self.ids.videoSlider.disabled = False

    def on_bbs(self, instance, value):
        self.ids.videoplayer.bbs = self.bbs

    def video_player_touch_down(self, touch):
        Logger.debug('video pressed')
        videoWidget = self.ids.videoplayer
        if 'pos' not in touch.profile:
            return
        else:
            if videoWidget.collide_point(touch.pos[0], touch.pos[1]) is False:
                return
        if 'button' in touch.profile:
            isLeftButton = (touch.button == 'left')
            if isLeftButton:
                Logger.debug("Left button pressed")
                self.currentLabelLeftTop = touch.pos
                self.currentLabelPivot = touch.pos
                self.activeLabel = YoBBWidget()
                videoWidget.add_widget(self.activeLabel)
                self.activeLabel.bbColor=get_color_from_hex(colors.YELLOW)

    def video_player_move(self, touch):
        isLeftButton = False
        if self.activeLabel is None:
            return
        if 'pos' in touch.profile:
            videoWidget = self.ids.videoplayer
            Logger.debug('widget-' + str(self.size))
            Logger.debug('video-size:' + str(videoWidget.size) + ' pos:' + str(videoWidget.pos))
            Logger.debug('touch before: '+ str(touch.pos))
            if videoWidget.collide_point(touch.pos[0], touch.pos[1]) is False:
                Logger.debug('Out of screen')
                touchX = touch.pos[0]
                touchY = touch.pos[1]
                if (touch.pos[0]<videoWidget.pos[0]):
                    touchX=videoWidget.pos[0]
                elif (touch.pos[0]>videoWidget.pos[0]+videoWidget.size[0]):
                    touchX = videoWidget.pos[0]+videoWidget.size[0]
                if (touch.pos[1]<videoWidget.pos[1]):
                    touchY =videoWidget.pos[1]
                elif (touch.pos[1]>videoWidget.pos[1]+videoWidget.size[1]):
                    touchY = videoWidget.pos[1]+videoWidget.size[1]

                touch.pos = (touchX ,touchY)
            Logger.debug('touch after: ' + str(touch.pos))
            if self.currentLabelPivot is not None:
                xMin = min(self.currentLabelPivot[0], touch.pos[0])
                xMax = max(self.currentLabelPivot[0], touch.pos[0])
                yMin = min(self.currentLabelPivot[1], touch.pos[1])
                yMax = max(self.currentLabelPivot[1], touch.pos[1])

                self.currentLabelLeftTop = (xMin, yMin)
                self.currentLabelSize = (xMax-xMin, yMax-yMin)
                self.activeLabel.update(self.currentLabelLeftTop, self.currentLabelSize)

    def video_player_touch_up(self, touch):
        if self.activeLabel is not None:
            videoWidget = self.ids.videoplayer
            self.add_bb(self.activeLabel)
            videoWidget.remove_widget(self.activeLabel)
        self.currentLabelLeftTop = None
        self.currentLabelPivot = None
        self.activeLabel = None

    def video_position_changed(self, value):
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
            imageFileName = self.workingAreaPath + r'\image'+ str(self.savedDataIndex)+ '.png'
            bbFileName    = self.workingAreaPath + r'\image'+ str(self.savedDataIndex)+ '.txt'
            bbData = ''
            if self.ids.videoplayer.texture.save(imageFileName):
                self.savedDataIndex += 1
                for bbWidget in self.ids.videoplayer.children:
                   bbData += bbWidget.get_yolo_repr() + '\n'
                if len(bbData) != 0:
                    bbFile = open(bbFileName, 'w')
                    bbFile.write(bbData)
                    bbFile.close()
