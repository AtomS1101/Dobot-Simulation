#!/usr/bin/env python3
from .render import Render
from .coordinates import angleToCrd, crdToAngles
from . import settings as S
import time
from enum import Enum

class JC:
	JogAPPressed = 1

class PTPMode(Enum):
	PTPJUMPXYZMode   = 0
	PTPMOVJXYZMode   = 1
	PTPMOVLXYZMode   = 2
	PTPJUMPANGLEMode = 3
	PTPMOVJANGLEMode = 4
	PTPMOVLANGLEMode = 5

class DobotConnect(Enum):
	DobotConnect_NoError = None

class Robot:
	def __init__(self):
		self._render = Render()
		self._render.drawAxis()
		self._port = None
		self._baudrate = None
		self._device_name = None
		self._timeout = 3000
		self._home = [0, 0, 0]
		self._offset = [0, 0, 0]
		self._xyz_acceleration = 1
		self._xyz_velocity = 1
		self._angle_acceleration = 1
		self._angle_velocity = 1
		self._velocity_ratio = 1
		self._acceleration_ratio = 1
		self._direction = 0
		self._angle1 = 45
		self._angle2 = 90

	def _setAngles(self, angle1: float, angle2: float, direction: float):
		self._angle1 = angle1
		self._angle2 = angle2
		self._direction = direction
		self._render.render(self._angle1, self._angle2, self._direction)

	def _setCoordinates(self, x: float, y: float, z: float):
		angle = crdToAngles(x - self._offset[0], y - self._offset[1], z - self._offset[2])
		if not angle:
			return
		self._setAngles(angle["angle1"], angle["angle2"], angle["direction"])

	def load(self):
		return "Dynamic-Link-Library-File"

	def SetCmdTimeout(self, api: str, timeout: int):
		self._timeout = timeout

	def ConnectDobot(self, api: str, port: str, baudrate: int):
		self._port = port
		self._baudrate = baudrate
		return [DobotConnect.DobotConnect_NoError]

	def SetDeviceName(self, api: str, name: str):
		self._device_name = name

	def SetQueuedCmdClear(self, api: str):
		return

	def SetQueuedCmdStartExec(self, api: str):
		return

	def DisconnectDobot(self, api: str):
		while True: # keep showing
			self._setAngles(self._angle1, self._angle2, self._direction)
			time.sleep(0.1)

	def SetQueuedCmdStopExec(self, api: str):
		return

	def SetEndEffectorParams(self, api: str, x: float, y: float, z: float, r: float, queued=True):
		self._offset = [x, y, z]

	def SetHOMEParams(self, api: str, x: float, y: float, z: float, r: float, queued=True):
		self._home = [x, y, z]

	def SetHOMECmdEx(self, api: str, mode: PTPMode, queued=True):
		self._setCoordinates(*self._home)

	def SetJOGJointParams(self, api:str, v1:float, v2:float, v3:float, v4:float, a1:float, a2:float, a3:float, a4:float, queued=True):
		return

	def SetPTPJointParams(self, api:str, v1:float, v2:float, v3:float, v4:float, a1:float, a2:float, a3:float, a4:float, queued=True):
		return

	def SetJOGCoordinateParams(self, api:str, v1:float, v2:float, v3:float, v4:float, a1:float, a2:float, a3:float, a4:float, queued=True):
		return

	def SetPTPCoordinateParams(self, api:str, v:float, a:float, rv:float, ra:float, queued=True):
		self._xyz_velocity = v
		self._xyz_acceleration = a

	def SetJOGCommonParams(self, api:str, v1:float, v2:float, queued=True):
		return

	def SetPTPCommonParams(self, api:str, v_ratio: float, a_ratio: float, queued=True):
		self._velocity_ratio = v_ratio / 100
		self._acceleration_ratio = a_ratio / 100

	def SetPTPJumpParams(self, api:str, v1:float, v2:float, queued=True):
		return

	def SetPTPCmdEx(self, api: str, mode: PTPMode, a: float, b: float, c: float, d: float, queued=True):
		if mode == PTPMode.PTPJUMPXYZMode:     # jump
			self._setCoordinates(a, b, c)
		elif mode == PTPMode.PTPMOVJXYZMode:   # move line
			self._setCoordinates(a, b, c)
		elif mode == PTPMode.PTPMOVLXYZMode:   # move jump
			currentCrd = angleToCrd(self._angle1, self._angle2, self._direction)
			currentX, currentY, currentZ = currentCrd["rx"], currentCrd["ry"], currentCrd["rz"]
			xGap, yGap, zGap = a - currentX, b - currentY, c - currentZ
			distance = (xGap**2 + yGap**2 + zGap**2)**0.5
			if distance == 0:
				self._setCoordinates(a, b, c)
				return
			maxVelocity = self._xyz_velocity * self._velocity_ratio
			acceleration = self._xyz_acceleration * self._acceleration_ratio
			accelerationTime = maxVelocity / acceleration
			accelerationDistance = 0.5 * acceleration * (accelerationTime ** 2)
			constantDistance = 0
			if distance < accelerationDistance * 2: # decelerating before reaching the maximum speed
				accelerationDistance = distance / 2
				accelerationTime = (2 * accelerationDistance / acceleration) ** 0.5
				maxVelocity = acceleration * accelerationTime
				constantTime = 0
				totalTime = accelerationTime * 2
			else: # there is uniform linear motion phase
				constantDistance = distance - (accelerationDistance * 2)
				constantTime = constantDistance / maxVelocity
				totalTime = (accelerationTime * 2) + constantTime
			startTime = time.time()
			elapsedTime = 0
			while elapsedTime < totalTime:
				if elapsedTime < accelerationTime:
					distanceTraveled = 0.5 * acceleration * (elapsedTime ** 2)
				elif elapsedTime < accelerationTime + constantTime:
					distanceTraveled = accelerationDistance + maxVelocity * (elapsedTime - accelerationTime)
				else:
					decelerationTime = elapsedTime - accelerationTime - constantTime
					distanceTraveled = accelerationDistance + constantDistance + (maxVelocity * decelerationTime) - (0.5 * acceleration * (decelerationTime ** 2))
				ratio = distanceTraveled / distance
				if ratio > 1.0:
					ratio = 1.0
				x = currentX + xGap * ratio
				y = currentY + yGap * ratio
				z = currentZ + zGap * ratio
				self._setCoordinates(x, y, z)
				time.sleep(1 / S.REFRESH_RATE)
				elapsedTime = time.time() - startTime
			self._setCoordinates(a, b, c)
		elif mode == PTPMode.PTPJUMPANGLEMode: # jump
			self._setAngles(c, a, b)
		elif mode == PTPMode.PTPMOVJANGLEMode: # move line
			self._setAngles(c, a, b)
		elif mode == PTPMode.PTPMOVLANGLEMode: # move jump
			self._setAngles(c, a, b)
