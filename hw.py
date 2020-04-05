from machine import Pin, ADC, I2C, SPI

from st7735 import ST7735

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

lcd_mosi_p = 19
lcd_sck_p = 18
lcd_cs_p = 5
lcd_dc_p = 23
lcd_rst_p = 26
lcd_bl_p = 27


led = Pin(led_p, Pin.OUT)

i2c = I2C(sda=Pin(sda_p), scl=Pin(scl_p))
spi = SPI(mosi=Pin(lcd_mosi_p), sck=Pin(lcd_sck_p), miso=Pin(37))

vbat = ADC(Pin(vbat_p))
vbus = ADC(Pin(vbus_p))
chg = Pin(chg_p, Pin.IN, Pin.PULL_UP)

touch = Pin(touch_p, Pin.IN)
touch_en = Pin(touch_en_p, Pin.OUT)

rtc_int = Pin(rtc_int_p, Pin.IN)
mpu_int = Pin(mpu_int_p, Pin.IN)

lcd_bl = Pin(lcd_bl_p, Pin.OUT, None)

lcd = ST7735(160, 80, spi, Pin(lcd_cs_p), Pin(lcd_dc_p), Pin(lcd_rst_p))


def deinit_hw_for_deepsleep(leave_touch=True):
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
