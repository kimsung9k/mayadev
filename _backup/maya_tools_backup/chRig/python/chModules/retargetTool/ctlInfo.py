class Move_CTL:
    parentList = ['World_CTL']


class Fly_CTL:
    parentList = ['Move_CTL','World_CTL']


class Root_CTL:
    parentList = ['Fly_CTL', 'Move_CTL']
    

class TorsoRotate_CTL:
    parentList = ['Root_CTL', 'Fly_CTL']


class Waist_CTL:
    parentList = ['TorsoRotate_CTL','Root_CTL', 'Fly_CTL']
    orientOriginRate =  True
    transOriginRate =  True
    

class Chest_CTL:
    parentList = ['TorsoRotate_CTL','Root_CTL', 'Fly_CTL']
    orientOrigin = 'Chest_CTL_Origin'
    transDirect = True

class ChestMove_CTL:
    parentList = ['Chest_CTL', 'TorsoRotate_CTL', 'Root_CTL', 'Fly_CTL']
    
    
class Neck_CTL:
    parentList = ['ChestMove_CTL', 'Chest_CTL', 'TorsoRotate_CTL', 'Root_CTL']
    transOriginRate = True


class NeckMiddle_CTL:
    parentList = ['Neck_CTL','ChestMove_CTL', 'Chest_CTL', 'TorsoRotate_CTL']
    transOriginRate = True

    
class Head_CTL:
    parentList = ['Neck_CTL','ChestMove_CTL', 'Chest_CTL', 'TorsoRotate_CTL']
    transOriginRate = True


class Eye_CTL:
    parentList = ['Head_CTL']
    orientOriginRate =  True
    transOriginRate =  True

    
class EyeAim_SIDE_CTL:
    parentList = ['Eye_CTL']
    orientOriginRate =  True
    transOriginRate =  True
    

class Collar_SIDE_CTL:
    parentList = ['ChestMove_CTL', 'Chest_CTL', 'TorsoRotate_CTL', 'Root_CTL']
    orientOriginRate =  True
    transOriginRate =  True


class Shoulder_SIDE_CTL:
    parentList = ['Collar_SIDE_CTL', 'ChestMove_CTL', 'Chest_CTL', 'TorsoRotate_CTL', 'Root_CTL']
    transOriginRate =  True


class Arm_SIDE_FKNUM_CTL:
    parentList = ['Shoulder_SIDE_CTL','Collar_SIDE_CTL', 'ChestMove_CTL', 'Chest_CTL', 'TorsoRotate_CTL', 'Root_CTL', 'Fly_CTL','Move_CTL']
    

class Arm_SIDE_IK_CTL:
    parentList = ['Collar_SIDE_CTL', 'ChestMove_CTL', 'Chest_CTL', 'TorsoRotate_CTL', 'Root_CTL', 'Fly_CTL','Move_CTL']
    transParent = 'Shoulder_SIDE_CTL'


class Arm_SIDE_PoleV_CTL:
    parentList = ['Arm_SIDE_IK_CTL']
 


class Arm_SIDE_IK_Pin_CTL:
    parentList = ['World_CTL']

class Arm_SIDE_IkItp_CTL:
    parentList = ['Arm_SIDE_IK_CTL']
    
class Arm_SIDE_UpperFlex_CTL:
    parentList = ['Arm_SIDE_CU0']
    
class Arm_SIDE_LowerFlex_CTL:
    parentList = ['Arm_SIDE_CU1']
    
class Arm_SIDE_Switch_CTL:
    parentList = ['Shoulder_SIDE_CTL']
    
class Leg_SIDE_IK_pin_CTL:
    parentList = ['World_CTL']

class Leg_SIDE_IkItp_CTL:
    parentList = ['Leg_SIDE_IK_CTL']
    
class Leg_SIDE_UpperFlex_CTL:
    parentList = ['Leg_SIDE_CU0']
    
class Leg_SIDE_LowerFlex_CTL:
    parentList = ['Leg_SIDE_CU1']
    
class Leg_SIDE_Switch_CTL:
    parentList = ['Hip_CTL']
       

class ThumbNUM_SIDE_CTL:
    parentList = ['Arm_SIDE_CU2']
    transOriginRate =  True
    

class IndexNUM_SIDE_CTL:
    parentList = ['Arm_SIDE_CU2']
    transOriginRate =  True


class MiddleNUM_SIDE_CTL:
    parentList = ['Arm_SIDE_CU2']
    transOriginRate =  True
    
    
class RingNUM_SIDE_CTL:
    parentList = ['Arm_SIDE_CU2']
    transOriginRate =  True
    

class PinkyNUM_SIDE_CTL:
    parentList = ['Arm_SIDE_CU2']
    transOriginRate =  True
    

class Hip_CTL:
    parentList = ['Root_CTL', 'Fly_CTL']
    
    
class Leg_SIDE_FKNUM_CTL:
    parentList = [ 'Hip_CTL', 'Root_CTL', 'Fly_CTL','Move_CTL']
    transParent = 'Hip_SIDE_Const'
    
    
class Leg_SIDE_IK_CTL:
    parentList = ['Hip_CTL','Root_CTL', 'Fly_CTL','Move_CTL']
    transParent = 'Hip_SIDE_Const'
    
    
class Leg_SIDE_PoleV_CTL:
    parentList = ['Leg_SIDE_IK_CTL']