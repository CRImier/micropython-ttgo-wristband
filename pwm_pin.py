from machine import Pin, PWM

max_pwm_duty = 1023

class PWMPin():
    def __init__(self, num, on_duty=1023, off_duty=0, init_value=1):
        self.p = Pin(num, Pin.OUT, None, value=init_value)
        if on_duty > max_pwm_duty:
            on_duty = max_pwm_duty
        init_duty = on_duty if init_value else off_duty
        self.pwm = PWM(self.p, duty=init_duty)
        self.on_duty = on_duty
        self.off_duty = off_duty
        self.on = init_value

    def on(self):
        self.on = True
        self.pwm.duty(self.on_duty)

    def off(self):
        self.on = False
        self.pwm.duty(self.off_duty)

    def value(self, value=None):
        if value is None: return self.on
        self.on() if value else self.off()

    def duty(self, duty=None):
        if duty is None: return self.pwm.duty()
        if duty > max_pwm_duty:
            duty = max_pwm_duty
        self.pwm.duty(duty)
