import math
import settings

def convCrd(viewMode: str, point: tuple) -> tuple:
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

