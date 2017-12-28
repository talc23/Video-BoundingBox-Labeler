from kivy.properties import ObjectProperty, ListProperty, StringProperty, ReferenceListProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.clock import Clock

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
    delete_all_bb_of_label = ObjectProperty(None)
    add_label = ObjectProperty(None)
    bb = ObjectProperty(None)
    labels = ListProperty(None)
    cancel = ObjectProperty(None)
    labelDialogControl = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(LabelDialog,self).__init__(**kwargs)

    def assign_label_to_bb(self, labelName):
        self.assign_label(self.bb, labelName)

class LabelDialogLabelsBox(StackLayout):
    assign_label = ObjectProperty(None)
    delete_label = ObjectProperty(None)
    delete_all_bb_of_label = ObjectProperty(None)
    labels = ListProperty(None)

    def __init__(self, **kwargs):
        super(LabelDialogLabelsBox,self).__init__(**kwargs)
        self.bind(labels=self.update_labels)


    def update_labels(self, instance=None, value=None):
        self.clear_widgets()
        for label in self.labels:
            print('update_labels= '+str(self.assign_label))
            btn = LabelDialogLabelButtonsBox(label=label,
                                             assign_label=self.assign_label,
                                             delete_label=self.delete_label,
                                             delete_all_bb_of_label=self.delete_all_bb_of_label,
                                        size_hint_x=1,
                                        size_hint_y=.1
                                             )
            self.add_widget(btn)

    def on_assign_label(self, inst, val):
        print('on_assign_label' + str(inst) + ' ' + str(val))
        for child in self.children:
            child.assign_label = val

class LabelDialogLabelButtonsBox(BoxLayout):
    assign_label = ObjectProperty(None)
    delete_label = ObjectProperty(None)
    delete_all_bb_of_label = ObjectProperty(None)
    label= StringProperty(None)

    # def __init__(self, **kwargs):
    #     super(LabelDialogLabelButtonsBox, self).__init__(**kwargs)