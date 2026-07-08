#!/usr/bin/env python3
from . import settings as S
from .canvas import Canvas
from .coordinates import convCrd, angleToCrd

class Render:
	def __init__(self):
		self._canvas = Canvas(S.SCREEN_WIDTH, S.SCREEN_HEIGHT)
		self._canvas.setup()
		self._canvas.pen("top_orbit").color(200, 0, 0).size(1).clear()
		self._canvas.pen("angled_orbit").color(0, 0, 200).size(1).clear()
		self._firstTime = True

	def showInfo(self, angle1: float, angle2: float, direction: float, crd: dict):
		self._canvas.pen("info").color(0, 0, 0).size(20).align("left").clear()
		self._canvas.pen("info").showText("< Information >", (140, 250))
		infoList = {"θ1": f"{angle1:.2f} °", "θ2": f"{angle2:.2f} °", "φ": f"{direction:.2f} °",
			"P": f"({crd['px']:.2f}, {crd['py']:.2f}, {crd['pz']:.2f})",
			"Q": f"({crd['qx']:.2f}, {crd['qy']:.2f}, {crd['qz']:.2f})",
			"R": f"({crd['rx']:.2f}, {crd['ry']:.2f}, {crd['rz']:.2f})"}
		for line, (key, value) in enumerate(infoList.items()):
			self._canvas.pen("info").showText(f"{key}", (150, 220 - (line * 30)))
			self._canvas.pen("info").showText(f": {value}", (180, 220 - (line * 30)))

	def showOrbit(self, rx: float, ry: float, rz: float):
		if (rz < S.PEN_TOLERANCE / 2) and (rz > - S.PEN_TOLERANCE / 2): # whether pen touches a paper
			self._canvas.pen("top_orbit").goto(convCrd("top", (rx, ry)), True)
			self._canvas.pen("angled_orbit").goto(convCrd("angled", (rx, ry, rz)), True)
		else:
			self._canvas.pen("top_orbit").goto(convCrd("top", (rx, ry)), False)
			self._canvas.pen("angled_orbit").goto(convCrd("angled", (rx, ry, rz)), False)
		if self._firstTime:
			self._canvas.pen("top_orbit").clear()
			self._canvas.pen("angled_orbit").clear()
			self._firstTime = False

	def render(self, angle1: float, angle2: float, direction: float):
		c = angleToCrd(angle1, angle2, direction)
		# Front View
		self._canvas.pen("front").width(2).color(0, 0, 0).size(16).align("right").clear()
		self._canvas.pen("front").drawLine(convCrd("front", (0, 0)), convCrd("front", (c["px"], c["pz"])))
		self._canvas.pen("front").drawLine(convCrd("front", (c["px"], c["pz"])), convCrd("front", (c["qx"], c["qz"])))
		self._canvas.pen("front").drawLine(convCrd("front", (c["qx"], c["qz"])), convCrd("front", (c["rx"], c["rz"])))
		self._canvas.pen("front").drawCircle(convCrd("front", (0, 0)), S.JOINT_SIZE)
		self._canvas.pen("front").drawCircle(convCrd("front", (c["px"], c["pz"])), S.JOINT_SIZE)
		self._canvas.pen("front").drawCircle(convCrd("front", (c["qx"], c["qz"])), S.JOINT_SIZE)
		self._canvas.pen("front").drawCircle(convCrd("front", (c["rx"], c["rz"])), S.JOINT_SIZE)
		# Top View
		self._canvas.pen("top").width(2).color(0, 0, 0).size(16).align("right").clear()
		self._canvas.pen("top").drawCircle(convCrd("top", (0, 0)), S.JOINT_SIZE)
		self._canvas.pen("top").drawLine(convCrd("top", (0, 0)), convCrd("top", (c["px"], c["py"])))
		self._canvas.pen("top").drawLine(convCrd("top", (c["px"], c["py"])), convCrd("top", (c["qx"], c["qy"])))
		self._canvas.pen("top").drawLine(convCrd("top", (c["qx"], c["qy"])), convCrd("top", (c["rx"], c["ry"])))
		self._canvas.pen("top").drawCircle(convCrd("top", (c["px"], c["py"])), S.JOINT_SIZE)
		self._canvas.pen("top").drawCircle(convCrd("top", (c["qx"], c["qy"])), S.JOINT_SIZE)
		self._canvas.pen("top").drawCircle(convCrd("top", (c["rx"], c["ry"])), S.JOINT_SIZE)
		# Angled View
		self._canvas.pen("angled").width(2).color(0, 0, 0).size(16).align("left").clear()
		self._canvas.pen("angled").drawLine(convCrd("angled", (0, 0, 0)), convCrd("angled", (c["px"], c["py"], c["pz"])))
		self._canvas.pen("angled").drawCircle(convCrd("angled", (0, 0, 0)), S.JOINT_SIZE)
		self._canvas.pen("angled").drawLine(convCrd("angled", (c["px"], c["py"], c["pz"])), convCrd("angled", (c["qx"], c["qy"], c["qz"])))
		self._canvas.pen("angled").drawLine(convCrd("angled", (c["qx"], c["qy"], c["qz"])), convCrd("angled", (c["rx"], c["ry"], c["rz"])))
		self._canvas.pen("angled").drawCircle(convCrd("angled", (c["qx"], c["qy"], c["qz"])), S.JOINT_SIZE)
		self._canvas.pen("angled").drawCircle(convCrd("angled", (c["px"], c["py"], c["pz"])), S.JOINT_SIZE)
		self._canvas.pen("angled").drawCircle(convCrd("angled", (c["rx"], c["ry"], c["rz"])), S.JOINT_SIZE)

		if S.SHOW_JOINT_NAME:
			self._canvas.pen("front").showText("P", convCrd("front", (c["px"] - 10, c["pz"])))
			self._canvas.pen("front").showText("Q", convCrd("front", (c["qx"] - 10, c["qz"])))
			self._canvas.pen("front").showText("R", convCrd("front", (c["rx"] - 10, c["rz"])))
			self._canvas.pen("top").showText("P", convCrd("top", (c["px"] - 10, c["py"])))
			self._canvas.pen("top").showText("Q", convCrd("top", (c["qx"] - 10, c["qy"])))
			self._canvas.pen("top").showText("R", convCrd("top", (c["rx"] + 40, c["ry"])))
			self._canvas.pen("angled").showText("P", convCrd("angled", (c["px"] + 10, c["py"], c["pz"])))
			self._canvas.pen("angled").showText("Q", convCrd("angled", (c["qx"] + 10, c["qy"], c["qz"])))
			self._canvas.pen("angled").showText("R", convCrd("angled", (c["rx"] + 10, c["ry"], c["rz"])))
		self.showInfo(angle1, angle2, direction, c)
		self.showOrbit(c["rx"], c["ry"], c["rz"])
		self._canvas.update()

	def drawAxis(self):
		self._canvas.pen("axis").color(0, 0, 0).width(1).clear()
		# Draw sub axis lines
		self._canvas.pen("axis").color(220, 220, 220).width(1)
		for i in range(7):
			self._canvas.pen("axis").drawLine(convCrd("angled", (i * S.AXIS_STEPS - 100, -100, 0)), convCrd("angled", (i * S.AXIS_STEPS - 100, 200, 0)))
		for i in range(7):
			self._canvas.pen("axis").drawLine(convCrd("angled", (- 100, i * S.AXIS_STEPS - 100, 0)), convCrd("angled", (250, i * S.AXIS_STEPS - 100, 0)))
		for i in range(10):
			self._canvas.pen("axis").drawLine(convCrd("top", (S.TOP_CRD_BEGIN[0] + S.AXIS_MARGIN, i * S.AXIS_STEPS - 200)), convCrd("top", (S.TOP_CRD_END[0] - S.AXIS_MARGIN, i * S.AXIS_STEPS - 200, 0)))
		for i in range(17):
			self._canvas.pen("axis").drawLine(convCrd("top", (i * S.AXIS_STEPS - 450, S.TOP_CRD_BEGIN[1] + S.AXIS_MARGIN)), convCrd("top", (i * S.AXIS_STEPS - 450, S.TOP_CRD_END[1] - S.AXIS_MARGIN)))
		for i in range(6):
			self._canvas.pen("axis").drawLine(convCrd("front", (S.FRONT_CRD_BEGIN[0] + S.AXIS_MARGIN, i * S.AXIS_STEPS)), convCrd("front", (S.FRONT_CRD_END[0] - S.AXIS_MARGIN, i * S.AXIS_STEPS, 0)))
		for i in range(8):
			self._canvas.pen("axis").drawLine(convCrd("front", (i * S.AXIS_STEPS - 200, S.FRONT_CRD_BEGIN[1] + S.AXIS_MARGIN)), convCrd("front", (i * S.AXIS_STEPS - 200, S.FRONT_CRD_END[1] - S.AXIS_MARGIN)))
		# Draw main axis lines
		self._canvas.pen("axis").color(0, 0, 0).width(2)
		self._canvas.pen("axis").drawLine(convCrd("angled", (-100, 0, 0)), convCrd("angled", (250, 0, 0))) # angled x axis
		self._canvas.pen("axis").drawLine(convCrd("angled", (0, -100, 0)), convCrd("angled", (0, 200, 0))) # angled y axis
		self._canvas.pen("axis").drawLine(convCrd("angled", (0, 0, -100)), convCrd("angled", (0, 0, 180))) # angled z axis
		self._canvas.pen("axis").drawLine(convCrd("top", (0, S.TOP_CRD_BEGIN[1] + S.AXIS_MARGIN)), convCrd("top", (0, S.TOP_CRD_END[1] - S.AXIS_MARGIN))) # top y axis
		self._canvas.pen("axis").drawLine(convCrd("top", (S.TOP_CRD_BEGIN[0] + S.AXIS_MARGIN, 0)), convCrd("top", (S.TOP_CRD_END[0] - S.AXIS_MARGIN, 0))) # top x axis
		self._canvas.pen("axis").drawLine(convCrd("front", (S.FRONT_CRD_BEGIN[0] + S.AXIS_MARGIN, 0)), convCrd("front", (S.FRONT_CRD_END[0] - S.AXIS_MARGIN, 0))) # front x axis
		self._canvas.pen("axis").drawLine(convCrd("front", (0, S.FRONT_CRD_BEGIN[1] + S.AXIS_MARGIN)), convCrd("front", (0, S.FRONT_CRD_END[1] - S.AXIS_MARGIN))) # front z axis
		# Draw axis labels
		self._canvas.pen("axis").align("center").size(20)
		self._canvas.pen("axis").showText("x", convCrd("front", (S.FRONT_CRD_END[0] - 20, -10)))
		self._canvas.pen("axis").showText("z", convCrd("front", (0, S.FRONT_CRD_END[1] - 20)))
		self._canvas.pen("axis").showText("x", convCrd("top", (S.TOP_CRD_END[0] - 10, 0)))
		self._canvas.pen("axis").showText("y", convCrd("top", (-10, S.TOP_CRD_END[1] - 30)))
		self._canvas.pen("axis").showText("x", convCrd("angled", (250, 0, 0)))
		self._canvas.pen("axis").showText("y", convCrd("angled", (0, 200, 0)))
		self._canvas.pen("axis").showText("z", convCrd("angled", (0, 0, 180)))
		# Draw view area squares
		self._canvas.pen("axis").size(18).align("right")
		self._canvas.pen("axis").drawSquare(S.ANGLED_VIEW_BEGIN, S.ANGLED_VIEW_END) # angled view area
		self._canvas.pen("axis").drawSquare(S.TOP_VIEW_BEGIN,    S.TOP_VIEW_END)    # top view area
		self._canvas.pen("axis").drawSquare(S.FRONT_VIEW_BEGIN,  S.FRONT_VIEW_END)  # front view area
		self._canvas.pen("axis").showText("Front View",  (S.FRONT_VIEW_END[0]  - 10, S.FRONT_VIEW_END[1]  - 25))
		self._canvas.pen("axis").showText("Top View",    (S.TOP_VIEW_END[0]    - 10, S.TOP_VIEW_END[1]    - 25))
		self._canvas.pen("axis").showText("Angled View", (S.ANGLED_VIEW_END[0] - 10, S.ANGLED_VIEW_END[1] - 25))
		self._canvas.update()
