from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty, DictProperty
from cfg.Colors import colors

class VideoLabelerScreen(BoxLayout):

    add_label = ObjectProperty(None)
    delete_label = ObjectProperty(None)
    add_bb = ObjectProperty(None)
    assign_label = ObjectProperty(None)
    bbs = ListProperty(None)
    labels = ListProperty(None)
    labelsColor = DictProperty(None)
    delete_all_bbs = ObjectProperty(None)
    delete_bb = ObjectProperty(None)

    availableColors = [colors.YELLOW, colors.BLUE, colors.GREEN, colors.PINK, colors.PURPLE]#, colors.WHITE]

    def __init__(self, **kwargs):
        super(VideoLabelerScreen, self).__init__(**kwargs)
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

    def load_movie(self, filename):
        self.ids.videoWidget.load(filename)
