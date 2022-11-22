from machine import Pin, PWM
from time import sleep

from machine import Pin, PWM
from time import sleep

pwm = PWM(Pin(20))

pwm.freq(300)

while True:
    for duty in range(65025):
        pwm.duty_u16(duty)
        sleep(0.0001)
    for duty in range(65025, 0, -1):
        pwm.duty_u16(duty)
        sleep(0.0001)