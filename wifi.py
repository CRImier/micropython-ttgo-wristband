import network

sta = network.WLAN(network.STA_IF)
ap = network.WLAN(network.AP_IF)

sta_ssid = "ssid"
sta_password = "password"

def default_setup():
    ap.active(False)
    sta.active(True)

def connect():
    sta.connect(sta_ssid, sta_password)
