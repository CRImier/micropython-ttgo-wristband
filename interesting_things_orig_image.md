`strings -n 10 orig_image.bin | head -n 95 | tail -n 29`

```
 I should be 
MPU9250 is online...
MPU9250 acceleration and gyration self test done!
MPU9250 initialized for active data mode....
AK8963 initialized for active data mode....
AK8963 magCalibration done!
I2C device found at address 0x
Unknow error at address 0x
No I2C devices found
Scan Network
no networks found
[%d]:%s(%d)
RTC Interrupt self test
Write DateTime FAIL
Write DateTime PASS
RTC Interrupt PASS
eFuse Vref:%u mV
Two Point --> coeff_a:%umV coeff_b:%umV
Default Vref: 1100mV
Dec  6 2019
--  ACC  GYR   MAG
x %.2f  %.2f  %.2f
y %.2f  %.2f  %.2f
z %.2f  %.2f  %.2f
Press again to wake up
Go to Sleep
g5h=G=F5F5F-%
%d-%d-%d/%d:%d:%d
syncToRtc: %d %d %d - %d %d %d 
```
