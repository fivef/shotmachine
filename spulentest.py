#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import required modules
import time
import RPi.GPIO as GPIO
import smbus
import pygame


# define GPIO pins


UltrasonicSensorI2CAddress = 0x71

#output e.g. relais
#output GPIO pins e.g. relais
GPIOOutput1 = 27
GPIOOutput2 = 22

# variables

#The min time (s) between two output switch events
DeadTime = 1

#Trigger distance
#If the detected distance is smaller than this value (cm) the output switch is opened
TriggerDistance = 30

#The time the output switch is open
OpenTime = 1

# main function
def main():

  initAudio()

  DeadTimeStart = 0

  try:
    while True:
      Distance = MeasureDistance()
      print("Measured Distance = %.1f cm" % Distance)

      if Distance <= TriggerDistance and time.time() - DeadTimeStart >= DeadTime:
	 DeadTimeStart = time.time()
         playSound()
         GPIO.output(GPIOOutput2, GPIO.LOW)
         time.sleep(OpenTime)
         GPIO.output(GPIOOutput2, GPIO.HIGH)

      

  # reset GPIO settings if user pressed Ctrl+C
  except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()


def MeasureDistance():
  i2c.write_byte_data(UltrasonicSensorI2CAddress, 0, 81)
  time.sleep(0.1)
  return i2c.read_word_data(UltrasonicSensorI2CAddress, 2) / 255


def initAudio():
  pygame.mixer.init()
  pygame.mixer.music.load("arrr.mp3")

def playSound():
  pygame.mixer.music.play()

if __name__ == '__main__':
  # use GPIO pin numbering convention (not the actual pin numbers)
  GPIO.setmode(GPIO.BCM)

  # set up GPIO pins
  GPIO.setup(GPIOOutput1, GPIO.OUT)
  GPIO.setup(GPIOOutput2, GPIO.OUT)
  
  GPIO.output(GPIOOutput2, GPIO.HIGH)
  GPIO.output(GPIOOutput2, GPIO.HIGH)


  #init smbus 1
  i2c = smbus.SMBus(1)

  time.sleep(1)

  # call main function
  main()
