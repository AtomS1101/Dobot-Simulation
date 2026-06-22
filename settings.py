# Screen Settings
SCREEN_WIDTH  = 1000
SCREEN_HEIGHT = 700

# Simulation Field Settings
AXIS_STEPS      = 50
X_AXIS_ANGLE    = 10
Y_AXIS_ANGLE    = 40
JOINT_SIZE      = 5
AXIS_MARGIN     = 30
SHOW_JOINT_NAME = True
SHOW_ORBIT      = False

# Angled Field Settings
ANGLED_VIEW_BEGIN = (-470, -320)
ANGLED_VIEW_END   = (10, 10)
ANGLED_ORIGIN     = (-350, -200)
ANGLED_CRD_BEGIN  = (0, 0)
ANGLED_CRD_END    = (400, 400)

# Front Field Settings
FRONT_VIEW_BEGIN = (30, -320)
FRONT_VIEW_END   = (470, 10)
FRONT_ORIGIN     = ((FRONT_VIEW_BEGIN[0] + FRONT_VIEW_END[0]) // 2, -279)
FRONT_CRD_BEGIN  = (-200, -50)
FRONT_CRD_END    = (200, 350)

# Top Field Settings
TOP_VIEW_BEGIN = (-470, 30)
TOP_VIEW_END   = (10, 320)
TOP_ORIGIN     = ((TOP_VIEW_END[0] + TOP_VIEW_BEGIN[0]) // 2, (TOP_VIEW_END[1] + TOP_VIEW_BEGIN[1]) // 2)  # default is center of the field
TOP_CRD_BEGIN  = (-500, -300)
TOP_CRD_END    = (500, 300)

# Robot Arm Settings
ARM_1_LENGTH = 135  # default is 135
ARM_2_LENGTH = 147  # default is 147
ARM_3_LENGTH = 10
