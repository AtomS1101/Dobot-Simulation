#!/usr/bin/env python3
from robot import Robot
import time
import math

def main():
	robot = Robot()
	robot.ConnectDobot("COM3", 115200)
	robot.SetDeviceName("Dobot Test")
	x, y, z = 0, 30, 50
	for n in range(100):
		x += 50/100
		y += 70/100
		z -= 50/100
		robot.test(x, y, z)
		time.sleep(0.01)
	t = 0
	while True:
		x = 50 * math.cos(5 * t) + 40 * math.sin(3 * t) # 50
		y = 50 * math.sin(3 * t) + 100 # 100
		t += 0.01
		robot.test(x, y, 0)
		time.sleep(0.01)

if __name__ == "__main__":
	main()
