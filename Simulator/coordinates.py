import math
from . import settings as S

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

def angleToCrd(angle1: float, angle2: float, direction: float) -> dict:
	px =  S.ARM_1_LENGTH * math.cos(math.radians(angle1)) * math.cos(math.radians(direction))
	py =  S.ARM_1_LENGTH * math.cos(math.radians(angle1)) * math.sin(math.radians(direction))
	pz =  S.ARM_1_LENGTH * math.sin(math.radians(angle1))
	qx = (S.ARM_1_LENGTH * math.cos(math.radians(angle1)) - S.ARM_2_LENGTH * math.cos(math.radians(angle1 + angle2))) * math.cos(math.radians(direction))
	qy = (S.ARM_1_LENGTH * math.cos(math.radians(angle1)) - S.ARM_2_LENGTH * math.cos(math.radians(angle1 + angle2))) * math.sin(math.radians(direction))
	qz =  S.ARM_1_LENGTH * math.sin(math.radians(angle1)) - S.ARM_2_LENGTH * math.sin(math.radians(angle1 + angle2))
	rx = qx
	ry = qy
	rz = qz - S.ARM_3_LENGTH
	return {"px": px, "py": py, "pz": pz, "qx": qx, "qy": qy, "qz": qz, "rx": rx, "ry": ry, "rz": rz}

def crdToAngles(x: float, y: float, z: float) -> dict:
	z += S.ARM_3_LENGTH
	try:
		direction = math.atan2(y, x)
		angle2 = math.acos((S.ARM_1_LENGTH**2 + S.ARM_2_LENGTH**2 - x**2 - y**2 - z**2)/(2 * S.ARM_1_LENGTH * S.ARM_2_LENGTH))
		R = math.sqrt(x**2 + y**2)
		A = S.ARM_1_LENGTH - S.ARM_2_LENGTH * math.cos(angle2)
		B = S.ARM_2_LENGTH * math.sin(angle2)
		angle1 = math.atan2(B * R + A * z, A * R - B * z)
		angle1 = math.degrees(angle1)
		angle2 = math.degrees(angle2)
		direction = math.degrees(direction)
		return {"angle1": angle1, "angle2": angle2, "direction": direction}
	except Exception as e:
		print(e)
		return {}
