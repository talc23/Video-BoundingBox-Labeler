from kivy.uix.videoplayer import VideoPlayer

from kivy.app import App

class MyVideoPlayer(VideoPlayer):
    def __init__(self):
        super(MyVideoPlayer, self).__init__()


class YoLabelerApp(App):
    def build(self):
        screen = MyVideoPlayer()
        return screen

if __name__ == '__main__':
    YoLabelerApp().run()