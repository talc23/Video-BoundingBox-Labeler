
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

    def get_yolo_repr(self):
        '''
        return a string of the Yolo represention
        :return:
        '''

        yoloRep = ''
        if self.label is '':
            yoloRep = 'Undefined class'
        else:
            yoloRep = str(self.label) + " "
            yoloRep += str(self.centerX) + " " \
                   + str(self.centerY) + " " \
                   + str(self.width) + " " \
                   + str(self.height)

        return yoloRep