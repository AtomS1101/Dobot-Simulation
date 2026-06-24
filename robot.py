#!/usr/bin/env python3
from render import Render
import settings
import math

class Robot:
	def __init__(self):
		self._render = Render()
		self._port = None
		self._baudrate = None
		self._device_name = None
		self._direction = 0
		self._angle1 = 45
		self._angle2 = 90
		self._render.drawAxis()

	def setAngles(self, angle1: float, angle2: float, direction: float):
		self._angle1 = angle1
		self._angle2 = angle2
		self._direction = direction

	def setCoordinates(self, x: float, y: float, z: float):
		z += settings.ARM_3_LENGTH
		try:
			direction = math.atan2(y, x)
			angle2 = math.acos((settings.ARM_1_LENGTH**2 + settings.ARM_2_LENGTH**2 - x**2 - y**2 - z**2)/(2 * settings.ARM_1_LENGTH * settings.ARM_2_LENGTH))
			R = math.sqrt(x**2 + y**2)
			A = settings.ARM_1_LENGTH - settings.ARM_2_LENGTH * math.cos(angle2)
			B = settings.ARM_2_LENGTH * math.sin(angle2)
			angle1 = math.atan2(B * R + A * z, A * R - B * z)
			self._angle1 = math.degrees(angle1)
			self._angle2 = math.degrees(angle2)
			self._direction = math.degrees(direction)
		except Exception as e:
			print(e)

	def ConnectDobot(self, port: str, baudrate: int):
		self._port = port
		self._baudrate = baudrate

	def SetQueuedCmdClear(self):
		return

	def SetQueuedCmdStartExec(self):
		return

	def SetDeviceName(self, name: str):
		self._device_name = name

	def SetJOGJointParams(self, *args):
		pass

	def test(self, x, y, z):
		self.setCoordinates(x, y, z)
		self._render.render(self._angle1, self._angle2, self._direction)
