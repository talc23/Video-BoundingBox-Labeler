from kivy.uix.video import Video

class MyVideo(Video):
    def __init__(self, **kwargs):
        super(MyVideo, self).__init__(**kwargs)
        self.currentImage = None

    def Save_To_File(self, path):
        pass