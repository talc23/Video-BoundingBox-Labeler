from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.videoplayer import VideoPlayer
from kivy.logger import Logger
from kivy.graphics import Rectangle
from kivy.graphics import Line, Color
from kivy.uix.popup import Popup
import os
from YoVideoPlayer import YoVideoPlayer

class YoLabelerScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(YoLabelerScreen, self).__init__(**kwargs)

class YoLabelerApp(App):
    def build(self):
        screen = YoLabelerScreen()
        return screen

if __name__ == '__main__':
    YoLabelerApp().run()