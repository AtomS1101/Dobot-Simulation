#!/usr/bin/env python3
import turtle
from pen import Pen

class Canvas:
	def __init__(self, width: int, height: int):
		self._window = turtle.Screen()
		self._pens = {}
		self._width = width
		self._height = height

	def setup(self):
		self._window.setup(self._width, self._height)
		self._window.colormode(255) # set color mode to 255
		self._window.bgcolor((255, 255, 255))
		self._window.tracer(0)

	def pen(self, name: str) -> Pen:
		if name not in self._pens:
			self._pens[name] = Pen(turtle.Turtle())
		return self._pens[name]

	def update(self):
		self._window.update()

	def exit(self):
		self._window.exitonclick()

if __name__ == "__main__":
	canvas = Canvas(800, 600)
	canvas.setup()
	canvas.pen("test").color((0, 255, 0)).width(10).drawLine((0, 0), (100, 100))
	canvas.update()
	canvas.exit()
