# micropython-ttgo-wristband

~~Code and data about TTGO/LilyGo T-Wristband and running MicroPython on it~~

MicroPython code for the T-Wristband platform. My wristband has an external battery attached - and a vibromotor, too.
It vibrates every minute. It can also do more.

Working:

- I2C interface
- Touch button
- Deepsleep wake using touch button
- Display backlight (PWMed)
- Display
- VBAT ADC
- VBUS ADC
- Charging detection
- MPU-9250
- RTC - no lib brought in, but it's query-able over I2C alright (use [this](https://github.com/lewisxhe/PCF8563_PythonLibrary/)?)

Not yet fully working (code not written/not yet tested/imperfect):

- Properly bringing out the display from low-power mode after deepsleep without a hardware reset of the display
- Bringing up the display after a Ctrl+D soft reset (is brought up from power-on reset and from deepsleep reset)
- Some GPIOs might not be brought into/from deepsleep correctly. This might be causing the two previous problems.

- `main.py`
  - My current `main.py` file
- `hw.py`
  - File with hardware definitions - pins, interfaces, some helper functions
- `st7735.py`
  - st7735 driver - not mine, taken from some other project, is under a different license
- `pwm_pin.py`
  - An object for a PWM-driven pin that still allows to treat the PWM object as a pin ( with .on(), .off() and .value(value) )
- `wifi.py`
  - File for your WiFi settings
- `ttp223_deepsleep_example.py`
  - A standalone example of how to do deepsleep with the TTP223
- `orig_image.bin`
  - The original ESP32 image that the wristband came flashed with from the factory. Source is not available, so, the image by itself is of interest.
- `original_firmware_serial_log.txt`
  - Log produced on the serial port when the original image executes and the touch button is pressed. Recorded using screen -L /dev/ttyUSB0 115200
- `original_firmware_serial_log_commented.txt`
  - Same log, but with comments marking moments when the button is pressed and when different things are shown on the screen
- `read_orig_image_cli.sh`
  - Script that contains the commandline to read the original image from the ESP32
- `write_orig_image_cli.sh`
  - Script that contains the commandline to write the original image back to the ESP32
- `interesting_things_orig_image.md`
  - Interesting observations about the original image
- `esp32-idf4-20191220-v1.12.bin`
  - The MicroPython image I'm using with this board
- `flash_micropython.sh`
  - A script to flash the MicroPython image included

MPU9250 bringup is two-step. AK8963 won't appear on the I2C bus (0x0C address) until you enable I2C passthrough mode on the MPU6500, and, this board
has a different I2C address for the MPU6500: 0x69.

```python
>>> from mpu9250 import MPU9250
>>> from mpu6500 import MPU6500
>>> m = MPU6500(i2c, address=0x69)
>>> m = MPU9250(i2c, mpu6500=m)
>>> i2c.scan()
[12, 81, 105]
```
MPU9250 code [available from here](https://github.com/tuupola/micropython-mpu9250/)
