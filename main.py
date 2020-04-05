from hw import *
from time import sleep
import machine

lcd.fill(0x7521)
lcd_bl.on()

import wifi

def scan_i2c():
    print([hex(i) for i in i2c.scan()])

scan_i2c()

def get_ip():
    import urequests as requests
    r = requests.get("http://icanhazip.com")
    return r.text.strip()

def read_touch():
    while True:
        print(touch.value())
        sleep(0.1)

def deepsleep():
    import esp32
    esp32.wake_on_ext0(pin=touch, level=esp32.WAKEUP_ANY_HIGH)
    # for deepsleep testing with the breakout
    # esp32.wake_on_ext1(pins=(Pin(14, Pin.IN, Pin.PULL_DOWN), touch), level=esp32.WAKEUP_ANY_HIGH)
    deinit_hw_for_deepsleep()
    #touch_en.on()
    print("Going to sleep")
    machine.deepsleep()

print("Will sleep in 5 seconds")
sleep(5)
deepsleep()
