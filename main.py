#!/usr/bin/env python3
from robot import Robot
import time

def main():
	robot = Robot()
	robot.ConnectDobot("COM3", 115200)
	robot.SetDeviceName("Dobot Test")
	while True:
		robot.test()
		time.sleep(0.01)

if __name__ == "__main__":
	main()
