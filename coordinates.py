import math
import settings as S

def convCrd(viewMode: str, point: tuple) -> tuple:
	if viewMode == "angled":
		x = point[0] * math.cos(math.radians(S.X_AXIS_ANGLE)) + point[1] * math.cos(math.radians(S.Y_AXIS_ANGLE)) + S.ANGLED_ORIGIN[0]
		y = point[2] - point[0] * math.sin(math.radians(S.X_AXIS_ANGLE)) + point[1] * math.sin(math.radians(S.Y_AXIS_ANGLE)) + S.ANGLED_ORIGIN[1]
	elif viewMode == "front":
		xArea = S.FRONT_VIEW_END[0] - S.FRONT_VIEW_BEGIN[0]
		yArea = S.FRONT_VIEW_END[1] - S.FRONT_VIEW_BEGIN[1]
		x = xArea / (S.FRONT_CRD_END[0] - S.FRONT_CRD_BEGIN[0]) * point[0] + S.FRONT_ORIGIN[0]
		y = yArea / (S.FRONT_CRD_END[1] - S.FRONT_CRD_BEGIN[1]) * point[1] + S.FRONT_ORIGIN[1]
	elif viewMode == "top":
		xArea = S.TOP_VIEW_END[0] - S.TOP_VIEW_BEGIN[0]
		yArea = S.TOP_VIEW_END[1] - S.TOP_VIEW_BEGIN[1]
		x = xArea / (S.TOP_CRD_END[0] - S.TOP_CRD_BEGIN[0]) * point[0] + S.TOP_ORIGIN[0]
		y = yArea / (S.TOP_CRD_END[1] - S.TOP_CRD_BEGIN[1]) * point[1] + S.TOP_ORIGIN[1]
	else:
		return point
	return (int(x), int(y))
