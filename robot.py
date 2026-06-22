#!/usr/bin/env python3
from render import Render

class Robot:
	def __init__(self):
		self._render = Render()
		self._port = None
		self._baudrate = None
		self._device_name = None
		self._direction = 45
		self._angle1 = 45
		self._angle2 = 90
		self._angle3 = 0
		self._render.drawAxis()

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

	def test(self):
		self._angle1 += 1
		self._angle2 += 1
		self._direction += 1
		self._render.render(self._angle1, self._angle2, self._direction)
