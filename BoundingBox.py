from Geometry import Point2d
import unittest

class BoundingBox():
    def __init__(self, leftTop: Point2d, rightBottom: Point2d, id):
        '''
        Constructor
        :param center:
        :param width:
        :param height:
        '''
        self._center = None
        self._width = None
        self._height = None
        self._id = id
        self._label = None
        self.update(leftTop, rightBottom)

    def update(self, leftTop: Point2d, rightBottom: Point2d):
        '''
        Given left-top corner and right-bottom corner update the BoundingBox attributes
        :param leftTop:
        :param rightBottom:
        :return:
        '''
        self._center = Point2d((leftTop.x+rightBottom.x)/2., (leftTop.y+rightBottom.y)/2.)
        self._width = abs(leftTop.x - rightBottom.x)
        self._height = abs(leftTop.y - rightBottom.y)

    def set_label(self, label):
        self._label = label

    def get_yolo_repr(self):
        '''

        :return string representing yolo label:
        <object-class> <x> <y> <width> <height>
        '''
        yoloRep = str(self._label) + " "\
                + str(self._center.x) + " "\
                + str(self._center.y) + " " \
                + str(self._width) + " " \
                + str(self._height)

        return yoloRep

class TestBoundingBox(unittest.TestCase):
    def test_yolo_repr(self):
        bb = BoundingBox(Point2d(0.1, 0.2), Point2d(0.3, 0.7), 17)
        bb.set_label('labelX')
        ##fails because of precision....
        self.assertEqual(bb.get_yolo_repr(), 'labelX 0.2 0.45 0.2 0.5')

if __name__ == '__main__':
    unittest.main()