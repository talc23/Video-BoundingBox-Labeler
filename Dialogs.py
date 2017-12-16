from kivy.properties import ObjectProperty, ListProperty, StringProperty, ReferenceListProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class LabelDialog(FloatLayout):
    assign_label = ObjectProperty(None)
    delete_label = ObjectProperty(None)
    add_label = ObjectProperty(None)
    bb = ObjectProperty(None)
    labels = ListProperty(None)
    cancel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(LabelDialog,self).__init__(**kwargs)
        for label in self.labels:
            btn = LabelDialogButtonsBox(assign=self.assign_label,
                                        delete=self.delete_label,
                                        bb = self.bb,
                                        label=label)
            self.ids.boxLayout.add_widget(btn)

    def update_labels(self, labels):
        self.labels=labels
        self.ids.boxLayout.clear_widgets()
        for label in self.labels:
            btn = LabelDialogButtonsBox(assign=self.assign_label,
                                        delete=self.delete_label,
                                        bb = self.bb,
                                        label=label)
            self.ids.boxLayout.add_widget(btn)


class LabelDialogButtonsBox(BoxLayout):
    assign = ObjectProperty(None)
    delete = ObjectProperty(None)
    bb = ObjectProperty(None)
    label= StringProperty(None)