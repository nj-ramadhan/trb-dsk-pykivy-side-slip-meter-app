from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.graphics.texture import Texture
from kivy.resources import resource_add_path
from kivy.uix.screenmanager import ScreenManager
from kivymd.font_definitions import theme_font_styles
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDIconButton, MDRectangleFlatIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivy.properties import StringProperty
from kivy.metrics import dp
from kivymd.toast import toast
from kivymd.app import MDApp
import os, sys, time, numpy as np
import configparser, hashlib, mysql.connector
import cv2
from pymodbus.client import ModbusTcpClient

colors = {
    "Red"   : {"A200": "#FF2A2A","A500": "#FF8080","A700": "#FFD5D5",},
    "Gray"  : {"200": "#CCCCCC","500": "#ECECEC","700": "#F9F9F9",},
    "Blue"  : {"200": "#4471C4","500": "#5885D8","700": "#6C99EC",},
    "Green" : {"200": "#2CA02C","500": "#2DB97F", "700": "#D5FFD5",},
    "Yellow": {"200": "#ffD42A","500": "#ffE680","700": "#fff6D5",},

    "Light" : {"StatusBar": "E0E0E0","AppBar": "#202020","Background": "#EEEEEE","CardsDialogs": "#FFFFFF","FlatButtonDown": "#CCCCCC","Text": "#000000",},
    "Dark"  : {"StatusBar": "101010","AppBar": "#E0E0E0","Background": "#111111","CardsDialogs": "#222222","FlatButtonDown": "#DDDDDD","Text": "#FFFFFF",},
}

if getattr(sys, 'frozen', False):
    app_path = os.path.dirname(os.path.abspath(__file__))
else:
    app_path = os.path.dirname(os.path.abspath(__file__))

config_path = os.path.join(app_path, 'config.ini')
print(f"Path config.ini: {config_path}")

config = configparser.ConfigParser()
config.read(config_path)

DB_HOST = config['mysql']['DB_HOST']
DB_USER = config['mysql']['DB_USER']
DB_PASSWORD = config['mysql']['DB_PASSWORD']
DB_NAME = config['mysql']['DB_NAME']
TB_DATA = config['mysql']['TB_DATA']
TB_USER = config['mysql']['TB_USER']
TB_MERK = config['mysql']['TB_MERK']

STANDARD_MAX_SIDE_SLIP = float(config['standard']['STANDARD_MAX_SIDE_SLIP']) # in mm

COUNT_STARTING = 3
COUNT_ACQUISITION = 4
TIME_OUT = 500

dt_side_slip_value = 0
dt_side_slip_flag = 0
dt_side_slip_user = 1
dt_side_slip_post = str(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()))
dt_user = ""
dt_no_antrian = ""
dt_no_pol = ""
dt_no_uji = ""
dt_nama = ""
dt_merk = ""
dt_type = ""
dt_jenis_kendaraan = ""
dt_jbb = ""
dt_bahan_bakar = ""
dt_warna = ""
dt_chasis = ""
dt_no_mesin = ""

modbus_client = ModbusTcpClient('192.168.1.111')

class ScreenHome(MDScreen):
    def __init__(self, **kwargs):
        super(ScreenHome, self).__init__(**kwargs)
        Clock.schedule_once(self.delayed_init, 1)

    def delayed_init(self, dt):
        Clock.schedule_interval(self.regular_update_display, 3)

    def regular_update_display(self, dt):
        try:
            self.ids.carousel.index += 1
            
        except Exception as e:
            toast_msg = f'Error Update Display: {e}'
            toast(toast_msg)                

    def exec_navigate_home(self):
        try:
            self.screen_manager.current = 'screen_home'

        except Exception as e:
            toast_msg = f'Error Navigate to Home Screen: {e}'
            toast(toast_msg)        

    def exec_navigate_login(self):
        global dt_user
        try:
            if (dt_user == ""):
                self.screen_manager.current = 'screen_login'
            else:
                toast(f"Anda sudah login sebagai {dt_user}")

        except Exception as e:
            toast_msg = f'Error Navigate to Login Screen: {e}'
            toast(toast_msg)     

    def exec_navigate_main(self):
        try:
            self.screen_manager.current = 'screen_main'

        except Exception as e:
            toast_msg = f'Error Navigate to Main Screen: {e}'
            toast(toast_msg)    

class ScreenLogin(MDScreen):
    def __init__(self, **kwargs):
        super(ScreenLogin, self).__init__(**kwargs)

    def exec_cancel(self):
        try:
            self.ids.tx_username.text = ""
            self.ids.tx_password.text = ""    

        except Exception as e:
            toast_msg = f'error Login: {e}'

    def exec_login(self):
        global mydb, db_users
        global dt_check_user, dt_user

        screen_main = self.screen_manager.get_screen('screen_main')

        try:
            screen_main.exec_reload_database()
            input_username = self.ids.tx_username.text
            input_password = self.ids.tx_password.text        
            # Adding salt at the last of the password
            dataBase_password = input_password
            # Encoding the password
            hashed_password = hashlib.md5(dataBase_password.encode())

            mycursor = mydb.cursor()
            mycursor.execute(f"SELECT id_user, nama, username, password, nama FROM {TB_USER} WHERE username = '{input_username}' and password = '{hashed_password.hexdigest()}'")
            myresult = mycursor.fetchone()
            db_users = np.array(myresult).T
            #if invalid
            if myresult == 0:
                toast('Gagal Masuk, Nama Pengguna atau Password Salah')
            #else, if valid
            else:
                toast_msg = f'Berhasil Masuk, Selamat Datang {myresult[1]}'
                toast(toast_msg)
                dt_check_user = myresult[0]
                dt_user = myresult[1]
                self.ids.tx_username.text = ""
                self.ids.tx_password.text = "" 
                self.screen_manager.current = 'screen_main'

        except Exception as e:
            toast_msg = f'error Login: {e}'
            toast(toast_msg)        
            toast('Gagal Masuk, Nama Pengguna atau Password Salah')

    def exec_navigate_home(self):
        try:
            self.screen_manager.current = 'screen_home'

        except Exception as e:
            toast_msg = f'Error Navigate to Home Screen: {e}'
            toast(toast_msg)        

    def exec_navigate_login(self):
        global dt_user
        try:
            if (dt_user == ""):
                self.screen_manager.current = 'screen_login'
            else:
                toast(f"Anda sudah login sebagai {dt_user}")

        except Exception as e:
            toast_msg = f'Error Navigate to Login Screen: {e}'
            toast(toast_msg)     

    def exec_navigate_main(self):
        try:
            self.screen_manager.current = 'screen_main'

        except Exception as e:
            toast_msg = f'Error Navigate to Main Screen: {e}'
            toast(toast_msg)     

class ScreenMain(MDScreen):   
    def __init__(self, **kwargs):
        super(ScreenMain, self).__init__(**kwargs)
        Clock.schedule_once(self.delayed_init, 1)                 

    def delayed_init(self, dt):
        global flag_conn_stat, flag_play
        global count_starting, count_get_data

        flag_conn_stat = False
        flag_play = False

        count_starting = COUNT_STARTING
        count_get_data = COUNT_ACQUISITION
        
        Clock.schedule_interval(self.regular_update_display, 1)
        self.exec_reload_database()
        self.exec_reload_table()

    def on_antrian_row_press(self, instance):
        global dt_no_antrian, dt_no_pol, dt_no_uji, dt_nama, dt_side_slip_flag
        global dt_merk, dt_type, dt_jenis_kendaraan, dt_jbb, dt_bahan_bakar, dt_warna
        global db_antrian, db_merk

        try:
            row = int(str(instance.id).replace("card_antrian",""))
            dt_no_antrian           = f"{db_antrian[0, row]}"
            dt_no_pol               = f"{db_antrian[1, row]}"
            dt_no_uji               = f"{db_antrian[2, row]}"
            dt_side_slip_flag       = 'Belum Tes' if (int(db_antrian[3, row]) == 0) else 'Sudah Tes'
            dt_nama                 = f"{db_antrian[4, row]}"
            dt_merk                 = f"{db_merk[np.where(db_merk == db_antrian[5, row])[0][0],1]}"
            dt_type                 = f"{db_antrian[6, row]}"
            dt_jenis_kendaraan      = f"{db_antrian[7, row]}"
            dt_jbb                  = f"{db_antrian[8, row]}"
            dt_bahan_bakar          = f"{db_antrian[9, row]}"
            dt_warna                = f"{db_antrian[10, row]}"
                        
            self.exec_start()

        except Exception as e:
            toast_msg = f'Error Execute Command from Table Row: {e}'
            toast(toast_msg)   

    def regular_update_display(self, dt):
        global flag_conn_stat
        global count_starting, count_get_data
        global dt_user, dt_no_antrian, dt_no_pol, dt_no_uji, dt_nama, dt_jenis_kendaraan, dt_side_slip_flag

        try:
            screen_home = self.screen_manager.get_screen('screen_home')
            screen_login = self.screen_manager.get_screen('screen_login')
            screen_slide_test = self.screen_manager.get_screen('screen_slide_test')

            self.ids.lb_time.text = str(time.strftime("%H:%M:%S", time.localtime()))
            self.ids.lb_date.text = str(time.strftime("%d/%m/%Y", time.localtime()))
            screen_home.ids.lb_time.text = str(time.strftime("%H:%M:%S", time.localtime()))
            screen_home.ids.lb_date.text = str(time.strftime("%d/%m/%Y", time.localtime()))
            screen_login.ids.lb_time.text = str(time.strftime("%H:%M:%S", time.localtime()))
            screen_login.ids.lb_date.text = str(time.strftime("%d/%m/%Y", time.localtime()))
            screen_slide_test.ids.lb_time.text = str(time.strftime("%H:%M:%S", time.localtime()))
            screen_slide_test.ids.lb_date.text = str(time.strftime("%d/%m/%Y", time.localtime()))

            screen_slide_test.ids.lb_no_antrian.text = str(dt_no_antrian)
            screen_slide_test.ids.lb_no_pol.text = str(dt_no_pol)
            screen_slide_test.ids.lb_no_uji.text = str(dt_no_uji)
            screen_slide_test.ids.lb_nama.text = str(dt_nama)
            screen_slide_test.ids.lb_jenis_kendaraan.text = str(dt_jenis_kendaraan)
            screen_slide_test.ids.lb_status.text = str(dt_side_slip_flag)

            if(not flag_play):
                screen_slide_test.ids.bt_save.md_bg_color = colors['Green']['200']
                screen_slide_test.ids.bt_save.disabled = False
                screen_slide_test.ids.bt_reload.md_bg_color = colors['Red']['A200']
                screen_slide_test.ids.bt_reload.disabled = False
            else:
                screen_slide_test.ids.bt_reload.disabled = True
                screen_slide_test.ids.bt_save.disabled = True

            if(not flag_conn_stat):
                self.ids.lb_comm.color = colors['Red']['A200']
                self.ids.lb_comm.text = 'PLC Tidak Terhubung'
                screen_home.ids.lb_comm.color = colors['Red']['A200']
                screen_home.ids.lb_comm.text = 'PLC Tidak Terhubung'
                screen_login.ids.lb_comm.color = colors['Red']['A200']
                screen_login.ids.lb_comm.text = 'PLC Tidak Terhubung'

            else:
                self.ids.lb_comm.color = colors['Blue']['200']
                self.ids.lb_comm.text = 'PLC Terhubung'
                screen_home.ids.lb_comm.color = colors['Blue']['200']
                screen_home.ids.lb_comm.text = 'PLC Terhubung'
                screen_login.ids.lb_comm.color = colors['Blue']['200']
                screen_login.ids.lb_comm.text = 'PLC Terhubung'

            if(count_starting <= 0):
                screen_slide_test.ids.lb_test_subtitle.text = "HASIL PENGUKURAN"
                screen_slide_test.ids.lb_side_slip.text = str(np.round(dt_side_slip_value, 2))
                if(dt_side_slip_value <= STANDARD_MAX_SIDE_SLIP):
                    screen_slide_test.ids.lb_info.text = f"Ambang Batas Bergesernya Roda Kendaraan adalah {STANDARD_MAX_SIDE_SLIP} mm,\nPergeseran Roda Kendaraan Anda Dalam Range Ambang Batas"
                else:
                    screen_slide_test.ids.lb_info.text = f"Ambang Batas Bergesernya Roda Kendaraan adalah {STANDARD_MAX_SIDE_SLIP} mm,\nPergeseran Roda Kendaraan Anda Diluar Ambang Batas"

            elif(count_starting > 0):
                if(flag_play):
                    screen_slide_test.ids.lb_test_subtitle.text = "MEMULAI PENGUKURAN"
                    screen_slide_test.ids.lb_side_slip.text = str(count_starting)
                    screen_slide_test.ids.lb_info.text = "Silahkan Gerakkan Kendaraan Anda Tanpa Memegang Kemudi"

            if(count_get_data <= 0):
                if(not flag_play):
                    if(dt_side_slip_value <= STANDARD_MAX_SIDE_SLIP):
                        screen_slide_test.ids.lb_test_result.md_bg_color = colors['Green']['200']
                        screen_slide_test.ids.lb_test_result.text = "LULUS"
                        dt_side_slip_flag = "Lulus"
                        screen_slide_test.ids.lb_test_result.text_color = colors['Green']['700']
                    else:
                        screen_slide_test.ids.lb_test_result.md_bg_color = colors['Red']['A200']
                        screen_slide_test.ids.lb_test_result.text = "TIDAK LULUS"
                        dt_side_slip_flag = "Tidak Lulus"
                        screen_slide_test.ids.lb_test_result.text_color = colors['Red']['A700']

            elif(count_get_data > 0):
                    screen_slide_test.ids.lb_test_result.md_bg_color = "#EEEEEE"
                    # screen_counter.ids.lb_test_result.size_hint_y = None
                    # screen_counter.ids.lb_test_result.height = dp(0)
                    screen_slide_test.ids.lb_test_result.text = ""

            self.ids.bt_logout.disabled = False if dt_user != '' else True
            # self.ids.bt_start.disabled = True if dt_user == '' else True if dt_check_flag != "Belum Tes" else False

            self.ids.lb_operator.text = f'Login Sebagai: {dt_user}' if dt_user != '' else 'Silahkan Login'
            screen_home.ids.lb_operator.text = f'Login Sebagai: {dt_user}' if dt_user != '' else 'Silahkan Login'
            screen_login.ids.lb_operator.text = f'Login Sebagai: {dt_user}' if dt_user != '' else 'Silahkan Login'
            screen_slide_test.ids.lb_operator.text = f'Login Sebagai: {dt_user}' if dt_user != '' else 'Silahkan Login'

        except Exception as e:
            toast_msg = f'Error Update Display: {e}'
            toast(toast_msg)                

    def regular_update_connection(self, dt):
        global flag_conn_stat

        try:
            modbus_client.connect()
            flag_conn_stat = modbus_client.connected
            modbus_client.close()     
            
        except Exception as e:
            toast_msg = f'{e}'
            toast(toast_msg)   
            flag_conn_stat = False

    def regular_get_data(self, dt):
        global count_starting, count_get_data
        global dt_side_slip_value
        global flag_play
        try:
            if(count_starting > 0):
                count_starting -= 1              

            if(count_get_data > 0):
                count_get_data -= 1
                
            elif(count_get_data <= 0):
                flag_play = False
                Clock.unschedule(self.regular_get_data)

            if flag_conn_stat:
                modbus_client.connect()
                side_slip_registers = modbus_client.read_holding_registers(1612, 1, slave=1) #V1100
                modbus_client.close()

                dt_side_slip_value = side_slip_registers.registers[0] / 10
                
        except Exception as e:
            toast_msg = f'Error Get Data: {e}'
            toast(toast_msg)     

    def exec_reload_database(self):
        global mydb
        try:
            mydb = mysql.connector.connect(host = DB_HOST,user = DB_USER,password = DB_PASSWORD,database = DB_NAME)
        except Exception as e:
            toast_msg = f'Error Initiate Database: {e}'
            toast(toast_msg)   

    def exec_reload_table(self):
        global mydb, db_antrian, db_merk
        global dt_dash_pendaftaran, dt_dash_belum_uji, dt_dash_sudah_uji

        try:
            tb_antrian = mydb.cursor()
            tb_antrian.execute(f"SELECT noantrian, nopol, nouji, sideslip_flag, user, merk, type, idjeniskendaraan, jbb, bahan_bakar, warna FROM {TB_DATA}")
            result_tb_antrian = tb_antrian.fetchall()
            mydb.commit()
            db_antrian = np.array(result_tb_antrian).T
            db_pendaftaran = np.array(result_tb_antrian)
            dt_dash_pendaftaran = db_pendaftaran[:,3].size
            dt_dash_belum_uji = np.where(db_pendaftaran[:,3] == 0)[0].size
            dt_dash_sudah_uji = np.where(db_pendaftaran[:,3] == 1)[0].size

            tb_merk = mydb.cursor()
            tb_merk.execute(f"SELECT ID, DESCRIPTION FROM {TB_MERK}")
            result_tb_merk = tb_merk.fetchall()
            mydb.commit()
            db_merk = np.array(result_tb_merk)

            layout_list = self.ids.layout_list
            layout_list.clear_widgets(children=None)

        except Exception as e:
            toast_msg = f'Error Remove Widget: {e}'
            print(toast_msg)
        
        try:           
            layout_list = self.ids.layout_list
            for i in range(db_antrian[0,:].size):
                layout_list.add_widget(
                    MDCard(
                        MDLabel(text=f"{db_antrian[0, i]}", size_hint_x= 0.05),
                        MDLabel(text=f"{db_antrian[1, i]}", size_hint_x= 0.08),
                        MDLabel(text=f"{db_antrian[2, i]}", size_hint_x= 0.08),
                        MDLabel(text='Belum Tes' if (int(db_antrian[3, i]) == 0) else 'Sudah Tes', size_hint_x= 0.08),
                        MDLabel(text=f"{db_antrian[4, i]}", size_hint_x= 0.12),
                        MDLabel(text=f"{db_merk[np.where(db_merk == db_antrian[5, i])[0][0],1]}", size_hint_x= 0.08),
                        MDLabel(text=f"{db_antrian[6, i]}", size_hint_x= 0.05),
                        MDLabel(text=f"{db_antrian[7, i]}", size_hint_x= 0.15),
                        MDLabel(text=f"{db_antrian[8, i]}", size_hint_x= 0.05),
                        MDLabel(text=f"{db_antrian[9, i]}", size_hint_x= 0.08),
                        MDLabel(text=f"{db_antrian[10, i]}", size_hint_x= 0.08),

                        ripple_behavior = True,
                        on_press = self.on_antrian_row_press,
                        padding = 20,
                        id=f"card_antrian{i}",
                        size_hint_y=None,
                        height="60dp",
                        )
                    )

        except Exception as e:
            toast_msg = f'Error Reload Table: {e}'
            print(toast_msg)

    def exec_start(self):
        global dt_side_slip_flag, dt_no_antrian, dt_user
        global flag_play

        if (dt_user != ''):
            if (dt_side_slip_flag == 'Belum Tes'):
                if(not flag_play):
                    Clock.schedule_interval(self.regular_get_data, 1)
                    self.open_screen_slide_test()
                    flag_play = True
            else:
                toast(f'No. Antrian {dt_no_antrian} Sudah Tes')
        else:
            toast(f'Silahkan Login Untuk Melakukan Pengujian')        

    def open_screen_slide_test(self):
        self.screen_manager.current = 'screen_slide_test'

    def exec_logout(self):
        global dt_user

        dt_user = ""
        self.screen_manager.current = 'screen_login'

    def exec_navigate_home(self):
        try:
            self.screen_manager.current = 'screen_home'

        except Exception as e:
            toast_msg = f'Error Navigate to Home Screen: {e}'
            toast(toast_msg)        

    def exec_navigate_login(self):
        global dt_user
        try:
            if (dt_user == ""):
                self.screen_manager.current = 'screen_login'
            else:
                toast(f"Anda sudah login sebagai {dt_user}")

        except Exception as e:
            toast_msg = f'Error Navigate to Login Screen: {e}'
            toast(toast_msg)    

    def exec_navigate_main(self):
        try:
            self.screen_manager.current = 'screen_main'

        except Exception as e:
            toast_msg = f'Error Navigate to Main Screen: {e}'
            toast(toast_msg)   

class ScreenSlideTest(MDScreen):        
    def __init__(self, **kwargs):
        super(ScreenSlideTest, self).__init__(**kwargs)
        Clock.schedule_once(self.delayed_init, 2)
        
    def delayed_init(self, dt):
        pass

    def exec_start(self):
        global flag_play
        global count_starting, count_get_data

        screen_main = self.screen_manager.get_screen('screen_main')

        count_starting = COUNT_STARTING
        count_get_data = COUNT_ACQUISITION

        if(not flag_play):
            Clock.schedule_interval(screen_main.regular_get_data, 1)
            flag_play = True

    def exec_reload(self):
        global flag_play
        global count_starting, count_get_data, dt_side_slip_value

        screen_main = self.screen_manager.get_screen('screen_main')

        count_starting = COUNT_STARTING
        count_get_data = COUNT_ACQUISITION
        dt_side_slip_value = 0
        self.ids.bt_reload.disabled = True
        self.ids.lb_side_slip.text = "..."

        if(not flag_play):
            Clock.schedule_interval(screen_main.regular_get_data, 1)
            flag_play = True

    def exec_save(self):
        global flag_play
        global count_starting, count_get_data
        global mydb, db_antrian
        global dt_no_antrian, dt_no_reg, dt_no_uji, dt_nama, dt_jenis_kendaraan
        global dt_side_slip_flag, dt_side_slip_value, dt_side_slip_user, dt_side_slip_post

        self.ids.bt_save.disabled = True

        mycursor = mydb.cursor()

        sql = f"UPDATE {TB_DATA} SET sideslip_flag = %s, sideslip_value = %s, sideslip_user = %s, sideslip_post = %s WHERE noantrian = %s"
        sql_sideslip_flag = (1 if dt_side_slip_flag == "Lulus" else 2)
        dt_side_slip_post = str(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()))
        print_datetime = str(time.strftime("%d %B %Y %H:%M:%S", time.localtime()))
        sql_val = (sql_sideslip_flag, dt_side_slip_value, dt_side_slip_user, dt_side_slip_post, dt_no_antrian)
        mycursor.execute(sql, sql_val)
        mydb.commit()

        self.open_screen_main()

    def open_screen_main(self):
        global flag_play        
        global count_starting, count_get_data

        screen_main = self.screen_manager.get_screen('screen_main')

        count_starting = COUNT_STARTING
        count_get_data = COUNT_ACQUISITION
        flag_play = False   
        screen_main.exec_reload_table()
        self.screen_manager.current = 'screen_main'

    def exec_logout(self):
        self.screen_manager.current = 'screen_login'

class RootScreen(ScreenManager):
    pass             

class SoundLevelMeterApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.colors = colors
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.accent_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        self.icon = 'assets/images/logo-app.png'

        LabelBase.register(
            name="Orbitron-Regular",
            fn_regular="assets/fonts/Orbitron-Regular.ttf")
        
        LabelBase.register(
            name="Draco",
            fn_regular="assets/fonts/Draco.otf")        

        LabelBase.register(
            name="Recharge",
            fn_regular="assets/fonts/Recharge.otf") 
        
        theme_font_styles.append('Display')
        self.theme_cls.font_styles["Display"] = [
            "Orbitron-Regular", 72, False, 0.15]       

        theme_font_styles.append('H4')
        self.theme_cls.font_styles["H4"] = [
            "Recharge", 30, False, 0.15] 

        theme_font_styles.append('H5')
        self.theme_cls.font_styles["H5"] = [
            "Recharge", 20, False, 0.15] 

        theme_font_styles.append('H6')
        self.theme_cls.font_styles["H6"] = [
            "Recharge", 16, False, 0.15] 

        theme_font_styles.append('Subtitle1')
        self.theme_cls.font_styles["Subtitle1"] = [
            "Recharge", 12, False, 0.15] 

        theme_font_styles.append('Body1')
        self.theme_cls.font_styles["Body1"] = [
            "Recharge", 12, False, 0.15] 
        
        theme_font_styles.append('Button')
        self.theme_cls.font_styles["Button"] = [
            "Recharge", 10, False, 0.15] 

        theme_font_styles.append('Caption')
        self.theme_cls.font_styles["Caption"] = [
            "Recharge", 8, False, 0.15]                                 
            
        Window.fullscreen = 'auto'
        # Window.borderless = False
        # Window.size = 1920, 1080
        # Window.allow_screensaver = True

        Builder.load_file('main.kv')
        return RootScreen()

if __name__ == '__main__':
    SoundLevelMeterApp().run()