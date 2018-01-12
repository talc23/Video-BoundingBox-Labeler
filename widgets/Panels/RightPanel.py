from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, ObjectProperty, ListProperty, StringProperty, DictProperty
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown


class ScreenControlPanel(StackLayout):
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
    isAllBBsAssigned = BooleanProperty(False)
    isVideoLoaded    = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(ScreenControlPanel, self).__init__(**kwargs)

    def _delete_label_clicked(self, inst):
        '''
        activates when a boundingbox label is clicked
        :param inst:
        :return:
        '''
        if len(self.labels) is 0:
            return
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

    def save_screen_clicked(self, inst):
        if self.isVideoLoaded is False:
            return
        self.save_screen()

    def confirm_save(self, inst, confirm):
        if confirm:
            self.save_screen()
        inst.parent.remove_widget(inst)

    def on_bbs(self, instance, value):
        if 'bbsStackLayout' not in self.ids:
            return
        self.ids.bbsStackLayout.clear_widgets()
        self.isAllBBsAssigned = True
        for bb in self.bbs:
            if bb.label is None or bb.label is "":
                self.isAllBBsAssigned = False
            btn = bbEntryRightControlPanel(size_hint=(1,.1),
                                           bb=bb,
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