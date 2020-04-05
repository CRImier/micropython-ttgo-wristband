# micropython-ttgo-wristband
Code and data about TTGO/LilyGo T-Wristband and running MicroPython on it

- `esp32-idf4-20191220-v1.12.bin`
  - The MicroPython image I'm using with this board
- `main.py`
  - My current `main.py` file
- `hw.py`
  - File with hardware definitions - pins, interfaces, some helper functions
- `st7735.py`
  - st7735 driver - not mine, taken from some other project, is under a different license
- `wifi.py`
  - File with WiFi settings
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

