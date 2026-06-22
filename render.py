#!/usr/bin/env python3
import math
import settings
from canvas import Canvas
from coordinates import convCrd

class Render:
	def __init__(self):
		self._canvas = Canvas(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
		self._canvas.setup()

	def showInfo(self, info: list):
		self._canvas.pen("info").color(0, 0, 0).size(20).align("left").clear()
		self._canvas.pen("info").showText("< Information >", (150, 250))
		infoList = {"θ1": info[0], "θ2": info[1], "φ": info[2], "P": f"({info[3]:.2f}, {info[4]:.2f}, {info[5]:.2f})", "Q": f"({info[6]:.2f}, {info[7]:.2f}, {info[8]:.2f})"}
		for line, (key, value) in enumerate(infoList.items()):
			self._canvas.pen("info").showText(f"{key}", (150, 220 - (line * 30)))
			self._canvas.pen("info").showText(f": {value}", (180, 220 - (line * 30)))

	def showOrbit(self, rx: float, ry: float, rz: float):
		self._canvas.pen("orbit").color(200, 0, 0).size(1)
		self._canvas.pen("orbit").goto(convCrd("angled", (rx, ry, rz)), True)

	def render(self, angle1: float, angle2: float, direction: float):
		px =  settings.ARM_1_LENGTH * math.cos(math.radians(angle1)) * math.cos(math.radians(direction))
		py =  settings.ARM_1_LENGTH * math.cos(math.radians(angle1)) * math.sin(math.radians(direction))
		pz =  settings.ARM_1_LENGTH * math.sin(math.radians(angle1))
		qx = (settings.ARM_1_LENGTH * math.cos(math.radians(angle1)) - settings.ARM_2_LENGTH * math.cos(math.radians(angle1 + angle2))) * math.cos(math.radians(direction))
		qy = (settings.ARM_1_LENGTH * math.cos(math.radians(angle1)) - settings.ARM_2_LENGTH * math.cos(math.radians(angle1 + angle2))) * math.sin(math.radians(direction))
		qz =  settings.ARM_1_LENGTH * math.sin(math.radians(angle1)) - settings.ARM_2_LENGTH * math.sin(math.radians(angle1 + angle2))
		rx = qx
		ry = qy
		rz = qz - settings.ARM_3_LENGTH
		# Front View
		self._canvas.pen("front").color(0, 0, 0).size(16).align("right").clear()
		self._canvas.pen("front").width(2).drawLine(convCrd("front", (0, 0)), convCrd("front", (px, pz)))
		self._canvas.pen("front").width(2).drawLine(convCrd("front", (px, pz)), convCrd("front", (qx, qz)))
		self._canvas.pen("front").width(2).drawLine(convCrd("front", (qx, qz)), convCrd("front", (rx, rz)))
		self._canvas.pen("front").width(2).drawCircle(convCrd("front", (0, 0)), settings.JOINT_SIZE)
		self._canvas.pen("front").width(2).drawCircle(convCrd("front", (px, pz)), settings.JOINT_SIZE)
		self._canvas.pen("front").width(2).drawCircle(convCrd("front", (qx, qz)), settings.JOINT_SIZE)
		self._canvas.pen("front").width(2).drawCircle(convCrd("front", (rx, rz)), settings.JOINT_SIZE)
		# Top View
		self._canvas.pen("top").color(0, 0, 0).size(16).align("right").clear()
		self._canvas.pen("top").width(2).drawLine(convCrd("top", (0, 0)), convCrd("top", (px, py)))
		self._canvas.pen("top").width(2).drawLine(convCrd("top", (px, py)), convCrd("top", (qx, qy)))
		self._canvas.pen("top").width(2).drawLine(convCrd("top", (qx, qy)), convCrd("top", (rx, ry)))
		self._canvas.pen("top").width(2).drawCircle(convCrd("top", (0, 0)), settings.JOINT_SIZE)
		self._canvas.pen("top").width(2).drawCircle(convCrd("top", (px, py)), settings.JOINT_SIZE)
		self._canvas.pen("top").width(2).drawCircle(convCrd("top", (qx, qy)), settings.JOINT_SIZE)
		self._canvas.pen("top").width(2).drawCircle(convCrd("top", (rx, ry)), settings.JOINT_SIZE)
		# Angled View
		self._canvas.pen("angled").color(0, 0, 0).size(16).align("left").clear()
		self._canvas.pen("angled").width(2).drawLine(convCrd("angled", (0, 0, 0)), convCrd("angled", (px, py, pz)))
		self._canvas.pen("angled").width(2).drawCircle(convCrd("angled", (0, 0, 0)), settings.JOINT_SIZE)
		self._canvas.pen("angled").width(2).drawLine(convCrd("angled", (px, py, pz)), convCrd("angled", (qx, qy, qz)))
		self._canvas.pen("angled").width(2).drawLine(convCrd("angled", (qx, qy, qz)), convCrd("angled", (rx, ry, rz)))
		self._canvas.pen("angled").width(2).drawCircle(convCrd("angled", (qx, qy, qz)), settings.JOINT_SIZE)
		self._canvas.pen("angled").width(2).drawCircle(convCrd("angled", (px, py, pz)), settings.JOINT_SIZE)
		self._canvas.pen("angled").width(2).drawCircle(convCrd("angled", (rx, ry, rz)), settings.JOINT_SIZE)

		if settings.SHOW_JOINT_NAME:
			self._canvas.pen("front").showText("P", convCrd("front", (px-10, pz)))
			self._canvas.pen("front").showText("Q", convCrd("front", (qx-10, qz)))
			self._canvas.pen("front").showText("R", convCrd("front", (rx-10, rz)))
			self._canvas.pen("top").showText("P", convCrd("top", (px-10, py)))
			self._canvas.pen("top").showText("Q", convCrd("top", (qx-10, qy)))
			self._canvas.pen("top").showText("R", convCrd("top", (rx+40, ry)))
			self._canvas.pen("angled").showText("P", convCrd("angled", (px+10, py, pz)))
			self._canvas.pen("angled").showText("Q", convCrd("angled", (qx+10, qy, qz)))
			self._canvas.pen("angled").showText("R", convCrd("angled", (rx+10, ry, rz)))
		infoList = [angle1, angle2, direction, px, py, pz, qx, qy, qz]
		self.showInfo(infoList)
		if settings.SHOW_ORBIT:
			self.showOrbit(rx, ry, rz)
		self._canvas.update()

	def drawAxis(self):
		self._canvas.pen("axis").color(0, 0, 0).width(1).size(18).align("right").clear()
		# Draw view area squares
		self._canvas.pen("axis").drawSquare(settings.ANGLED_VIEW_BEGIN, settings.ANGLED_VIEW_END) # angled view area
		self._canvas.pen("axis").drawSquare(settings.TOP_VIEW_BEGIN,    settings.TOP_VIEW_END)    # top view area
		self._canvas.pen("axis").drawSquare(settings.FRONT_VIEW_BEGIN,  settings.FRONT_VIEW_END)  # front view area
		self._canvas.pen("axis").showText("Front View",  (settings.FRONT_VIEW_END[0]  - 5, settings.FRONT_VIEW_END[1]  - 20))
		self._canvas.pen("axis").showText("Top View",    (settings.TOP_VIEW_END[0]    - 5, settings.TOP_VIEW_END[1]    - 20))
		self._canvas.pen("axis").showText("Angled View", (settings.ANGLED_VIEW_END[0] - 5, settings.ANGLED_VIEW_END[1] - 20))
		# Draw sub axis lines
		self._canvas.pen("axis").color(220, 220, 220).width(1)
		for i in range(7):
			self._canvas.pen("axis").drawLine(convCrd("angled", (i * settings.AXIS_STEPS - 100, -100, 0)), convCrd("angled", (i * settings.AXIS_STEPS - 100, 200, 0)))
		for i in range(7):
			self._canvas.pen("axis").drawLine(convCrd("angled", (- 100, i * settings.AXIS_STEPS - 100, 0)), convCrd("angled", (250, i * settings.AXIS_STEPS - 100, 0)))
		for i in range(10):
			self._canvas.pen("axis").drawLine(convCrd("top", (settings.TOP_CRD_BEGIN[0] + settings.AXIS_MARGIN, i * settings.AXIS_STEPS - 200)), convCrd("top", (settings.TOP_CRD_END[0] - settings.AXIS_MARGIN, i * settings.AXIS_STEPS - 200, 0)))
		for i in range(20):
			self._canvas.pen("axis").drawLine(convCrd("top", (i * settings.AXIS_STEPS - 470, settings.TOP_CRD_BEGIN[1] + settings.AXIS_MARGIN)), convCrd("top", (i * settings.AXIS_STEPS - 470, settings.TOP_CRD_END[1] - settings.AXIS_MARGIN)))
		for i in range(7):
			self._canvas.pen("axis").drawLine(convCrd("front", (settings.FRONT_CRD_BEGIN[0] + settings.AXIS_MARGIN, i * settings.AXIS_STEPS - 30)), convCrd("front", (settings.FRONT_CRD_END[0] - settings.AXIS_MARGIN, i * settings.AXIS_STEPS - 30, 0)))
		for i in range(8):
			self._canvas.pen("axis").drawLine(convCrd("front", (i * settings.AXIS_STEPS - 200, settings.FRONT_CRD_BEGIN[1] + settings.AXIS_MARGIN)), convCrd("front", (i * settings.AXIS_STEPS - 200, settings.FRONT_CRD_END[1] - settings.AXIS_MARGIN)))
		# Draw main axis lines
		self._canvas.pen("axis").color(0, 0, 0).width(2)
		self._canvas.pen("axis").drawLine(convCrd("angled", (-100, 0, 0)), convCrd("angled", (250, 0, 0))) # angled x axis
		self._canvas.pen("axis").drawLine(convCrd("angled", (0, -100, 0)), convCrd("angled", (0, 200, 0))) # angled y axis
		self._canvas.pen("axis").drawLine(convCrd("angled", (0, 0, -100)), convCrd("angled", (0, 0, 180))) # angled z axis
		self._canvas.pen("axis").drawLine(convCrd("top", (0, settings.TOP_CRD_BEGIN[1] + settings.AXIS_MARGIN)), convCrd("top", (0, settings.TOP_CRD_END[1] - settings.AXIS_MARGIN))) # top y axis
		self._canvas.pen("axis").drawLine(convCrd("top", (settings.TOP_CRD_BEGIN[0] + settings.AXIS_MARGIN, 0)), convCrd("top", (settings.TOP_CRD_END[0] - settings.AXIS_MARGIN, 0))) # top x axis
		self._canvas.pen("axis").drawLine(convCrd("front", (settings.FRONT_CRD_BEGIN[0] + settings.AXIS_MARGIN, 0)), convCrd("front", (settings.FRONT_CRD_END[0] - settings.AXIS_MARGIN, 0))) # front x axis
		self._canvas.pen("axis").drawLine(convCrd("front", (0, settings.FRONT_CRD_BEGIN[1] + settings.AXIS_MARGIN)), convCrd("front", (0, settings.FRONT_CRD_END[1] - settings.AXIS_MARGIN))) # front z axis
		# Draw axis labels
		self._canvas.pen("axis").align("center").size(20)
		self._canvas.pen("axis").showText("x", convCrd("front", (settings.FRONT_CRD_END[0] - 20, -10)))
		self._canvas.pen("axis").showText("z", convCrd("front", (0, settings.FRONT_CRD_END[1] - 20)))
		self._canvas.pen("axis").showText("x", convCrd("top", (settings.TOP_CRD_END[0] - 10, 0)))
		self._canvas.pen("axis").showText("y", convCrd("top", (-10, settings.TOP_CRD_END[1] - 30)))
		self._canvas.pen("axis").showText("x", convCrd("angled", (250, 0, 0)))
		self._canvas.pen("axis").showText("y", convCrd("angled", (0, 200, 0)))
		self._canvas.pen("axis").showText("z", convCrd("angled", (0, 0, 180)))
		self._canvas.update()

if __name__ == "__main__":
	render = Render()
	print(convCrd("front", (-200, -30)))
