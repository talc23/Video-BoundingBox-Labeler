from kivy.uix.bubble import Bubble
from kivy.properties import ObjectProperty

class ConfirmBubble(Bubble):
    confirm = ObjectProperty(None)