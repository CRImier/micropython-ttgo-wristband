import network

sta = network.WLAN(network.STA_IF)
ap = network.WLAN(network.AP_IF)

ap.active(False)
sta.active(True)

sta.connect("ssid", "password")
print(sta.ifconfig())
