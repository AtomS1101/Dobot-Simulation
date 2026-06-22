#!/usr/bin/env python3
import settings
import math
from canvas import Canvas

class Render:
	def __init__(self):
		self._canvas = Canvas(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
		self._canvas.setup()

	def _convCrd(self, viewMode: str, point: tuple) -> tuple:
		if viewMode == "angled":
			x = point[0] * math.cos(math.radians(settings.X_AXIS_ANGLE)) + point[1] * math.cos(math.radians(settings.Y_AXIS_ANGLE)) + settings.ANGLED_ORIGIN[0]
			y = point[2] - point[0] * math.sin(math.radians(settings.X_AXIS_ANGLE)) + point[1] * math.sin(math.radians(settings.Y_AXIS_ANGLE)) + settings.ANGLED_ORIGIN[1]
		elif viewMode == "front":
			xArea = settings.FRONT_VIEW_END[0] - settings.FRONT_VIEW_BEGIN[0]
			yArea = settings.FRONT_VIEW_END[1] - settings.FRONT_VIEW_BEGIN[1]
			x = xArea / (settings.FRONT_CRD_END[0] - settings.FRONT_CRD_BEGIN[0]) * point[0] + settings.FRONT_ORIGIN[0]
			y = yArea / (settings.FRONT_CRD_END[1] - settings.FRONT_CRD_BEGIN[1]) * point[1] + settings.FRONT_ORIGIN[1]
		elif viewMode == "top":
			xArea = settings.TOP_VIEW_END[0] - settings.TOP_VIEW_BEGIN[0]
			yArea = settings.TOP_VIEW_END[1] - settings.TOP_VIEW_BEGIN[1]
			x = xArea / (settings.TOP_CRD_END[0] - settings.TOP_CRD_BEGIN[0]) * point[0] + settings.TOP_ORIGIN[0]
			y = yArea / (settings.TOP_CRD_END[1] - settings.TOP_CRD_BEGIN[1]) * point[1] + settings.TOP_ORIGIN[1]
		else:
			return point
		return (int(x), int(y))

	def _showInfo(self, info: list):
		self._canvas.pen("info")\
			.color((0, 0, 0))\
			.size(20)\
			.align("left")\
			.clear()
		self._canvas.pen("info").showText("< Information >", (150, 250))
		self._canvas.pen("info").showText("θ_1", (150, 220))
		self._canvas.pen("info").showText("θ_2", (150, 190))
		self._canvas.pen("info").showText("φ",  (150, 160))
		self._canvas.pen("info").showText("P",  (150, 130))
		self._canvas.pen("info").showText("Q",  (150, 100))
		self._canvas.pen("info").showText(f": {info[0]:.2f} °", (190, 220))
		self._canvas.pen("info").showText(f": {info[1]:.2f} °", (190, 190))
		self._canvas.pen("info").showText(f": {info[2]:.2f} °",  (190, 160))
		self._canvas.pen("info").showText(f": ({info[3]:.2f}, {info[4]:.2f}, {info[5]:.2f})",  (190, 130))
		self._canvas.pen("info").showText(f": ({info[6]:.2f}, {info[7]:.2f}, {info[8]:.2f})",  (190, 100))

	def render(self, angle1: float, angle2: float, direction: float):
		px =  settings.ARM_1_LENGTH * math.cos(math.radians(angle1)) * math.cos(math.radians(direction))
		py =  settings.ARM_1_LENGTH * math.cos(math.radians(angle1)) * math.sin(math.radians(direction))
		pz =  settings.ARM_1_LENGTH * math.sin(math.radians(angle1))
		qx = (settings.ARM_1_LENGTH * math.cos(math.radians(angle1)) - settings.ARM_2_LENGTH * math.cos(math.radians(angle1 + angle2))) * math.cos(math.radians(direction))
		qy = (settings.ARM_1_LENGTH * math.cos(math.radians(angle1)) - settings.ARM_2_LENGTH * math.cos(math.radians(angle1 + angle2))) * math.sin(math.radians(direction))
		qz =  settings.ARM_1_LENGTH * math.sin(math.radians(angle1)) - settings.ARM_2_LENGTH * math.sin(math.radians(angle1 + angle2))

		# Front View
		self._canvas.pen("front").color((0, 0, 0)).size(16).align("right").clear()
		self._canvas.pen("front").width(2).drawLine(self._convCrd("front", (0, 0)), self._convCrd("front", (px, pz)))
		self._canvas.pen("front").width(2).drawLine(self._convCrd("front", (px, pz)), self._convCrd("front", (qx, qz)))
		self._canvas.pen("front").width(2).drawCircle(self._convCrd("front", (0, 0)), settings.JOINT_SIZE)
		self._canvas.pen("front").width(2).drawCircle(self._convCrd("front", (px, pz)), settings.JOINT_SIZE)
		self._canvas.pen("front").width(2).drawCircle(self._convCrd("front", (qx, qz)), settings.JOINT_SIZE)

		# Top View
		self._canvas.pen("top").color((0, 0, 0)).size(16).align("right").clear()
		self._canvas.pen("top").width(2).drawLine(self._convCrd("top", (0, 0)), self._convCrd("top", (px, py)))
		self._canvas.pen("top").width(2).drawLine(self._convCrd("top", (px, py)), self._convCrd("top", (qx, qy)))
		self._canvas.pen("top").width(2).drawCircle(self._convCrd("top", (0, 0)), settings.JOINT_SIZE)
		self._canvas.pen("top").width(2).drawCircle(self._convCrd("top", (px, py)), settings.JOINT_SIZE)
		self._canvas.pen("top").width(2).drawCircle(self._convCrd("top", (qx, qy)), settings.JOINT_SIZE)

		# Angled View
		self._canvas.pen("angled").color((0, 0, 0)).size(16).align("left").clear()
		self._canvas.pen("angled").width(2).drawLine(self._convCrd("angled", (0, 0, 0)), self._convCrd("angled", (px, py, pz)))
		self._canvas.pen("angled").width(2).drawCircle(self._convCrd("angled", (0, 0, 0)), settings.JOINT_SIZE)
		self._canvas.pen("angled").width(2).drawLine(self._convCrd("angled", (px, py, pz)), self._convCrd("angled", (qx, qy, qz)))
		self._canvas.pen("angled").width(2).drawCircle(self._convCrd("angled", (qx, qy, qz)), settings.JOINT_SIZE)
		self._canvas.pen("angled").width(2).drawCircle(self._convCrd("angled", (px, py, pz)), settings.JOINT_SIZE)

		if settings.SHOW_JOINT_NAME:
			self._canvas.pen("front").showText("P", self._convCrd("front", (px-10, pz)))
			self._canvas.pen("front").showText("Q", self._convCrd("front", (qx-10, qz)))
			self._canvas.pen("top").showText("P", self._convCrd("top", (px-10, py)))
			self._canvas.pen("top").showText("Q", self._convCrd("top", (qx-10, qy)))
			self._canvas.pen("angled").showText("P", self._convCrd("angled", (px+10, py, pz)))
			self._canvas.pen("angled").showText("Q", self._convCrd("angled", (qx+10, qy, qz)))
		infoList = [angle1, angle2, direction, px, py, pz, qx, qy, qz]
		self._showInfo(infoList)
		self._canvas.update()

	def drawAxis(self):
		self._canvas.pen("axis")\
			.color((0, 0, 0))\
			.width(1)\
			.size(18)\
			.align("right")\
			.clear()
		self._canvas.pen("axis").drawSquare(settings.ANGLED_VIEW_BEGIN, settings.ANGLED_VIEW_END) # angled view area
		self._canvas.pen("axis").drawSquare(settings.TOP_VIEW_BEGIN,    settings.TOP_VIEW_END)    # top view area
		self._canvas.pen("axis").drawSquare(settings.FRONT_VIEW_BEGIN,  settings.FRONT_VIEW_END)  # front view area
		self._canvas.pen("axis").showText("Front View",  (settings.FRONT_VIEW_END[0]  - 5, settings.FRONT_VIEW_END[1]  - 20))
		self._canvas.pen("axis").showText("Top View",    (settings.TOP_VIEW_END[0]    - 5, settings.TOP_VIEW_END[1]    - 20))
		self._canvas.pen("axis").showText("Angled View", (settings.ANGLED_VIEW_END[0] - 5, settings.ANGLED_VIEW_END[1] - 20))
		self._canvas.pen("axis").width(2)
		self._canvas.pen("axis").drawLine(self._convCrd("angled", (-100, 0, 0)), self._convCrd("angled", (250, 0, 0))) # angled x axis
		self._canvas.pen("axis").drawLine(self._convCrd("angled", (0, -100, 0)), self._convCrd("angled", (0, 200, 0))) # angled y axis
		self._canvas.pen("axis").drawLine(self._convCrd("angled", (0, 0, -100)), self._convCrd("angled", (0, 0, 180))) # angled z axis
		self._canvas.pen("axis").drawLine(self._convCrd("top", (0, settings.TOP_CRD_BEGIN[1] + settings.AXIS_MARGIN)), self._convCrd("top", (0, settings.TOP_CRD_END[1] - settings.AXIS_MARGIN))) # top y axis
		self._canvas.pen("axis").drawLine(self._convCrd("top", (settings.TOP_CRD_BEGIN[0] + settings.AXIS_MARGIN, 0)), self._convCrd("top", (settings.TOP_CRD_END[0] - settings.AXIS_MARGIN, 0))) # top x axis
		self._canvas.pen("axis").drawLine(self._convCrd("front", (settings.FRONT_CRD_BEGIN[0] + settings.AXIS_MARGIN, 0)), self._convCrd("front", (settings.FRONT_CRD_END[0] - settings.AXIS_MARGIN, 0))) # front x axis
		self._canvas.pen("axis").drawLine(self._convCrd("front", (0, settings.FRONT_CRD_BEGIN[1] + settings.AXIS_MARGIN)), self._convCrd("front", (0, settings.FRONT_CRD_END[1] - settings.AXIS_MARGIN))) # front z axis
		self._canvas.pen("axis").align("center").size(20)
		self._canvas.pen("axis").showText("x", self._convCrd("front", (settings.FRONT_CRD_END[0] - 20, -10)))
		self._canvas.pen("axis").showText("z", self._convCrd("front", (0, settings.FRONT_CRD_END[1] - 20)))
		self._canvas.pen("axis").showText("x", self._convCrd("top", (settings.TOP_CRD_END[0] - 10, 0)))
		self._canvas.pen("axis").showText("y", self._convCrd("top", (-10, settings.TOP_CRD_END[1] - 30)))
		self._canvas.pen("axis").showText("x", self._convCrd("angled", (250, 0, 0)))
		self._canvas.pen("axis").showText("y", self._convCrd("angled", (0, 200, 0)))
		self._canvas.pen("axis").showText("z", self._convCrd("angled", (0, 0, 180)))
		self._canvas.update()

if __name__ == "__main__":
	render = Render()
	print(render._convCrd("front", (-200, -30)))
