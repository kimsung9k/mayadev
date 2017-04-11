
class Root_DRV:
    
    parent = 'DRV_JNT_GRP'
    poseTarget = 'Spline0_BJT'
    


class Hip_SIDE_DRV:
    
    parent = 'Root_DRV'
    poseTarget = 'Leg_SIDE_Upper0_BJT'
    
    

class Knee_SIDE_DRV:
    
    parent = 'Hip_SIDE_DRV'
    poseTarget = 'Leg_SIDE_Lower0_BJT'
    
    
    

class Ankle_SIDE_DRV:
    
    parent = 'Knee_SIDE_DRV'
    poseTarget = 'Leg_SIDE_LowerLAST_BJT'
    


class Ball_SIDE_DRV:
    
    parent = 'Ankle_SIDE_DRV'
    poseTarget = 'Leg_SIDE_Foot0_BJT'
    
    

class BodyRot_DRV:
    
    parent = 'Root_DRV'
    poseTarget = 'SplineENUM_BJT'
    


class Chest_DRV:
    
    parent = 'BodyRot_DRV'
    poseTarget = 'SplineENUM_BJT'
    


class Neck_DRV:
    
    parent = 'Chest_DRV'
    poseTarget = 'Neck_Spline0_BJT'
    
    

class Head_DRV:
    
    parent = 'Neck_DRV'
    poseTarget = 'Neck_SplineENUM_BJT'
    


class Collar_SIDE_DRV:
    
    parent = 'Chest_DRV'
    poseTarget = 'Collar0_SIDE_BJT'
    
    

class Shoulder_SIDE_DRV:
    
    parent = 'Collar_SIDE_DRV'
    poseTarget = 'Arm_SIDE_Upper0_BJT'



class Elbow_SIDE_DRV:
    
    parent = 'Shoulder_SIDE_DRV'
    poseTarget = 'Arm_SIDE_Lower0_BJT'
    


class Hand_SIDE_DRV:
    
    parent = 'Elbow_SIDE_DRV'
    poseTarget = 'Arm_SIDE_LowerENUM_BJT'    