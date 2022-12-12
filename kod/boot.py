import gc
import machine
import network
import upip
import senko
import time


def connect_wlan(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    sta_if.active(True)
    ap_if.active(False)

    if not sta_if.isconnected():
        print("Connecting to WLAN ({})...".format(ssid))
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass

    return True
    

SSID = "Test"
PASSWORD = "Lifelinetest51"

connect_wlan(SSID, PASSWORD)
    
OTA = senko.Senko(user="cinarseyit", repo="Lifeline", branch = "main", working_dir="code", files=["main.py"])

if OTA.update():
    print("Updated to the latest version! Rebooting...")
    time.sleep(5)
    machine.reset()



