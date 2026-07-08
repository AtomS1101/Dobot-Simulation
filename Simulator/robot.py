#!/usr/bin/env python3
from .render import Render
from .coordinates import angleToCrd, crdToAngles
from . import settings as S
import time
from enum import Enum

class JC(Enum):
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
		self._xyz_acceleration = 50
		self._xyz_velocity = 50
		self._angle_acceleration = 50
		self._angle_velocity = 50
		self._velocity_ratio = 1
		self._acceleration_ratio = 1
		self._jump_height = 10
		self._zLimit = None
		self._plan_acc = 50
		self._junc_vel = 50
		self._actual_acc = 50
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

	def _uniformMove(self, x: float, y: float, z: float, velocity: float):
		currentCrd = angleToCrd(self._angle1, self._angle2, self._direction)
		currentX, currentY, currentZ = currentCrd["rx"], currentCrd["ry"], currentCrd["rz"]
		xGap, yGap, zGap = x - currentX, y - currentY, z - currentZ
		distance = (xGap**2 + yGap**2 + zGap**2)**0.5
		if distance == 0:
			self._setCoordinates(x, y, z)
			return
		velocity /= S.REFRESH_RATE
		nextX, nextY, nextZ = currentX, currentY, currentZ
		for _ in range(int(distance / velocity)):
			nextX += velocity * xGap / distance
			nextY += velocity * yGap / distance
			nextZ += velocity * zGap / distance
			self._setCoordinates(nextX, nextY, nextZ)
			time.sleep(1 / S.REFRESH_RATE)
		self._setCoordinates(x, y, z)

	def _smoothMove(self, x: float, y: float, z: float):
		currentCrd = angleToCrd(self._angle1, self._angle2, self._direction)
		currentX, currentY, currentZ = currentCrd["rx"], currentCrd["ry"], currentCrd["rz"]
		xGap, yGap, zGap = x - currentX, y - currentY, z - currentZ
		distance = (xGap**2 + yGap**2 + zGap**2)**0.5
		if distance == 0:
			self._setCoordinates(x, y, z)
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
			nextX = currentX + xGap * ratio
			nextY = currentY + yGap * ratio
			nextZ = currentZ + zGap * ratio
			self._setCoordinates(nextX, nextY, nextZ)
			time.sleep(1 / S.REFRESH_RATE)
			elapsedTime = time.time() - startTime
		self._setCoordinates(x, y, z)

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

	def DisconnectDobot(self, api: str):
		while True: # keep showing
			self._setAngles(self._angle1, self._angle2, self._direction)
			time.sleep(0.1)

	def SetEndEffectorParams(self, api: str, x: float, y: float, z: float, r: float, queued=True):
		self._offset = [x, y, z]

	def SetHOMEParams(self, api: str, x: float, y: float, z: float, r: float, queued=True):
		self._home = [x, y, z]

	def SetHOMECmdEx(self, api: str, mode: PTPMode, queued=True):
		self._smoothMove(*self._home)

	def SetPTPCoordinateParams(self, api:str, v: float, a: float, rv: float, ra: float, queued=True):
		self._xyz_velocity = v
		self._xyz_acceleration = a

	def SetPTPCommonParams(self, api:str, vRatio: float, aRatio: float, queued=True):
		self._velocity_ratio = vRatio / 100
		self._acceleration_ratio = aRatio / 100

	def SetPTPJumpParams(self, api:str, height: float, zLimit: float, queued=True):
		self._jump_height = height
		self._zLimit = zLimit

	def SetCPParams(self, api:str, planAcc: float, juncVel: float, actualAcc: float, realTime: bool, queued=True):
		self._plan_acc = planAcc
		self._junc_vel = juncVel
		self._actual_acc = actualAcc

	def SetCPCmd(self, api: str, cpMode: int, x: float, y: float, z: float, velocity: float, queued=True):
		# velocity ignored in non-realtime mode
		if cpMode == 0: # Relative (increment)
			currentCrd = angleToCrd(self._angle1, self._angle2, self._direction)
			x, y, z = x + currentCrd["rx"], y + currentCrd["ry"], z + currentCrd["rz"]
		self._uniformMove(x, y, z, self._junc_vel)

	def SetPTPCmdEx(self, api: str, mode: PTPMode, a: float, b: float, c: float, d: float, queued=True):
		if mode == PTPMode.PTPJUMPXYZMode:     # jump
			self._setCoordinates(a, b, c)
		elif mode == PTPMode.PTPMOVJXYZMode:   # move jump
			currentCrd = angleToCrd(self._angle1, self._angle2, self._direction)
			currentX, currentY, currentZ = currentCrd["rx"], currentCrd["ry"], currentCrd["rz"]
			self._smoothMove(currentX, currentY, currentZ + self._jump_height) # up
			self._smoothMove(a, b, c + self._jump_height) # move
			self._smoothMove(a, b, c) # down
		elif mode == PTPMode.PTPMOVLXYZMode:   # move line
			self._smoothMove(a, b, c)
		elif mode == PTPMode.PTPJUMPANGLEMode: # jump
			self._setAngles(c, a, b)
		elif mode == PTPMode.PTPMOVJANGLEMode: # move jump
			self._setAngles(c, a, b)
		elif mode == PTPMode.PTPMOVLANGLEMode: # move line
			self._setAngles(c, a, b)

	# ==================================================
	# These will not be required in this project
	def SetQueuedCmdClear(self, api: str):
		return

	def SetQueuedCmdStartExec(self, api: str):
		return

	def SetQueuedCmdStopExec(self, api: str):
		return

	def SetJOGJointParams(self, api:str, v1:float, v2:float, v3:float, v4:float, a1:float, a2:float, a3:float, a4:float, queued=True):
		return

	def SetPTPJointParams(self, api:str, v1:float, v2:float, v3:float, v4:float, a1:float, a2:float, a3:float, a4:float, queued=True):
		return

	def SetJOGCoordinateParams(self, api:str, v1:float, v2:float, v3:float, v4:float, a1:float, a2:float, a3:float, a4:float, queued=True):
		return

	def SetJOGCommonParams(self, api:str, vRatio: float, aRatio: float, queued=True):
		return
