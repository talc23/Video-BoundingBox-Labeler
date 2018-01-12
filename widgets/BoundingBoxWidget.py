from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy import utils
import numpy

from data.BoundingBox import BoundingBox

class BoundingBoxWidget(Widget):
    linepoints = ListProperty()
    labelName = StringProperty()
    labelId = StringProperty()
    bbColor = ListProperty([1,1,1])
    bbColorHex = StringProperty()
    _centerX = NumericProperty(0)
    _centerY = NumericProperty(0)

    def __init__(self, **kwargs):
        super(BoundingBoxWidget, self).__init__(**kwargs)
        self.linepoints = [0,0]
        self.labelName = ""
        self.shapeSize = [0,0]

    def on_touch_down (self, touch):
        leftTop = numpy.array((self.linepoints[0],self.linepoints[1]))
        touchPoint = numpy.array((touch.pos[0], touch.pos[1]))
        dist = numpy.linalg.norm(leftTop-touchPoint)
        print(dist)
        if dist<5:
            self.add_widget(CircleWidget(x=self.linepoints[0], y=self.linepoints[1]))

    def on_mouse_move(self, x, y, modifiers):
        leftTop = numpy.array((self.linepoints[0],self.linepoints[1]))
        touchPoint = numpy.array((x,y))
        dist = numpy.linalg.norm(leftTop-touchPoint)
        print(dist)
        if dist<5:
            self.add_widget(CircleWidget(x=self.linepoints[0], y=self.linepoints[1]))

    def on_bbColor(self, instance, value):
        self.bbColorHex = utils.get_hex_from_color(self.bbColor)


    def update_bb(self, boundingBox: BoundingBox):
        leftTop = [0, 0]
        size = [0, 0]
        size[0] = boundingBox.width * self.parent.size[0]
        size[1] = boundingBox.height * self.parent.size[1]
        leftTop[0] = boundingBox.centerX * self.parent.size[0] - size[0] / 2 + self.parent.pos[0]
        leftTop[1] = boundingBox.centerY * self.parent.size[1] + size[1] / 2 + self.parent.pos[1]
        self.labelId = str(boundingBox.id)
        self.update(leftTop, size)

    def update(self, leftTop, size):
        self.linepoints = [leftTop[0], leftTop[1],
                       leftTop[0]+size[0], leftTop[1],
                       leftTop[0] + size[0], leftTop[1]-size[1],
                       leftTop[0], leftTop[1]-size[1],
                       leftTop[0], leftTop[1]]
        self.ids.labelname.pos = (self.linepoints[0], self.linepoints[1])
        self.ids.labelid.pos = (self.linepoints[6], self.linepoints[7])
        self._centerX = (float(leftTop[0]) + float(size[0]) / 2 - self.parent.pos[0]) / self.parent.size[0]
        self._centerY = (float(leftTop[1]) - float(size[1]) / 2 - self.parent.pos[1]) / self.parent.size[1]
        self._width   = float(size[0])/self.parent.size[0]
        self._height = float(size[1]) / self.parent.size[1]
        #



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

        yoloRep = ''
        if self.labelName is '':
            yoloRep = 'Undefined class'
        else:
            yoloRep = str(self.labelName) + " "
        yoloRep += str(self._centerX) + " "\
                + str(self._centerY) + " " \
                + str(self._width) + " " \
                + str(self._height)

        return yoloRep


class CircleWidget():
    x = NumericProperty(None)
    y = NumericProperty(None)