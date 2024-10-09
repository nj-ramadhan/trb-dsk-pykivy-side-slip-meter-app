from cv2 import DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMINGLUT
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.toast import toast
import numpy as np
import time
import os
import win32com.client
import usb.core as usb_core
from usb.backend import libusb1
import libusb_package
import serial
import pyaudio
from math import log10
import audioop  
colors = {
    "Red": {
        "A200": "#A51919",
        "A500": "#A51919",
        "A700": "#A51919",
    },

    "Gray": {
        "200": "#999999",
        "500": "#999999",
        "700": "#999999",
    },

    "Blue": {
        "200": "#196BA5",
        "500": "#196BA5",
        "700": "#196BA5",
    },

    "Green": {
        "200": "#19A56B",
        "500": "#19A56B",
        "700": "#19A56B",
    },

    "Light": {
        "StatusBar": "E0E0E0",
        "AppBar": "#202020",
        "Background": "#EEEEEE",
        "CardsDialogs": "#FFFFFF",
        "FlatButtonDown": "#CCCCCC",
    },

    "Dark": {
        "StatusBar": "101010",
        "AppBar": "#E0E0E0",
        "Background": "#111111",
        "CardsDialogs": "#000000",
        "FlatButtonDown": "#333333",
    },
}

VENDOR_ID = 0x04F2
PRODUCT_ID = 0xB6A8
SER_BAUD = 9600
SER_PORT = "COM9"
SER_DTR = 1
SER_DSR = True
SER_TIMEOUT = 1

FORMAT = pyaudio.paInt16
# FORMAT = pyaudio.paFloat32
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 0.1
WAVE_OUTPUT_FILENAME = "file.wav"
WIDTH = 2

sound_rms = 1
flag_device = False
flag_conn_stat = False
flag_play = False
serial_com = serial.Serial()
dt_sound = 45.5

p = pyaudio.PyAudio() # start the PyAudio class
stream=p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,
        frames_per_buffer=CHUNK) #uses default input device

class ScreenMain(MDScreen):        
    def __init__(self, **kwargs):
        super(ScreenMain, self).__init__(**kwargs)
        Clock.schedule_once(self.delayed_init, 0.1)
        
    def delayed_init(self, dt):
        Clock.schedule_interval(self.regular_update_connection, 5)
        Clock.schedule_interval(self.regular_update_display, 1)
    
    def regular_update_display(self, dt):
        global flag_conn_stat, flag_device
        global serial_com
        global dt_sound

        try:
            self.ids.lb_datetime.text = str(time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))

            if(flag_play):
                # self.ids.bt_run.md_bg_color = colors['Gray']['200']
                self.ids.bt_run.disabled = True
                self.ids.bt_stop.md_bg_color = colors['Red']['A200']
                self.ids.bt_stop.disabled = False
            else:
                self.ids.bt_run.md_bg_color = colors['Red']['A200']
                self.ids.bt_run.disabled = False
                # self.ids.bt_stop.md_bg_color = colors['Gray']['200']
                self.ids.bt_stop.disabled = True


            if(not flag_conn_stat):
                self.ids.lb_comm.color = colors['Red']['A200']
                self.ids.lb_comm.text = 'Status : Disconnected'

            else:
                self.ids.lb_comm.color = colors['Blue']['200']
                self.ids.lb_comm.text = 'Status : Connected'
                if(not flag_device):
                    toast('Device successfully connected')
            
            # if(flag_device):
            #     serial_com.baudrate = SER_BAUD
            #     serial_com.port = SER_PORT
            #     serial_com.dtr = SER_DTR
            #     serial_com.dsrdtr = SER_DSR
            #     serial_com.write_timeout = SER_TIMEOUT
            #     serial_com.timeout = SER_TIMEOUT
            #     Clock.schedule_interval(self.regular_get_data, 1)

            self.ids.lb_sound.text = str(np.round(dt_sound, 2))
            if(dt_sound >= 83 and dt_sound <= 118):
                self.ids.lb_status.md_bg_color = colors['Green']['200']
                self.ids.lb_status.text = "PASS"
            else:
                self.ids.lb_status.md_bg_color = colors['Red']['A200']
                self.ids.lb_status.text = "FAIL"

        except Exception as e:
            toast_msg = f'error update display: {e}'
            toast(toast_msg)                

    def regular_update_connection(self, dt):
        global flag_conn_stat, flag_device
        global serial_com
        try:
            wmi = win32com.client.GetObject ("winmgmts:")
            for usb in wmi.InstancesOf ("Win32_USBHub"):
                print(usb.DeviceID)
            backend = libusb1.get_backend(find_library=libusb_package.find_library)
            dev = usb_core.find(idVendor = VENDOR_ID, idProduct = PRODUCT_ID, backend=backend,)

            if(dev is None):
                flag_device = False
            else:
                flag_device = True
            
            if(flag_device):
                flag_conn_stat = serial_com.isOpen()
                # serial_com.baudrate = SER_BAUD
                # serial_com.port = SER_PORT
                # serial_com.dtr = SER_DTR
                # serial_com.dsrdtr = SER_DSR
                # serial_com.write_timeout = SER_TIMEOUT
                # serial_com.timeout = SER_TIMEOUT
                if(serial_com.isOpen() == False):
                    serial_com.open()              

        except Exception as e:
            flag_conn_stat = False
            flag_device = False
            toast_msg = f'error update connection: {e}'
            toast(toast_msg)         
    
    def callback(self, in_data, frame_count, time_info, status):
        global sound_rms
        sound_rms = audioop.rms(in_data, WIDTH) / 32767
        return in_data, pyaudio.paContinue

    def regular_get_data(self, dt):
        global serial_com
        global dt_sound
        global sound_rms
        try:
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                sound_rms = audioop.rms(stream.read(CHUNK), WIDTH) / 32767
                db = 20 * log10(sound_rms) #0.033, 0.109, 0.347
                # mod = 20 * log10(rms * 32767)
                mod_Amp = sound_rms * 1600000
                # mod_Amp = amp * 1518727
                mod_dB = 20 * log10(mod_Amp)
                # mod_dB = 20 * log10(sound_rms) + 93.37
                print(f"RMS: {sound_rms} DB: {db} mod_Amp: {mod_Amp} mod_dB: {mod_dB}") 
                dt_sound = mod_dB
            # serial_com.open()
            # byte_read = serial_com.read
            # serial_com.close()
            # dt_sound = np.random.uniform(40.0, 105.0)
            # print("dt_sound:", dt_sound)
            # dt_sound = str(byte_read.decode("utf-8"))
                
        except Exception as e:
            toast_msg = f'error get data: {e}'
            print(toast_msg) 

    def exec_play(self):
        global flag_play, stream, p

        if(not flag_play):
            stream.start_stream()
            Clock.schedule_interval(self.regular_get_data, 1)
            flag_play = True

    def exec_stop(self):
        global flag_play, stream, p

        if(flag_play):
            stream.close()
            p.terminate()            
            Clock.unschedule(self.regular_get_data)
            flag_play = False

    def exec_shutdown(self):
        os.system("shutdown /s /t 1") #for windows os
        toast("shutting down system")
        # os.system("shutdown -h now")


class RootScreen(ScreenManager):

    pass

class SoundLevelMeterApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.colors = colors
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Gray"
        self.icon = 'asset/logo.png'
        Window.fullscreen = 'auto'
        Window.borderless = False
        # Window.size = 900, 1440
        # Window.size = 450, 720
        # Window.allow_screensaver = True

        Builder.load_file('main.kv')
        return RootScreen()

if __name__ == '__main__':
    SoundLevelMeterApp().run()