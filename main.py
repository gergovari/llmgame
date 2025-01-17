from dm import DM, BlockManager, LLM
from block import *
import json

import os
from typing import List, Dict

import kivy
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty, BooleanProperty, ListProperty, ObjectProperty, ColorProperty
from kivy.metrics import dp
import kivymd
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.button import Button

def block_from_json(data: dict) -> object:
    block_type = data.get("type")
    if block_type not in globals():
        raise ValueError(f"Unknown block type: {block_type}")
    return globals()[block_type](**{k: v for k, v in data.items() if k != "type"})
with open("blocks.json", "r") as file:
    blocks_data = json.load(file)
blocks = [block_from_json(data) for data in blocks_data]
dm = DM(BlockManager(blocks), LLM())
#dm.continue_game()
print(dm.blockmanager.blocks)
print()

class ChatBlock(BoxLayout):
    block = ObjectProperty(None)
    background_color = ColorProperty((0.25, 0.25, 0.25, 1)) 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if isinstance(self.block, User):
            self.background_color = (.5, .75, 0, 1)
        elif isinstance(self.block, (Assistant, Initial)):
            self.background_color = (0.5, 0.5, 0.5, 1)
        else:
            self.background_color = (0.75, 0.5, 0.5, 1)

class ChatArea(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_kv_post(self, base):
        for block in dm.blockmanager.blocks:
            self.ids.box.add_widget(ChatBlock(block=block))
            self.ids.box.scroll_y = 0

class ChatScreen(MDScreen):
    old = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.old = list(dm.blockmanager.blocks)
    
    def update_blocks(self):
        for block in [elem for elem in dm.blockmanager.blocks if elem not in self.old]:
            self.ids.chat_area.ids.box.add_widget(ChatBlock(block=block))
        self.ids.chat_area.scroll_y = 0 
        self.old = list(dm.blockmanager.blocks)

    def send(self, message):
        dm.turn(message)
        self.ids.chat_input.text = ""
        self.update_blocks()

    def continue_game(self):
        dm.continue_game()
        self.update_blocks()

    def retry(self):
        dm.retry()
        self.update_blocks()
    
    
class ChatGPTApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Orange"  # Primary color theme
        self.theme_cls.theme_style = "Dark"    # "Light" or "Dark"
        
        return Builder.load_file('chat_app.kv')

if __name__ == '__main__':
    ChatGPTApp().run()
