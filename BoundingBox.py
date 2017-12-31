from kivy.graphics import Line, Point, Color
from kivy.graphics.instructions import InstructionGroup
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ListProperty
from kivy import utils

import random

class BoundingBox():
    def __init__(self, width, height, centerX, centerY, id):
        self.width = width
        self.height = height
        self.centerX = centerX
        self.centerY = centerY
        self.id = id
        self.label = ""

    def __str__(self):
        return "BoundingBox({}, {}, {}, {}, {})".format(self.width, self.height, self.centerX, self.centerY, self.id)

    def assign_label(self, label):
        self.label = label

class YoBBWidget(Widget):
    linepoints = ListProperty()
    labelName = StringProperty()
    labelId = StringProperty()
    bbColor = ListProperty([1,1,1])
    bbColorHex = StringProperty()

    def __init__(self, **kwargs):
        super(YoBBWidget, self).__init__(**kwargs)
        self.linepoints = [0,0]
        self.labelName = ""
        self.shapeSize = [0,0]
        # self.center

    def on_bbColor(self, instance, value):
        self.bbColorHex = utils.get_hex_from_color(self.bbColor)


    def to_string(self):
        return "YoBBWidget(labelName={}, labelId={}).update(({},{}), ({},{}))"\
            .format(self.labelName, self.labelId, self.linepoints[0], self.linepoints[1], self.shapeSize[0], self.shapeSize[1])

    def update_bb(self, boundingBox: BoundingBox):
        leftTop = [0, 0]
        size = [0, 0]
        size[0] = boundingBox.width * self.parent.size[0]
        size[1] = boundingBox.height * self.parent.size[1]
        leftTop[0] = boundingBox.centerX * self.parent.size[0] - size[0] / 2
        leftTop[1] = boundingBox.centerY * self.parent.size[1] - size[1] / 2
        self.labelId = str(boundingBox.id)
        self.update(leftTop, size)


    def update(self, leftTop, size):
        self.linepoints = [leftTop[0], leftTop[1],
                       leftTop[0]+size[0], leftTop[1],
                       leftTop[0] + size[0], leftTop[1]+size[1],
                       leftTop[0], leftTop[1]+size[1],
                       leftTop[0], leftTop[1]]
        self.shapeSize = size
        self.ids.labelname.pos = (self.linepoints[0], self.linepoints[1])
        self.ids.labelid.pos = (self.linepoints[6], self.linepoints[7])
        self._centerX = (float(leftTop[0]) + size[0] / 2) / self.parent.size[0]
        self._centerY = (float(leftTop[1]) + size[1] / 2) / self.parent.size[1]
        self._width   = float(size[0])/self.parent.size[0]
        self._height = float(size[1]) / self.parent.size[1]

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