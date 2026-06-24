#!/usr/bin/env python3
from robot import Robot
import time

def main():
	robot = Robot()
	robot.ConnectDobot("COM3", 115200)
	robot.SetDeviceName("Dobot Test")
	x = -100
	y = 0
	while True:
		x += 1
		y = 1/50 * x**2
		robot.test(x, y, 0)
		time.sleep(0.02)

if __name__ == "__main__":
	main()
