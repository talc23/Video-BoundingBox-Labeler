from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.logger import Logger
from Dialogs import LoadDialog, SaveDialog, LabelDialog
from kivy.uix.widget import Widget
from copy import copy
import cv2


from YoLabel import YoBBWidget, YoBBWidgetGroup

import os

class YoVideoPlayer(BoxLayout):
    def __init__(self, **kwargs):
        super(YoVideoPlayer, self).__init__(**kwargs)
        self.activeLabel = None
        self.labelDropDown = None
        self.labelGroup = {}
        self.labelGroup['Undefined'] = YoBBWidgetGroup('Undefined')
        self.workingAreaPath = r'C:\Labeler'
        self.savedDataIndex = 0

    def VideoplayerTouchDown(self, touch):
        Logger.debug('video pressed')
        videoWidget = self.ids.videoplayer
        if self.labelDropDown is not None:
            return
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

    def VideoplayerMove(self, touch):
        isLeftButton = False
        if 'pos' in touch.profile:
            videoWidget = self.children[0].children[1]
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

    def VideoplayerTouchUp(self, touch):
        if self.activeLabel is not None and self.activeLabel.isUpdated:
            videoWidget = self.children[0].children[1]
            if self.activeLabel.is_legal_size() is False:
                videoWidget.remove_widget(self.activeLabel)
                self.activeLabel = None
                return
            else:
                self.labelGroup['Undefined'].add_yobbwidget(self.activeLabel)

                content = LabelDialog(assign_label=self.assign_label,
                                      delete_label=self.delete_label,
                                      add_label=self.add_label,
                                      bb = self.activeLabel,
                                      labels=self.labelGroup.keys(),
                                      cancel=self.dismiss_popup
                                      )
                self.activePopup = Popup(title='Choose label to bounding box', content=content,
                                            size_hint=(0.9, 0.9))
                self.activePopup.open()
        self.currentLabelLeftTop = None
        self.currentLabelPivot = None
        self.activeLabel = None

    def LoadMovie(self):
        Logger.debug("Load Movie released")
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self.activePopup = Popup(title='Choose file to load...', content=content,
                                    size_hint=(0.9, 0.9))
        self.activePopup.open()

    def load(self, path, filename):
        fullPath = os.path.join(path, filename[0])
        self.ids.videoplayer.source = fullPath
        # self.ids.videoplayer.state = 'play'
        self.dismiss_popup()

    def dismiss_popup(self):
        self.activePopup.dismiss()
        self.activePopup = None

    def StopPressed(self):
        self.ids.videoplayer.state = 'stop'

    def PlayPausePressed(self):
        if self.ids.videoplayer.state is 'play':
            self.ids.videoplayer.state = 'pause'
            self.ids.playPauseButton.text = 'play'
        elif self.ids.videoplayer.state is 'pause' or self.ids.videoplayer.state is 'stop':
            self.ids.videoplayer.state = 'play'
            self.ids.playPauseButton.text = 'pause'

    def save(self):
        if self.ids.videoplayer.loaded:
            imageFileName = self.workingAreaPath + r'\image'+ str(self.savedDataIndex)+ '.png'
            bbFileName    = self.workingAreaPath + r'\image'+ str(self.savedDataIndex)+ '.txt'
            bbData = ''
            if self.ids.videoplayer.texture.save(imageFileName):
                self.savedDataIndex += 1
                for key in self.labelGroup.keys():
                    bbList  = self.labelGroup[key].get_all_bbs()
                    for bb in bbList:
                        bbData += bb.get_yolo_repr() + '\n'
                if len(bbData) != 0:
                    bbFile = open(bbFileName, 'w')
                    bbFile.write(bbData)
                    bbFile.close()


    def clear_labels(self):
        Logger.debug('clear_labels pressed')
        videoWidget = self.children[0].children[1]
        for key in self.labelGroup.keys():
            while self.labelGroup[key].is_empty() is False:
                label = self.labelGroup[key].get_next_bb()
                self.labelGroup[key].delete_yobbwidget(label)
                videoWidget.remove_widget(label)

    def add_label(self, newLabel):
        if newLabel is not "":
            if newLabel not in self.labelGroup.keys():
                newGroup = YoBBWidgetGroup(newLabel)
                self.labelGroup[newLabel] = newGroup
                self.activePopup.content.update_labels(self.labelGroup.keys())
            else:
                print(newLabel + 'is already defined')

    def assign_label(self, bb: YoBBWidget, labelName):
        if labelName not in self.labelGroup.keys():
            return
        else:
            self.labelGroup[bb.labelName].delete_yobbwidget(bb)
            self.labelGroup[labelName].add_yobbwidget(bb)
            bb.labelName = labelName
            self.dismiss_popup()

    def delete_label(self, labelName):
        if labelName not in self.labelGroup.keys():
            return
        else:
            videoWidget = self.children[0].children[1]
            while self.labelGroup[labelName].is_empty() is False:
                label = self.labelGroup[labelName].get_next_bb()
                self.labelGroup[labelName].delete_yobbwidget(label)
                videoWidget.remove_widget(label)
            self.labelGroup.pop(labelName)
            self.activePopup.content.update_labels(self.labelGroup.keys())