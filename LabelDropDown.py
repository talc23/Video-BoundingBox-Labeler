from kivy.uix.dropdown import DropDown
from kivy.properties import ObjectProperty
from kivy.uix.button import Button

class LabelDropDown(DropDown):
    add_label = ObjectProperty(None)
    dismissed = ObjectProperty(None)
    # def __init__(self, **kwargs):
    #     super(LabelDropDown, self).__init__(**kwargs)

    def add_buttons(self, list, on_release):
        for item in list:
            btn = LabelDropDownButton(text=str(item),
                                  released=on_release
                                  )
            self.add_widget(btn)

class LabelDropDownButton(Button):
    released = ObjectProperty(None)