#! /usr/bin/env python

import rospy
from std_msgs.msg import String

import Tkinter as tk
from Tkinter import *
import ttk 
import smbus
import time
import RPi.GPIO as GPIO

'''
outputs generated :
1. val (int) - which reads one cell voltages
2. status (String) - which reads status of battery leak sensor
3. status (String) - which reads status of computer vessel leak sensor
'''
class GUI:
    def __init__(self, master):
        self.master = master
        master.title('Battery Monitor')
        self.font = ('times', '20', 'bold')
        self.batt_vals = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0,0,0,0],[0,0]]
        self.val2volt = 5.0/1023
        self.max_scale = 500.0/(1023*4.2)
        self.address = 0x04
        self.bus = smbus.SMBus(1)
        self.comp_leak = 10
        self.create_tabs()
        self.create_cells()

    #define the publisher
    def status_Publisher(self):
	rospy.init_node('Leak_status_talker', anonymous=True)
	pub = rospy.Publisher('Battery_Leak_sensor', String,queue_size=10)
	rate = rospy.Rate(10)	#10hz

	while not rospy.is_shutdown():
		self.batteryLeakStatus = self.leak_sensor(19)
		rospy.loginfo(self.batteryLeakStatus)
		pub.publish(self.batteryLeakStatus)
		rate.sleep()	
		
    #create tabs
    def create_tabs(self):
        self.tab_ctrl = ttk.Notebook(self.master)
        self.tabs = []
        for i in range(5):
            tab = ttk.Frame(self.tab_ctrl)
            self.tabs.append(tab)
            if i != 4:
                self.tab_ctrl.add(self.tabs[i], text='Battery_'+str(i+1))
            else:
                self.tab_ctrl.add(self.tabs[i], text='Leak Sensor')
        self.tab_ctrl.pack(expand=1, fill='both')


    #initialize grids
    def create_cells(self):
        self.batts = []
        self.bars = []
        
        #3 batteries each with 4 cells
        for i in range(3):
            batts = []
            bars = []
            for j in range(4):
                cell = tk.Label(self.tabs[i], text='', fg='black', bg='white', font=self.font, relief=tk.RIDGE, width=15)
                cell.grid(row=j, column=0)
                batts.append(cell)

                bar = ttk.Progressbar(self.tabs[i], length=200, value=50, style='black.Horizontal.TProgressbar')
                bar.grid(row=j, column=1)
                bars.append(bar) 
            self.batts.append(batts)
            self.bars.append(bars)

        #1 big battery with 7 cells
        batts = []
        bars = []
        for i in range(7):
            cell = tk.Label(self.tabs[3], text='', fg='black', bg='white', font=self.font, relief=tk.RIDGE, width=15)
            cell.grid(row=i, column=0)
            batts.append(cell)
    
            bar = ttk.Progressbar(self.tabs[3], length=200, value=50, style='black.Horizontal.TProgressbar')
            bar.grid(row=i, column=1)
            bars.append(bar) 
        self.batts.append(batts)
        self.bars.append(bars)
        '''
        # leak sensor
        batts = []
        bars = []
        cell = tk.Label(self.tabs[4], text='',fg='black',bg='white',font=self.font,relief=tk.RIDGE,width=15)
        cell.grid(row=0, column=0)
        batts.append(cell)
        self.batts.append(batts)
        '''

        # leak sensor
        batts = []
        bars = []
        for i in range(2):
            cell = tk.Label(self.tabs[4], text='',fg='black',bg='white',font=self.font,relief=tk.RIDGE,width=30)
            cell.grid(row=i, column=0)
            batts.append(cell)
        self.batts.append(batts)

    #read one cell voltages
    def read_cell(self,index):
        self.bus.write_byte(self.address, index)
        time.sleep(0.05)
        lower = self.bus.read_byte(self.address)
        upper = self.bus.read_byte(self.address)
        val = lower + upper*256
        return val
    
    def leak_sensor(self, index):
        self.bus.write_byte(self.address, index)
        time.sleep(0.05)
        byte1 = self.bus.read_byte(self.address)
        byte2 = self.bus.read_byte(self.address)
        print "Byte 1: ",byte1
        print "Byte 2: ",byte2
     #   status = "Not Leak"
        if (byte1 or byte2) == 0:
            status = "Leak"
            # print status
        else:
            status = "Not Leak"
        return status
    
    def computer_leak_sensor(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.comp_leak,GPIO.IN)
        comp = GPIO.input(self.comp_leak)
        # print comp
       # status = "Not Leak"
        if comp == 0:
            status = "Leak"
        else:
            status = "Not Leak"
        # print("computer: "+str(comp))
        # time.sleep(1)
        return status

    #read all cell voltages
    def read(self):
        for i in range(3):
            for j in range(4):
                index = i*4 + j
                self.batt_vals[i][j] = self.read_cell(index)

        for j in range(7):
            index = 12 + j
            self.batt_vals[3][j] = self.read_cell(index) 
        # self.batt_vals[4][0] = self.leak_sensor(19)
        for i in range(2):
            self.batt_vals[4][0] = self.leak_sensor(19)
            self.batt_vals[4][1] = self.computer_leak_sensor()

    #update gui:
    def update(self):
        for i in range(3):
            for j in range(4):
                text = 'cell_' + str(j+1) + ':\t' + '{0:.2f}'.format(self.batt_vals[i][j]*self.val2volt) + 'V'
                self.batts[i][j].configure(text=text)
                self.bars[i][j]['value'] = int(self.batt_vals[i][j]*self.max_scale)

        for i in range(7):
            text = 'cell_' + str(i+1) + ':\t' + '{0:.2f}'.format(self.batt_vals[3][i]*self.val2volt) + 'V'
            self.batts[3][i].configure(text=text)
            self.bars[3][i]['value'] = int(self.batt_vals[3][i]*self.max_scale)
        '''
        text = self.leak_sensor(19)
        self.batts[4][0].configure(text=text)
        '''
        
        for i in range(2):
            if (i == 1):
                text = 'Battery Vessel' + ':\t' +  self.leak_sensor(19)
                self.batts[4][0].configure(text=text)
            else:
                text = 'Computer Vessel' + ':\t' + self.computer_leak_sensor()
                self.batts[4][1].configure(text=text)      

    def time_update(self):
        self.read()
        self.update()
	status_Publisher()
        self.master.after(100,self.time_update)

#read_every_second()

root = tk.Tk()
my_gui = GUI(root)
my_gui.time_update()
root.mainloop()
