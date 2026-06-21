#!/usr/bin/env python3
import turtle

class Pen:
	def __init__(self, pen: turtle.Turtle):
		self._pen = pen
		self._color = (0, 0, 0) # default color
		self._width = 1  # default pen width
		self._size = 16  # default text size
		self._fill = False
		self._align = "center"
		self._pen.hideturtle()

	def color(self, color: tuple):
		self._color = color
		self._pen.color(color)
		return self

	def width(self, width: int):
		self._width = width
		self._pen.width(width)
		return self

	def size(self, size: int):
		self._size = size
		return self

	def align(self, align: str):
		self._align = align
		return self

	def fill(self, fill: bool):
		self._fill = fill
		return self

	def goto(self, point: tuple):
		self._pen.penup()
		self._pen.goto(point)

	def showText(self, text: str, point: tuple):
		self._pen.penup()
		self._pen.goto(point)
		self._pen.write(text, False, self._align, ("Times New Roman", self._size, "normal"))
		return self

	def drawLine(self, start: tuple, end: tuple):
		self._pen.penup()
		self._pen.goto(start)
		self._pen.pendown()
		self._pen.goto(end)

	def drawSquare(self, start: tuple, end: tuple):
		self.drawLine((start[0], start[1]), (end[0],   start[1]))
		self.drawLine((end[0],   start[1]), (end[0],   end[1]))
		self.drawLine((end[0],   end[1]),   (start[0], end[1]))
		self.drawLine((start[0], end[1]),   (start[0], start[1]))

	def drawCircle(self, center: tuple, radius: float):
		self._pen.penup()
		self._pen.setheading(0)
		self._pen.goto(center[0], center[1] - radius)
		self._pen.pendown()
		self._pen.fillcolor((255, 255, 255))
		self._pen.begin_fill()
		self._pen.circle(radius)
		self._pen.end_fill()


	def clear(self):
		self._pen.clear()

if __name__ == "__main__":
	window = turtle.Screen()
	window.setup(800, 600)
	window.colormode(255)
	pen = Pen(turtle.Turtle())
	pen.color((255, 0, 0)).width(10).drawLine((0, 0), (100, 100))
	pen.color((0, 0, 255)).width(5).drawCircle((0, 0), 30)
	pen.color((0, 0, 0)).size(20).align("right").showText("Hello, World!", (-50, 0))
	window.exitonclick()
