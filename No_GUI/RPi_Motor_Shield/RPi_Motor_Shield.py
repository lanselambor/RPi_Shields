
'''
/*
 * RPi_Motor_Shield.py
 * Demo for RAspberry Pi Motor Shield 
 *
 * Copyright (c) 2012 seeed technology inc.
 * Website    : www.seeed.cc
 * Author     : Lambor
 * Create Time: Nov 2015
 * Change Log :
 *
 * The MIT License (MIT)
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
'''
#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import signal	

from PiSoftPwm import *

#print 'Go_1...'
#frequency = 1.0 / self.sc_1.GetValue()
#speed = self.sc_2.GetValue()
	



class Motor():
    def __init__(self):
	# MC33932 pins
	self.PWMA = 25  
	self.PWMB = 22
	self._IN1 = 23  
	self._IN2 = 24 
	self._IN3 = 17
	self._IN4 = 27

	# Initialize PWMA PWMB 
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(self.PWMA, GPIO.OUT)
	GPIO.setup(self.PWMB, GPIO.OUT)
	GPIO.output(self.PWMA, True)
	GPIO.output(self.PWMB, True)


	# Initialize PWM outputs
	self.OUT_1  = PiSoftPwm(0.1, 100, self._IN1, GPIO.BCM)
	self.OUT_2  = PiSoftPwm(0.1, 100, self._IN2, GPIO.BCM)
	self.OUT_3  = PiSoftPwm(0.1, 100, self._IN3, GPIO.BCM)
	self.OUT_4  = PiSoftPwm(0.1, 100, self._IN4, GPIO.BCM)

        # Close pwm output
	self.OUT_1.start(0)
	self.OUT_2.start(0)
	self.OUT_3.start(0)
	self.OUT_4.start(0)
        
        self.frequency = 0.01
        self.duty = 60

    def Setting(self, frequency, duty):
        self.frequency = frequency
        self.duty = duty

    def Go_1(self):
	self.OUT_1.changeBaseTime(self.frequency)
	self.OUT_2.changeBaseTime(self.frequency)
	self.OUT_1.changeNbSlicesOn(self.duty)
	self.OUT_2.changeNbSlicesOn(0)


    def Back_1(self):
	self.OUT_1.changeBaseTime(self.frequency)
	self.OUT_2.changeBaseTime(self.frequency)
	self.OUT_1.changeNbSlicesOn(0)
	self.OUT_2.changeNbSlicesOn(self.duty)


    def Go_2(self):
	self.OUT_3.changeBaseTime(self.frequency)
	self.OUT_4.changeBaseTime(self.frequency)
	self.OUT_3.changeNbSlicesOn(0)
	self.OUT_4.changeNbSlicesOn(self.duty)

    def Back_2(self):
	self.OUT_3.changeBaseTime(self.frequency)
	self.OUT_4.changeBaseTime(self.frequency)
	self.OUT_3.changeNbSlicesOn(self.duty)
	self.OUT_4.changeNbSlicesOn(0)

    def Stop():
	self.OUT_1.changeNbSlicesOn(0)
	self.OUT_2.changeNbSlicesOn(0)
	self.OUT_3.changeNbSlicesOn(0)
	self.OUT_4.changeNbSlicesOn(0)

if __name__=="__main__":
    motor=Motor()
    # Called on process interruption. Set all pins to "Input" default mode.
    def endProcess(signalnum = None, handler = None):
	    motor.OUT_1.stop()
	    motor.OUT_2.stop()
	    motor.OUT_3.stop()
	    motor.OUT_4.stop()
	    motor.GPIO.cleanup()
	    exit(0)

    # Prepare handlers for process exit
    signal.signal(signal.SIGTERM, endProcess)
    signal.signal(signal.SIGINT, endProcess)
    signal.signal(signal.SIGHUP, endProcess)
    signal.signal (signal.SIGQUIT, endProcess)

    motor.Setting(0.01, 60)
    print 'motor start...'
    while True:
        print 'turning direction...'
        motor.Go_1()
        time.sleep(1)
        motor.Back_1()
        time.sleep(1)
        motor.Go_2()
        time.sleep(1)
        motor.Back_2()
        time.sleep(1)
