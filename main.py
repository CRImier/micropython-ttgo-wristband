from hw import *
from time import sleep
import machine

machine.freq(80*1000*1000)

import wifi

def scan_i2c():
    print([hex(i) for i in i2c.scan()])

#scan_i2c()

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
    print("Going to sleep")
    machine.deepsleep()

init_all_hw()


red = color565(255, 0, 0)
blue = color565(0, 0, 255)
green = color565(0, 255, 0)

lcd.fill(green)
lcd_bl.on()
sleep(1)

led.value(is_charging())

"""
lcd.fill(red)

colors = (0, green, blue, green|blue, red|blue, red|green|blue)

for i in range(80/5):
    lcd.pixel(i*10, i*5, colors[(i+0)%len(colors)])

lcd.fill_rectangle(10, 15, 20, 30, green|red)
lcd.fill_rectangle(30, 45, 20, 30, blue|red)
"""

sleep(1)
lcd.fill(0)
lcd.text("Hello world!", 0, 0, color=green)
lcd.text(" ".join([hex(i) for i in i2c.scan()]), 0, 10, color=blue)
lcd.text("Going to sleep in", 0, 30, color=green)
lcd.text("5 seconds!", 0, 40, color=green)

for i in range(10):
    voltage_texts = battery_voltage(str=True) + "V " + charging_voltage(str=True) + "V"
    lcd.text(voltage_texts, 0, 20, color=red)
    sleep(0.5)
deepsleep()

