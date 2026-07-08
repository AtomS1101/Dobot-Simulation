#!/usr/bin/env python3
from Simulator.robot import Robot, PTPMode

def main():
	robot = Robot()
	api = robot.load()
	robot.ConnectDobot(api, "COM3", 115200)
	robot.SetDeviceName(api, "Dobot Test")
	robot.SetPTPCoordinateParams(api, 300, 50, 100, 100, True)
	robot.SetPTPCommonParams(api, 100, 100, True)
	robot.SetPTPJumpParams(api, 15, 10, True)
	robot.SetCPParams(api, 100, 100, 100, False, True)

	robot.SetHOMEParams(api, 100, 0, 0, 0, True)
	robot.SetHOMECmdEx(api, PTPMode.PTPMOVJXYZMode, True)
	while True:
		robot.SetPTPCmdEx(api, PTPMode.PTPMOVJXYZMode, 100,  50, 0, 0, True) # jump
		robot.SetPTPCmdEx(api, PTPMode.PTPMOVLXYZMode, 100, -50, 0, 0, True) # line
		robot.SetCPCmd(api, 1, 200, 0, 0, 0, True) # uniform move

if __name__ == "__main__":
	main()
