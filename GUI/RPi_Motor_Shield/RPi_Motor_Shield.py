
'''
/*
 * RPi_Motor_Shield.py
 * Demo for RAspberry Pi Motor Shield 
 *
 * Copyright (c) 2012 seeed technology inc.
 * Website    : www.seeed.cc
 * Author     : Lambor
 * Create Time: Nov 2014
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

import wx
import RPi.GPIO as GPIO
import time
import signal	

from PiSoftPwm import *

# Called on process interruption. Set all pins to "Input" default mode.
def endProcess(signalnum = None, handler = None):
	OUT_1.stop()
	OUT_2.stop()
	OUT_3.stop()
	OUT_4.stop()
	GPIO.cleanup()
	exit(0)

# Prepare handlers for process exit
signal.signal(signal.SIGTERM, endProcess)
signal.signal(signal.SIGINT, endProcess)
signal.signal(signal.SIGHUP, endProcess)
signal.signal (signal.SIGQUIT, endProcess)


# MC33932 pins
PWMA = 25  
PWMB = 22
_IN1 = 23  
_IN2 = 24 
_IN3 = 17
_IN4 = 27

# Initialize PWMA PWMB 
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)
GPIO.output(PWMA, True)
GPIO.output(PWMB, True)


# Initialize PWM outputs
OUT_1  = PiSoftPwm(0.1, 100, _IN1, GPIO.BCM)
OUT_2  = PiSoftPwm(0.1, 100, _IN2, GPIO.BCM)
OUT_3  = PiSoftPwm(0.1, 100, _IN3, GPIO.BCM)
OUT_4  = PiSoftPwm(0.1, 100, _IN4, GPIO.BCM)

OUT_1.start(0)
OUT_2.start(0)
OUT_3.start(0)
OUT_4.start(0)


def MoveGo_1(frequency, duty):
	OUT_1.changeBaseTime(frequency)
	OUT_2.changeBaseTime(frequency)
	OUT_1.changeNbSlicesOn(duty)
	OUT_2.changeNbSlicesOn(0)


def MoveBack_1(frequency, duty):
	OUT_1.changeBaseTime(frequency)
	OUT_2.changeBaseTime(frequency)
	OUT_1.changeNbSlicesOn(0)
	OUT_2.changeNbSlicesOn(duty)


def MoveGo_2(frequency, duty):
	OUT_3.changeBaseTime(frequency)
	OUT_4.changeBaseTime(frequency)
	OUT_3.changeNbSlicesOn(0)
	OUT_4.changeNbSlicesOn(duty)

def MoveBack_2(frequency, duty):
	OUT_3.changeBaseTime(frequency)
	OUT_4.changeBaseTime(frequency)
	OUT_3.changeNbSlicesOn(duty)
	OUT_4.changeNbSlicesOn(0)

def MoveStop():
	OUT_1.changeNbSlicesOn(0)
	OUT_2.changeNbSlicesOn(0)
	OUT_3.changeNbSlicesOn(0)
	OUT_4.changeNbSlicesOn(0)

class MyDialog(wx.Dialog):
	def __init__(self, parent, id, title):
		wx.Dialog.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(500, 240))

		wx.StaticText(self, -1, 'Motor A ', (20, 40))
		wx.StaticText(self, -1, 'Motor B ', (20, 120))
		wx.StaticText(self, -1, 'Frequency(Hz)', (80, 20))
		wx.StaticText(self, -1, 'Speed(%) ', (80, 60))
		wx.StaticText(self, -1, 'Frequency(Hz)', (80, 100))
		wx.StaticText(self, -1, 'Speed(%) ', (80, 140))

		self.sc_1 = wx.SpinCtrl(self, -1, '',  (180, 20), (80, -1))
		self.sc_1.SetRange(0, 10000)
		self.sc_1.SetValue(2000)
		self.sc_2 = wx.SpinCtrl(self, -1, '',  (180, 60), (80, -1))
		self.sc_2.SetRange(0, 100)
		self.sc_2.SetValue(50)

		self.sc_3 = wx.SpinCtrl(self, -1, '',  (180, 100), (80, -1))
		self.sc_3.SetRange(0, 10000)
		self.sc_3.SetValue(2000)
		self.sc_4 = wx.SpinCtrl(self, -1, '',  (180, 140), (80, -1))
		self.sc_4.SetRange(0, 100)
		self.sc_4.SetValue(50)

		self.button_1 = wx.Button(self, -1, 'Go', (280, 40))
		self.button_2 = wx.Button(self, -1, 'Back', (360, 40))
		self.button_3 = wx.Button(self, -1, 'Go', (280, 120))
		self.button_4 = wx.Button(self, -1, 'Back', (360, 120))

		button_stop = wx.Button(self, 2, 'Stop', (260, 180))
		button_stop.SetFocus()
		button_cancel = wx.Button(self, 3, 'Cancel', (360, 180))

		self.Bind(wx.EVT_BUTTON, self.OnStop, id=2)
		self.Bind(wx.EVT_BUTTON, self.OnCancel, id=3)
		self.Bind(wx.EVT_BUTTON, self.OnGo_1, self.button_1)
		self.Bind(wx.EVT_BUTTON, self.OnBack_1, self.button_2)
		self.Bind(wx.EVT_BUTTON, self.OnGo_2, self.button_3)
		self.Bind(wx.EVT_BUTTON, self.OnBack_2, self.button_4)

	def OnCancel(self, event):
		endProcess()
		self.Destroy()

	def OnStop(self, event):
		print 'Stop...'	
		MoveStop()
	
	def OnGo_1(self, event):
		print 'Go_1...'
		frequency = 1.0 / self.sc_1.GetValue()
		speed = self.sc_2.GetValue()
		MoveGo_1(frequency, speed)

	def OnBack_1(self, event):
		print 'Back_1...'
		frequency = 1.0 / self.sc_1.GetValue()
		speed = self.sc_2.GetValue()
		MoveBack_1(frequency, speed)
	
	def OnGo_2(self, event):
		print 'Go_2...'
		frequency = 1.0 / self.sc_3.GetValue()
		speed = self.sc_4.GetValue()
		MoveGo_2(frequency, speed)

	def OnBack_2(self, event):
		print 'Back_2...'
		frequency = 1.0 / self.sc_3.GetValue()
		speed = self.sc_4.GetValue()
		MoveBack_2(frequency, speed)

class MyApp(wx.App):
	def OnInit(self):
		dlg = MyDialog(None, -1, 'RPi Motor Shield Controler')
		dlg.Show(True)
		dlg.Centre()
		return True

app = MyApp(0)
app.MainLoop()
