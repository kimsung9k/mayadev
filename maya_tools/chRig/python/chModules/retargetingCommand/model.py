import maya.cmds as cmds
import math


class BodyCTLs:
    
    _items = []
    
    _items.append( 'Root_CTL' )
    _items.append( 'Fly_CTL' )
    _items.append( 'Hip_CTL' )
    _items.append( 'TorsoRotate_CTL' )
    _items.append( 'Chest_CTL' )
    _items.append( 'Waist_CTL' )
    _items.append( 'ChestMove_CTL' )
    _items.append( 'Collar_L_CTL' )
    _items.append( 'Collar_R_CTL' )
    _items.append( 'Shoulder_L_CTL' )
    _items.append( 'Shoulder_R_CTL' )
    
    
    
class HeadCTLs:
    
    _items = []
    
    _items.append( 'Neck_CTL' )
    _items.append( 'Head_CTL' )
    _items.append( 'Eye_CTL' )
    
    
    
class Arm_L_CTLs:
    
    _items = []
    
    _items.append( 'Arm_L_FK0_CTL' )
    _items.append( 'Arm_L_FK1_CTL' )
    _items.append( 'Arm_L_FK2_CTL' )
    _items.append( 'Arm_L_IK_CTL' )
    _items.append( 'Arm_L_IkItp_CTL' )
    _items.append( 'Arm_L_PoleV_CTL' )
    _items.append( 'Arm_L_Switch_CTL' )
    

 
class Arm_R_CTLs:
    
    _items = []
    
    _items.append( 'Arm_R_FK0_CTL' )
    _items.append( 'Arm_R_FK1_CTL' )
    _items.append( 'Arm_R_FK2_CTL' )
    _items.append( 'Arm_R_IK_CTL' )
    _items.append( 'Arm_R_IkItp_CTL' )
    _items.append( 'Arm_R_PoleV_CTL' )
    _items.append( 'Arm_R_Switch_CTL' )
    


class Leg_L_CTLs:
    
    _items = []
    
    _items.append( 'Leg_L_FK0_CTL' )
    _items.append( 'Leg_L_FK1_CTL' )
    _items.append( 'Leg_L_FK2_CTL' )
    _items.append( 'Leg_L_FK3_CTL' )
    _items.append( 'Leg_L_IK_CTL' )
    _items.append( 'Leg_L_Foot_IK_CTL' )
    _items.append( 'Leg_L_IkItp_CTL' )
    _items.append( 'Leg_L_PoleV_CTL' )
    _items.append( 'Leg_L_Switch_CTL' )
    

    
class Leg_R_CTLs:
    
    _items = []
    
    _items.append( 'Leg_R_FK0_CTL' )
    _items.append( 'Leg_R_FK1_CTL' )
    _items.append( 'Leg_R_FK2_CTL' )
    _items.append( 'Leg_R_FK3_CTL' )
    _items.append( 'Leg_R_IK_CTL' )
    _items.append( 'Leg_R_Foot_IK_CTL' )
    _items.append( 'Leg_R_IkItp_CTL' )
    _items.append( 'Leg_R_PoleV_CTL' )
    _items.append( 'Leg_R_Switch_CTL' )
    

    
class Finger_L_CTLs:
    
    _items = []
    
    _items.append( 'Thumb0_L_CTL' ); _items.append( 'Thumb1_L_CTL' ); _items.append( 'Thumb2_L_CTL' )
    _items.append( 'Index0_L_CTL' ); _items.append( 'Index1_L_CTL' ); _items.append( 'Index2_L_CTL' ); _items.append( 'Index3_L_CTL' )
    _items.append( 'Middle0_L_CTL' ); _items.append( 'Middle1_L_CTL' ); _items.append( 'Middle2_L_CTL' ); _items.append( 'Middle3_L_CTL' )
    _items.append( 'Ring0_L_CTL' ); _items.append( 'Ring1_L_CTL' ); _items.append( 'Ring2_L_CTL' ); _items.append( 'Ring3_L_CTL' )
    _items.append( 'Pinky0_L_CTL' ); _items.append( 'Pinky1_L_CTL' ); _items.append( 'Pinky2_L_CTL' ); _items.append( 'Pinky3_L_CTL' )



class Finger_R_CTLs:
    
    _items = []
    
    _items.append( 'Thumb0_R_CTL' ); _items.append( 'Thumb1_R_CTL' ); _items.append( 'Thumb2_R_CTL' )
    _items.append( 'Index0_R_CTL' ); _items.append( 'Index1_R_CTL' ); _items.append( 'Index2_R_CTL' ); _items.append( 'Index3_R_CTL' )
    _items.append( 'Middle0_R_CTL' ); _items.append( 'Middle1_R_CTL' ); _items.append( 'Middle2_R_CTL' ); _items.append( 'Middle3_R_CTL' )
    _items.append( 'Ring0_R_CTL' ); _items.append( 'Ring1_R_CTL' ); _items.append( 'Ring2_R_CTL' ); _items.append( 'Ring3_R_CTL' )
    _items.append( 'Pinky0_R_CTL' ); _items.append( 'Pinky1_R_CTL' ); _items.append( 'Pinky2_R_CTL' ); _items.append( 'Pinky3_R_CTL' )



class ExportDataInfo:
    
    _namespace = ''
    
    _startFrame = 0.0
    _endFrame   = 23.0
    _offsetFrame = 0.0
    _checkFrames = []
    
    _enableDefault = True
    _enablePartList = []
    _enableCtlList = []
    
    _ctlSet = { 'Body':BodyCTLs, 'Head':HeadCTLs, 'ArmL':Arm_L_CTLs, 'ArmR':Arm_R_CTLs, 
                'LegL':Leg_L_CTLs, 'LegR':Leg_R_CTLs, 'HandL':Finger_L_CTLs, 'HandR':Finger_R_CTLs }
    _ctlParts = ['Body', 'Head', 'ArmL', 'ArmR', 'LegL', 'LegR', 'HandL', 'HandR' ]

    
    
class ImportDataInfo:
    
    _namespaceList = []
    _canimPath = ''
    
    _setRoof = False
    _startFrame = 0.0
    _endFrame   = 10.0
    _baseOffsetframe = 0.0
    _offsetFrame = 0.0
    _speedFrame  = 1.0
    _endFrame    = 10.0
    
    _fliped = False
    
    _enableDefault = True
    _enablePartList = []
    _enableCtlList = []
    _enableFollowList = []
    
    _weightDefault  = 1.0
    _weightCtlList = []
    _weightPartList = []
    
    _ctlSet = { 'Body':BodyCTLs, 'Head':HeadCTLs, 'ArmL':Arm_L_CTLs, 'ArmR':Arm_R_CTLs, 
                'LegL':Leg_L_CTLs, 'LegR':Leg_R_CTLs, 'HandL':Finger_L_CTLs, 'HandR':Finger_R_CTLs }
    _ctlParts = ['Body', 'Head', 'ArmL', 'ArmR', 'LegL', 'LegR', 'HandL', 'HandR' ]
