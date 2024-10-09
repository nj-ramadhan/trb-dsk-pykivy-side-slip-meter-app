from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivymd.font_definitions import theme_font_styles

from kivymd.app import MDApp
# import numpy as np
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
# import time

class ScreenLogin(MDScreen):
    def __init__(self, **kwargs):
        super(ScreenLogin, self).__init__(**kwargs)

class ScreenMain(MDScreen):   
    def __init__(self, **kwargs):
        super(ScreenMain, self).__init__(**kwargs)

class ScreenCounter(MDScreen):        
    def __init__(self, **kwargs):
        super(ScreenCounter, self).__init__(**kwargs)
        Clock.schedule_once(self.delayed_init, 2)

    def delayed_init(self, dt):
        pass

class RootScreen(ScreenManager):
    pass       


class TestApp(MDApp):
    def build(self):
        self.theme_style = "Light"
        self.title = "Test App"
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.accent_palette = "BlueGray"
        self.icon = 'assets/logo.png'

        LabelBase.register(
            name="Orbitron-Regular",
            fn_regular="assets/fonts/Orbitron-Regular.ttf")

        theme_font_styles.append('Display')
        self.theme_cls.font_styles["Display"] = [
            "Orbitron-Regular", 72, False, 0.15]       
        
        Window.fullscreen = 'auto'

        Builder.load_file('main.kv')
        return RootScreen()

if __name__ == '__main__':
    TestApp().run()
