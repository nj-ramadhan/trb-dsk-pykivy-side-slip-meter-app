import pyaudio
import time
from math import log10
import audioop  

p = pyaudio.PyAudio()
WIDTH = 2
RATE = int(p.get_default_input_device_info()['defaultSampleRate'])
DEVICE = p.get_default_input_device_info()['index']
rms = 1
print(p.get_default_input_device_info())

def callback(in_data, frame_count, time_info, status):
    global rms, amp
    rms = audioop.rms(in_data, WIDTH) / 32767
    return in_data, pyaudio.paContinue


stream = p.open(format=p.get_format_from_width(WIDTH),
                input_device_index=DEVICE,
                channels=2,
                rate=RATE,
                input=True,
                output=False,
                stream_callback=callback)

stream.start_stream()

while stream.is_active(): 
    db = 20 * log10(rms) #0.033, 0.109, 0.347
    # mod = 20 * log10(rms * 32767)
    mod_Amp = rms * 1600000
    # mod_Amp = amp * 1518727
    mod_dB = 20 * log10(mod_Amp)
    print(f"RMS: {rms} DB: {db} mod_Amp: {mod_Amp} mod_dB: {mod_dB}") 
    # refresh every 0.3 seconds 
    time.sleep(0.3)

stream.stop_stream()
stream.close()

p.terminate()