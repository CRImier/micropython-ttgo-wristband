from machine import Pin, deepsleep
from time import sleep
import esp32

touch_en_p = 25
touch_p = 33

touch = Pin(touch_p, Pin.IN)
Pin(touch_en_p, Pin.OUT, Pin.PULL_HOLD, value=1)

esp32.wake_on_ext0(pin=touch, level=esp32.WAKEUP_ANY_HIGH)
print("Will sleep in 5 seconds")
sleep(5)
print("Going to sleep")
deepsleep()
