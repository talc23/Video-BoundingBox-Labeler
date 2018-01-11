from kivy.properties import ObjectProperty, ListProperty, StringProperty, ReferenceListProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from os import path

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(LoadDialog, self).__init__(**kwargs)
        pass

    def load_clicked(self, path, filename):
        print('load_clicked path={}, filename={}'.format(str(path), str(filename)))
        if len(filename) is not 0:
            self.load(path, filename)