from pickle import NONE

from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty, StringProperty, ReferenceListProperty
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

class RightControlPanel(StackLayout):
    labels = ListProperty(None)
    bbs = ListProperty(None)
    delete_label = ObjectProperty(None)
    add_label = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(RightControlPanel,self).__init__(**kwargs)

    def delete_label_clicked(self, inst):
        dropdown = DropDown()
        for label in self.labels:
            btn = Button(text=str(label),
                         size_hint_y=None,
                         height=40,
                         background_color =  (.8, .8, .3, 1),
                         background_normal= ''
                         )
            btn.bind(on_release=lambda btn: self.delete_label_choosed(dropdown, btn.text))
            dropdown.add_widget(btn)
        dropdown.auto_dismiss = True
        dropdown.open(inst)

    def on_bbs(self, instance, value):
        if 'bbsStackLayout' not in self.ids:
            return
        self.ids.bbsStackLayout.clear_widgets()
        for bb in self.bbs:
            btn = bbEntryRightControlPanel(bb=bb,
                         labels = self.labels,
                         assign_label=None
                         )
            self.ids.bbsStackLayout.add_widget(btn)
        self.ids.bbsStackLayout

    def delete_label_choosed(self, dropdown,  labelName):
        self.delete_label(labelName)
        dropdown.dismiss()

class bbEntryRightControlPanel(BoxLayout):
    bb = ObjectProperty(None)
    labels = ListProperty(None)
    assign_label = ObjectProperty(None)
    bbId = StringProperty(None)

    def __init__(self, **kwargs):
        super(bbEntryRightControlPanel,self).__init__(**kwargs)

    def on_bb(self, instance, value):
        self.bbId = str(self.bb.id)

    def assign_label_clicked(self):
        print('assign_label_clicked')

class BottomControlPanel(StackLayout):
    def __init__(self, **kwargs):
        super(BottomControlPanel,self).__init__(**kwargs)
