from pickle import NONE

from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty, StringProperty, DictProperty, OptionProperty
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

class RightControlPanel(StackLayout):
    labels = ListProperty(None)
    bbs = ListProperty(None)
    delete_bb = ObjectProperty(None)
    add_label = ObjectProperty(None)
    delete_label = ObjectProperty(None)
    assign_label = ObjectProperty(None)
    labelsColor = DictProperty(None)
    save_screen = ObjectProperty(None)
    clear_screen = ObjectProperty(None)
    delete_label_clicked = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(RightControlPanel,self).__init__(**kwargs)

    def delete_label_clicked(self, inst):
        self.dropdown = DropDown()
        for label in self.labels:
            btn = Button(text=str(label),
                         size_hint_y=None,
                         height=40,
                         background_color =  (1, 0, 0, 1),
                         background_normal= ''
                         )
            btn.bind(on_release=lambda btn: self.delete_label_choosed(self.dropdown, btn.text))
            self.dropdown.add_widget(btn)
            self.dropdown.auto_dismiss = True
        self.dropdown.open(inst)

    def on_labels(self, instance, value):
        if 'bbsStackLayout' not in self.ids:
            return
        self.ids.bbsStackLayout.clear_widgets()
        for bb in self.bbs:
            btn = bbEntryRightControlPanel(bb=bb,
                         labels = self.labels,
                         assign_label=self.assign_label,
                         delete_bb=self.delete_bb
                         )
            self.ids.bbsStackLayout.add_widget(btn)

    def on_bbs(self, instance, value):
        if 'bbsStackLayout' not in self.ids:
            return
        self.ids.bbsStackLayout.clear_widgets()
        for bb in self.bbs:
            btn = bbEntryRightControlPanel(bb=bb,
                         labels = self.labels,
                         assign_label=self.assign_label,
                         delete_bb=self.delete_bb
                         )
            self.ids.bbsStackLayout.add_widget(btn)

    def delete_label_choosed(self, dropdown,  labelName):
        self.delete_label(labelName)
        dropdown.dismiss()

class bbEntryRightControlPanel(BoxLayout):

    bb = ObjectProperty(None)
    labels = ListProperty(None)

    assign_label = ObjectProperty(None)
    delete_bb = ObjectProperty(None)

    bbId = StringProperty(None)
    bbLabel = StringProperty(None)

    def __init__(self, **kwargs):
        super(bbEntryRightControlPanel,self).__init__(**kwargs)

    def set_label_button_text(self):
        if self.bb.label:
            self.bbLabel = str(self.bb.label)
        else:
            self.bbLabel = "Undefined Label"

    def on_bb(self, instance, value):
        self.bbId = str(self.bb.id)
        self.set_label_button_text()

    def assign_label_clicked(self, inst):
        self.bbLabel = 'Choose label'
        self.dropdown = DropDown(on_dismiss=self.dropdown_dismissed)
        for label in self.labels:
            btn = Button(text=str(label),
                         size_hint_y=None,
                         height=40,
                         background_color =  (.8, .8, .3, 1),
                         background_normal= ''
                         )
            btn.bind(on_release=lambda btn: self.label_clicked(btn, self.bb))
            self.dropdown.add_widget(btn)
        self.dropdown.auto_dismiss = True
        self.dropdown.open(inst)

    def dropdown_dismissed(self, value):
        self.set_label_button_text()

    def label_clicked(self, inst, bb):
        if self.dropdown:
            self.dropdown.dismiss()
            self.set_label_button_text()

        self.assign_label(bb, inst.text)
        self.bbLabel = str(self.bb.label)

class BottomControlPanel(StackLayout):
    load_movie = ObjectProperty(None)
    play_pause_pressed = ObjectProperty(None)
    stop_pressed = ObjectProperty(None)
    video_state = StringProperty(None)
    def __init__(self, **kwargs):
        super(BottomControlPanel,self).__init__(**kwargs)

    def on_video_state(self, instance, value):
        if value is 'play':
            self.ids.playPauseButton.text = 'pause'
        else:
            self.ids.playPauseButton.text = 'play'
