from kivy.graphics import Line, Point, Color
from kivy.graphics.instructions import InstructionGroup
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ListProperty
from kivy import utils

import random

class YoBBWidget(Widget):
    labelCount = 0
    linepoints = ListProperty()
    labelName = StringProperty()
    labelId = StringProperty()
    groupColor = ListProperty([1,1,1])
    bbColor = StringProperty()

    def __init__(self, **kwargs):
        super(YoBBWidget, self).__init__(**kwargs)
        self.linepoints = []
        self.labelName = ""
        self.isUpdated = False
        self.groupColor = [1,1,1]
        # self.center

    def update(self, leftTop, size):
        self.linepoints = [leftTop[0], leftTop[1],
                       leftTop[0]+size[0], leftTop[1],
                       leftTop[0] + size[0], leftTop[1]+size[1],
                       leftTop[0], leftTop[1]+size[1],
                       leftTop[0], leftTop[1]]
        self.ids.labelname.pos = (self.linepoints[0], self.linepoints[1])
        self.ids.labelid.pos = (self.linepoints[6], self.linepoints[7])
        self._centerX = (float(leftTop[0]) + size[0] / 2) / self.parent.size[0]
        self._centerY = (float(leftTop[1]) + size[1] / 2) / self.parent.size[1]
        self._width   = float(size[0])/self.parent.size[0]
        self._height = float(size[1]) / self.parent.size[1]
        print(self.get_yolo_repr())
        if self.isUpdated is False:
            YoBBWidget.labelCount+=1
            self.labelId = str(self.labelCount)
            self.isUpdated = True

    def set_name(self, name):
        self.labelName = name

    def is_legal_size(self):
        if len(self.linepoints) < 8:
            return False
        width =  abs(self.linepoints[2]-self.linepoints[0])
        height = abs(self.linepoints[1] - self.linepoints[5])
        if width>20 and height>20:
            return True
        return False

    def get_yolo_repr(self):
        '''
        return a string of the Yolo represention
        :return:
        '''

        yoloRep = str(self.labelName) + " "\
                + str(self._centerX) + " "\
                + str(self._centerY) + " " \
                + str(self._width) + " " \
                + str(self._height)

        return yoloRep

class YoBBWidgetGroup():
    def __init__(self, name):
        self.yoBBWidgets = []
        self.color = Color(random.uniform(0,1),
                           random.uniform(0, 1),
                           random.uniform(0, 1))
        self.bbcodeColor = utils.get_hex_from_color(self.color.rgb)
        self.name = name

    def add_yobbwidget(self, yoLabel :YoBBWidget):
        if yoLabel in self.yoBBWidgets:
            print('error, yolabel already in list')
            return
        self.yoBBWidgets.append(yoLabel)
        yoLabel.groupColor = [self.color.r, self.color.g, self.color.b]
        yoLabel.bbColor = self.bbcodeColor
        yoLabel.labelName = self.name
        print(self.yoBBWidgets)

    def delete_yobbwidget(self, yoLabel :YoBBWidget):

        self.yoBBWidgets.remove(yoLabel)

    def is_empty(self):
        return len(self.yoBBWidgets) == 0

    def get_next_bb(self):
        if len(self.yoBBWidgets) > 0:
            return self.yoBBWidgets[0]
        return None

    def get_all_bbs(self):
        return self.yoBBWidgets