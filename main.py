#!/usr/bin/env python3
from robot import Robot
from robot import PTPMode

def main():
	robot = Robot()
	api = robot.load()
	robot.ConnectDobot(api, "COM3", 115200)
	robot.SetDeviceName(api, "Dobot Test")
	robot.SetPTPCoordinateParams(api, 300, 200, 100, 100, True)
	robot.SetPTPCommonParams(api, 100, 100, True)
	while True:
		robot.SetPTPCmdEx(api, PTPMode.PTPMOVLXYZMode, 100,  50, 0, 0, True)
		robot.SetPTPCmdEx(api, PTPMode.PTPMOVLXYZMode, 100, -50, 0, 0, True)
		robot.SetPTPCmdEx(api, PTPMode.PTPMOVLXYZMode, 200,   0, 0, 0, True)

if __name__ == "__main__":
	main()
