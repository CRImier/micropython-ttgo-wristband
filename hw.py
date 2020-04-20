from machine import Pin, ADC, I2C, SPI
import machine
import gc

from st7735 import ST7735
from pwm_pin import PWMPin

led_p = 4

vbus_p = 36
vbat_p = 35
chg_p = 32

touch_en_p = 25
touch_p = 33

sda_p = 21
scl_p = 22
rtc_int_p = 34
mpu_int_p = 38

# Yes, the PCB has native MISO and MOSI switched
# No idea why. It's an old bug, same goes for TTGO T-Display
lcd_mosi_p = 19
lcd_miso_p = 23 # unconnected - fake pin
lcd_sck_p = 18
lcd_cs_p = 5
lcd_dc_p = 23
lcd_rst_p = 26
lcd_bl_p = 27


led = PWMPin(led_p, on_duty=512, init_value=0)

i2c = I2C(sda=Pin(sda_p, Pin.OUT, None), scl=Pin(scl_p, Pin.OUT, None))

#sck = Pin(lcd_sck_p, Pin.OUT, None)
#mosi = Pin(lcd_sck_p, Pin.OUT, None)
#spi = SPI(2, sck=sck, mosi=mosi, miso=Pin(lcd_miso_p), baudrate=20*1000*1000, polarity=0, phase=0)
spi = SPI(2, sck=Pin(lcd_sck_p), mosi=Pin(lcd_mosi_p), miso=Pin(lcd_miso_p), baudrate=20*1000*1000, polarity=0, phase=0)

vbat = ADC(Pin(vbat_p))
vbus = ADC(Pin(vbus_p))
chg = Pin(chg_p, Pin.IN, Pin.PULL_UP)

touch = Pin(touch_p, Pin.IN, None)
touch_en = Pin(touch_en_p, Pin.OUT, None)

rtc_int = Pin(rtc_int_p, Pin.IN, None)
mpu_int = Pin(mpu_int_p, Pin.IN, None)

lcd_bl = PWMPin(lcd_bl_p, on_duty=512, init_value=0)

lcd = ST7735(160, 80, spi, Pin(lcd_cs_p), Pin(lcd_dc_p), Pin(lcd_rst_p))

def init_display(reset_cause=None):
    if reset_cause is None:
        reset_cause = machine.reset_cause()
    """if reset_cause in (machine.PWRON_RESET, machine.HARD_RESET):
        print("Doing hard HW reset")"""
    lcd.pwron_init()
    """elif reset_cause in (machine.WDT_RESET, machine.DEEPSLEEP_RESET, machine.SOFT_RESET):
        print("Doing soft HW bringup")
        lcd.init_gpio()
        lcd.from_sleep()
        lcd.turn_on()"""

def init_all_hw():
    init_display()

def deinit_hw_for_deepsleep(leave_touch=True):
    lcd.turn_off()
    lcd.to_sleep()

    Pin(led_p, Pin.IN, Pin.PULL_HOLD)

    #Pin(vbat_p, Pin.IN, Pin.PULL_HOLD)
    #Pin(vbus_p, Pin.IN, Pin.PULL_HOLD)
    Pin(chg_p, Pin.IN, Pin.PULL_HOLD)

    #Pin(rtc_int_p, Pin.IN, Pin.PULL_HOLD)
    #Pin(mpu_int_p, Pin.IN, Pin.PULL_HOLD)

    Pin(lcd_bl_p, Pin.IN, Pin.PULL_HOLD)
    Pin(lcd_mosi_p, Pin.IN, Pin.PULL_HOLD)
    Pin(lcd_sck_p, Pin.IN, Pin.PULL_HOLD)
    Pin(lcd_cs_p, Pin.IN, Pin.PULL_HOLD)
    Pin(lcd_dc_p, Pin.IN, Pin.PULL_HOLD)
    Pin(lcd_rst_p, Pin.IN, Pin.PULL_HOLD)

    if not leave_touch:
        Pin(touch_p, Pin.IN, Pin.PULL_HOLD)
        Pin(touch_en_p, Pin.IN, Pin.PULL_HOLD)
    else:
        Pin(touch_en_p, Pin.OUT, None)
        Pin(touch_en_p, Pin.OUT, Pin.PULL_HOLD, value=1)


# Display functions
def color565(r, g, b):
    return (b & 0xf8) << 8 | (g & 0xfc) << 3 | r >> 3
