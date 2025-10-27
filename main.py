import datetime
import os, sys, time

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
    running_mode = 'Frozen/executable'
else:
    try:
        app_full_path = os.path.realpath(__file__)
        application_path = os.path.dirname(app_full_path)
        running_mode = "Non-interactive"
    except NameError:
        application_path = os.getcwd()
        running_mode = 'Interactive'

logger_name = f'app.log'
logger_dir = os.path.join(application_path, "logs")

from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemanddock')

from kivy.logger import Logger
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from kivymd.font_definitions import theme_font_styles
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp
from kivymd.toast import toast
from kivymd.app import MDApp
import numpy as np
import configparser, hashlib, mysql.connector
from pymodbus.client import ModbusTcpClient
from fpdf import FPDF
import ssl 
ssl._create_default_https_context = ssl._create_unverified_context

colors = {
    "Red"   : {"A200": "#FF2A2A","A500": "#FF8080","A700": "#FFD5D5",},
    "Gray"  : {"200": "#CCCCCC","500": "#ECECEC","700": "#F9F9F9",},
    "Blue"  : {"200": "#4471C4","500": "#5885D8","700": "#6C99EC",},
    "Green" : {"200": "#2CA02C","500": "#2DB97F", "700": "#D5FFD5",},
    "Yellow": {"200": "#ffD42A","500": "#ffE680","700": "#fff6D5",},

    "Light" : {"StatusBar": "E0E0E0","AppBar": "#202020","Background": "#EEEEEE","CardsDialogs": "#FFFFFF","FlatButtonDown": "#CCCCCC",},
    "Dark"  : {"StatusBar": "101010","AppBar": "#E0E0E0","Background": "#111111","CardsDialogs": "#222222","FlatButtonDown": "#DDDDDD",},
}

config_name = 'config.ini'
config_full_path = os.path.join(application_path, config_name)
config = configparser.ConfigParser()
config.read(config_full_path)

## App Setting
APP_TITLE = config['app']['APP_TITLE']
APP_SUBTITLE = config['app']['APP_SUBTITLE']
IMG_LOGO_PEMKAB = config['app']['IMG_LOGO_PEMKAB']
IMG_LOGO_DISHUB = config['app']['IMG_LOGO_DISHUB']
LB_PEMKAB = config['app']['LB_PEMKAB']
LB_DISHUB = config['app']['LB_DISHUB']
LB_UNIT = config['app']['LB_UNIT']
LB_UNIT_ADDRESS = config['app']['LB_UNIT_ADDRESS']

# SQL setting
DB_HOST = "156.67.217.60"
DB_USER = "pkbsorong2024!"
DB_PASSWORD = "@Sorongpkb2024"
DB_NAME = "dishub"

TB_DATA = "tb_cekident"
TB_USER = "users"
TB_MERK = "merk"
TB_BAHAN_BAKAR = "bahanbakar"
TB_WARNA = "warna"
TB_DATA_MASTER = "identkendaraan"

FTP_HOST = "194.31.53.37"
FTP_USER = "root"
FTP_PASS = "@D15HUBp2022!"

## System Setting
TIME_OUT = int(config['setting']['TIME_OUT'])
COUNT_STARTING_SIDESLIP = int(config['setting']['COUNT_STARTING_SIDESLIP'])
COUNT_ACQUISITION_SIDESLIP = int(config['setting']['COUNT_ACQUISITION_SIDESLIP'])
UPDATE_CAROUSEL_INTERVAL = float(config['setting']['UPDATE_CAROUSEL_INTERVAL'])
UPDATE_CONNECTION_INTERVAL = float(config['setting']['UPDATE_CONNECTION_INTERVAL'])
GET_DATA_INTERVAL = float(config['setting']['GET_DATA_INTERVAL'])

MODBUS_IP_PLC = config['setting']['MODBUS_IP_PLC']
MODBUS_CLIENT = ModbusTcpClient(MODBUS_IP_PLC)
REGISTER_DATA_SIDE_SLIP = int(config['setting']['REGISTER_DATA_SIDE_SLIP']) # 1612 = V1100

## system standard
STANDARD_MAX_SIDESLIP = float(config['standard']['STANDARD_MAX_SIDESLIP']) # in mm
SIDESLIP_OFFSET_NOL = float(config.get('sideslip', 'OFFSET_NOL', fallback=160.0))

class ScreenHome(MDScreen):
    def __init__(self, **kwargs):
        super(ScreenHome, self).__init__(**kwargs)
        Clock.schedule_once(self.delayed_init, 1)
    
    def delayed_init(self, dt):
        self.ids.lb_title.text = APP_TITLE
        self.ids.lb_subtitle.text = APP_SUBTITLE        
        self.ids.img_pemkab.source = f'assets/images/{IMG_LOGO_PEMKAB}'
        self.ids.img_dishub.source = f'assets/images/{IMG_LOGO_DISHUB}'
        self.ids.lb_pemkab.text = LB_PEMKAB
        self.ids.lb_dishub.text = LB_DISHUB
        self.ids.lb_unit.text = LB_UNIT
        self.ids.lb_unit_address.text = LB_UNIT_ADDRESS

    def on_enter(self):
        Clock.schedule_interval(self.regular_update_carousel, 3)

    def on_leave(self):
        Clock.unschedule(self.regular_update_carousel)

    def regular_update_carousel(self, dt):
        try:
            self.ids.carousel.index += 1
            
        except Exception as e:
            toast_msg = f'Gagal Memperbaharui Tampilan Carousel'
            toast_msg = f'Error Update Carousel: {e}'
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
            toast_msg = f'Terjadi kesalahan saat berpindah ke halaman Login'
            toast(toast_msg)
            Logger.error(f"{self.name}: {toast_msg}, {e}")  

    def exec_navigate_main(self):
        try:
            self.screen_manager.current = 'screen_main'

        except Exception as e:
            toast_msg = f'Terjadi kesalahan saat berpindah ke halaman Utama'
            toast(toast_msg)
            Logger.error(f"{self.name}: {toast_msg}, {e}")  

class ScreenLogin(MDScreen):
    def __init__(self, **kwargs):
        super(ScreenLogin, self).__init__(**kwargs)
        Clock.schedule_once(self.delayed_init, 1)
    
    def delayed_init(self, dt):
        self.ids.lb_title.text = APP_TITLE
        self.ids.lb_subtitle.text = APP_SUBTITLE  
        self.ids.img_pemkab.source = f'assets/images/{IMG_LOGO_PEMKAB}'
        self.ids.img_dishub.source = f'assets/images/{IMG_LOGO_DISHUB}'
        self.ids.lb_pemkab.text = LB_PEMKAB
        self.ids.lb_dishub.text = LB_DISHUB
        self.ids.lb_unit.text = LB_UNIT
        self.ids.lb_unit_address.text = LB_UNIT_ADDRESS

    def exec_cancel(self):
        try:
            self.ids.tx_username.text = ""
            self.ids.tx_password.text = ""    

        except Exception as e:
            toast_msg = f'error Login: {e}'

    def exec_login(self):
        global mydb, db_users
        global dt_id_user, dt_user, dt_foto_user

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
            mycursor.execute(f"SELECT id_user, nama, username, password, image FROM {TB_USER} WHERE username = '{input_username}' and password = '{hashed_password.hexdigest()}'")
            myresult = mycursor.fetchone()
            db_users = np.array(myresult).T
            
            if myresult is None:
                toast_msg = f'Gagal Masuk, Nama Pengguna atau Password Salah'
                toast(toast_msg) 
                Logger.warning(f"{self.name}: {toast_msg}") 
            else:
                toast_msg = f'Berhasil Masuk, Selamat Datang {myresult[1]}'
                toast(toast_msg)
                Logger.info(f"{self.name}: {toast_msg}")  

                dt_id_user = myresult[0]
                dt_user = myresult[1]
                dt_foto_user = myresult[4]
                self.ids.tx_username.text = ""
                self.ids.tx_password.text = "" 
                self.screen_manager.current = 'screen_main'

        except Exception as e:
            toast_msg = f'Gagal masuk, silahkan isi nama user dan password yang sesuai'
            toast(toast_msg)  
            Logger.error(f"{self.name}: {toast_msg}, {e}")  

    def exec_navigate_home(self):
        try:
            self.screen_manager.current = 'screen_home'

        except Exception as e:
            toast_msg = f'Gagal Berpindah ke Halaman Awal'
            toast(toast_msg)
            Logger.error(f"{self.name}: {toast_msg}, {e}")

    def exec_navigate_login(self):
        global dt_user
        try:
            if (dt_user == ""):
                self.screen_manager.current = 'screen_login'
            else:
                toast_msg = f"Anda sudah login sebagai {dt_user}"
                toast(toast_msg)
                Logger.info(f"{self.name}: {toast_msg}")  

        except Exception as e:
            toast_msg = f'Gagal Berpindah ke Halaman Login'
            toast(toast_msg)
            Logger.error(f"{self.name}: {toast_msg}, {e}")  

    def exec_navigate_main(self):
        try:
            self.screen_manager.current = 'screen_main'

        except Exception as e:
            toast_msg = f'Gagal Berpindah ke Halaman Utama'
            toast(toast_msg)
            Logger.error(f"{self.name}: {toast_msg}, {e}") 

class ScreenMain(MDScreen):   
    def __init__(self, **kwargs):
        super(ScreenMain, self).__init__(**kwargs)
        global flag_conn_stat, flag_play, flag_cylinder
        global count_starting, count_get_data
        global dt_user, dt_foto_user, dt_no_antri, dt_no_pol, dt_no_uji, dt_sts_uji, dt_nama
        global dt_merk, dt_type, dt_jns_kend, dt_jbb, dt_brt_ksg, dt_bhn_bkr, dt_warna, dt_chasis, dt_no_mesin
        global dt_id_user
        global dt_sideslip_flag, dt_sideslip_value
        global dt_dash_pendaftaran, dt_dash_belum_uji, dt_dash_sudah_uji

        flag_conn_stat = flag_play = flag_cylinder = False
        dt_user = dt_foto_user = dt_no_antri = dt_no_pol = dt_no_uji = dt_sts_uji = dt_nama = ""
        dt_merk = dt_type = dt_jns_kend = dt_jbb = dt_brt_ksg = dt_bhn_bkr = dt_warna = dt_chasis = dt_no_mesin = ""
        dt_id_user = 1
        dt_dash_pendaftaran = dt_dash_belum_uji = dt_dash_sudah_uji = 0
        dt_sideslip_value = dt_sideslip_flag = 0

        count_starting = COUNT_STARTING_SIDESLIP
        count_get_data = COUNT_ACQUISITION_SIDESLIP

        Clock.schedule_once(self.delayed_init, 1)            

    def delayed_init(self, dt):   
        self.ids.lb_title.text = APP_TITLE
        self.ids.lb_subtitle.text = APP_SUBTITLE              
        self.ids.img_pemkab.source = f'assets/images/{IMG_LOGO_PEMKAB}'
        self.ids.img_dishub.source = f'assets/images/{IMG_LOGO_DISHUB}'
        self.ids.lb_pemkab.text = LB_PEMKAB
        self.ids.lb_dishub.text = LB_DISHUB
        self.ids.lb_unit.text = LB_UNIT
        self.ids.lb_unit_address.text = LB_UNIT_ADDRESS
        
        Clock.schedule_interval(self.regular_update_display, 1)
        Clock.schedule_interval(self.regular_update_connection, UPDATE_CONNECTION_INTERVAL)

    def on_enter(self):
        self.exec_reload_database()
        self.exec_reload_table()

    def regular_update_display(self, dt):
        global flag_conn_stat
        global count_starting, count_get_data
        global dt_sideslip_flag, dt_sideslip_value
        
        try:
            screen_home = self.screen_manager.get_screen('screen_home')
            screen_login = self.screen_manager.get_screen('screen_login')
            screen_calibration = self.screen_manager.get_screen('screen_calibration')
            screen_sideslip_meter = self.screen_manager.get_screen('screen_sideslip_meter')
            
            self.ids.lb_time.text = str(time.strftime("%H:%M:%S", time.localtime()))
            self.ids.lb_date.text = str(time.strftime("%d/%m/%Y", time.localtime()))
            screen_home.ids.lb_time.text = str(time.strftime("%H:%M:%S", time.localtime()))
            screen_home.ids.lb_date.text = str(time.strftime("%d/%m/%Y", time.localtime()))
            screen_login.ids.lb_time.text = str(time.strftime("%H:%M:%S", time.localtime()))
            screen_login.ids.lb_date.text = str(time.strftime("%d/%m/%Y", time.localtime()))
            screen_calibration.ids.lb_time.text = str(time.strftime("%H:%M:%S", time.localtime()))
            screen_calibration.ids.lb_date.text = str(time.strftime("%d/%m/%Y", time.localtime()))
            screen_sideslip_meter.ids.lb_time.text = str(time.strftime("%H:%M:%S", time.localtime()))
            screen_sideslip_meter.ids.lb_date.text = str(time.strftime("%d/%m/%Y", time.localtime()))

            self.ids.lb_dash_pendaftaran.text = str(dt_dash_pendaftaran)
            self.ids.lb_dash_belum_uji.text = str(dt_dash_belum_uji)
            self.ids.lb_dash_sudah_uji.text = str(dt_dash_sudah_uji)

            screen_sideslip_meter.ids.lb_sideslip_val.text = str(dt_sideslip_value)

            if(not flag_play):
                screen_sideslip_meter.ids.bt_save.md_bg_color = colors['Green']['200']
                screen_sideslip_meter.ids.bt_save.disabled = False
                screen_sideslip_meter.ids.bt_reload.md_bg_color = colors['Red']['A200']
                screen_sideslip_meter.ids.bt_reload.disabled = False
            else:
                screen_sideslip_meter.ids.bt_reload.disabled = True
                screen_sideslip_meter.ids.bt_save.disabled = True

            if(not flag_conn_stat):
                self.ids.lb_comm.color = colors['Red']['A200']
                self.ids.lb_comm.text = 'PLC Tidak Terhubung'
                screen_home.ids.lb_comm.color = colors['Red']['A200']
                screen_home.ids.lb_comm.text = 'PLC Tidak Terhubung'
                screen_login.ids.lb_comm.color = colors['Red']['A200']
                screen_login.ids.lb_comm.text = 'PLC Tidak Terhubung'
                screen_calibration.ids.lb_comm.color = colors['Red']['A200']
                screen_calibration.ids.lb_comm.text = 'PLC Tidak Terhubung'
                screen_sideslip_meter.ids.lb_comm.color = colors['Red']['A200']
                screen_sideslip_meter.ids.lb_comm.text = 'PLC Tidak Terhubung'

            else:
                self.ids.lb_comm.color = colors['Blue']['200']
                self.ids.lb_comm.text = 'PLC Terhubung'
                screen_home.ids.lb_comm.color = colors['Blue']['200']
                screen_home.ids.lb_comm.text = 'PLC Terhubung'
                screen_login.ids.lb_comm.color = colors['Blue']['200']
                screen_login.ids.lb_comm.text = 'PLC Terhubung'
                screen_calibration.ids.lb_comm.color = colors['Blue']['200']
                screen_calibration.ids.lb_comm.text = 'PLC Terhubung'
                screen_sideslip_meter.ids.lb_comm.color = colors['Blue']['200']
                screen_sideslip_meter.ids.lb_comm.text = 'PLC Terhubung'

            if(count_starting <= 0):
                screen_sideslip_meter.ids.lb_test_subtitle.text = "HASIL PENGUKURAN"
                screen_sideslip_meter.ids.lb_sideslip_val.text = str(dt_sideslip_value)

                if((dt_sideslip_value <= STANDARD_MAX_SIDESLIP) and (dt_sideslip_value >= -STANDARD_MAX_SIDESLIP)):
                    screen_sideslip_meter.ids.lb_info.text = f"Ambang Batas Bergesernya Roda Kendaraan adalah {STANDARD_MAX_SIDESLIP} mm,\nPergeseran Roda Kendaraan Anda Dalam Range Ambang Batas"
                else:
                    screen_sideslip_meter.ids.lb_info.text = f"Ambang Batas Bergesernya Roda Kendaraan adalah {STANDARD_MAX_SIDESLIP} mm,\nPergeseran Roda Kendaraan Anda Diluar Ambang Batas"

            elif(count_starting > 0):
                if(flag_play):
                    screen_sideslip_meter.ids.lb_test_subtitle.text = "MEMULAI PENGUKURAN"
                    screen_sideslip_meter.ids.lb_sideslip.text = str(count_starting)
                    screen_sideslip_meter.ids.lb_info.text = "Silahkan Gerakkan Kendaraan Anda Tanpa Memegang Kemudi"

            if(count_get_data <= 0):
                if(not flag_play):
                    if(dt_sideslip_value <= STANDARD_MAX_SIDESLIP):
                        screen_sideslip_meter.ids.lb_test_result.md_bg_color = colors['Green']['200']
                        screen_sideslip_meter.ids.lb_test_result.text = "LULUS"
                        dt_sideslip_flag = 1
                    else:
                        screen_sideslip_meter.ids.lb_test_result.md_bg_color = colors['Red']['A200']
                        screen_sideslip_meter.ids.lb_test_result.text = "TIDAK LULUS"
                        dt_sideslip_flag = 0
                if(not flag_play): # Jika tes sudah selesai
                    if(dt_sideslip_flag == 1): # LULUS
                        screen_sideslip_meter.ids.lb_info.text = "HASIL: Pergeseran roda kendaraan berada dalam batas toleransi yang diizinkan. Tekan SIMPAN untuk melanjutkan."
                    else: # TIDAK LULUS
                        screen_sideslip_meter.ids.lb_info.text = "HASIL: Pergeseran roda kendaraan MELEBIHI batas toleransi. Direkomendasikan untuk melakukan spooring."
                else: # Jika tes masih berjalan (tahap pengukuran)
                    screen_sideslip_meter.ids.lb_info.text = "PENGUKURAN: Harap jalankan kendaraan lurus ke depan secara perlahan melewati alat uji."

            elif(count_get_data > 0):
                screen_sideslip_meter.ids.lb_test_result.md_bg_color = "#EEEEEE"
                screen_sideslip_meter.ids.lb_test_result.text = ""
                screen_sideslip_meter.ids.lb_info.text = "PERSIAPAN: Uji akan dimulai. Luruskan kendaraan pada alat uji dan jangan sentuh kemudi."

            if self.screen_manager.current == 'screen_calibration':
                global SIDESLIP_OFFSET_NOL
                if flag_conn_stat:
                    try:
                        raw_reg = MODBUS_CLIENT.read_holding_registers(1622, 1, slave=1).registers[0]
                        scaled_reg = MODBUS_CLIENT.read_holding_registers(1612, 1, slave=1).registers[0]

                        scaled_value_from_plc = self.unsigned_to_signed(scaled_reg)
                        
                        final_value = scaled_value_from_plc - SIDESLIP_OFFSET_NOL

                        screen_calibration.ids.lb_raw_value.text = str(self.unsigned_to_signed(raw_reg))
                        screen_calibration.ids.lb_scaled_value.text = str(scaled_value_from_plc)
                        screen_calibration.ids.lb_final_value.text = f"{final_value:.2f}"
                        
                    except Exception as e:
                        screen_calibration.ids.lb_raw_value.text = "Error"
                        screen_calibration.ids.lb_scaled_value.text = "Error"
                        screen_calibration.ids.lb_final_value.text = "Error"

            self.ids.bt_calibrate.disabled = False if dt_user != '' else True
            self.ids.bt_logout.disabled = False if dt_user != '' else True
            self.ids.lb_operator.text = f'Login Sebagai: \n{dt_user}' if dt_user != '' else 'Silahkan Login'
            screen_home.ids.lb_operator.text = f'Login Sebagai: \n{dt_user}' if dt_user != '' else 'Silahkan Login'
            screen_login.ids.lb_operator.text = f'Login Sebagai: \n{dt_user}' if dt_user != '' else 'Silahkan Login'
            screen_calibration.ids.lb_operator.text = f'Login Sebagai: \n{dt_user}' if dt_user != '' else 'Silahkan Login'
            screen_sideslip_meter.ids.lb_operator.text = f'Login Sebagai: \n{dt_user}' if dt_user != '' else 'Silahkan Login'

            if dt_user != '':
                self.ids.img_user.source = f'https://{FTP_HOST}/ujikir/foto_user/{dt_foto_user}'
                screen_home.ids.img_user.source = f'https://{FTP_HOST}/ujikir/foto_user/{dt_foto_user}'
                screen_login.ids.img_user.source = f'https://{FTP_HOST}/ujikir/foto_user/{dt_foto_user}'
            else:
                self.ids.img_user.source = 'assets/images/icon-login.png'
                screen_home.ids.img_user.source = 'assets/images/icon-login.png'
                screen_login.ids.img_user.source = 'assets/images/icon-login.png'
            if dt_user == "":
                self.ids.lb_info.text = "Silakan login terlebih dahulu untuk dapat memilih kendaraan dan memulai pengujian."
            elif not flag_conn_stat:
                self.ids.lb_info.text = "PERINGATAN: PLC tidak terhubung. Periksa koneksi jaringan dan pastikan alat uji menyala."
            else:
                self.ids.lb_info.text = "SISTEM SIAP. Silakan pilih kendaraan dari daftar antrian di atas untuk memulai pengujian."

        except Exception as e:
            toast_msg = f'Gagal Memperbaharui Tampilan'
            toast(toast_msg)
            Logger.error(f"{self.name}: {toast_msg}, {e}")

    def regular_update_connection(self, dt):
        global flag_conn_stat
        try:
            if not MODBUS_CLIENT.is_socket_open():
                Logger.info("Modbus: Mencoba menghubungkan kembali...")
                MODBUS_CLIENT.connect()
            if MODBUS_CLIENT.read_holding_registers(0, 1, slave=1).isError():
                raise ConnectionError("Gagal membaca dari PLC")
            flag_conn_stat = True
        except Exception as e:
            Logger.warning(f"Modbus: Koneksi gagal atau terputus: {e}")
            flag_conn_stat = False
            MODBUS_CLIENT.close()

    def unsigned_to_signed(self, val):
        if val >= 32768:
            return val - 65536
        return val

    def regular_get_data(self, dt):
        global count_starting, count_get_data
        global dt_sideslip_value
        global flag_play
        global SIDESLIP_OFFSET_NOL
        try:
            if(count_starting > 0):
                count_starting -= 1

            if(count_get_data > 0):
                count_get_data -= 1
                
                if flag_conn_stat:
                    sideslip_registers = MODBUS_CLIENT.read_holding_registers(REGISTER_DATA_SIDE_SLIP, count=1, slave=1)
                    
                    scaled_value_from_plc = self.unsigned_to_signed(sideslip_registers.registers[0])
                    final_value = scaled_value_from_plc - SIDESLIP_OFFSET_NOL
                    dt_sideslip_value = abs(round(final_value/10,2))
            
            elif(count_get_data <= 0):
                flag_play = False
                Clock.unschedule(self.regular_get_data)
        except Exception as e:
            toast_msg = f'Gagal Mengambil Data dari PLC'
            toast(toast_msg)
            Logger.error(f"{self.name}: {toast_msg}, {e}")

    def exec_reload_database(self):
        global mydb
        try:
            mydb = mysql.connector.connect(host = DB_HOST,user = DB_USER,password = DB_PASSWORD, database = DB_NAME)
        except Exception as e:
            toast_msg = f'Gagal Menginisiasi Database'
            toast(toast_msg)
            Logger.error(f"{self.name}: {toast_msg}, {e}") 

    def exec_reload_table(self):
        global mydb, db_antrian
        global db_merk, db_bahan_bakar, db_warna
        global dt_dash_antri, dt_dash_belum_uji, dt_dash_sudah_uji
        global window_size_x, window_size_y

        try:
            cursor = mydb.cursor()
            today = str(time.strftime("%Y-%m-%d", time.localtime()))
            delete_query = f"DELETE FROM {TB_DATA} WHERE DATE(tgl_daftar) != %s"
            cursor.execute(delete_query, (today,))
            mydb.commit()
            toast_msg = f'Berhasil menghapus data kemarin'
        except Exception as e:
            toast_msg = f'Gagal menghapus data kemarin'
            toast(toast_msg)
            Logger.error(f"{self.name}: {toast_msg}, {e}")  

        try:
            cursor = mydb.cursor()
            cursor.execute(f"SELECT ID, DESCRIPTION FROM {TB_MERK}")
            result_tb_merk = cursor.fetchall()
            db_merk = np.array(result_tb_merk)

            cursor.execute(f"SELECT ID, DESCRIPTION FROM {TB_BAHAN_BAKAR}")
            result_tb_bahan_bakar = cursor.fetchall()
            db_bahan_bakar = np.array(result_tb_bahan_bakar)

            cursor.execute(f"SELECT id_warna, nama FROM {TB_WARNA}")
            result_tb_warna = cursor.fetchall()
            db_warna = np.array(result_tb_warna)

            cursor.execute(f"SELECT COUNT(*) FROM {TB_DATA}")
            result = cursor.fetchone()  # Returns tuple like (123,)

            if result is None:
                dt_dash_antri = 0
                toast('Data Tabel cekident kosong')
            else:
                dt_dash_antri = result[0]

                cursor.execute(f"SELECT noantrian, nopol, nouji, statusuji, merk, type, idjeniskendaraan, jbb, berat_kosong, bahan_bakar, warna, sideslip_flag FROM {TB_DATA} WHERE sideslip_flag = 2")
                result_tb_antrian = cursor.fetchall()
                db_antrian = np.array(result_tb_antrian).T

                db_pendaftaran = np.array(result_tb_antrian)
                dt_dash_belum_uji = db_pendaftaran[:,0].size
                dt_dash_sudah_uji = dt_dash_antri - dt_dash_belum_uji
            
            cursor.close()

        except Exception as e:
            toast_msg = f'Gagal mengambil data antrian harian'
            toast(toast_msg)
            Logger.error(f"{self.name}: {toast_msg}, {e}")  
        
        try:
            layout_list = self.ids.layout_list
            layout_list.clear_widgets(children=None)
        except Exception as e:
            toast_msg = f'Gagal menghapus widget tabel'
            toast(toast_msg)
            Logger.error(f"{self.name}: {toast_msg}, {e}")   
        
        try:
            layout_list = self.ids.layout_list
            for i in range(db_antrian[0,:].size):
                layout_list.add_widget(
                    MDCard(
                        MDLabel(text=f"{db_antrian[0, i]}", size_hint_x= 0.05),
                        MDLabel(text=f"{db_antrian[1, i]}", size_hint_x= 0.07),
                        MDLabel(text=f"{db_antrian[2, i]}", size_hint_x= 0.08),
                        MDLabel(text='Berkala' if db_antrian[3, i] == 'B' else 'Uji Ulang' if (db_antrian[3, i]) == 'U' else 'Baru' if (db_antrian[3, i]) == 'BR' else 'Numpang Uji' if (db_antrian[3, i]) == 'NB' else 'Mutasi', size_hint_x= 0.07),
                        MDLabel(text='-' if db_antrian[4, i] == None else f"{db_merk[np.where(db_merk == db_antrian[4, i])[0][0],1]}" , size_hint_x= 0.08),
                        MDLabel(text=f"{db_antrian[5, i]}", size_hint_x= 0.07),
                        MDLabel(text=f"{db_antrian[6, i]}", size_hint_x= 0.15),
                        MDLabel(text=f"{db_antrian[7, i]}", size_hint_x= 0.05),
                        MDLabel(text=f"{db_antrian[8, i]}", size_hint_x= 0.05),
                        MDLabel(text='-' if db_antrian[9, i] == None else f"{db_bahan_bakar[np.where(db_bahan_bakar == db_antrian[9, i])[0][0],1]}" , size_hint_x= 0.08),
                        MDLabel(text='-' if db_antrian[10, i] == None else f"{db_warna[np.where(db_warna == db_antrian[10, i])[0][0],1]}" , size_hint_x= 0.11),
                        MDLabel(text='Lulus' if (int(db_antrian[11, i]) == 1) else 'Tidak Lulus' if (int(db_antrian[11, i]) == 0) else 'Belum Uji', size_hint_x= 0.07),

                        ripple_behavior = True,
                        on_press = self.on_antrian_row_press,
                        padding = 20,
                        id=f"card_antrian{i}",
                        size_hint_y=None,
                        height=dp(int(60 * 800 / window_size_y)),
                        )
                    )
        except Exception as e:
            toast_msg = f'Gagal reload tabel'
            toast(toast_msg)
            Logger.error(f"{self.name}: {toast_msg}, {e}")  

    def on_antrian_row_press(self, instance):
        global mydb, db_antrian, db_merk, db_bahan_bakar, db_warna
        global dt_no_antri, dt_no_pol, dt_no_uji, dt_sts_uji
        global dt_merk, dt_type, dt_jns_kend, dt_jbb, dt_brt_ksg, dt_bhn_bkr, dt_warna, dt_sideslip_flag
        global dt_id_user, dt_foto_user

        try:
            row = int(str(instance.id).replace("card_antrian",""))
            dt_no_antri             = db_antrian[0, row]
            dt_no_pol               = db_antrian[1, row]
            dt_no_uji               = db_antrian[2, row]
            dt_sts_uji              = db_antrian[3, row]
            dt_merk                 = db_antrian[4, row]
            dt_type                 = db_antrian[5, row]
            dt_jns_kend             = db_antrian[6, row]
            dt_jbb                  = db_antrian[7, row]
            dt_brt_ksg              = db_antrian[8, row]
            dt_bhn_bkr              = db_antrian[9, row]
            dt_warna                = db_antrian[10, row]
            dt_sideslip_flag        = db_antrian[11, row]

            self.exec_start_test_directly()

        except Exception as e:
            toast_msg = f'Gagal mengeksekusi perintah dari baris tabel'
            toast(toast_msg)
            Logger.error(f"{self.name}: {toast_msg}, {e}")   

    def exec_start_test_directly(self):
        global dt_sideslip_flag, dt_no_antri, dt_user, flag_play
        global count_starting, count_get_data

        if (dt_user != ''):
            if (int(dt_sideslip_flag) == 2):
                
                count_starting = COUNT_STARTING_SIDESLIP
                count_get_data = COUNT_ACQUISITION_SIDESLIP

                if not flag_play:
                    Clock.schedule_interval(self.regular_get_data, GET_DATA_INTERVAL)
                    flag_play = True
                
                self.screen_manager.current = 'screen_sideslip_meter'

            else:
                toast_msg = f'No. Antrian {dt_no_antri} Sudah Melakukan Tes Sideslip'
                toast(toast_msg)
                Logger.info(f"{self.name}: {toast_msg}")
        else:
            toast_msg = f'Silahkan Login Untuk Melakukan Pengujian'
            toast(toast_msg)
            Logger.info(f"{self.name}: {toast_msg}")       

    def exec_logout(self):
        global dt_user

        dt_user = ""
        self.screen_manager.current = 'screen_login'

    def exec_navigate_home(self):
        try:
            self.screen_manager.current = 'screen_home'

        except Exception as e:
            toast_msg = f'Terjadi kesalahan saat berpindah ke halaman Beranda'
            toast(toast_msg)
            Logger.error(f"{self.name}: {toast_msg}, {e}")   

    def exec_navigate_login(self):
        global dt_user
        try:
            if (dt_user == ""):
                self.screen_manager.current = 'screen_login'
            else:
                toast_msg = f"Anda sudah login sebagai {dt_user}"
                toast(toast_msg)
                Logger.info(f"{self.name}: {toast_msg}")

        except Exception as e:
            toast_msg = f'Terjadi kesalahan saat berpindah ke halaman Login'
            toast(toast_msg)
            Logger.error(f"{self.name}: {toast_msg}, {e}")      


    def exec_navigate_calibration(self):
        global dt_user
        try:
            self.screen_manager.current = 'screen_calibration'

        except Exception as e:
            toast_msg = f'Error Navigate to Calibration Screen: {e}'
            toast(toast_msg)
            Logger.error(f"{self.name}: {toast_msg}, {e}")  

    def exec_navigate_main(self):
        try:
            self.screen_manager.current = 'screen_main'

        except Exception as e:
            toast_msg = f'Terjadi kesalahan saat berpindah ke halaman Utama'
            toast(toast_msg)
            Logger.error(f"{self.name}: {toast_msg}, {e}")    

class ScreenCalibration(MDScreen):
    def __init__(self, **kwargs):
        super(ScreenCalibration, self).__init__(**kwargs)
        Clock.schedule_once(self.delayed_init, 1)
    
    def delayed_init(self, dt):
        self.ids.lb_title.text = APP_TITLE
        self.ids.lb_subtitle.text = APP_SUBTITLE
        self.ids.img_pemkab.source = f'assets/images/{IMG_LOGO_PEMKAB}'
        self.ids.img_dishub.source = f'assets/images/{IMG_LOGO_DISHUB}'
        self.ids.lb_pemkab.text = LB_PEMKAB
        self.ids.lb_dishub.text = LB_DISHUB
        self.ids.lb_unit.text = LB_UNIT
        self.ids.lb_unit_address.text = LB_UNIT_ADDRESS

    def on_enter(self):
        global SIDESLIP_OFFSET_NOL 
        self.load_current_calibration()
        self.ids.tx_offset_nol.text = str(SIDESLIP_OFFSET_NOL)
        self.ids.lb_info.text = "Panduan: Posisikan alat pada titik MIN/MAX, lalu masukkan 'Nilai Raw Sensor' ke kolom input yang sesuai dan tekan KIRIM."

    def on_leave(self):
        pass

    def load_current_calibration(self):
        """Membaca nilai kalibrasi yang ada di PLC dan menampilkannya di text field."""
        global flag_conn_stat
        if not flag_conn_stat:
            toast("PLC tidak terhubung, tidak dapat memuat parameter.")
            return
        try:
            regs = MODBUS_CLIENT.read_holding_registers(1614, 4, slave=1).registers
            
            if regs:
                self.ids.tx_raw_min.text = str(regs[0])
                self.ids.tx_raw_max.text = str(regs[1])
                self.ids.tx_display_min.text = str(regs[2])
                self.ids.tx_display_max.text = str(regs[3])
        except Exception as e:
            toast(f"Gagal memuat parameter kalibrasi: {e}")
            Logger.error(f"{self.name}: Error loading calibration: {e}")

    def send_calibration_to_plc(self):
        """Mengirim nilai dari 4 text field ke register PLC 1614-1617."""
        global flag_conn_stat
        if not flag_conn_stat:
            toast("PLC tidak terhubung.")
            return
        try:
            raw_min = int(self.ids.tx_raw_min.text)
            raw_max = int(self.ids.tx_raw_max.text)
            display_min = int(self.ids.tx_display_min.text)
            display_max = int(self.ids.tx_display_max.text)

            MODBUS_CLIENT.write_registers(1614, [raw_min, raw_max, display_min, display_max], slave=1)
            
            self.save_offset_to_config() 
            self.ids.lb_info.text = "SUKSES: Parameter kalibrasi dan offset telah disimpan. Amati nilai 'Real-Time' untuk verifikasi."
            toast("Parameter kalibrasi berhasil dikirim.")

        except Exception as e:
            toast(f"Gagal mengirim data: {e}")
            Logger.error(f"{self.name}: Error sending calibration: {e}")

    def save_offset_to_config(self):
        """Menyimpan nilai dari tx_offset_nol ke file config.ini."""
        global SIDESLIP_OFFSET_NOL # Ini penting untuk mengubah variabel global
        try:
            new_offset = float(self.ids.tx_offset_nol.text)
            config.set('sideslip', 'OFFSET_NOL', str(new_offset))
            with open(config_full_path, 'w') as configfile:
                config.write(configfile)
            
            SIDESLIP_OFFSET_NOL = new_offset
            toast(f"Offset Nol berhasil disimpan: {new_offset}")
        except Exception as e:
            toast(f"Gagal menyimpan offset: {e}")
            Logger.error(f"{self.name}: Error saving offset: {e}")

    def reset_calibration_default(self):
        """Mengirim sinyal reset ke coil di PLC, lalu menjadwalkan untuk mematikannya."""
        global flag_conn_stat
        if not flag_conn_stat:
            toast("PLC tidak terhubung.")
            return
        try:
            MODBUS_CLIENT.write_coil(3102, True, slave=1)
            toast("Sinyal Reset telah dikirim ke PLC.")
            Clock.schedule_once(self._turn_off_reset_coil, 0.5)
            Clock.schedule_once(lambda dt: self.load_current_calibration(), 1)
            
        except Exception as e:
            toast(f"Gagal mengirim sinyal Reset: {e}")
            Logger.error(f"{self.name}: Error sending reset signal: {e}")

    def _turn_off_reset_coil(self, dt):
        """Fungsi helper untuk mengirim perintah mematikan coil."""
        try:
            MODBUS_CLIENT.write_coil(3102, False, slave=1)
            Logger.info(f"{self.name}: Reset coil (3102) turned OFF.")
        except Exception as e:
            Logger.error(f"{self.name}: Failed to turn off reset coil: {e}")

    def exec_navigate_main(self):
        try:
            self.screen_manager.current = 'screen_main'
        except Exception as e:
            toast_msg = f'Terjadi kesalahan saat berpindah ke halaman Utama'
            toast(toast_msg)
            Logger.error(f"{self.name}: {toast_msg}, {e}")

class ScreenSideSlipMeter(MDScreen):        
    def __init__(self, **kwargs):
        super(ScreenSideSlipMeter, self).__init__(**kwargs)
        Clock.schedule_once(self.delayed_init, 1)
    
    def delayed_init(self, dt):
        self.ids.img_pemkab.source = f'assets/images/{IMG_LOGO_PEMKAB}'
        self.ids.img_dishub.source = f'assets/images/{IMG_LOGO_DISHUB}'
        self.ids.lb_pemkab.text = LB_PEMKAB
        self.ids.lb_dishub.text = LB_DISHUB
        self.ids.lb_unit.text = LB_UNIT
        self.ids.lb_unit_address.text = LB_UNIT_ADDRESS

    def on_enter(self):
        global db_merk, db_bahan_bakar, db_warna
        global dt_no_antri, dt_no_pol, dt_no_uji, dt_sts_uji
        global dt_merk, dt_type, dt_jns_kend, dt_jbb, dt_brt_ksg, dt_bhn_bkr, dt_warna

        self.ids.lb_no_antri.text = str(dt_no_antri)
        self.ids.lb_no_pol.text = str(dt_no_pol)
        self.ids.lb_no_uji.text = str(dt_no_uji)
        self.ids.lb_sts_uji.text = 'Berkala' if dt_sts_uji == 'B' else 'Uji Ulang' if dt_sts_uji == 'U' else 'Baru' if dt_sts_uji == 'BR' else 'Numpang Uji' if dt_sts_uji == 'NB' else 'Mutasi'
        self.ids.lb_merk.text = '-' if dt_merk == None else f"{db_merk[np.where(db_merk == dt_merk)[0][0],1]}"
        self.ids.lb_type.text = str(dt_type)
        self.ids.lb_jns_kend.text = str(dt_jns_kend)
        self.ids.lb_jbb.text = str(dt_jbb)
        self.ids.lb_brt_ksg.text = str(dt_brt_ksg)
        self.ids.lb_bhn_bkr.text = '-' if dt_bhn_bkr == None else f"{db_bahan_bakar[np.where(db_bahan_bakar == dt_bhn_bkr)[0][0],1]}"
        self.ids.lb_warna.text = '-' if dt_warna == None else f"{db_warna[np.where(db_warna == dt_warna)[0][0],1]}"
        
        self.exec_start_sideslip()

    def exec_start_sideslip(self):
        global flag_play
        global count_starting, count_get_data
        try:
            screen_main = self.screen_manager.get_screen('screen_main')

            count_starting = COUNT_STARTING_SIDESLIP
            count_get_data = COUNT_ACQUISITION_SIDESLIP

            if(not flag_play):
                Clock.schedule_interval(screen_main.regular_get_data, GET_DATA_INTERVAL)
                flag_play = True            
        except Exception as e:
            toast_msg = f'Terjadi kesalahan saat memulai pengujian Sideslip'
            toast(toast_msg)
            Logger.error(f"{self.name}: {toast_msg}, {e}")  


    def exec_reload(self):
        global flag_play
        global count_starting, count_get_data, dt_sideslip_value
        try:
            screen_main = self.screen_manager.get_screen('screen_main')
            count_starting = COUNT_STARTING_SIDESLIP
            count_get_data = COUNT_ACQUISITION_SIDESLIP
            dt_sideslip_value = 0
            self.ids.bt_reload.disabled = True
            self.ids.lb_sideslip_val.text = "..."

            if(not flag_play):
                Clock.schedule_interval(screen_main.regular_get_data, GET_DATA_INTERVAL)
                flag_play = True          
        except Exception as e:
            toast_msg = f'Terjadi kesalahan saat memulai ulang pengujian Sideslip'
            toast(toast_msg)
            Logger.error(f"{self.name}: {toast_msg}, {e}")  

    def exec_save(self):
        global mydb, db_antrian
        global dt_no_antri, dt_no_pol, dt_no_uji, dt_nama
        global dt_sideslip_flag, dt_sideslip_value, dt_id_user

        self.ids.bt_save.disabled = True
        try:
            tb_sideslip_data = mydb.cursor()
            sql = f"UPDATE {TB_DATA} SET sideslip_flag = %s, sideslip_value = %s, sideslip_user = %s, sideslip_post = %s WHERE noantrian = %s"
            sql_sideslip_flag = dt_sideslip_flag
            now = str(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()))
            sql_val = (sql_sideslip_flag, dt_sideslip_value, dt_id_user, now, dt_no_antri)
            tb_sideslip_data.execute(sql, sql_val)
            mydb.commit()
            self.open_screen_main()
            self.ids.bt_save.disabled = True

        except Exception as e:
            toast_msg = f'Gagal menyimpan data sideslip ke tabel antrian'
            toast(toast_msg)
            Logger.error(f"{self.name}: {toast_msg}, {e}") 

    def exec_print(self):
        try:
            global dt_sideslip_flag
            tb_status = mydb.cursor()
            tb_status.execute(f"SELECT sideslip_flag FROM {TB_DATA} WHERE noantrian = '{dt_no_antri}'")
            result_tb_status = tb_status.fetchone()
            mydb.commit()
            db_status = np.array(result_tb_status).T
            dt_sideslip_flag = int(db_status[0])
            
            self.exec_print_pdf()

            self.ids.bt_print.disabled = True

        except Exception as e:
            toast_msg = f'Gagal Mencetak Hasil Uji'
            toast(toast_msg)
            Logger.error(f"{self.name}: {toast_msg}, {e}")  

    def exec_print_pdf(self):
        global flag_play
        global count_starting, count_get_data
        global mydb, db_antrian
        global dt_no_antri, dt_no_pol, dt_no_uji, dt_nama, dt_jns_kend

        try:
            print_datetime = str(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()))
            pdf = FPDF()
            pdf.add_page()
            pdf.set_xy(0, 2)
            pdf.image(f"assets/images/{IMG_LOGO_DISHUB}", w=30.0, h=0, x=20)
            pdf.set_xy(0, 2)
            pdf.image(f"assets/images/{IMG_LOGO_PEMKAB}", w=30.0, h=0, x=180)            
            pdf.set_font('Arial', 'B', 24.0)
            pdf.cell(ln=1, h=5.0, w=0)
            pdf.cell(ln=1, h=15.0, align='C', w=0, txt="DINAS PERHUBUNGAN", border=0)
            pdf.cell(ln=1, h=15.0, align='C', w=0, txt="UPTD PKB KAB. PANDEGLANG", border=0)
            pdf.cell(ln=1, h=5.0, w=0)
            pdf.set_font('Arial', 'B', 14.0)
            pdf.cell(ln=0, h=10.0, align='L', w=0, txt=f"Tanggal: {print_datetime}", border=0)
            pdf.cell(ln=1, h=10.0, align='R', w=0, txt=f"No Reg Kend: {dt_no_pol}", border=0)
            pdf.cell(ln=0, h=10.0, align='L', w=0, txt=f"No Antrian: {dt_no_antri}", border=0)
            pdf.cell(ln=1, h=10.0, align='R', w=0, txt=f"No Uji: {dt_no_uji}", border=0)
            pdf.cell(ln=1, h=10.0, align='L', w=0, txt=f"Jenis Kendaraan: {dt_jns_kend}", border=0)
            pdf.cell(ln=1, h=10.0, align='L', w=0, txt=f"Nama: {dt_nama}", border=0)
            pdf.cell(ln=0, h=10.0, align='L', w=0, txt=f"JBB: {dt_jbb}", border=0)
            pdf.cell(ln=1, h=10.0, align='R', w=0, txt=f"Berat Kosong: {float(dt_brt_ksg)}", border=0)
            pdf.cell(ln=1, h=10.0, w=0)
            pdf.set_font('Arial', '', 14.0)
            pdf.cell(ln=1, h=10.0, align='L', w=80, txt=f"SIDESLIP METER")
            pdf.cell(ln=1, h=10.0, align='L', w=0, txt=f"Nilai Pengujian : {float(dt_sideslip_value)} mm")
            pdf.cell(ln=1, h=10.0, align='L', w=0, txt=f"Status Pengujian: {'Lulus' if int(dt_sideslip_flag) == 1 else 'Tidak Lulus' if int(dt_sideslip_flag) == 0 else 'Belum Diuji'}")
            pdf.cell(ln=1, h=5.0, w=0)

            documents_dir = os.path.join(os.environ["USERPROFILE"], "Documents")

            folder_name = f"Hasil_Uji_VIIS_Sideslip_Tester_{time.strftime('%Y-%m-%d', time.localtime())}"
            date_folder_path = os.path.join(documents_dir, folder_name)
            
            if not os.path.exists(date_folder_path):
                os.makedirs(date_folder_path)
                toast(f"Folder created: {date_folder_path}")
            else:
                toast(f"Folder already exists: {date_folder_path}")

            pdf_filename = f"Hasil_Uji_No_{dt_no_antri}.pdf"
            pdf_path = os.path.join(date_folder_path, pdf_filename)

            pdf.output(pdf_path, 'F')
            toast(f"PDF saved to: {pdf_path}")
            os.startfile(pdf_path)

        except Exception as e:
            toast_msg = f'Gagal menyimpan ke pdf'
            toast(toast_msg)
            Logger.error(f"{self.name}: {toast_msg}, {e}")  

    def open_screen_main(self):
        global flag_play        
        global count_starting, count_get_data

        try:
            screen_main = self.screen_manager.get_screen('screen_main')
            flag_play = False
            self.screen_manager.current = 'screen_main'
        except Exception as e:
            toast_msg = f'Gagal Berpindah halaman ke Main: {e}'
            toast(toast_msg)

class RootScreen(ScreenManager):
    pass             

class SideslipApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_resize=self.on_window_resize)

    def build(self):
        global window_size_x, window_size_y
        self.theme_cls.colors = colors
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.accent_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        self.icon = 'assets/images/logo-load-app.png'
        window_size_y = Window.size[0]
        window_size_x = Window.size[1]
        self.set_dynamic_fonts(Window.size)

        LabelBase.register(
            name="Orbitron-Regular",
            fn_regular="assets/fonts/Orbitron-Regular.ttf")
        
        LabelBase.register(
            name="Draco",
            fn_regular="assets/fonts/Draco.otf")        

        LabelBase.register(
            name="Recharge",
            fn_regular="assets/fonts/Recharge.otf") 
        
        theme_font_styles.append('H1')
        self.theme_cls.font_styles["H1"] = [
            "Orbitron-Regular", 64, False, 0.15]       

        theme_font_styles.append('H2')
        self.theme_cls.font_styles["H2"] = [
            "Orbitron-Regular", 32, False, 0.15] 
        
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
            "Recharge", 11, False, 0.15] 

        theme_font_styles.append('Body1')
        self.theme_cls.font_styles["Body1"] = [
            "Recharge", 10, False, 0.15] 
        
        theme_font_styles.append('Button')
        self.theme_cls.font_styles["Button"] = [
            "Recharge", 9, False, 0.15] 

        theme_font_styles.append('Caption')
        self.theme_cls.font_styles["Caption"] = [
            "Recharge", 8, False, 0.15]       
        
        Window.fullscreen = 'auto'
        Builder.load_file('main.kv')
        return RootScreen()

    def on_window_resize(self, window, width, height):
        Logger.info(f"Window size: {width}x{height}")
        self.set_dynamic_fonts((width, height))
        self.refresh_all_fonts()

    def refresh_all_fonts(self):
        if hasattr(self, 'root') and hasattr(self.root, 'screens'):
            for screen in self.root.screens:
                self.refresh_fonts(screen)

    def refresh_fonts(self, widget):
        from kivymd.uix.label import MDLabel
        if isinstance(widget, MDLabel):
            original_style = widget.font_style
            temp_style = "Body1" if original_style != "Body1" else "H6"
            widget.font_style = temp_style
            widget.font_style = original_style
        if hasattr(widget, 'children'):
            for child in widget.children:
                self.refresh_fonts(child)

    def set_dynamic_fonts(self, size):
        try:
            screen_size_x = Window.system_size[0]
            screen_size_y = Window.system_size[1]
        except AttributeError:
            screen_size_x = Window._get_system_size()[0]
            screen_size_y = Window._get_system_size()[1]
        font_size_l = np.array([64, 32, 30, 20, 16, 11, 10, 9, 8])
        scale = min(screen_size_x / 1920, screen_size_y / 1080)
        font_size = np.round(font_size_l * scale, 0)
        Logger.info(f"Font resized: {font_size_l} to {font_size}")
        self.theme_cls.font_styles["H1"] = [
            "Orbitron-Regular", font_size[0], False, 0.15]
        self.theme_cls.font_styles["H2"] = [
            "Orbitron-Regular", font_size[1], False, 0.15]
        self.theme_cls.font_styles["H4"] = [
            "Recharge", font_size[2], False, 0.15]
        self.theme_cls.font_styles["H5"] = [
            "Recharge", font_size[3], False, 0.15]
        self.theme_cls.font_styles["H6"] = [
            "Recharge", font_size[4], False, 0.15]
        self.theme_cls.font_styles["Subtitle1"] = [
            "Recharge", font_size[5], False, 0.15]
        self.theme_cls.font_styles["Body1"] = [
            "Recharge", font_size[6], False, 0.15]
        self.theme_cls.font_styles["Button"] = [
            "Recharge", font_size[7], False, 0.15]
        self.theme_cls.font_styles["Caption"] = [
            "Recharge", font_size[8], False, 0.15]       

        if hasattr(self, 'root'):
            self.refresh_fonts(self.root)

if __name__ == '__main__':
    SideslipApp().run()
