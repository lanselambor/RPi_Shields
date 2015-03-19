'''
/*
 * RPi_Relay_Shield.py
 * Demo for Raspberry Pi Relay Shield
 *
 * Copyright (c) 2014 seeed technology inc.
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
import time
import smbus

bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
DEVICE_ADDRESS = 0x20      #7 bit address (will be left shifted to add the read write bit)
DEVICE_REG_MODE1 = 0x06
DEVICE_REG_DATA = 0xff
bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, DEVICE_REG_DATA)
		
# Called on process interruption. Set all pins to "Input" default mode.
def endProcess(signalnum = None, handler = None):
	bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, 0xff)
	
	
class MyDialog(wx.Dialog):
	def __init__(self, parent, id, title):
		wx.Dialog.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(300, 310))
		
		wx.StaticText(self, -1, 'Relay 1 ', (20, 20))
		wx.StaticText(self, -1, 'Relay 2 ', (20, 60))
		wx.StaticText(self, -1, 'Relay 3 ', (20, 100))
		wx.StaticText(self, -1, 'Relay 4 ', (20, 140))
		
		self.button_1 = wx.Button(self, -1, 'ON', (80, 20))
		self.button_2 = wx.Button(self, -1, 'ON', (80, 60))
		self.button_3 = wx.Button(self, -1, 'ON', (80, 100))
		self.button_4 = wx.Button(self, -1, 'ON', (80, 140))
		self.button_5 = wx.Button(self, -1, 'OFF', (160, 20))
		self.button_6 = wx.Button(self, -1, 'OFF', (160, 60))
		self.button_7 = wx.Button(self, -1, 'OFF', (160, 100))
		self.button_8 = wx.Button(self, -1, 'OFF', (160, 140))
		self.button_9 = wx.Button(self, -1, 'ALLON', (20, 200))
		self.button_10 = wx.Button(self, -1, 'ALLOFF', (100, 200))
		button_cancel = wx.Button(self, 1, 'Cancel', (180, 200))

		self.Bind(wx.EVT_BUTTON, self.OnCancel, id=1)
		self.Bind(wx.EVT_BUTTON, self.ON_1, self.button_1)
		self.Bind(wx.EVT_BUTTON, self.ON_2, self.button_2)
		self.Bind(wx.EVT_BUTTON, self.ON_3, self.button_3)
		self.Bind(wx.EVT_BUTTON, self.ON_4, self.button_4)
		self.Bind(wx.EVT_BUTTON, self.OFF_1, self.button_5)
		self.Bind(wx.EVT_BUTTON, self.OFF_2, self.button_6)
		self.Bind(wx.EVT_BUTTON, self.OFF_3, self.button_7)
		self.Bind(wx.EVT_BUTTON, self.OFF_4, self.button_8)	
		self.Bind(wx.EVT_BUTTON, self.ALLON, self.button_9)
		self.Bind(wx.EVT_BUTTON, self.ALLOFF, self.button_10)
		

	def OnCancel(self, event):
		endProcess()
		self.Destroy()
	
	def ON_1(self, event):
		print 'ON_1...'
		global DEVICE_REG_DATA
		DEVICE_REG_DATA &= ~(0x1<<0)  
		bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, DEVICE_REG_DATA)
	def ON_2(self, event):
		print 'ON_2...'
		global DEVICE_REG_DATA
		DEVICE_REG_DATA &= ~(0x1<<1)
		bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, DEVICE_REG_DATA)
	def ON_3(self, event):
		print 'ON_3...'
		global DEVICE_REG_DATA
		DEVICE_REG_DATA &= ~(0x1<<2)
		bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, DEVICE_REG_DATA)
	def ON_4(self, event):
		print 'ON_4...'
		global DEVICE_REG_DATA
		DEVICE_REG_DATA &= ~(0x1<<3)
		bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, DEVICE_REG_DATA)
	
	def OFF_1(self, event):
		print 'OFF_1...'
		global DEVICE_REG_DATA
		DEVICE_REG_DATA |= (0x1<<0)
		bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, DEVICE_REG_DATA)
	
	def OFF_2(self, event):
		print 'OFF_2...'
		global DEVICE_REG_DATA
		DEVICE_REG_DATA |= (0x1<<1)
		bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, DEVICE_REG_DATA)

	def OFF_3(self, event):
		print 'OFF_3...'
		global DEVICE_REG_DATA
		DEVICE_REG_DATA |= (0x1<<2)
		bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, DEVICE_REG_DATA)
	
	def OFF_4(self, event):
		print 'OFF_4...'
		global DEVICE_REG_DATA
		DEVICE_REG_DATA |= (0x1<<3)
		bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, DEVICE_REG_DATA)
	
	def ALLON(self, event):
		print 'ALLON...'
		global DEVICE_REG_DATA
		DEVICE_REG_DATA &= ~(0xf<<0)
		bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, DEVICE_REG_DATA)
	
	def ALLOFF(self, event):
		print 'ALLOFF...'
		global DEVICE_REG_DATA
		DEVICE_REG_DATA |= (0xf<<0)
		bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, DEVICE_REG_DATA)
		

class MyApp(wx.App):
	def OnInit(self):
		dlg = MyDialog(None, -1, 'RPi Delay Shield Controler')
		dlg.Show(True)
		dlg.Centre()
		return True

app = MyApp(0)
app.MainLoop()
