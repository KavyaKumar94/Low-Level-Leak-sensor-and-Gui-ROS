#! /usr/bin/env python
import rospy
from std_msgs.msg import String

import time
import RPi.GPIO as GPIO
import smbus
'''
bat_leak = 6
comp_leak = 10
GPIO.setmode(GPIO.BCM)
GPIO.setup(bat_leak, GPIO.IN)
GPIO.setup(comp_leak, GPIO.IN)

while True:
	bat = GPIO.input(bat_leak)
	comp = GPIO.input(comp_leak)
	print("battery: "+str(bat))
	print("computer: "+str(comp))
	time.sleep(1)
'''
def _init_(self):
    #self.master = master
    self.bus = smbus.SMBus(1)
    self.comp_leak = 10

def leak_sensor(self, index):
    self.bus.write_byte(self.address, index)
    time.sleep(0.05)
    byte1 = self.bus.read_byte(self.address)
    byte2 = self.bus.read_byte(self.address)
    #print "Byte 1: ",byte1
    #print "Byte 2: ",byte2

    #status = "Not Leak"
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

#define the publisher
def status_Publisher(self):
    rospy.init_node('Leak_status_talker', anonymous=True)
    pub1 = rospy.Publisher('Battery_Leak_sensor', String,queue_size=10)
    pub2 = rospy.Publisher('ComputerVessel_Leak_sensor', String,queue_size=10)
    rate = rospy.Rate(10)	#10hz

    while not rospy.is_shutdown():
        self.batteryLeakStatus = self.leak_sensor(19)
        self.ComputerLeakStatus = self.computer_leak_sensor()

        rospy.loginfo(self.batteryLeakStatus)
        rospy.loginfo(self.ComputerLeakStatus)

        pub1.publish(self.batteryLeakStatus)
        pub2.publish(self.ComputerLeakStatus)
        rate.sleep()

#read_every_second()
def main():
    while True:
        bat = leak_sensor(19)
        comp = computer_leak_sensor()
        status_Publisher()
        print("battery: "+str(bat))
        print("computer: "+str(comp))
        time.sleep(1)

if __name__== "__main__":
  main()