'''
DJB_Character.Character
Handles:
    Class for a character rig
'''
from MayaAutoControlRig.Utils import *
from CharacterNode import *
from BlendshapeTracker import *
import FacialControls
import FacePlus

import maya.cmds as mayac
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import math
import sys
import re
import cPickle
import os
mel.eval("source channelBoxCommand.mel;")
mel.eval("cycleCheck -e off")

FBXpluginLoaded = mayac.pluginInfo("fbxmaya", query = True, loaded = True)
if not FBXpluginLoaded:
    mayac.loadPlugin( "fbxmaya")
    

def createCharacterClassInstance():
    DJB_CharacterInstance = []
    mayac.select(all = True, hi = True)
    unknownNodes = mayac.ls(selection = True, type = "transform")
    infoNodes = []
    for check in unknownNodes:
        if "MIXAMO_CHARACTER_infoNode" in check:
            infoNodes.append(check)
    for infoNode in infoNodes:
        DJB_CharacterInstance.append(DJB_Character(infoNode_ = infoNode))
    mayac.select(clear = True)
    return DJB_CharacterInstance
    

class DJB_Character():
    def __init__(self, infoNode_ = None, hulaOption_ = 0, name_ = "Character"):
        self.characterNameSpace = None
        self.name = None
        self.joints = None
        self.original_Mesh_Names = None
        self.mesh = None
        self.joint_namespace = None
        self.BoundingBox = None
        self.Root = None
        self.Hips = None
        self.Spine = None
        self.Spine1 = None
        self.Spine2 = None
        self.Spine3 = None
        self.Neck = None
        self.Neck1 = None
        self.Head = None
        self.HeadTop_End = None
        self.LeftShoulder = None
        self.LeftArm = None
        self.LeftForeArm = None
        self.LeftHand = None
        self.fingerFlip = False
        self.LeftHandThumb1 = None
        self.LeftHandThumb2 = None
        self.LeftHandThumb3 = None
        self.LeftHandThumb4 = None
        self.LeftHandIndex1 = None
        self.LeftHandIndex2 = None
        self.LeftHandIndex3 = None
        self.LeftHandIndex4 = None
        self.LeftHandMiddle1 = None
        self.LeftHandMiddle2 = None
        self.LeftHandMiddle3 = None
        self.LeftHandMiddle4 = None
        self.LeftHandRing1 = None
        self.LeftHandRing2 = None
        self.LeftHandRing3 = None
        self.LeftHandRing4 = None
        self.LeftHandPinky1 = None
        self.LeftHandPinky2 = None
        self.LeftHandPinky3 = None
        self.LeftHandPinky4 = None
        self.RightShoulder = None
        self.RightArm = None
        self.RightForeArm = None
        self.RightHand = None
        self.RightHandThumb1 = None
        self.RightHandThumb2 = None
        self.RightHandThumb3 = None
        self.RightHandThumb4 = None
        self.RightHandIndex1 = None
        self.RightHandIndex2 = None
        self.RightHandIndex3 = None
        self.RightHandIndex4 = None
        self.RightHandMiddle1 = None
        self.RightHandMiddle2 = None
        self.RightHandMiddle3 = None
        self.RightHandMiddle4 = None
        self.RightHandRing1 = None
        self.RightHandRing2 = None
        self.RightHandRing3 = None
        self.RightHandRing4 = None
        self.RightHandPinky1 = None
        self.RightHandPinky2 = None
        self.RightHandPinky3 = None
        self.RightHandPinky4 = None
        self.LeftUpLeg = None
        self.LeftLeg = None
        self.LeftFoot = None
        self.LeftToeBase = None
        self.LeftToe_End = None
        self.RightUpLeg = None
        self.RightLeg = None
        self.RightFoot = None
        self.RightToeBase = None
        self.RightToe_End = None
        self.bodyParts = None
        self.proportions = {}
        self.defaultControlScale = 0
        self.Character_GRP = None
        self.global_CTRL = None
        self.CTRL_GRP = None
        self.Joint_GRP = None
        self.AnimData_Joint_GRP = None
        self.Bind_Joint_GRP = None
        self.Mesh_GRP = None
        self.Misc_GRP = None
        self.LeftArm_Switch_Reverse = None
        self.RightArm_Switch_Reverse = None
        self.LeftLeg_Switch_Reverse = None
        self.RightLeg_Switch_Reverse = None
        self.Bind_Joint_SelectSet = None
        self.AnimData_Joint_SelectSet = None
        self.Controls_SelectSet = None
        self.Geo_SelectSet = None
        self.Left_Toe_IK_AnimData_GRP = None
        self.Left_Toe_IK_CTRL = None
        self.Left_ToeBase_IK_AnimData_GRP = None
        self.Left_IK_ToeBase_animData_MultNode = None
        self.Left_ToeBase_IK_CTRL = None
        self.Left_Ankle_IK_AnimData_GRP = None
        self.Left_Ankle_IK_CTRL = None
        self.Left_ToeBase_IkHandle = None
        self.Left_ToeEnd_IkHandle = None
        self.Right_Toe_IK_AnimData_GRP = None
        self.Right_Toe_IK_CTRL = None
        self.Right_ToeBase_IK_AnimData_GRP = None
        self.Right_IK_ToeBase_animData_MultNode = None
        self.Right_ToeBase_IK_CTRL = None
        self.Right_Ankle_IK_AnimData_GRP = None
        self.Right_Ankle_IK_CTRL = None
        self.Right_ToeBase_IkHandle = None
        self.Right_ToeEnd_IkHandle = None
        self.LeftHand_CTRLs_GRP = None
        self.RightHand_CTRLs_GRP = None
        self.LeftFoot_FootRoll_MultNode = None
        self.LeftFoot_ToeRoll_MultNode = None
        self.RightFoot_FootRoll_MultNode = None
        self.RightFoot_ToeRoll_MultNode = None
        self.RightFoot_HipPivot_MultNode = None
        self.RightFoot_BallPivot_MultNode = None
        self.RightFoot_ToePivot_MultNode = None
        self.RightFoot_HipSideToSide_MultNode = None
        self.RightFoot_ToeRotate_MultNode = None
        self.IK_Dummy_Joint_GRP = None
        self.LeftHand_grandparent_Constraint = None
        self.LeftHand_grandparent_Constraint_Reverse = None
        self.RightHand_grandparent_Constraint = None
        self.RightHand_grandparent_Constraint_Reverse = None
        self.LeftForeArm_grandparent_Constraint = None
        self.LeftForeArm_grandparent_Constraint_Reverse = None
        self.RightForeArm_grandparent_Constraint = None
        self.RightForeArm_grandparent_Constraint_Reverse = None
        self.origAnim = None
        self.origAnimation_Layer = None
        self.Mesh_Layer = None
        self.Control_Layer = None
        self.Bind_Joint_Layer = None
        self.infoNode = infoNode_
        self.rigType = None
        self.blendShapeTrackers = None
        self.LeftEye = None
        self.RightEye = None
        
        
        self.ExtraJoints = None
        self.numExtraJointChains = 0
        self.Dyn_CTRL = None
        
        self.hulaOption = hulaOption_
        self.exportList = None
        self.FacialControls = None
        self.FacialControl_Layer = None
        self.FacialControl_Mover = None
        self.knownJoints = ['Hips', 'Spine', 'Spine1', 'Spine2', 'Neck', 'Head', 'HeadTop_End', 'RightEye', 'LeftEye', 
                            'LeftShoulder', 'LeftArm', 'LeftForeArm', 'LeftHand', 'LeftHandThumb1', 'LeftHandThumb2', 
                            'LeftHandThumb3', 'LeftHandThumb4', 'LeftHandIndex1', 'LeftHandIndex2', 'LeftHandIndex3', 
                            'LeftHandIndex4', 'LeftHandMiddle1', 'LeftHandMiddle2', 'LeftHandMiddle3', 'LeftHandMiddle4', 
                            'LeftHandRing1', 'LeftHandRing2', 'LeftHandRing3', 'LeftHandRing4', 'LeftHandPinky1', 
                            'LeftHandPinky2', 'LeftHandPinky3', 'LeftHandPinky4', 'RightShoulder', 'RightArm', 'RightForeArm', 
                            'RightHand', 'RightHandPinky1', 'RightHandPinky2', 'RightHandPinky3', 'RightHandPinky4', 
                            'RightHandRing1', 'RightHandRing2', 'RightHandRing3', 'RightHandRing4', 'RightHandMiddle1', 
                            'RightHandMiddle2', 'RightHandMiddle3', 'RightHandMiddle4', 'RightHandIndex1', 'RightHandIndex2', 
                            'RightHandIndex3', 'RightHandIndex4', 'RightHandThumb1', 'RightHandThumb2', 'RightHandThumb3', 
                            'RightHandThumb4', 'RightUpLeg', 'RightLeg', 'RightFoot', 'RightToeBase', 'RightToe_End', 'LeftUpLeg',
                             'LeftLeg', 'LeftFoot', 'LeftToeBase', 'LeftToe_End']
        
        
        
        if not self.infoNode:
            #Fix_Eye_Placement()
            
            #No rig, create
            self.name = name_
            mayac.currentTime(1)
            self.joints = mayac.ls(type = "joint")
            locators = mayac.ls(et = "locator")
            if locators:
                mayac.delete(locators)
            self.mesh = []
            temp = mayac.ls(geometry = True)
            self.original_Mesh_Names = []
            shapes = []
            for geo in temp:
                #Shape22Orig, ShapeOrig, should make a better test
                if "Orig" not in geo and "Bounding_Box_Override_Cube" not in geo:
                    shapes.append(geo)
                    transform = mayac.listRelatives(geo, parent = True)[0]
                    self.original_Mesh_Names.append(transform)
            for geo in shapes:
                parent = mayac.listRelatives(geo, parent = True, path = True)[0]
                if "|" in geo:
                    geo = makeUnique(geo, "Shape")
                parent = mayac.listRelatives(geo, parent = True, path = True)[0]
                DJB_Unlock(parent)
                parent = mayac.rename(parent, "Mesh_%s" % (DJB_findAfterSeperator(parent, ":")))
                self.mesh.append(mayac.listRelatives(parent, children = True, type = "shape", path = True)[0])
                
            print "ASPDOIJASDPOIJASPDOIJASD"
            #check for _
            nameSpaceFound = False
            if not self.joint_namespace:
                for i in range(len(self.joints)):
                    if not self.joint_namespace:
                        print self.joints[i]
                        for check in self.knownJoints:
                            if not self.joint_namespace:
                                print "\t%s"%check
                                if check in self.joints[i]:
                                    self.joint_namespace = DJB_findBeforeSeparator(self.joints[i], ':')
                                    if not self.joint_namespace and "_End" not in self.joints[i]:
                                        self.joint_namespace = DJB_findBeforeSeparator(self.joints[i], '_')
                                    break
                
            
            #override box gets proportions if it exists
            Bounding_Box_Override_Cube = mayac.ls("*Bounding_Box_Override_Cube*")
            if Bounding_Box_Override_Cube:
                    self.BoundingBox = mayac.exactWorldBoundingBox(Bounding_Box_Override_Cube)
                    mayac.delete(Bounding_Box_Override_Cube)
            else:
                self.BoundingBox = mayac.exactWorldBoundingBox(self.mesh)
            
            if self.hulaOption:              
                self.Root = DJB_CharacterNode("Root", actAsRoot_ = 1, optional_ = 1, joint_namespace_ = self.joint_namespace)
                if not self.Root.Bind_Joint:
                    mayac.duplicate(self.joint_namespace + "Hips", parentOnly = True, name = self.joint_namespace + "Root")
                    self.Root = DJB_CharacterNode("Root", actAsRoot_ = 1, joint_namespace_ = self.joint_namespace)
                self.Hips = DJB_CharacterNode("Hips", parent = self.Root, joint_namespace_ = self.joint_namespace)
                self.Spine = DJB_CharacterNode("Spine", parent = self.Root, joint_namespace_ = self.joint_namespace)
                mayac.parent(self.Hips.Bind_Joint, self.Spine.Bind_Joint, self.Root.Bind_Joint)
            else:
                self.Root = DJB_CharacterNode("Root", optional_ = 1, joint_namespace_ = self.joint_namespace)
                if self.Root.Bind_Joint:
                    self.Hips = DJB_CharacterNode("Hips", joint_namespace_ = self.joint_namespace)
                    self.hulaOption = True
                else:
                    print "adspofapsdofijasdf"
                    print self.joint_namespace
                    self.Hips = DJB_CharacterNode("Hips", actAsRoot_ = 1, joint_namespace_ = self.joint_namespace)
                    print "adspofapsdofijasdf"
                self.Spine = DJB_CharacterNode("Spine", parent = self.Hips, joint_namespace_ = self.joint_namespace)
                
            self.Spine1 = DJB_CharacterNode("Spine1", parent = self.Spine, joint_namespace_ = self.joint_namespace)
            self.Spine2 = DJB_CharacterNode("Spine2", parent = self.Spine1, optional_ = 1, joint_namespace_ = self.joint_namespace)
            if self.Spine2.Bind_Joint:
                self.Spine3 = DJB_CharacterNode("Spine3", parent = self.Spine2, optional_ = 1, joint_namespace_ = self.joint_namespace)
                if self.Spine3.Bind_Joint:
                    self.Neck = DJB_CharacterNode("Neck", parent = self.Spine3, joint_namespace_ = self.joint_namespace)
                else:
                    self.Neck = DJB_CharacterNode("Neck", parent = self.Spine2, joint_namespace_ = self.joint_namespace)
                self.Neck1 = DJB_CharacterNode("Neck1", parent = self.Neck, optional_ = 1, joint_namespace_ = self.joint_namespace)
                if self.Neck1.Bind_Joint:
                    self.Head = DJB_CharacterNode("Head", parent = self.Neck1, joint_namespace_ = self.joint_namespace)
                else:
                    self.Head = DJB_CharacterNode("Head", parent = self.Neck, joint_namespace_ = self.joint_namespace)
                self.HeadTop_End = DJB_CharacterNode("HeadTop_End", parent = self.Head, alias_ = ["Head_End", "Head_END"], joint_namespace_ = self.joint_namespace)
                if self.Spine3.Bind_Joint:
                    self.LeftShoulder = DJB_CharacterNode("LeftShoulder", parent = self.Spine3, joint_namespace_ = self.joint_namespace)
                else:
                    self.LeftShoulder = DJB_CharacterNode("LeftShoulder", parent = self.Spine2, joint_namespace_ = self.joint_namespace)
            else:
                #going to put in a blank spine3 just to mitigate errors, TODO: better handling
                self.Spine3 = DJB_CharacterNode("Spine3", parent = self.Spine1, optional_ = 1, joint_namespace_ = self.joint_namespace)
                self.Neck = DJB_CharacterNode("Neck", parent = self.Spine1, joint_namespace_ = self.joint_namespace)
                self.Neck1 = DJB_CharacterNode("Neck1", parent = self.Neck, optional_ = 1, joint_namespace_ = self.joint_namespace)
                if self.Neck1.Bind_Joint:
                    self.Head = DJB_CharacterNode("Head", parent = self.Neck1, joint_namespace_ = self.joint_namespace)
                else:
                    self.Head = DJB_CharacterNode("Head", parent = self.Neck, joint_namespace_ = self.joint_namespace)
                self.HeadTop_End = DJB_CharacterNode("HeadTop_End", parent = self.Head, alias_ = ["Head_End", "Head_END"], joint_namespace_ = self.joint_namespace)
                self.LeftShoulder = DJB_CharacterNode("LeftShoulder", parent = self.Spine1, joint_namespace_ = self.joint_namespace)
            self.LeftArm = DJB_CharacterNode("LeftArm", parent = self.LeftShoulder, joint_namespace_ = self.joint_namespace)
            self.LeftForeArm = DJB_CharacterNode("LeftForeArm", parent = self.LeftArm, joint_namespace_ = self.joint_namespace)
            self.LeftHand = DJB_CharacterNode("LeftHand", parent = self.LeftForeArm, joint_namespace_ = self.joint_namespace)
            self.LeftHandThumb1 = DJB_CharacterNode("LeftHandThumb1", optional_ = 1, parent = self.LeftHand, joint_namespace_ = self.joint_namespace)
            self.LeftHandThumb2 = DJB_CharacterNode("LeftHandThumb2", optional_ = 1, parent = self.LeftHandThumb1, joint_namespace_ = self.joint_namespace)
            self.LeftHandThumb3 = DJB_CharacterNode("LeftHandThumb3", optional_ = 1, parent = self.LeftHandThumb2, joint_namespace_ = self.joint_namespace)
            self.LeftHandThumb4 = DJB_CharacterNode("LeftHandThumb4", optional_ = 1, parent = self.LeftHandThumb3, joint_namespace_ = self.joint_namespace)
            self.LeftHandIndex1 = DJB_CharacterNode("LeftHandIndex1", optional_ = 1,parent = self.LeftHand, joint_namespace_ = self.joint_namespace)
            self.LeftHandIndex2 = DJB_CharacterNode("LeftHandIndex2", optional_ = 1, parent = self.LeftHandIndex1, joint_namespace_ = self.joint_namespace)
            self.LeftHandIndex3 = DJB_CharacterNode("LeftHandIndex3", optional_ = 1, parent = self.LeftHandIndex2, joint_namespace_ = self.joint_namespace)
            self.LeftHandIndex4 = DJB_CharacterNode("LeftHandIndex4", optional_ = 1, parent = self.LeftHandIndex3, joint_namespace_ = self.joint_namespace)
            self.LeftHandMiddle1 = DJB_CharacterNode("LeftHandMiddle1", optional_ = 1, parent = self.LeftHand, joint_namespace_ = self.joint_namespace)
            self.LeftHandMiddle2 = DJB_CharacterNode("LeftHandMiddle2", optional_ = 1, parent = self.LeftHandMiddle1, joint_namespace_ = self.joint_namespace)
            self.LeftHandMiddle3 = DJB_CharacterNode("LeftHandMiddle3", optional_ = 1, parent = self.LeftHandMiddle2, joint_namespace_ = self.joint_namespace)
            self.LeftHandMiddle4 = DJB_CharacterNode("LeftHandMiddle4", optional_ = 1, parent = self.LeftHandMiddle3, joint_namespace_ = self.joint_namespace)
            self.LeftHandRing1 = DJB_CharacterNode("LeftHandRing1", optional_ = 1, parent = self.LeftHand, joint_namespace_ = self.joint_namespace)
            self.LeftHandRing2 = DJB_CharacterNode("LeftHandRing2", optional_ = 1, parent = self.LeftHandRing1, joint_namespace_ = self.joint_namespace)
            self.LeftHandRing3 = DJB_CharacterNode("LeftHandRing3", optional_ = 1, parent = self.LeftHandRing2, joint_namespace_ = self.joint_namespace)
            self.LeftHandRing4 = DJB_CharacterNode("LeftHandRing4", optional_ = 1, parent = self.LeftHandRing3, joint_namespace_ = self.joint_namespace)
            self.LeftHandPinky1 = DJB_CharacterNode("LeftHandPinky1", optional_ = 1, parent = self.LeftHand, joint_namespace_ = self.joint_namespace)
            self.LeftHandPinky2 = DJB_CharacterNode("LeftHandPinky2", optional_ = 1, parent = self.LeftHandPinky1, joint_namespace_ = self.joint_namespace)
            self.LeftHandPinky3 = DJB_CharacterNode("LeftHandPinky3", optional_ = 1, parent = self.LeftHandPinky2, joint_namespace_ = self.joint_namespace)
            self.LeftHandPinky4 = DJB_CharacterNode("LeftHandPinky4", optional_ = 1, parent = self.LeftHandPinky3, joint_namespace_ = self.joint_namespace)
            if self.Spine2.Bind_Joint:
                if self.Spine3.Bind_Joint:
                    self.RightShoulder = DJB_CharacterNode("RightShoulder", parent = self.Spine3, joint_namespace_ = self.joint_namespace)
                else:
                    self.RightShoulder = DJB_CharacterNode("RightShoulder", parent = self.Spine2, joint_namespace_ = self.joint_namespace)
            else:
                self.RightShoulder = DJB_CharacterNode("RightShoulder", parent = self.Spine1, joint_namespace_ = self.joint_namespace)
            self.RightArm = DJB_CharacterNode("RightArm", parent = self.RightShoulder, joint_namespace_ = self.joint_namespace)
            self.RightForeArm = DJB_CharacterNode("RightForeArm", parent = self.RightArm, joint_namespace_ = self.joint_namespace)
            self.RightHand = DJB_CharacterNode("RightHand", parent = self.RightForeArm, joint_namespace_ = self.joint_namespace)
            self.RightHandThumb1 = DJB_CharacterNode("RightHandThumb1", optional_ = 1, parent = self.RightHand, joint_namespace_ = self.joint_namespace)
            self.RightHandThumb2 = DJB_CharacterNode("RightHandThumb2", optional_ = 1, parent = self.RightHandThumb1, joint_namespace_ = self.joint_namespace)
            self.RightHandThumb3 = DJB_CharacterNode("RightHandThumb3", optional_ = 1, parent = self.RightHandThumb2, joint_namespace_ = self.joint_namespace)
            self.RightHandThumb4 = DJB_CharacterNode("RightHandThumb4", optional_ = 1, parent = self.RightHandThumb3, joint_namespace_ = self.joint_namespace)
            self.RightHandIndex1 = DJB_CharacterNode("RightHandIndex1", optional_ = 1, parent = self.RightHand, joint_namespace_ = self.joint_namespace)
            self.RightHandIndex2 = DJB_CharacterNode("RightHandIndex2", optional_ = 1, parent = self.RightHandIndex1, joint_namespace_ = self.joint_namespace)
            self.RightHandIndex3 = DJB_CharacterNode("RightHandIndex3", optional_ = 1, parent = self.RightHandIndex2, joint_namespace_ = self.joint_namespace)
            self.RightHandIndex4 = DJB_CharacterNode("RightHandIndex4", optional_ = 1, parent = self.RightHandIndex3, joint_namespace_ = self.joint_namespace)
            self.RightHandMiddle1 = DJB_CharacterNode("RightHandMiddle1", optional_ = 1, parent = self.RightHand, joint_namespace_ = self.joint_namespace)
            self.RightHandMiddle2 = DJB_CharacterNode("RightHandMiddle2", optional_ = 1, parent = self.RightHandMiddle1, joint_namespace_ = self.joint_namespace)
            self.RightHandMiddle3 = DJB_CharacterNode("RightHandMiddle3", optional_ = 1, parent = self.RightHandMiddle2, joint_namespace_ = self.joint_namespace)
            self.RightHandMiddle4 = DJB_CharacterNode("RightHandMiddle4", optional_ = 1, parent = self.RightHandMiddle3, joint_namespace_ = self.joint_namespace)
            self.RightHandRing1 = DJB_CharacterNode("RightHandRing1", optional_ = 1, parent = self.RightHand, joint_namespace_ = self.joint_namespace)
            self.RightHandRing2 = DJB_CharacterNode("RightHandRing2", optional_ = 1, parent = self.RightHandRing1, joint_namespace_ = self.joint_namespace)
            self.RightHandRing3 = DJB_CharacterNode("RightHandRing3", optional_ = 1, parent = self.RightHandRing2, joint_namespace_ = self.joint_namespace)
            self.RightHandRing4 = DJB_CharacterNode("RightHandRing4", optional_ = 1, parent = self.RightHandRing3, joint_namespace_ = self.joint_namespace)
            self.RightHandPinky1 = DJB_CharacterNode("RightHandPinky1", optional_ = 1, parent = self.RightHand, joint_namespace_ = self.joint_namespace)
            self.RightHandPinky2 = DJB_CharacterNode("RightHandPinky2", optional_ = 1, parent = self.RightHandPinky1, joint_namespace_ = self.joint_namespace)
            self.RightHandPinky3 = DJB_CharacterNode("RightHandPinky3", optional_ = 1, parent = self.RightHandPinky2, joint_namespace_ = self.joint_namespace)
            self.RightHandPinky4 = DJB_CharacterNode("RightHandPinky4", optional_ = 1, parent = self.RightHandPinky3, joint_namespace_ = self.joint_namespace)
            self.LeftUpLeg = DJB_CharacterNode("LeftUpLeg", parent = self.Hips, joint_namespace_ = self.joint_namespace)
            self.LeftLeg = DJB_CharacterNode("LeftLeg", parent = self.LeftUpLeg, joint_namespace_ = self.joint_namespace)
            self.LeftFoot = DJB_CharacterNode("LeftFoot", parent = self.LeftLeg, joint_namespace_ = self.joint_namespace)
            self.LeftToeBase = DJB_CharacterNode("LeftToeBase", parent = self.LeftFoot, joint_namespace_ = self.joint_namespace)
            self.LeftToe_End = DJB_CharacterNode("LeftToe_End", parent = self.LeftToeBase, alias_ = ["toe_L", "LeftFootToeBase_End"], joint_namespace_ = self.joint_namespace)
            self.RightUpLeg = DJB_CharacterNode("RightUpLeg", parent = self.Hips, joint_namespace_ = self.joint_namespace)
            self.RightLeg = DJB_CharacterNode("RightLeg", parent = self.RightUpLeg, joint_namespace_ = self.joint_namespace)
            self.RightFoot = DJB_CharacterNode("RightFoot", parent = self.RightLeg, joint_namespace_ = self.joint_namespace)
            self.RightToeBase = DJB_CharacterNode("RightToeBase", parent = self.RightFoot, joint_namespace_ = self.joint_namespace)
            self.RightToe_End = DJB_CharacterNode("RightToe_End", parent = self.RightToeBase, alias_ = ["toe_R", "RightFootToeBase_End"], joint_namespace_ = self.joint_namespace)
            self.LeftEye = DJB_CharacterNode("LeftEye", optional_ = 1, parent = self.Head, joint_namespace_ = self.joint_namespace)
            self.RightEye = DJB_CharacterNode("RightEye", optional_ = 1, parent = self.Head, joint_namespace_ = self.joint_namespace)
            #educated guess with 2 samples for rig type
            if mayac.getAttr("%s.jointOrient" % self.LeftUpLeg.Bind_Joint)[0] == (0,0,0) and mayac.getAttr("%s.jointOrient" % self.RightArm.Bind_Joint)[0] == (0,0,0):
                self.rigType = "World"
            else:
                self.rigType = "AutoRig"
            
            #educated guess for fingerFlip
            if self.LeftHandIndex1.Bind_Joint:
                jox = mayac.getAttr("%s.jointOrientX" % (self.LeftHandIndex1.Bind_Joint))
                if jox < -100 or jox > 100:
                    self.fingerFlip = False
                else:
                    self.fingerFlip = True
        
            
        #there is an infoNode for this Character
        else:
            
            self.characterNameSpace = DJB_findBeforeSeparator(self.infoNode, ':')
            if not self.characterNameSpace:
                self.characterNameSpace = DJB_findBeforeSeparator(self.infoNode, 'MIXAMO_CHARACTER_infoNode')
            print self.characterNameSpace
            
            self.joint_namespace = attrToPy("%s.joint_namespace" % (self.infoNode))
            #filmbox attrs
            self.name = attrToPy("%s.name" % (self.infoNode))
            
            
            
            self.mesh = attrToPy("%s.mesh" % (self.infoNode))
            self.original_Mesh_Names = attrToPy("%s.original_Mesh_Names" % (self.infoNode))
            self.BoundingBox = attrToPy("%s.BoundingBox" % (self.infoNode))
            self.rigType = attrToPy("%s.rigType" % (self.infoNode))
            #####################
            self.hulaOption = attrToPy("%s.hulaOption" % (self.infoNode))
            
            self.Root = DJB_CharacterNode("Root", infoNode_ = attrToPy("%s.Root" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            if self.hulaOption:
                if not self.Root.Bind_Joint:
                    return None
                self.Hips = DJB_CharacterNode("Hips", parent = self.Root, infoNode_ = attrToPy("%s.Hips" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
                self.Spine = DJB_CharacterNode("Spine", parent = self.Root, infoNode_ = attrToPy("%s.Spine" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            else:
                self.Hips = DJB_CharacterNode("Hips", infoNode_ = attrToPy("%s.Hips" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
                self.Spine = DJB_CharacterNode("Spine", parent = self.Hips, infoNode_ = attrToPy("%s.Spine" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.Spine1 = DJB_CharacterNode("Spine1", parent = self.Spine, infoNode_ = attrToPy("%s.Spine1" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.Spine2 = DJB_CharacterNode("Spine2", parent = self.Spine1, optional_ = 1, infoNode_ = attrToPy("%s.Spine2" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            if self.Spine2.Bind_Joint:
                self.Spine3 = DJB_CharacterNode("Spine3", parent = self.Spine2, optional_ = 1, infoNode_ = attrToPy("%s.Spine3" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
                if self.Spine3.Bind_Joint:
                    self.Neck = DJB_CharacterNode("Neck", parent = self.Spine3, infoNode_ = attrToPy("%s.Neck" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
                else:
                    self.Neck = DJB_CharacterNode("Neck", parent = self.Spine2, infoNode_ = attrToPy("%s.Neck" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            else:
                self.Spine3 = DJB_CharacterNode("Spine3", parent = self.Spine1, optional_ = 1, infoNode_ = attrToPy("%s.Spine3" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
                self.Neck = DJB_CharacterNode("Neck", parent = self.Spine1, infoNode_ = attrToPy("%s.Neck" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.Neck1 = DJB_CharacterNode("Neck1", parent = self.Neck, optional_ = 1, infoNode_ = attrToPy("%s.Neck1" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            if self.Neck1.Bind_Joint:
                self.Head = DJB_CharacterNode("Head", parent = self.Neck1, infoNode_ = attrToPy("%s.Head" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            else:
                self.Head = DJB_CharacterNode("Head", parent = self.Neck, infoNode_ = attrToPy("%s.Head" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.HeadTop_End = DJB_CharacterNode("HeadTop_End", parent = self.Head, infoNode_ = attrToPy("%s.HeadTop_End" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            if self.Spine2.Bind_Joint:
                if self.Spine3.Bind_Joint:
                    self.LeftShoulder = DJB_CharacterNode("LeftShoulder", parent = self.Spine3, infoNode_ = attrToPy("%s.LeftShoulder" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
                else:
                    self.LeftShoulder = DJB_CharacterNode("LeftShoulder", parent = self.Spine2, infoNode_ = attrToPy("%s.LeftShoulder" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            else:
                self.LeftShoulder = DJB_CharacterNode("LeftShoulder", parent = self.Spine1, infoNode_ = attrToPy("%s.LeftShoulder" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.LeftArm = DJB_CharacterNode("LeftArm", parent = self.LeftShoulder, infoNode_ = attrToPy("%s.LeftArm" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.LeftForeArm = DJB_CharacterNode("LeftForeArm", parent = self.LeftArm, infoNode_ = attrToPy("%s.LeftForeArm" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.LeftHand = DJB_CharacterNode("LeftHand", parent = self.LeftForeArm, infoNode_ = attrToPy("%s.LeftHand" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.LeftHandThumb1 = DJB_CharacterNode("LeftHandThumb1", optional_ = 1, parent = self.LeftHand, infoNode_ = attrToPy("%s.LeftHandThumb1" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.LeftHandThumb2 = DJB_CharacterNode("LeftHandThumb2", optional_ = 1, parent = self.LeftHandThumb1, infoNode_ = attrToPy("%s.LeftHandThumb2" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.LeftHandThumb3 = DJB_CharacterNode("LeftHandThumb3", optional_ = 1, parent = self.LeftHandThumb2, infoNode_ = attrToPy("%s.LeftHandThumb3" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.LeftHandThumb4 = DJB_CharacterNode("LeftHandThumb4", optional_ = 1, parent = self.LeftHandThumb3, infoNode_ = attrToPy("%s.LeftHandThumb4" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.LeftHandIndex1 = DJB_CharacterNode("LeftHandIndex1", optional_ = 1, parent = self.LeftHand, infoNode_ = attrToPy("%s.LeftHandIndex1" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.LeftHandIndex2 = DJB_CharacterNode("LeftHandIndex2", optional_ = 1, parent = self.LeftHandIndex1, infoNode_ = attrToPy("%s.LeftHandIndex2" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.LeftHandIndex3 = DJB_CharacterNode("LeftHandIndex3", optional_ = 1, parent = self.LeftHandIndex2, infoNode_ = attrToPy("%s.LeftHandIndex3" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.LeftHandIndex4 = DJB_CharacterNode("LeftHandIndex4", optional_ = 1, parent = self.LeftHandIndex3, infoNode_ = attrToPy("%s.LeftHandIndex4" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.LeftHandMiddle1 = DJB_CharacterNode("LeftHandMiddle1", optional_ = 1, parent = self.LeftHand, infoNode_ = attrToPy("%s.LeftHandMiddle1" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.LeftHandMiddle2 = DJB_CharacterNode("LeftHandMiddle2", optional_ = 1, parent = self.LeftHandMiddle1, infoNode_ = attrToPy("%s.LeftHandMiddle2" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.LeftHandMiddle3 = DJB_CharacterNode("LeftHandMiddle3", optional_ = 1, parent = self.LeftHandMiddle2, infoNode_ = attrToPy("%s.LeftHandMiddle3" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.LeftHandMiddle4 = DJB_CharacterNode("LeftHandMiddle4", optional_ = 1, parent = self.LeftHandMiddle3, infoNode_ = attrToPy("%s.LeftHandMiddle4" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.LeftHandRing1 = DJB_CharacterNode("LeftHandRing1", optional_ = 1, parent = self.LeftHand, infoNode_ = attrToPy("%s.LeftHandRing1" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.LeftHandRing2 = DJB_CharacterNode("LeftHandRing2", optional_ = 1, parent = self.LeftHandRing1, infoNode_ = attrToPy("%s.LeftHandRing2" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.LeftHandRing3 = DJB_CharacterNode("LeftHandRing3", optional_ = 1, parent = self.LeftHandRing2, infoNode_ = attrToPy("%s.LeftHandRing3" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.LeftHandRing4 = DJB_CharacterNode("LeftHandRing4", optional_ = 1, parent = self.LeftHandRing3, infoNode_ = attrToPy("%s.LeftHandRing4" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.LeftHandPinky1 = DJB_CharacterNode("LeftHandPinky1", optional_ = 1, parent = self.LeftHand, infoNode_ = attrToPy("%s.LeftHandPinky1" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.LeftHandPinky2 = DJB_CharacterNode("LeftHandPinky2", optional_ = 1, parent = self.LeftHandPinky1, infoNode_ = attrToPy("%s.LeftHandPinky2" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.LeftHandPinky3 = DJB_CharacterNode("LeftHandPinky3", optional_ = 1, parent = self.LeftHandPinky2, infoNode_ = attrToPy("%s.LeftHandPinky3" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.LeftHandPinky4 = DJB_CharacterNode("LeftHandPinky4", optional_ = 1, parent = self.LeftHandPinky3, infoNode_ = attrToPy("%s.LeftHandPinky4" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            if self.Spine2.Bind_Joint:
                if self.Spine3.Bind_Joint:
                    self.RightShoulder = DJB_CharacterNode("RightShoulder", parent = self.Spine3, infoNode_ = attrToPy("%s.RightShoulder" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
                else:
                    self.RightShoulder = DJB_CharacterNode("RightShoulder", parent = self.Spine2, infoNode_ = attrToPy("%s.RightShoulder" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            else:
                self.RightShoulder = DJB_CharacterNode("RightShoulder", parent = self.Spine1, infoNode_ = attrToPy("%s.RightShoulder" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.RightArm = DJB_CharacterNode("RightArm", parent = self.RightShoulder, infoNode_ = attrToPy("%s.RightArm" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.RightForeArm = DJB_CharacterNode("RightForeArm", parent = self.RightArm, infoNode_ = attrToPy("%s.RightForeArm" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.RightHand = DJB_CharacterNode("RightHand", parent = self.RightForeArm, infoNode_ = attrToPy("%s.RightHand" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.RightHandThumb1 = DJB_CharacterNode("RightHandThumb1", optional_ = 1, parent = self.RightHand, infoNode_ = attrToPy("%s.RightHandThumb1" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.RightHandThumb2 = DJB_CharacterNode("RightHandThumb2", optional_ = 1, parent = self.RightHandThumb1, infoNode_ = attrToPy("%s.RightHandThumb2" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.RightHandThumb3 = DJB_CharacterNode("RightHandThumb3", optional_ = 1, parent = self.RightHandThumb2, infoNode_ = attrToPy("%s.RightHandThumb3" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.RightHandThumb4 = DJB_CharacterNode("RightHandThumb4", optional_ = 1, parent = self.RightHandThumb3, infoNode_ = attrToPy("%s.RightHandThumb4" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.RightHandIndex1 = DJB_CharacterNode("RightHandIndex1", optional_ = 1, parent = self.RightHand, infoNode_ = attrToPy("%s.RightHandIndex1" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.RightHandIndex2 = DJB_CharacterNode("RightHandIndex2", optional_ = 1, parent = self.RightHandIndex1, infoNode_ = attrToPy("%s.RightHandIndex2" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.RightHandIndex3 = DJB_CharacterNode("RightHandIndex3", optional_ = 1, parent = self.RightHandIndex2, infoNode_ = attrToPy("%s.RightHandIndex3" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.RightHandIndex4 = DJB_CharacterNode("RightHandIndex4", optional_ = 1, parent = self.RightHandIndex3, infoNode_ = attrToPy("%s.RightHandIndex4" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.RightHandMiddle1 = DJB_CharacterNode("RightHandMiddle1", optional_ = 1, parent = self.RightHand, infoNode_ = attrToPy("%s.RightHandMiddle1" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.RightHandMiddle2 = DJB_CharacterNode("RightHandMiddle2", optional_ = 1, parent = self.RightHandMiddle1, infoNode_ = attrToPy("%s.RightHandMiddle2" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.RightHandMiddle3 = DJB_CharacterNode("RightHandMiddle3", optional_ = 1, parent = self.RightHandMiddle2, infoNode_ = attrToPy("%s.RightHandMiddle3" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.RightHandMiddle4 = DJB_CharacterNode("RightHandMiddle4", optional_ = 1, parent = self.RightHandMiddle3, infoNode_ = attrToPy("%s.RightHandMiddle4" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.RightHandRing1 = DJB_CharacterNode("RightHandRing1", optional_ = 1, parent = self.RightHand, infoNode_ = attrToPy("%s.RightHandRing1" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.RightHandRing2 = DJB_CharacterNode("RightHandRing2", optional_ = 1, parent = self.RightHandRing1, infoNode_ = attrToPy("%s.RightHandRing2" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.RightHandRing3 = DJB_CharacterNode("RightHandRing3", optional_ = 1, parent = self.RightHandRing2, infoNode_ = attrToPy("%s.RightHandRing3" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.RightHandRing4 = DJB_CharacterNode("RightHandRing4", optional_ = 1, parent = self.RightHandRing3, infoNode_ = attrToPy("%s.RightHandRing4" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.RightHandPinky1 = DJB_CharacterNode("RightHandPinky1", optional_ = 1, parent = self.RightHand, infoNode_ = attrToPy("%s.RightHandPinky1" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.RightHandPinky2 = DJB_CharacterNode("RightHandPinky2", optional_ = 1, parent = self.RightHandPinky1, infoNode_ = attrToPy("%s.RightHandPinky2" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.RightHandPinky3 = DJB_CharacterNode("RightHandPinky3", optional_ = 1, parent = self.RightHandPinky2, infoNode_ = attrToPy("%s.RightHandPinky3" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.RightHandPinky4 = DJB_CharacterNode("RightHandPinky4", optional_ = 1, parent = self.RightHandPinky3, infoNode_ = attrToPy("%s.RightHandPinky4" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.LeftUpLeg = DJB_CharacterNode("LeftUpLeg", parent = self.Hips, infoNode_ = attrToPy("%s.LeftUpLeg" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.LeftLeg = DJB_CharacterNode("LeftLeg", parent = self.LeftUpLeg, infoNode_ = attrToPy("%s.LeftLeg" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.LeftFoot = DJB_CharacterNode("LeftFoot", parent = self.LeftLeg, infoNode_ = attrToPy("%s.LeftFoot" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.LeftToeBase = DJB_CharacterNode("LeftToeBase", parent = self.LeftFoot, infoNode_ = attrToPy("%s.LeftToeBase" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.LeftToe_End = DJB_CharacterNode("LeftToe_End", parent = self.LeftToeBase, infoNode_ = attrToPy("%s.LeftToe_End" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.RightUpLeg = DJB_CharacterNode("RightUpLeg", parent = self.Hips, infoNode_ = attrToPy("%s.RightUpLeg" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.RightLeg = DJB_CharacterNode("RightLeg", parent = self.RightUpLeg, infoNode_ = attrToPy("%s.RightLeg" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.RightFoot = DJB_CharacterNode("RightFoot", parent = self.RightLeg, infoNode_ = attrToPy("%s.RightFoot" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.RightToeBase = DJB_CharacterNode("RightToeBase", parent = self.RightFoot, infoNode_ = attrToPy("%s.RightToeBase" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.RightToe_End = DJB_CharacterNode("RightToe_End", parent = self.RightToeBase, infoNode_ = attrToPy("%s.RightToe_End" % (self.infoNode)), nameSpace_ = self.characterNameSpace)

            ##############################################
            self.proportions = attrToPy("%s.proportions" % (self.infoNode))
            self.defaultControlScale = attrToPy("%s.defaultControlScale" % (self.infoNode))
            self.Character_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Character_GRP" % (self.infoNode)))
            self.global_CTRL = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.global_CTRL" % (self.infoNode)))
            self.CTRL_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.CTRL_GRP" % (self.infoNode)))
            self.Joint_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Joint_GRP" % (self.infoNode)))
            self.AnimData_Joint_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.AnimData_Joint_GRP" % (self.infoNode)))
            self.Bind_Joint_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Bind_Joint_GRP" % (self.infoNode)))
            self.Mesh_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Mesh_GRP" % (self.infoNode)))
            self.Misc_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Misc_GRP" % (self.infoNode)))
            self.LeftArm_Switch_Reverse = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Misc_GRP" % (self.infoNode)))
            self.RightArm_Switch_Reverse = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.RightArm_Switch_Reverse" % (self.infoNode)))
            self.LeftLeg_Switch_Reverse = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.LeftLeg_Switch_Reverse" % (self.infoNode)))
            self.RightLeg_Switch_Reverse = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.RightLeg_Switch_Reverse" % (self.infoNode)))
            self.Bind_Joint_SelectSet = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Bind_Joint_SelectSet" % (self.infoNode)))
            self.AnimData_Joint_SelectSet = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.AnimData_Joint_SelectSet" % (self.infoNode)))
            self.Controls_SelectSet = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Controls_SelectSet" % (self.infoNode)))
            self.Geo_SelectSet = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Geo_SelectSet" % (self.infoNode)))
            self.Left_Toe_IK_AnimData_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Left_Toe_IK_AnimData_GRP" % (self.infoNode)))
            self.Left_Toe_IK_CTRL = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Left_Toe_IK_CTRL" % (self.infoNode)))
            self.Left_ToeBase_IK_AnimData_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Left_ToeBase_IK_AnimData_GRP" % (self.infoNode)))
            self.Left_IK_ToeBase_animData_MultNode = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Left_IK_ToeBase_animData_MultNode" % (self.infoNode)))
            self.Left_ToeBase_IK_CTRL = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Left_ToeBase_IK_CTRL" % (self.infoNode)))
            self.Left_Ankle_IK_AnimData_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Left_Ankle_IK_AnimData_GRP" % (self.infoNode)))
            self.Left_Ankle_IK_CTRL = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Left_Ankle_IK_CTRL" % (self.infoNode)))
            self.Left_ToeBase_IkHandle = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Left_ToeBase_IkHandle" % (self.infoNode)))
            self.Left_ToeEnd_IkHandle = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Left_ToeEnd_IkHandle" % (self.infoNode)))
            self.Right_Toe_IK_AnimData_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Right_Toe_IK_AnimData_GRP" % (self.infoNode)))
            self.Right_Toe_IK_CTRL = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Right_Toe_IK_CTRL" % (self.infoNode)))
            self.Right_ToeBase_IK_AnimData_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Right_ToeBase_IK_AnimData_GRP" % (self.infoNode)))
            self.Right_IK_ToeBase_animData_MultNode = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Right_IK_ToeBase_animData_MultNode" % (self.infoNode)))
            self.Right_ToeBase_IK_CTRL = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Right_ToeBase_IK_CTRL" % (self.infoNode)))
            self.Right_Ankle_IK_AnimData_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Right_Ankle_IK_AnimData_GRP" % (self.infoNode)))
            self.Right_Ankle_IK_CTRL = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Right_Ankle_IK_AnimData_GRP" % (self.infoNode)))
            self.Right_ToeBase_IkHandle = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Right_ToeBase_IkHandle" % (self.infoNode)))
            self.Right_ToeEnd_IkHandle = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Right_ToeEnd_IkHandle" % (self.infoNode)))
            self.LeftHand_CTRLs_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.LeftHand_CTRLs_GRP" % (self.infoNode)))
            self.RightHand_CTRLs_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.RightHand_CTRLs_GRP" % (self.infoNode)))
            self.LeftFoot_FootRoll_MultNode = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.LeftFoot_FootRoll_MultNode" % (self.infoNode)))
            self.LeftFoot_ToeRoll_MultNode = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.LeftFoot_ToeRoll_MultNode" % (self.infoNode)))
            self.RightFoot_FootRoll_MultNode = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.RightFoot_FootRoll_MultNode" % (self.infoNode)))
            self.RightFoot_ToeRoll_MultNode = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.RightFoot_ToeRoll_MultNode" % (self.infoNode)))
            self.RightFoot_HipPivot_MultNode = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.RightFoot_HipPivot_MultNode" % (self.infoNode)))
            self.RightFoot_BallPivot_MultNode = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.RightFoot_BallPivot_MultNode" % (self.infoNode)))
            self.RightFoot_ToePivot_MultNode = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.RightFoot_ToePivot_MultNode" % (self.infoNode)))
            self.RightFoot_HipSideToSide_MultNode = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.RightFoot_HipSideToSide_MultNode" % (self.infoNode)))
            self.RightFoot_ToeRotate_MultNode = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.RightFoot_ToeRotate_MultNode" % (self.infoNode)))
            self.IK_Dummy_Joint_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.IK_Dummy_Joint_GRP" % (self.infoNode)))
            self.LeftHand_grandparent_Constraint = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.LeftHand_grandparent_Constraint" % (self.infoNode)))
            self.LeftHand_grandparent_Constraint_Reverse = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.LeftHand_grandparent_Constraint_Reverse" % (self.infoNode)))
            self.RightHand_grandparent_Constraint = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.RightHand_grandparent_Constraint" % (self.infoNode)))
            self.RightHand_grandparent_Constraint_Reverse = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.RightHand_grandparent_Constraint_Reverse" % (self.infoNode)))
            self.LeftForeArm_grandparent_Constraint = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.LeftForeArm_grandparent_Constraint" % (self.infoNode)))
            self.LeftForeArm_grandparent_Constraint_Reverse = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.LeftForeArm_grandparent_Constraint_Reverse" % (self.infoNode)))
            self.RightForeArm_grandparent_Constraint = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.RightForeArm_grandparent_Constraint" % (self.infoNode)))
            self.RightForeArm_grandparent_Constraint_Reverse = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.RightForeArm_grandparent_Constraint_Reverse" % (self.infoNode)))
            self.exportList = attrToPy("%s.exportList" % (self.infoNode))
            
            if attrToPy("%s.origAnim" % (self.infoNode)):
                if mayac.objExists(DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.origAnim" % (self.infoNode)))):
                    self.origAnim = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.origAnim" % (self.infoNode)))
                    self.origAnimation_Layer = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.origAnimation_Layer" % (self.infoNode)))
                else:
                    self.origAnim = attrToPy("%s.origAnim" % (self.infoNode))
                    self.origAnimation_Layer = attrToPy("%s.origAnimation_Layer" % (self.infoNode))
            self.Mesh_Layer = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Mesh_Layer" % (self.infoNode)))
            #self.Control_Layer = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Control_Layer" % (self.infoNode)))
            self.Bind_Joint_Layer = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Bind_Joint_Layer" % (self.infoNode)))
            self.fingerFlip = attrToPy("%s.fingerFlip" % (self.infoNode))
            self.LeftEye = DJB_CharacterNode("LeftEye", optional_ = 1, parent = self.Head, infoNode_ = attrToPy("%s.LeftEye" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.RightEye = DJB_CharacterNode("RightEye", optional_ = 1, parent = self.Head, infoNode_ = attrToPy("%s.RightEye" % (self.infoNode)), nameSpace_ = self.characterNameSpace)
            self.FacialControl_Layer = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.FacialControl_Layer" % (self.infoNode)))
            self.FacialControl_Mover = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.FacialControl_Mover" % (self.infoNode)))
            
            
            
            
        
        
           
        self.bodyParts = []
        for bodyPart in (self.Root, self.Hips, self.Spine, self.Spine1, self.Spine2, self.Spine3, self.Neck, self.Neck1, self.Head, self.HeadTop_End, self.LeftShoulder, 
                              self.LeftArm, self.LeftForeArm, self.LeftHand, self.LeftHandThumb1, self.LeftHandThumb2, self.LeftHandThumb3, 
                              self.LeftHandThumb4, self.LeftHandIndex1, self.LeftHandIndex2, self.LeftHandIndex3, self.LeftHandIndex4,
                              self.LeftHandMiddle1, self.LeftHandMiddle2, self.LeftHandMiddle3, self.LeftHandMiddle4, self.LeftHandRing1,
                              self.LeftHandRing2, self.LeftHandRing3, self.LeftHandRing4, self.LeftHandPinky1, self.LeftHandPinky2, 
                              self.LeftHandPinky3, self.LeftHandPinky4, self.RightShoulder, self.RightArm, self.RightForeArm, 
                              self.RightHand, self.RightHandThumb1, self.RightHandThumb2, self.RightHandThumb3, 
                              self.RightHandThumb4, self.RightHandIndex1, self.RightHandIndex2, self.RightHandIndex3, self.RightHandIndex4,
                              self.RightHandMiddle1, self.RightHandMiddle2, self.RightHandMiddle3, self.RightHandMiddle4, self.RightHandRing1,
                              self.RightHandRing2, self.RightHandRing3, self.RightHandRing4, self.RightHandPinky1, self.RightHandPinky2, 
                              self.RightHandPinky3, self.RightHandPinky4, self.LeftUpLeg, self.LeftLeg, self.LeftFoot, self.LeftToeBase,
                              self.LeftToe_End, self.RightUpLeg, self.RightLeg, self.RightFoot, self.RightToeBase, self.RightToe_End,
                              self.LeftEye, self.RightEye):
            if bodyPart and bodyPart.Bind_Joint:
                self.bodyParts.append(bodyPart)
                
        #Dynamics
        if self.infoNode:
            self.Dyn_CTRL = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Dyn_CTRL" % (self.infoNode)))
            self.numExtraJointChains = attrToPy("%s.numExtraJointChains" % (self.infoNode))
            self.ExtraJoints = []
            extraJointInfoNodes = attrToPy("%s.ExtraJoints" % (self.infoNode))
            if extraJointInfoNodes:
                for extraJointInfoNode in extraJointInfoNodes:
                    extraJointInfoNode = DJB_addNameSpace(self.characterNameSpace, extraJointInfoNode)
                    extraJointName = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.nodeName" % (extraJointInfoNode)))
                    if not extraJointName:
                        extraJointName = attrToPy("%s.Bind_Joint" % (extraJointInfoNode))[5:]
                    nodesParent = None
                    parentShouldBe = attrToPy("%s.parent" % (extraJointInfoNode))
                    if not parentShouldBe:
                        parentShouldBe = mayac.listRelatives(DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Bind_Joint" % (extraJointInfoNode))), parent = True)[0]
                        parentShouldBe = DJB_findAfterSeperator(parentShouldBe, ":")[5:]
                    for bodyPart in self.bodyParts:
                        if bodyPart.nodeName == parentShouldBe:
                            nodesParent = bodyPart
                    if not nodesParent:
                        for bodyPart in self.ExtraJoints:
                            if bodyPart.nodeName == parentShouldBe:
                                nodesParent = bodyPart
                    if not nodesParent:
                        for bodyPart in self.ExtraJoints:
                            parentShouldBeNamespaced = DJB_addNameSpace(self.characterNameSpace, parentShouldBe)
                            if bodyPart.nodeName == parentShouldBeNamespaced:
                                nodesParent = bodyPart
                    extraJointInfoNode = DJB_findAfterSeperator(extraJointInfoNode, ":")
                    self.ExtraJoints.append(DJB_CharacterNode(extraJointName, parent = nodesParent, infoNode_ = extraJointInfoNode, nameSpace_ = self.characterNameSpace))
            else:
                self.ExtraJoints = None  
        
        
        #Create controls, etc
        if not self.infoNode:
            self.fixArmsAndLegs()
            self.makeAnimDataJoints()
            self.makeControls()
            self.hookUpControls()
            self.writeInfoNode()
            
        mayac.select(clear = True)
        

    
    def fixArmsAndLegs(self):
        LAnklePosStart = mayac.xform(self.LeftFoot.Bind_Joint, query = True, worldSpace = True, absolute = True, translation = True)
        RAnklePosStart = mayac.xform(self.RightFoot.Bind_Joint, query = True, worldSpace = True, absolute = True, translation = True)
        
        if self.rigType == "World":
            value = -1
            while not DJB_CheckAngle(self.LeftUpLeg.Bind_Joint, self.LeftLeg.Bind_Joint, self.LeftFoot.Bind_Joint, axis = "x", multiplier = -1):
                mayac.rotate(value, 0, 0, self.LeftUpLeg.Bind_Joint, relative = True)
                mayac.rotate(value*-1, 0, 0, self.LeftLeg.Bind_Joint, relative = True)
                mayac.refresh()
            mayac.rotate(-45, 0, 0, self.LeftUpLeg.Bind_Joint, relative = True)
            mayac.rotate(90, 0, 0, self.LeftLeg.Bind_Joint, relative = True)
            mayac.joint(self.LeftUpLeg.Bind_Joint, edit = True, setPreferredAngles=True, children=True)
            mayac.rotate(45, 0, 0, self.LeftUpLeg.Bind_Joint, relative = True)
            mayac.rotate(-90, 0, 0, self.LeftLeg.Bind_Joint, relative = True)
              
            value = -1
            while not DJB_CheckAngle(self.RightUpLeg.Bind_Joint, self.RightLeg.Bind_Joint, self.RightFoot.Bind_Joint, axis = "x", multiplier = -1):
                mayac.rotate(value, 0, 0, self.RightUpLeg.Bind_Joint, relative = True)
                mayac.rotate(value*-1, 0, 0, self.RightLeg.Bind_Joint, relative = True)
                mayac.refresh()
            mayac.rotate(-45, 0, 0, self.RightUpLeg.Bind_Joint, relative = True)
            mayac.rotate(90, 0, 0, self.RightLeg.Bind_Joint, relative = True)
            mayac.joint( self.RightUpLeg.Bind_Joint, edit = True, setPreferredAngles=True, children=True)
            mayac.rotate(45, 0, 0, self.RightUpLeg.Bind_Joint, relative = True)
            mayac.rotate(-90, 0, 0, self.RightLeg.Bind_Joint, relative = True)
            
            value = -1
            while not DJB_CheckAngle(self.LeftArm.Bind_Joint, self.LeftForeArm.Bind_Joint, self.LeftHand.Bind_Joint, axis = "y", multiplier = 1):
                mayac.rotate(0, value, 0, self.LeftForeArm.Bind_Joint, relative = True)
                mayac.refresh()
            tempRotData = mayac.getAttr("%s.rotate" %(self.LeftArm.Bind_Joint))
            mayac.rotate(0, 0, 0, self.LeftArm.Bind_Joint, absolute = True)
            mayac.rotate(0, -90, 0, self.LeftForeArm.Bind_Joint, relative = True)
            mayac.joint( self.LeftArm.Bind_Joint, edit = True, setPreferredAngles=True, children=True)
            mayac.setAttr("%s.rotate" %(self.LeftArm.Bind_Joint), tempRotData[0][0], tempRotData[0][1], tempRotData[0][2], type = "double3")
            mayac.rotate(0, 90, 0, self.LeftForeArm.Bind_Joint, relative = True)
                
            value = 1
            while not DJB_CheckAngle(self.RightArm.Bind_Joint, self.RightForeArm.Bind_Joint, self.RightHand.Bind_Joint, axis = "y", multiplier = -1):
                mayac.rotate(0, value, 0, self.RightForeArm.Bind_Joint, relative = True)
                mayac.refresh()
            tempRotData = mayac.getAttr("%s.rotate" %(self.RightArm.Bind_Joint))
            mayac.rotate(0, 0, 0, self.RightArm.Bind_Joint, absolute = True)
            mayac.rotate(0, 90, 0, self.RightForeArm.Bind_Joint, relative = True)
            mayac.joint( self.RightArm.Bind_Joint, edit = True, setPreferredAngles=True, children=True)
            mayac.setAttr("%s.rotate" %(self.RightArm.Bind_Joint), tempRotData[0][0], tempRotData[0][1], tempRotData[0][2], type = "double3")
            mayac.rotate(0, -90, 0, self.RightForeArm.Bind_Joint, relative = True)
        
        elif self.rigType =="AutoRig":
            value = 1
            while not DJB_CheckAngle(self.LeftUpLeg.Bind_Joint, self.LeftLeg.Bind_Joint, self.LeftFoot.Bind_Joint, axis = "x", multiplier = 1):
                mayac.rotate(value, 0, 0, self.LeftUpLeg.Bind_Joint, relative = True)
                mayac.rotate(value*-1, 0, 0, self.LeftLeg.Bind_Joint, relative = True)
                mayac.refresh()
            mayac.rotate(45, 0, 0, self.LeftUpLeg.Bind_Joint, relative = True)
            mayac.rotate(-90, 0, 0, self.LeftLeg.Bind_Joint, relative = True)
            mayac.joint(self.LeftUpLeg.Bind_Joint, edit = True, setPreferredAngles=True, children=True)
            mayac.rotate(-45, 0, 0, self.LeftUpLeg.Bind_Joint, relative = True)
            mayac.rotate(90, 0, 0, self.LeftLeg.Bind_Joint, relative = True)
              
            value = 1
            while not DJB_CheckAngle(self.RightUpLeg.Bind_Joint, self.RightLeg.Bind_Joint, self.RightFoot.Bind_Joint, axis = "x", multiplier = 1):
                mayac.rotate(value, 0, 0, self.RightUpLeg.Bind_Joint, relative = True)
                mayac.rotate(value*-1, 0, 0, self.RightLeg.Bind_Joint, relative = True)
                mayac.refresh()
            mayac.rotate(45, 0, 0, self.RightUpLeg.Bind_Joint, relative = True)
            mayac.rotate(-90, 0, 0, self.RightLeg.Bind_Joint, relative = True)
            mayac.joint( self.RightUpLeg.Bind_Joint, edit = True, setPreferredAngles=True, children=True)
            mayac.rotate(-45, 0, 0, self.RightUpLeg.Bind_Joint, relative = True)
            mayac.rotate(90, 0, 0, self.RightLeg.Bind_Joint, relative = True)
            
            value = 1
            while not DJB_CheckAngle(self.LeftArm.Bind_Joint, self.LeftForeArm.Bind_Joint, self.LeftHand.Bind_Joint, axis = "z", multiplier = -1):
                mayac.rotate(0, 0, value, self.LeftForeArm.Bind_Joint, relative = True)
                mayac.refresh()
            tempRotData = mayac.getAttr("%s.rotate" %(self.LeftArm.Bind_Joint))
            mayac.rotate(0, 0, 0, self.LeftArm.Bind_Joint, absolute = True)
            mayac.rotate(0, 0, 90, self.LeftForeArm.Bind_Joint, relative = True)
            mayac.joint( self.LeftArm.Bind_Joint, edit = True, setPreferredAngles=True, children=True)
            mayac.setAttr("%s.rotate" %(self.LeftArm.Bind_Joint), tempRotData[0][0], tempRotData[0][1], tempRotData[0][2], type = "double3")
            mayac.rotate(0, 0, -90, self.LeftForeArm.Bind_Joint, relative = True)
                
            value = -1
            while not DJB_CheckAngle(self.RightArm.Bind_Joint, self.RightForeArm.Bind_Joint, self.RightHand.Bind_Joint, axis = "z", multiplier = 1):
                mayac.rotate(0, 0, value, self.RightForeArm.Bind_Joint, relative = True)
                mayac.refresh()
            tempRotData = mayac.getAttr("%s.rotate" %(self.RightArm.Bind_Joint))
            mayac.rotate(0, 0, 0, self.RightArm.Bind_Joint, absolute = True)
            mayac.rotate(0, 0, -90, self.RightForeArm.Bind_Joint, relative = True)
            mayac.joint( self.RightArm.Bind_Joint, edit = True, setPreferredAngles=True, children=True)
            mayac.setAttr("%s.rotate" %(self.RightArm.Bind_Joint), tempRotData[0][0], tempRotData[0][1], tempRotData[0][2], type = "double3")
            mayac.rotate(0, 0, 90, self.RightForeArm.Bind_Joint, relative = True)
        
        LAnklePosEnd = mayac.xform(self.LeftFoot.Bind_Joint, query = True, worldSpace = True, absolute = True, translation = True)
        RAnklePosEnd = mayac.xform(self.RightFoot.Bind_Joint, query = True, worldSpace = True, absolute = True, translation = True)
        AvgDiff = (LAnklePosStart[1]-LAnklePosEnd[1] + RAnklePosStart[1] - RAnklePosEnd[1]) / 2
        
        if self.hulaOption:
            mayac.move(0,AvgDiff,0, self.Root.Bind_Joint, relative = True)
        else:
            mayac.move(0,AvgDiff,0, self.Hips.Bind_Joint, relative = True)
        
        
        
    def makeAnimDataJoints(self):
        for bodyPart in self.bodyParts:
            bodyPart.duplicateJoint("AnimData")
        mayac.select(clear = True)
        
        #IK dummy joints
        if self.Root.Bind_Joint:
            self.Root.duplicateJoint("IK_Dummy")
        self.Hips.duplicateJoint("IK_Dummy")
        self.Spine.duplicateJoint("IK_Dummy")
        self.Spine1.duplicateJoint("IK_Dummy")
        self.Spine2.duplicateJoint("IK_Dummy")
        if self.Spine3 and self.Spine3.Bind_Joint:
            self.Spine3.duplicateJoint("IK_Dummy")
        self.LeftShoulder.duplicateJoint("IK_Dummy")
        self.RightShoulder.duplicateJoint("IK_Dummy")
            
    def makeControls(self, estimateSize = True):
    
        if len(self.mesh):
            bbox = self.BoundingBox
            
            self.proportions["highPoint"] = bbox[4]
            self.proportions["lowPoint"] = bbox[1]
            self.proportions["height"] = bbox[4]-bbox[1]
            self.proportions["front"] = bbox[5]
            self.proportions["back"] = bbox[2]
            self.proportions["depth"] = bbox[5]-bbox[2]
            self.proportions["depthMidpoint"] = ((bbox[5]-bbox[2])/2) + bbox[2]
            self.proportions["left"] = bbox[0]
            self.proportions["right"] = bbox[3]
            self.proportions["width"] = bbox[3]-bbox[0]
            self.proportions["widthMidpoint"] = ((bbox[3]-bbox[0])/2) + bbox[0]
            
        #global   
        temp = mayac.circle(
                        radius = (self.proportions["width"]+self.proportions["depth"])*.35,
                        constructionHistory = False,
                        name = "global_CTRL")
        self.global_CTRL = temp[0]
        mayac.move(self.proportions["widthMidpoint"], self.proportions["lowPoint"], self.proportions["depthMidpoint"], absolute = True, worldSpace = True)
        mayac.rotate(90,0,0, self.global_CTRL)
        DJB_cleanGEO(self.global_CTRL)
        DJB_ChangeDisplayColor(self.global_CTRL)
        
        
        
        if self.rigType == "AutoRig":  
            #root
            if self.Root.Bind_Joint:
                self.Root.createControl(type = "normal", 
                                    style = "circle", 
                                    scale = (self.proportions["depth"]*0.8, self.proportions["depth"]*0.8, self.proportions["depth"]*0.8), 
                                    offset = (0,0,0), 
                                    estimateSize = estimateSize)
            
                #hips
                self.Hips.createControl(type = "normal", 
                                        style = "hula", 
                                        scale = (self.proportions["depth"]*0.75, self.proportions["depth"]*0.75, self.proportions["depth"]*0.75),
                                        offset = (0,-.01*self.proportions["height"],0), 
                                        estimateSize = estimateSize,
                                        color_ = "yellow")
            else:
                #hips
                self.Hips.createControl(type = "normal", 
                                    style = "circle", 
                                    scale = (self.proportions["depth"]*0.8, self.proportions["depth"]*0.8, self.proportions["depth"]*0.8), 
                                    offset = (0,0,0), 
                                    estimateSize = estimateSize)
            #spine
            self.Spine.createControl(type = "normal", 
                                    style = "circle", 
                                    scale = (self.proportions["depth"]*0.7, self.proportions["depth"]*0.7, self.proportions["depth"]*0.7),
                                    offset = (0,0,self.proportions["depth"]*0.1), 
                                    estimateSize = estimateSize,
                                    color_ = "yellow")
            
            #spine1
            if self.Spine2.Bind_Joint:
                self.Spine1.createControl(type = "normal", 
                                        style = "circle", 
                                        scale = (self.proportions["depth"]*0.6, self.proportions["depth"]*0.6, self.proportions["depth"]*0.6),
                                        offset = (0,0,self.proportions["depth"]*0.15), 
                                        estimateSize = estimateSize,
                                        color_ = "yellow")
                #spine2
                if self.Spine3.Bind_Joint:
                    self.Spine2.createControl(type = "normal", 
                                        style = "circle", 
                                        scale = (self.proportions["depth"]*0.6, self.proportions["depth"]*0.6, self.proportions["depth"]*0.6),
                                        offset = (0,0,self.proportions["depth"]*0.15), 
                                        estimateSize = estimateSize,
                                        color_ = "yellow")
                    self.Spine3.createControl(type = "normal", 
                                        style = "box", 
                                        scale = (self.proportions["depth"]*0.7, self.proportions["depth"]*0.7, (self.proportions["depth"])*0.8), 
                                        offset = (0,self.proportions["depth"]*.2,self.proportions["depth"]*0.1), 
                                        estimateSize = estimateSize,
                                        color_ = "yellow")
                else:
                    self.Spine2.createControl(type = "normal", 
                                        style = "box", 
                                        scale = (self.proportions["depth"]*0.7, self.proportions["depth"]*0.7, (self.proportions["depth"])*0.8), 
                                        offset = (0,self.proportions["depth"]*.2,self.proportions["depth"]*0.1), 
                                        estimateSize = estimateSize,
                                        color_ = "yellow")
            else:
                self.Spine1.createControl(type = "normal", 
                                        style = "box", 
                                        scale = (self.proportions["depth"]*0.7, self.proportions["depth"]*0.7, (self.proportions["depth"])*0.8), 
                                        offset = (0,self.proportions["depth"]*.2,self.proportions["depth"]*0.1), 
                                        estimateSize = estimateSize,
                                        color_ = "yellow")
                                    
            #neck
            self.Neck.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*-0.18, self.proportions["depth"]*0.18, self.proportions["depth"]*0.18),
                                    offset = (self.proportions["height"]*0.033, 0, self.proportions["height"]*-0.04),  
                                    estimateSize = estimateSize,
                                    color_ = "yellow")
            if self.Neck1.Bind_Joint:
                self.Neck1.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*-0.18, self.proportions["depth"]*0.18, self.proportions["depth"]*0.18),
                                    offset = (self.proportions["height"]*0.033, 0, self.proportions["height"]*-0.04),  
                                    estimateSize = estimateSize,
                                    color_ = "yellow")
                                    
            #head
            self.Head.createControl(type = "normal", 
                                    style = "box", 
                                    scale = (self.proportions["depth"]*0.4, self.proportions["height"]*0.13, (self.proportions["depth"])*0.5), 
                                    offset = (0,self.proportions["height"]*.08,self.proportions["depth"]*0.1), 
                                    estimateSize = estimateSize,
                                    color_ = "yellow")
                              
            #LeftShoulder
            self.LeftShoulder.createControl(type = "normal", 
                                    style = "circleWrapped", 
                                    scale = (self.proportions["depth"]*0.4, self.proportions["depth"]*0.15, self.proportions["depth"]*0.15), 
                                    offset = (0,self.proportions["depth"]*0.3,self.proportions["height"]*-0.04),  
                                    estimateSize = estimateSize,
                                    color_ = "blue1")
                                    
            #RightShoulder
            self.RightShoulder.createControl(type = "normal", 
                                    style = "circleWrapped", 
                                    scale = (self.proportions["depth"]*0.4, self.proportions["depth"]*0.15, self.proportions["depth"]*0.15), 
                                    offset = (0,self.proportions["depth"]*0.3,self.proportions["height"]*-0.04),  
                                    estimateSize = estimateSize,
                                    color_ = "red1")
            
            #LeftArm
            self.LeftArm.createControl(type = "FK", 
                                    style = "circle", 
                                    scale = (self.proportions["depth"]*0.25, self.proportions["depth"]*0.25, self.proportions["depth"]*0.25),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "blue1")
            
            #RightArm
            self.RightArm.createControl(type = "FK", 
                                    style = "circle", 
                                    scale = (self.proportions["depth"]*0.25, self.proportions["depth"]*0.25, self.proportions["depth"]*0.25),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "red1")
            
            #LeftForeArm
            self.LeftForeArm.createControl(type = "FK", 
                                    style = "circle", 
                                    scale = (self.proportions["depth"]*0.25, self.proportions["depth"]*0.25, self.proportions["depth"]*0.25),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "blue1")
            
            self.LeftForeArm.createControl(type = "IK", 
                                    style = "PoleVector", 
                                    scale = (self.proportions["depth"]*0.1, self.proportions["depth"]*0.2, self.proportions["depth"]*0.1),
                                    offset = (0, 0, 0),
                                    rotate = (0, 90, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "blue2")
            
            #RightForeArm
            self.RightForeArm.createControl(type = "FK", 
                                    style = "circle", 
                                    scale = (self.proportions["depth"]*0.25, self.proportions["depth"]*0.25, self.proportions["depth"]*0.25),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "red1")
            
            self.RightForeArm.createControl(type = "IK", 
                                    style = "PoleVector", 
                                    scale = (self.proportions["depth"]*0.1, self.proportions["depth"]*0.2, self.proportions["depth"]*0.1),
                                    offset = (0, 0, 0),  
                                    rotate = (0, -90, 0),
                                    estimateSize = estimateSize,
                                    color_ = "red2")
            
            #LeftHand
            self.LeftHand.createControl(type = "FK", 
                                    style = "circle", 
                                    scale = (self.proportions["depth"]*0.2, self.proportions["depth"]*0.2, self.proportions["depth"]*0.2),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "blue1")
            
            self.LeftHand.createControl(type = "IK", 
                                    style = "box", 
                                    scale = (self.proportions["depth"]*0.2, self.proportions["depth"]*0.3, self.proportions["depth"]*0.2),
                                    offset = (0, self.proportions["depth"]*0.3, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "blue2")
            
            #RightHand
            self.RightHand.createControl(type = "FK", 
                                    style = "circle", 
                                    scale = (self.proportions["depth"]*0.2, self.proportions["depth"]*0.2, self.proportions["depth"]*0.2),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "red1")
            
            self.RightHand.createControl(type = "IK", 
                                    style = "box", 
                                    scale = (self.proportions["depth"]*0.2, self.proportions["depth"]*0.3, self.proportions["depth"]*0.2),
                                    offset = (0, self.proportions["depth"]*0.3, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "red2")
                                    
                                    
            #LeftUpLeg
            self.LeftUpLeg.createControl(type = "FK", 
                                    style = "pin", 
                                    scale = (self.proportions["depth"]*0.1, self.proportions["depth"]*0.1, self.proportions["depth"]*0.1),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "blue1")
                                    
            #LeftLeg
            self.LeftLeg.createControl(type = "FK", 
                                    style = "pin", 
                                    scale = (self.proportions["depth"]*0.09, self.proportions["depth"]*0.09, self.proportions["depth"]*0.09),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "blue1")
                                    
            self.LeftLeg.createControl(type = "IK", 
                                    style = "PoleVector", 
                                    scale = (self.proportions["depth"]*0.1, self.proportions["depth"]*0.2, self.proportions["depth"]*0.1),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "blue2")
            
            #LeftFoot
            self.LeftFoot.createControl(type = "FK", 
                                    style = "pin", 
                                    scale = (self.proportions["depth"]*0.08, self.proportions["depth"]*0.08, self.proportions["depth"]*0.08),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "blue1")
            
            self.LeftFoot.createControl(type = "IK", 
                                    style = "footBox", 
                                    scale = (self.proportions["depth"]*0.4, self.proportions["depth"]*0.7, self.proportions["depth"]*-0.4),
                                    offset = (0, self.proportions["depth"]*0.1, self.proportions["depth"]*0.1),
                                    rotate = (90, 0, 0),  
                                    partialConstraint = 1,
                                    estimateSize = estimateSize,
                                    color_ = "blue2")
            mayac.move(self.proportions["lowPoint"], "%s.scalePivot" % (self.LeftFoot.IK_CTRL),  "%s.rotatePivot" % (self.LeftFoot.IK_CTRL),  y = True)
    
            #LeftToeBase
            self.LeftToeBase.createControl(type = "FK", 
                                    style = "pin", 
                                    scale = (self.proportions["depth"]*0.07, self.proportions["depth"]*0.07, self.proportions["depth"]*0.07),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "blue1")
                                    
                                    
            #RightUpLeg
            self.RightUpLeg.createControl(type = "FK", 
                                    style = "pin", 
                                    scale = (self.proportions["depth"]*-0.1, self.proportions["depth"]*0.1, self.proportions["depth"]*0.1),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "red1")
                                    
            #RightLeg
            self.RightLeg.createControl(type = "FK", 
                                    style = "pin", 
                                    scale = (self.proportions["depth"]*-0.09, self.proportions["depth"]*0.09, self.proportions["depth"]*0.09),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "red1")
            
            self.RightLeg.createControl(type = "IK", 
                                    style = "PoleVector", 
                                    scale = (self.proportions["depth"]*0.1, self.proportions["depth"]*0.2, self.proportions["depth"]*0.1),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "red2")
                                    
            #RightFoot
            self.RightFoot.createControl(type = "FK", 
                                    style = "pin", 
                                    scale = (self.proportions["depth"]*-0.08, self.proportions["depth"]*0.08, self.proportions["depth"]*0.08),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "red1")
            
            self.RightFoot.createControl(type = "IK", 
                                    style = "footBox", 
                                    scale = (self.proportions["depth"]*0.4, self.proportions["depth"]*0.7, self.proportions["depth"]*-0.4),
                                    offset = (0, self.proportions["depth"]*0.1, self.proportions["depth"]*0.1),
                                    rotate = (90, 0, 0),
                                    partialConstraint = 1,  
                                    estimateSize = estimateSize,
                                    color_ = "red2")
            mayac.move(self.proportions["lowPoint"], "%s.scalePivot" % (self.RightFoot.IK_CTRL),  "%s.rotatePivot" % (self.RightFoot.IK_CTRL),  y = True)
    
            #RightToeBase
            self.RightToeBase.createControl(type = "FK", 
                                    style = "pin", 
                                    scale = (self.proportions["depth"]*-0.07, self.proportions["depth"]*0.07, self.proportions["depth"]*0.07),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "red1")
            
            #fingers
            if self.LeftHandThumb1.Bind_Joint:
                self.LeftHandThumb1.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.02, self.proportions["depth"]*0.02, self.proportions["depth"]*0.02),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "blue2")
                self.LeftHandThumb2.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.016, self.proportions["depth"]*0.016, self.proportions["depth"]*0.016),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "blue2")
                self.LeftHandThumb3.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.012, self.proportions["depth"]*0.012, self.proportions["depth"]*0.012),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "blue2")
            if self.LeftHandIndex1.Bind_Joint:
                self.LeftHandIndex1.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.02, self.proportions["depth"]*0.02, self.proportions["depth"]*0.02),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "blue2")
                self.LeftHandIndex2.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.016, self.proportions["depth"]*0.016, self.proportions["depth"]*0.016),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "blue2")
                self.LeftHandIndex3.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.012, self.proportions["depth"]*0.012, self.proportions["depth"]*0.012),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "blue2")
            if self.LeftHandMiddle1.Bind_Joint:
                self.LeftHandMiddle1.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.02, self.proportions["depth"]*0.02, self.proportions["depth"]*0.02),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "blue2")
                self.LeftHandMiddle2.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.016, self.proportions["depth"]*0.016, self.proportions["depth"]*0.016),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "blue2")
                self.LeftHandMiddle3.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.012, self.proportions["depth"]*0.012, self.proportions["depth"]*0.012),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "blue2")
            if self.LeftHandRing1.Bind_Joint:
                self.LeftHandRing1.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.02, self.proportions["depth"]*0.02, self.proportions["depth"]*0.02),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "blue2")
                self.LeftHandRing2.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.016, self.proportions["depth"]*0.016, self.proportions["depth"]*0.016),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "blue2")
                self.LeftHandRing3.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.012, self.proportions["depth"]*0.012, self.proportions["depth"]*0.012),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "blue2")
            if self.LeftHandPinky1.Bind_Joint:
                self.LeftHandPinky1.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.02, self.proportions["depth"]*0.02, self.proportions["depth"]*0.02),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "blue2")
                self.LeftHandPinky2.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.016, self.proportions["depth"]*0.016, self.proportions["depth"]*0.016),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "blue2")
                self.LeftHandPinky3.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.012, self.proportions["depth"]*0.012, self.proportions["depth"]*0.012),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "blue2")
                
            if self.RightHandThumb1.Bind_Joint:
                self.RightHandThumb1.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.02, self.proportions["depth"]*0.02, self.proportions["depth"]*0.02),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "red2")
                self.RightHandThumb2.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.016, self.proportions["depth"]*0.016, self.proportions["depth"]*0.016),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "red2")
                self.RightHandThumb3.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.012, self.proportions["depth"]*0.012, self.proportions["depth"]*0.012),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "red2")
            if self.RightHandIndex1.Bind_Joint:
                self.RightHandIndex1.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.02, self.proportions["depth"]*0.02, self.proportions["depth"]*0.02),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "red2")
                self.RightHandIndex2.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.016, self.proportions["depth"]*0.016, self.proportions["depth"]*0.016),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "red2")
                self.RightHandIndex3.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.012, self.proportions["depth"]*0.012, self.proportions["depth"]*0.012),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "red2")
            if self.RightHandMiddle1.Bind_Joint:
                self.RightHandMiddle1.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.02, self.proportions["depth"]*0.02, self.proportions["depth"]*0.02),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "red2")
                self.RightHandMiddle2.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.016, self.proportions["depth"]*0.016, self.proportions["depth"]*0.016),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "red2")
                self.RightHandMiddle3.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.012, self.proportions["depth"]*0.012, self.proportions["depth"]*0.012),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "red2")
            if self.RightHandRing1.Bind_Joint:
                self.RightHandRing1.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.02, self.proportions["depth"]*0.02, self.proportions["depth"]*0.02),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "red2")
                self.RightHandRing2.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.016, self.proportions["depth"]*0.016, self.proportions["depth"]*0.016),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "red2")
                self.RightHandRing3.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.012, self.proportions["depth"]*0.012, self.proportions["depth"]*0.012),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "red2")
            if self.RightHandPinky1.Bind_Joint:
                self.RightHandPinky1.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.02, self.proportions["depth"]*0.02, self.proportions["depth"]*0.02),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "red2")
                self.RightHandPinky2.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.016, self.proportions["depth"]*0.016, self.proportions["depth"]*0.016),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "red2")
                self.RightHandPinky3.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.012, self.proportions["depth"]*0.012, self.proportions["depth"]*0.012),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    flipFingers = self.fingerFlip,
                                    color_ = "red2")
                
            #Options
            self.LeftFoot.createControl(type = "options", 
                                    style = "options", 
                                    scale = (self.proportions["depth"]*0.12, self.proportions["depth"]*0.12, self.proportions["depth"]*-0.12),
                                    offset = (0, 0, self.proportions["depth"]*-0.4),  
                                    estimateSize = estimateSize,
                                    partialConstraint = 2,
                                    color_ = "black")
            
            self.RightFoot.createControl(type = "options", 
                                    style = "options", 
                                    scale = (self.proportions["depth"]*0.12, self.proportions["depth"]*0.12, self.proportions["depth"]*-0.12),
                                    offset = (0, 0, self.proportions["depth"]*-0.4),  
                                    estimateSize = estimateSize,
                                    partialConstraint = 2,
                                    color_ = "black")
            
            self.LeftHand.createControl(type = "options", 
                                    style = "options", 
                                    scale = (self.proportions["depth"]*0.12, self.proportions["depth"]*0.12, self.proportions["depth"]*-0.12),
                                    offset = (0, self.proportions["depth"]*0.3, self.proportions["depth"]*-0.3),  
                                    estimateSize = estimateSize,
                                    color_ = "black")
            
            self.RightHand.createControl(type = "options", 
                                    style = "options", 
                                    scale = (self.proportions["depth"]*0.12, self.proportions["depth"]*0.12, self.proportions["depth"]*-0.12),
                                    offset = (0, self.proportions["depth"]*0.3, self.proportions["depth"]*-0.3),  
                                    estimateSize = estimateSize,
                                    color_ = "black")
            if self.LeftEye.Bind_Joint and self.RightEye.Bind_Joint:
                self.LeftEye.createControl(type = "FK", 
                                        style = "sphere", 
                                        scale = (self.proportions["depth"]*0.075, self.proportions["depth"]*0.075, self.proportions["depth"]*0.075), 
                                        estimateSize = estimateSize,
                                        color_ = "white")
                self.RightEye.createControl(type = "FK", 
                                        style = "sphere", 
                                        scale = (self.proportions["depth"]*0.075, self.proportions["depth"]*0.075, self.proportions["depth"]*0.075), 
                                        estimateSize = estimateSize,
                                        color_ = "white")
        
        
        elif self.rigType == "World":     
            #root
            if self.Root.Bind_Joint:
                self.Root.createControl(type = "normal", 
                                    style = "circle", 
                                    scale = (self.proportions["depth"]*0.8, self.proportions["depth"]*0.8, self.proportions["depth"]*0.8), 
                                    offset = (0,0,0), 
                                    estimateSize = estimateSize)
            
                #hips
                self.Hips.createControl(type = "normal", 
                                        style = "hula", 
                                        scale = (self.proportions["depth"]*0.75, self.proportions["depth"]*0.75, self.proportions["depth"]*0.75),
                                        offset = (0,-.01*self.proportions["height"],0), 
                                        estimateSize = estimateSize,
                                        color_ = "yellow")
            else:
                #hips
                self.Hips.createControl(type = "normal", 
                                    style = "circle", 
                                    scale = (self.proportions["depth"]*0.8, self.proportions["depth"]*0.8, self.proportions["depth"]*0.8), 
                                    offset = (0,0,0), 
                                    estimateSize = estimateSize)
            #spine
            self.Spine.createControl(type = "normal", 
                                    style = "circle", 
                                    scale = (self.proportions["depth"]*0.7, self.proportions["depth"]*0.7, self.proportions["depth"]*0.7),
                                    offset = (0,0,0), 
                                    estimateSize = estimateSize,
                                    color_ = "yellow")
            
            #spine1
            self.Spine1.createControl(type = "normal", 
                                    style = "circle", 
                                    scale = (self.proportions["depth"]*0.6, self.proportions["depth"]*0.6, self.proportions["depth"]*0.6),
                                    offset = (0,0,0), 
                                    estimateSize = estimateSize,
                                    color_ = "yellow")
            #spine2
            if self.Spine3.Bind_Joint:
                self.Spine2.createControl(type = "normal", 
                                    style = "circle", 
                                    scale = (self.proportions["depth"]*0.6, self.proportions["depth"]*0.6, self.proportions["depth"]*0.6),
                                    offset = (0,0,0), 
                                    estimateSize = estimateSize,
                                    color_ = "yellow")
                self.Spine3.createControl(type = "normal", 
                                    style = "box", 
                                    scale = (self.proportions["depth"]*0.7, self.proportions["depth"]*0.7, (self.proportions["depth"])*0.8), 
                                    offset = (0,self.proportions["depth"]*.2,0), 
                                    estimateSize = estimateSize,
                                    color_ = "yellow")
            else:
                self.Spine2.createControl(type = "normal", 
                                    style = "box", 
                                    scale = (self.proportions["depth"]*0.7, self.proportions["depth"]*0.7, (self.proportions["depth"])*0.8), 
                                    offset = (0,self.proportions["depth"]*.2,0), 
                                    estimateSize = estimateSize,
                                    color_ = "yellow")
                                    
            #neck
            self.Neck.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*-0.18, self.proportions["depth"]*0.18, self.proportions["depth"]*0.18),
                                    offset = (self.proportions["height"]*0.033, 0, self.proportions["height"]*-0.04),  
                                    estimateSize = estimateSize,
                                    color_ = "yellow")
            if self.Neck1.Bind_Joint:
                self.Neck1.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*-0.18, self.proportions["depth"]*0.18, self.proportions["depth"]*0.18),
                                    offset = (self.proportions["height"]*0.033, 0, self.proportions["height"]*-0.04),  
                                    estimateSize = estimateSize,
                                    color_ = "yellow")
                                    
            #head
            self.Head.createControl(type = "normal", 
                                    style = "box", 
                                    scale = (self.proportions["depth"]*0.4, self.proportions["height"]*0.13, (self.proportions["depth"])*0.5), 
                                    offset = (0,self.proportions["height"]*.06,self.proportions["depth"]*0.1), 
                                    estimateSize = estimateSize,
                                    color_ = "yellow")
                               
            #LeftShoulder
            self.LeftShoulder.createControl(type = "normal", 
                                    style = "circleWrapped", 
                                    scale = (self.proportions["depth"]*0.4, self.proportions["depth"]*0.15, self.proportions["depth"]*0.15), 
                                    offset = (self.proportions["height"]*0.04, self.proportions["depth"]*0.3, 0), 
                                    rotate = (0, -90, 90), 
                                    estimateSize = estimateSize,
                                    color_ = "blue1")
                                    
            #RightShoulder
            self.RightShoulder.createControl(type = "normal", 
                                    style = "circleWrapped", 
                                    scale = (self.proportions["depth"]*0.4, self.proportions["depth"]*0.15, self.proportions["depth"]*0.15), 
                                    offset = (self.proportions["height"]*-0.04, self.proportions["depth"]*0.3, 0), 
                                    rotate = (0, -90, 90),  
                                    estimateSize = estimateSize,
                                    color_ = "red1")
            
            #LeftArm
            self.LeftArm.createControl(type = "FK", 
                                    style = "circle", 
                                    scale = (self.proportions["depth"]*0.25, self.proportions["depth"]*0.25, self.proportions["depth"]*0.25),
                                    offset = (0, 0, 0),
                                    rotate = (0, 90, 0), 
                                    rigType = "World",
                                    estimateSize = estimateSize,
                                    color_ = "blue1")
            
            #RightArm
            self.RightArm.createControl(type = "FK", 
                                    style = "circle", 
                                    scale = (self.proportions["depth"]*0.25, self.proportions["depth"]*0.25, self.proportions["depth"]*0.25),
                                    offset = (0, 0, 0),
                                    rotate = (0, 90, 0), 
                                    rigType = "World",
                                    estimateSize = estimateSize,
                                    color_ = "red1")
            
            #LeftForeArm
            self.LeftForeArm.createControl(type = "FK", 
                                    style = "circle", 
                                    scale = (self.proportions["depth"]*0.25, self.proportions["depth"]*0.25, self.proportions["depth"]*0.25),
                                    offset = (0, 0, 0),
                                    rotate = (0, 90, 0),  
                                    rigType = "World",
                                    estimateSize = estimateSize,
                                    color_ = "blue1")
            
            self.LeftForeArm.createControl(type = "IK", 
                                    style = "PoleVector", 
                                    scale = (self.proportions["depth"]*0.1, self.proportions["depth"]*0.2, self.proportions["depth"]*0.1),
                                    offset = (0, 0, 0),
                                    rotate = (0, 180, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "blue2")
            
            #RightForeArm
            self.RightForeArm.createControl(type = "FK", 
                                    style = "circle", 
                                    scale = (self.proportions["depth"]*0.25, self.proportions["depth"]*0.25, self.proportions["depth"]*0.25),
                                    offset = (0, 0, 0),
                                    rotate = (0, 90, 0), 
                                    rigType = "World", 
                                    estimateSize = estimateSize,
                                    color_ = "red1")
            
            self.RightForeArm.createControl(type = "IK", 
                                    style = "PoleVector", 
                                    scale = (self.proportions["depth"]*0.1, self.proportions["depth"]*0.2, self.proportions["depth"]*0.1),
                                    offset = (0, 0, 0),  
                                    rotate = (0, 180, 0),
                                    estimateSize = estimateSize,
                                    color_ = "red2")
            
            #LeftHand
            self.LeftHand.createControl(type = "FK", 
                                    style = "circle", 
                                    scale = (self.proportions["depth"]*0.2, self.proportions["depth"]*0.2, self.proportions["depth"]*0.2),
                                    offset = (0, 0, 0), 
                                    rotate = (0, 90, 0), 
                                    rigType = "World",
                                    estimateSize = estimateSize,
                                    color_ = "blue1")
            
            self.LeftHand.createControl(type = "IK", 
                                    style = "box", 
                                    scale = (self.proportions["depth"]*0.2, self.proportions["depth"]*0.3, self.proportions["depth"]*0.2),
                                    offset = (self.proportions["depth"]*0.3, 0, 0),  
                                    rotate = (0, -90, -90),
                                    estimateSize = estimateSize,
                                    color_ = "blue2")
            
            #RightHand
            self.RightHand.createControl(type = "FK", 
                                    style = "circle", 
                                    scale = (self.proportions["depth"]*0.2, self.proportions["depth"]*0.2, self.proportions["depth"]*0.2),
                                    offset = (0, 0, 0),
                                    rotate = (0, 90, 0),
                                    rigType = "World",
                                    estimateSize = estimateSize,
                                    color_ = "red1")
            
            self.RightHand.createControl(type = "IK", 
                                    style = "box", 
                                    scale = (self.proportions["depth"]*0.2, self.proportions["depth"]*0.3, self.proportions["depth"]*0.2),
                                    offset = (self.proportions["depth"]*-0.3, 0, 0), 
                                    rotate = (0, 90, 90), 
                                    estimateSize = estimateSize,
                                    color_ = "red2")
                                    
                                    
            #LeftUpLeg
            self.LeftUpLeg.createControl(type = "FK", 
                                    style = "pin", 
                                    scale = (self.proportions["depth"]*0.1, self.proportions["depth"]*0.1, self.proportions["depth"]*0.1),
                                    offset = (0, 0, 0),
                                    rotate = (0, 180, 0), 
                                    estimateSize = estimateSize,
                                    color_ = "blue1")
                                    
            #LeftLeg
            self.LeftLeg.createControl(type = "FK", 
                                    style = "pin", 
                                    scale = (self.proportions["depth"]*0.09, self.proportions["depth"]*0.09, self.proportions["depth"]*0.09),
                                    offset = (0, 0, 0),
                                    rotate = (0, 180, 0),
                                    estimateSize = estimateSize,
                                    color_ = "blue1")
                                    
            self.LeftLeg.createControl(type = "IK", 
                                    style = "PoleVector", 
                                    scale = (self.proportions["depth"]*0.1, self.proportions["depth"]*0.2, self.proportions["depth"]*0.1),
                                    offset = (0, 0, 0), 
                                    estimateSize = estimateSize,
                                    color_ = "blue2")
            
            #LeftFoot
            self.LeftFoot.createControl(type = "FK", 
                                    style = "pin", 
                                    scale = (self.proportions["depth"]*0.08, self.proportions["depth"]*0.08, self.proportions["depth"]*0.08),
                                    offset = (0, 0, 0),
                                    rotate = (0, 180, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "blue1")
            
            self.LeftFoot.createControl(type = "IK", 
                                    style = "footBox", 
                                    scale = (self.proportions["depth"]*0.4, self.proportions["depth"]*0.7, self.proportions["depth"]*-0.4),
                                    offset = (0, self.proportions["depth"]*0.1, self.proportions["depth"]*0.1),
                                    rotate = (90, 0, 0),  
                                    partialConstraint = 1,
                                    estimateSize = estimateSize,
                                    color_ = "blue2")
            mayac.move(self.proportions["lowPoint"], "%s.scalePivot" % (self.LeftFoot.IK_CTRL),  "%s.rotatePivot" % (self.LeftFoot.IK_CTRL),  y = True)
    
            #LeftToeBase
            self.LeftToeBase.createControl(type = "FK", 
                                    style = "pin", 
                                    scale = (self.proportions["depth"]*0.07, self.proportions["depth"]*0.07, self.proportions["depth"]*0.07),
                                    offset = (0, 0, 0),
                                    rotate = (0, 180, 0),   
                                    estimateSize = estimateSize,
                                    color_ = "blue1")
                                    
                                    
            #RightUpLeg
            self.RightUpLeg.createControl(type = "FK", 
                                    style = "pin", 
                                    scale = (self.proportions["depth"]*-0.1, self.proportions["depth"]*0.1, self.proportions["depth"]*0.1),
                                    offset = (0, 0, 0),
                                    rotate = (0, 180, 0), 
                                    estimateSize = estimateSize,
                                    color_ = "red1")
                                    
            #RightLeg
            self.RightLeg.createControl(type = "FK", 
                                    style = "pin", 
                                    scale = (self.proportions["depth"]*-0.09, self.proportions["depth"]*0.09, self.proportions["depth"]*0.09),
                                    offset = (0, 0, 0),
                                    rotate = (0, 180, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "red1")
            
            self.RightLeg.createControl(type = "IK", 
                                    style = "PoleVector", 
                                    scale = (self.proportions["depth"]*0.1, self.proportions["depth"]*0.2, self.proportions["depth"]*0.1),
                                    offset = (0, 0, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "red2")
                                    
            #RightFoot
            self.RightFoot.createControl(type = "FK", 
                                    style = "pin", 
                                    scale = (self.proportions["depth"]*-0.08, self.proportions["depth"]*0.08, self.proportions["depth"]*0.08),
                                    offset = (0, 0, 0),  
                                    rotate = (0, 180, 0), 
                                    estimateSize = estimateSize,
                                    color_ = "red1")
            
            self.RightFoot.createControl(type = "IK", 
                                    style = "footBox", 
                                    scale = (self.proportions["depth"]*0.4, self.proportions["depth"]*0.7, self.proportions["depth"]*-0.4),
                                    offset = (0, self.proportions["depth"]*0.1, self.proportions["depth"]*0.1),
                                    rotate = (90, 0, 0),
                                    partialConstraint = 1,  
                                    estimateSize = estimateSize,
                                    color_ = "red2")
            mayac.move(self.proportions["lowPoint"], "%s.scalePivot" % (self.RightFoot.IK_CTRL),  "%s.rotatePivot" % (self.RightFoot.IK_CTRL),  y = True)
    
            #RightToeBase
            self.RightToeBase.createControl(type = "FK", 
                                    style = "pin", 
                                    scale = (self.proportions["depth"]*-0.07, self.proportions["depth"]*0.07, self.proportions["depth"]*0.07),
                                    offset = (0, 0, 0),
                                    rotate = (0, 180, 0), 
                                    estimateSize = estimateSize,
                                    color_ = "red1")
            
            #fingers
            if self.LeftHandThumb1.Bind_Joint:
                self.LeftHandThumb1.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.02, self.proportions["depth"]*0.02, self.proportions["depth"]*0.02),
                                    offset = (0, 0, 0),
                                    rotate = (0, 90, 0), 
                                    estimateSize = estimateSize,
                                    color_ = "blue2")
                self.LeftHandThumb2.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.016, self.proportions["depth"]*0.016, self.proportions["depth"]*0.016),
                                    offset = (0, 0, 0),
                                    rotate = (0, 90, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "blue2")
                self.LeftHandThumb3.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.012, self.proportions["depth"]*0.012, self.proportions["depth"]*0.012),
                                    offset = (0, 0, 0),
                                    rotate = (0, 90, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "blue2")
            if self.LeftHandIndex1.Bind_Joint:
                self.LeftHandIndex1.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.02, self.proportions["depth"]*0.02, self.proportions["depth"]*0.02),
                                    offset = (0, 0, 0), 
                                    rotate = (0, 90, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "blue2")
                self.LeftHandIndex2.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.016, self.proportions["depth"]*0.016, self.proportions["depth"]*0.016),
                                    offset = (0, 0, 0),  
                                    rotate = (0, 90, 0), 
                                    estimateSize = estimateSize,
                                    color_ = "blue2")
                self.LeftHandIndex3.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.012, self.proportions["depth"]*0.012, self.proportions["depth"]*0.012),
                                    offset = (0, 0, 0),  
                                    rotate = (0, 90, 0), 
                                    estimateSize = estimateSize,
                                    color_ = "blue2")
            if self.LeftHandMiddle1.Bind_Joint:
                self.LeftHandMiddle1.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.02, self.proportions["depth"]*0.02, self.proportions["depth"]*0.02),
                                    offset = (0, 0, 0),  
                                    rotate = (0, 90, 0), 
                                    estimateSize = estimateSize,
                                    color_ = "blue2")
                self.LeftHandMiddle2.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.016, self.proportions["depth"]*0.016, self.proportions["depth"]*0.016),
                                    offset = (0, 0, 0),  
                                    rotate = (0, 90, 0), 
                                    estimateSize = estimateSize,
                                    color_ = "blue2")
                self.LeftHandMiddle3.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.012, self.proportions["depth"]*0.012, self.proportions["depth"]*0.012),
                                    offset = (0, 0, 0), 
                                    rotate = (0, 90, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "blue2")
            if self.LeftHandRing1.Bind_Joint:
                self.LeftHandRing1.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.02, self.proportions["depth"]*0.02, self.proportions["depth"]*0.02),
                                    offset = (0, 0, 0),  
                                    rotate = (0, 90, 0), 
                                    estimateSize = estimateSize,
                                    color_ = "blue2")
                self.LeftHandRing2.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.016, self.proportions["depth"]*0.016, self.proportions["depth"]*0.016),
                                    offset = (0, 0, 0),  
                                    rotate = (0, 90, 0), 
                                    estimateSize = estimateSize,
                                    color_ = "blue2")
                self.LeftHandRing3.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.012, self.proportions["depth"]*0.012, self.proportions["depth"]*0.012),
                                    offset = (0, 0, 0),  
                                    rotate = (0, 90, 0), 
                                    estimateSize = estimateSize,
                                    color_ = "blue2")
            if self.LeftHandPinky1.Bind_Joint:
                self.LeftHandPinky1.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.02, self.proportions["depth"]*0.02, self.proportions["depth"]*0.02),
                                    offset = (0, 0, 0), 
                                    rotate = (0, 90, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "blue2")
                self.LeftHandPinky2.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.016, self.proportions["depth"]*0.016, self.proportions["depth"]*0.016),
                                    offset = (0, 0, 0), 
                                    rotate = (0, 90, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "blue2")
                self.LeftHandPinky3.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.012, self.proportions["depth"]*0.012, self.proportions["depth"]*0.012),
                                    offset = (0, 0, 0),  
                                    rotate = (0, 90, 0), 
                                    estimateSize = estimateSize,
                                    color_ = "blue2")
                
            if self.RightHandThumb1.Bind_Joint:
                self.RightHandThumb1.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.02, self.proportions["depth"]*0.02, self.proportions["depth"]*0.02),
                                    offset = (0, 0, 0), 
                                    rotate = (0, 90, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "red2")
                self.RightHandThumb2.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.016, self.proportions["depth"]*0.016, self.proportions["depth"]*0.016),
                                    offset = (0, 0, 0),  
                                    rotate = (0, 90, 0), 
                                    estimateSize = estimateSize,
                                    color_ = "red2")
                self.RightHandThumb3.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.012, self.proportions["depth"]*0.012, self.proportions["depth"]*0.012),
                                    offset = (0, 0, 0),  
                                    rotate = (0, 90, 0), 
                                    estimateSize = estimateSize,
                                    color_ = "red2")
            if self.RightHandIndex1.Bind_Joint:
                self.RightHandIndex1.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.02, self.proportions["depth"]*0.02, self.proportions["depth"]*0.02),
                                    offset = (0, 0, 0), 
                                    rotate = (0, 90, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "red2")
                self.RightHandIndex2.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.016, self.proportions["depth"]*0.016, self.proportions["depth"]*0.016),
                                    offset = (0, 0, 0),  
                                    rotate = (0, 90, 0), 
                                    estimateSize = estimateSize,
                                    color_ = "red2")
                self.RightHandIndex3.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.012, self.proportions["depth"]*0.012, self.proportions["depth"]*0.012),
                                    offset = (0, 0, 0), 
                                    rotate = (0, 90, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "red2")
            if self.RightHandMiddle1.Bind_Joint:
                self.RightHandMiddle1.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.02, self.proportions["depth"]*0.02, self.proportions["depth"]*0.02),
                                    offset = (0, 0, 0),  
                                    rotate = (0, 90, 0), 
                                    estimateSize = estimateSize,
                                    color_ = "red2")
                self.RightHandMiddle2.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.016, self.proportions["depth"]*0.016, self.proportions["depth"]*0.016),
                                    offset = (0, 0, 0), 
                                    rotate = (0, 90, 0),  
                                    estimateSize = estimateSize,
                                    color_ = "red2")
                self.RightHandMiddle3.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.012, self.proportions["depth"]*0.012, self.proportions["depth"]*0.012),
                                    offset = (0, 0, 0),  
                                    rotate = (0, 90, 0), 
                                    estimateSize = estimateSize,
                                    color_ = "red2")
            if self.RightHandRing1.Bind_Joint:
                self.RightHandRing1.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.02, self.proportions["depth"]*0.02, self.proportions["depth"]*0.02),
                                    offset = (0, 0, 0),  
                                    rotate = (0, 90, 0), 
                                    estimateSize = estimateSize,
                                    color_ = "red2")
                self.RightHandRing2.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.016, self.proportions["depth"]*0.016, self.proportions["depth"]*0.016),
                                    offset = (0, 0, 0),  
                                    rotate = (0, 90, 0), 
                                    estimateSize = estimateSize,
                                    color_ = "red2")
                self.RightHandRing3.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.012, self.proportions["depth"]*0.012, self.proportions["depth"]*0.012),
                                    offset = (0, 0, 0),  
                                    rotate = (0, 90, 0), 
                                    estimateSize = estimateSize,
                                    color_ = "red2")
            if self.RightHandPinky1.Bind_Joint:
                self.RightHandPinky1.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.02, self.proportions["depth"]*0.02, self.proportions["depth"]*0.02),
                                    offset = (0, 0, 0),  
                                    rotate = (0, 90, 0), 
                                    estimateSize = estimateSize,
                                    color_ = "red2")
                self.RightHandPinky2.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.016, self.proportions["depth"]*0.016, self.proportions["depth"]*0.016),
                                    offset = (0, 0, 0),  
                                    rotate = (0, 90, 0), 
                                    estimateSize = estimateSize,
                                    color_ = "red2")
                self.RightHandPinky3.createControl(type = "normal", 
                                    style = "pin1", 
                                    scale = (self.proportions["depth"]*0.012, self.proportions["depth"]*0.012, self.proportions["depth"]*0.012),
                                    offset = (0, 0, 0),  
                                    rotate = (0, 90, 0), 
                                    estimateSize = estimateSize,
                                    color_ = "red2")
        
            #Options
            self.LeftFoot.createControl(type = "options", 
                                    style = "options", 
                                    scale = (self.proportions["depth"]*0.12, self.proportions["depth"]*0.12, self.proportions["depth"]*-0.12),
                                    offset = (0, 0, self.proportions["depth"]*-0.4),  
                                    estimateSize = estimateSize,
                                    partialConstraint = 2,
                                    color_ = "black")
            
            self.RightFoot.createControl(type = "options", 
                                    style = "options", 
                                    scale = (self.proportions["depth"]*0.12, self.proportions["depth"]*0.12, self.proportions["depth"]*-0.12),
                                    offset = (0, 0, self.proportions["depth"]*-0.4),  
                                    estimateSize = estimateSize,
                                    partialConstraint = 2,
                                    color_ = "black")
            
            self.LeftHand.createControl(type = "options", 
                                    style = "options", 
                                    scale = (self.proportions["depth"]*0.12, self.proportions["depth"]*0.12, self.proportions["depth"]*-0.12),
                                    offset = (self.proportions["depth"]*0.3, self.proportions["depth"]*0.3, 0),  
                                    rotate = (-90, 0, -90),  
                                    estimateSize = estimateSize,
                                    color_ = "black")
            
            self.RightHand.createControl(type = "options", 
                                    style = "options", 
                                    scale = (self.proportions["depth"]*0.12, self.proportions["depth"]*0.12, self.proportions["depth"]*-0.12),
                                    offset = (self.proportions["depth"]*-0.3, self.proportions["depth"]*0.3, 0),  
                                    rotate = (-90, 0, -90), 
                                    estimateSize = estimateSize,
                                    color_ = "black")
            if self.LeftEye.Bind_Joint and self.RightEye.Bind_Joint:
                self.LeftEye.createControl(type = "FK", 
                                        style = "sphere", 
                                        scale = (self.proportions["depth"]*0.06, self.proportions["depth"]*0.06, self.proportions["depth"]*0.06), 
                                        estimateSize = estimateSize,
                                        color_ = "blue1")
                self.RightEye.createControl(type = "FK", 
                                        style = "sphere", 
                                        scale = (self.proportions["depth"]*0.06, self.proportions["depth"]*0.06, self.proportions["depth"]*0.06), 
                                        estimateSize = estimateSize,
                                        color_ = "red1")
                                
                
                
    def hookUpControls(self):
        #Groupings
        self.Character_GRP = mayac.group(em = True, name = "Character")
        DJB_movePivotToObject(self.Character_GRP, self.global_CTRL)
        self.CTRL_GRP = mayac.group(em = True, name = "CTRL_GRP")
        DJB_movePivotToObject(self.CTRL_GRP, self.global_CTRL)
        mayac.parent(self.global_CTRL, self.CTRL_GRP)
        mayac.parent(self.CTRL_GRP, self.Character_GRP)
        self.Joint_GRP = mayac.group(em = True, name = "Joint_GRP")
        DJB_movePivotToObject(self.Joint_GRP, self.global_CTRL)
        mayac.parent(self.Joint_GRP, self.Character_GRP)
        self.AnimData_Joint_GRP = mayac.group(em = True, name = "AnimData_Joint_GRP")
        DJB_movePivotToObject(self.AnimData_Joint_GRP, self.global_CTRL)
        mayac.parent(self.AnimData_Joint_GRP, self.Joint_GRP)
        if self.hulaOption:
            mayac.parent(self.Root.AnimData_Joint, self.AnimData_Joint_GRP)
        else:
            mayac.parent(self.Hips.AnimData_Joint, self.AnimData_Joint_GRP)
        self.Bind_Joint_GRP = mayac.group(em = True, name = "Bind_Joint_GRP")
        DJB_movePivotToObject(self.Bind_Joint_GRP, self.global_CTRL)
        mayac.parent(self.Bind_Joint_GRP, self.Joint_GRP)
        if self.hulaOption:
            mayac.parent(self.Root.Bind_Joint, self.Bind_Joint_GRP)
        else:
            mayac.parent(self.Hips.Bind_Joint, self.Bind_Joint_GRP)
        self.Mesh_GRP = mayac.group(em = True, name = "Mesh_GRP")
        DJB_movePivotToObject(self.Mesh_GRP, self.global_CTRL)
        tempTransList =[]
        for geo in self.mesh:
            transform = mayac.listRelatives(geo, parent = True)
            if mayac.objectType(transform) == "transform" and transform not in tempTransList:
                mayac.parent(transform, self.Mesh_GRP)
                DJB_LockNHide(transform[0])
                tempTransList.append(transform)
        mayac.parent(self.Mesh_GRP, self.Character_GRP)

        #get rid of any limitations
        for bodyPart in self.bodyParts:
            if bodyPart.Bind_Joint:
                mayac.transformLimits(bodyPart.Bind_Joint, rm = True)
        
        #create FK and IK Joints
        self.LeftArm.duplicateJoint("FK", parent_ = "Bind_Joint")
        self.LeftForeArm.duplicateJoint("FK")
        self.LeftHand.duplicateJoint("FK")
        self.RightArm.duplicateJoint("FK", parent_ = "Bind_Joint")
        self.RightForeArm.duplicateJoint("FK")
        self.RightHand.duplicateJoint("FK")
        self.LeftUpLeg.duplicateJoint("FK", parent_ = "Bind_Joint")
        self.LeftLeg.duplicateJoint("FK")
        self.LeftFoot.duplicateJoint("FK")
        self.LeftToeBase.duplicateJoint("FK")
        self.LeftToe_End.duplicateJoint("FK")
        self.RightUpLeg.duplicateJoint("FK", parent_ = "Bind_Joint")
        self.RightLeg.duplicateJoint("FK")
        self.RightFoot.duplicateJoint("FK")
        self.RightToeBase.duplicateJoint("FK")
        self.RightToe_End.duplicateJoint("FK")
        
        self.LeftArm.duplicateJoint("IK", parent_ = "Bind_Joint")
        self.LeftForeArm.duplicateJoint("IK")
        self.LeftHand.duplicateJoint("IK")
        self.RightArm.duplicateJoint("IK", parent_ = "Bind_Joint")
        self.RightForeArm.duplicateJoint("IK")
        self.RightHand.duplicateJoint("IK")
        self.LeftUpLeg.duplicateJoint("IK", parent_ = "Bind_Joint")
        self.LeftLeg.duplicateJoint("IK")
        self.LeftFoot.duplicateJoint("IK")
        self.LeftToeBase.duplicateJoint("IK")
        self.LeftToe_End.duplicateJoint("IK")
        self.RightUpLeg.duplicateJoint("IK", parent_ = "Bind_Joint")
        self.RightLeg.duplicateJoint("IK")
        self.RightFoot.duplicateJoint("IK")
        self.RightToeBase.duplicateJoint("IK")
        self.RightToe_End.duplicateJoint("IK")
        
        if self.LeftEye and self.RightEye:
            self.LeftEye.duplicateJoint("IK", parent_ = "Bind_Joint")
            self.LeftEye.duplicateJoint("FK", parent_ = "Bind_Joint")
            self.RightEye.duplicateJoint("IK", parent_ = "Bind_Joint")
            self.RightEye.duplicateJoint("FK", parent_ = "Bind_Joint")
            
        #check if facial rig capable
        self.FacialControls = FacialControls.FacialControls(self.mesh)
            
        print self.FacialControls.blendshapeNodes
        if self.FacialControls.blendshapeNodes or (self.LeftEye and self.LeftEye.Bind_Joint and self.RightEye and self.RightEye.Bind_Joint):
            blends = True if self.FacialControls.blendshapeNodes else False
            self.FacialControls.create(self.global_CTRL, self.Head.FK_CTRL, self.LeftEye, self.RightEye, blends=blends)
            mayac.parent(self.FacialControls.FacialGRP, self.Character_GRP, noConnections=True)
            if blends:
                mayac.parent(self.FacialControls.hookupNode, self.Misc_GRP)
                self.FacialControl_Mover = self.FacialControls.moverNode
            self.FacialControl_Layer = self.FacialControls.FacialControl_Layer
        
        
        #finalize CTRLs
        for bodyPart in self.bodyParts:
            print bodyPart.nodeName
            bodyPart.finalizeCTRLs()
            
        #Left Arm IK BakingLOC Positions
        selfPOS = mayac.xform(self.LeftForeArm.Bind_Joint, query = True, absolute = True, worldSpace = True, translation = True)
        parentPOS = mayac.xform(self.LeftForeArm.parent.Bind_Joint, query = True, absolute = True, worldSpace = True, translation = True)
        tempDistance = math.sqrt((selfPOS[0]-parentPOS[0])*(selfPOS[0]-parentPOS[0]) + (selfPOS[1]-parentPOS[1])*(selfPOS[1]-parentPOS[1]) + (selfPOS[2]-parentPOS[2])*(selfPOS[2]-parentPOS[2]))
        if self.rigType == "AutoRig":
            mayac.setAttr("%s.translateX" % (self.LeftForeArm.IK_BakingLOC), tempDistance / 2)
        elif self.rigType == "World":  
            mayac.setAttr("%s.translateZ" % (self.LeftForeArm.IK_BakingLOC), tempDistance / -2)
            
        #Right Arm IK BakingLOC Positions
        selfPOS = mayac.xform(self.RightForeArm.Bind_Joint, query = True, absolute = True, worldSpace = True, translation = True)
        parentPOS = mayac.xform(self.RightForeArm.parent.Bind_Joint, query = True, absolute = True, worldSpace = True, translation = True)
        tempDistance = math.sqrt((selfPOS[0]-parentPOS[0])*(selfPOS[0]-parentPOS[0]) + (selfPOS[1]-parentPOS[1])*(selfPOS[1]-parentPOS[1]) + (selfPOS[2]-parentPOS[2])*(selfPOS[2]-parentPOS[2]))
        if self.rigType == "AutoRig":
            mayac.setAttr("%s.translateX" % (self.RightForeArm.IK_BakingLOC), tempDistance / -2)
        elif self.rigType == "World":  
            mayac.setAttr("%s.translateZ" % (self.RightForeArm.IK_BakingLOC), tempDistance / -2)
            
        #more groupings
        self.LeftHand_CTRLs_GRP = mayac.group(em = True, name = "LeftHand_CTRLs_GRP")
        self.RightHand_CTRLs_GRP = mayac.group(em = True, name = "RightHand_CTRLs_GRP")
        DJB_movePivotToObject(self.LeftHand_CTRLs_GRP, self.LeftHand.Bind_Joint)
        DJB_movePivotToObject(self.RightHand_CTRLs_GRP, self.RightHand.Bind_Joint)
        #set rotation orders
        mayac.setAttr("%s.rotateOrder" % (self.LeftHand_CTRLs_GRP), self.LeftHand.rotOrder)
        mayac.setAttr("%s.rotateOrder" % (self.RightHand_CTRLs_GRP), self.RightHand.rotOrder)

        mayac.parent(self.LeftHand_CTRLs_GRP, self.RightHand_CTRLs_GRP, self.global_CTRL)
        if self.LeftHandIndex1.Bind_Joint:
            mayac.parent(self.LeftHandIndex1.FK_CTRL_POS_GRP, self.LeftHand_CTRLs_GRP)
        if self.LeftHandThumb1.Bind_Joint:
            mayac.parent(self.LeftHandThumb1.FK_CTRL_POS_GRP, self.LeftHand_CTRLs_GRP)
        if self.LeftHandMiddle1.Bind_Joint:
            mayac.parent(self.LeftHandMiddle1.FK_CTRL_POS_GRP, self.LeftHand_CTRLs_GRP)
        if self.LeftHandRing1.Bind_Joint:
            mayac.parent(self.LeftHandRing1.FK_CTRL_POS_GRP, self.LeftHand_CTRLs_GRP)
        if self.LeftHandPinky1.Bind_Joint:
            mayac.parent(self.LeftHandPinky1.FK_CTRL_POS_GRP, self.LeftHand_CTRLs_GRP)
        if self.RightHandIndex1.Bind_Joint:
            mayac.parent(self.RightHandIndex1.FK_CTRL_POS_GRP, self.RightHand_CTRLs_GRP)    
        if self.RightHandThumb1.Bind_Joint:
            mayac.parent(self.RightHandThumb1.FK_CTRL_POS_GRP, self.RightHand_CTRLs_GRP)
        if self.RightHandMiddle1.Bind_Joint:
            mayac.parent(self.RightHandMiddle1.FK_CTRL_POS_GRP, self.RightHand_CTRLs_GRP)
        if self.RightHandRing1.Bind_Joint:
            mayac.parent(self.RightHandRing1.FK_CTRL_POS_GRP, self.RightHand_CTRLs_GRP)
        if self.RightHandPinky1.Bind_Joint:
            mayac.parent(self.RightHandPinky1.FK_CTRL_POS_GRP, self.RightHand_CTRLs_GRP)

        mayac.parentConstraint(self.LeftHand.Bind_Joint, self.LeftHand_CTRLs_GRP, name = "%s_Constraint" %(self.LeftHand_CTRLs_GRP))
        mayac.parentConstraint(self.RightHand.Bind_Joint, self.RightHand_CTRLs_GRP, name = "%s_Constraint" %(self.RightHand_CTRLs_GRP))
        DJB_LockNHide(self.LeftHand_CTRLs_GRP)
        DJB_LockNHide(self.RightHand_CTRLs_GRP)
        
        mayac.parent(self.LeftFoot.Options_CTRL, self.RightFoot.Options_CTRL, self.LeftHand.Options_CTRL, self.RightHand.Options_CTRL, self.global_CTRL)
        if self.hulaOption:
            mayac.parent(self.Root.FK_CTRL_POS_GRP, self.global_CTRL)
        else:
            mayac.parent(self.Hips.FK_CTRL_POS_GRP, self.global_CTRL)
        mayac.parent(self.LeftForeArm.IK_CTRL_parent_POS_GRP, self.global_CTRL)
        mayac.parent(self.LeftHand.IK_CTRL_grandparent_POS_GRP, self.global_CTRL)
        mayac.parent(self.RightForeArm.IK_CTRL_parent_POS_GRP, self.global_CTRL)
        mayac.parent(self.RightHand.IK_CTRL_grandparent_POS_GRP, self.global_CTRL)
        mayac.parent(self.LeftLeg.IK_CTRL_parent_POS_GRP, self.global_CTRL)
        mayac.parent(self.LeftFoot.IK_CTRL_grandparent_POS_GRP, self.global_CTRL)
        mayac.parent(self.RightLeg.IK_CTRL_parent_POS_GRP, self.global_CTRL)
        mayac.parent(self.RightFoot.IK_CTRL_grandparent_POS_GRP, self.global_CTRL)
        
        self.IK_Dummy_Joint_GRP = mayac.group(em = True, name = "IK_Dummy_Joint_GRP")
        if self.hulaOption:
            mayac.parent(self.Root.IK_Dummy_Joint, self.IK_Dummy_Joint_GRP)
        else:
            mayac.parent(self.Hips.IK_Dummy_Joint, self.IK_Dummy_Joint_GRP)
        mayac.parent(self.IK_Dummy_Joint_GRP, self.global_CTRL)
        
        #IKFK follow body
        #arms
        temp = mayac.parentConstraint(self.LeftShoulder.IK_Dummy_Joint, self.LeftHand.IK_CTRL_grandparent_POS_GRP, maintainOffset = True)
        self.LeftHand_grandparent_Constraint = temp[0]
        mayac.parentConstraint(self.LeftShoulder.Bind_Joint, self.LeftHand.IK_CTRL_grandparent_POS_GRP, maintainOffset = True)
        self.LeftHand_grandparent_Constraint_Reverse = mayac.createNode( 'reverse', n="LeftHand_grandparent_Constraint_Reverse")
        mayac.connectAttr("%s.FollowBody" %(self.LeftHand.IK_CTRL), "%s.inputX" %(self.LeftHand_grandparent_Constraint_Reverse))
        mayac.connectAttr("%s.FollowBody" %(self.LeftHand.IK_CTRL), "%s.%sW1" %(self.LeftHand_grandparent_Constraint, self.LeftShoulder.Bind_Joint))
        mayac.connectAttr("%s.outputX" %(self.LeftHand_grandparent_Constraint_Reverse), "%s.%sW0" %(self.LeftHand_grandparent_Constraint, self.LeftShoulder.IK_Dummy_Joint))
        mayac.setAttr("%s.interpType" %(self.LeftHand_grandparent_Constraint), 2)
        
        temp = mayac.parentConstraint(self.RightShoulder.IK_Dummy_Joint, self.RightHand.IK_CTRL_grandparent_POS_GRP, maintainOffset = True)
        self.RightHand_grandparent_Constraint = temp[0]
        mayac.parentConstraint(self.RightShoulder.Bind_Joint, self.RightHand.IK_CTRL_grandparent_POS_GRP, maintainOffset = True)
        self.RightHand_grandparent_Constraint_Reverse = mayac.createNode( 'reverse', n="RightHand_grandparent_Constraint_Reverse")
        mayac.connectAttr("%s.FollowBody" %(self.RightHand.IK_CTRL), "%s.inputX" %(self.RightHand_grandparent_Constraint_Reverse))
        mayac.connectAttr("%s.FollowBody" %(self.RightHand.IK_CTRL), "%s.%sW1" %(self.RightHand_grandparent_Constraint, self.RightShoulder.Bind_Joint))
        mayac.connectAttr("%s.outputX" %(self.RightHand_grandparent_Constraint_Reverse), "%s.%sW0" %(self.RightHand_grandparent_Constraint, self.RightShoulder.IK_Dummy_Joint))
        mayac.setAttr("%s.interpType" %(self.RightHand_grandparent_Constraint), 2)
        
        temp = mayac.parentConstraint(self.LeftShoulder.IK_Dummy_Joint, self.LeftForeArm.IK_CTRL_parent_POS_GRP, maintainOffset = True)
        self.LeftForeArm_parent_Constraint = temp[0]
        mayac.parentConstraint(self.LeftShoulder.Bind_Joint, self.LeftForeArm.IK_CTRL_parent_POS_GRP, maintainOffset = True)
        self.LeftForeArm_parent_Constraint_Reverse = mayac.createNode( 'reverse', n="LeftForeArm_parent_Constraint_Reverse")
        mayac.connectAttr("%s.FollowBody" %(self.LeftForeArm.IK_CTRL), "%s.inputX" %(self.LeftForeArm_parent_Constraint_Reverse))
        mayac.connectAttr("%s.FollowBody" %(self.LeftForeArm.IK_CTRL), "%s.%sW1" %(self.LeftForeArm_parent_Constraint, self.LeftShoulder.Bind_Joint))
        mayac.connectAttr("%s.outputX" %(self.LeftForeArm_parent_Constraint_Reverse), "%s.%sW0" %(self.LeftForeArm_parent_Constraint, self.LeftShoulder.IK_Dummy_Joint))
        mayac.setAttr("%s.interpType" %(self.LeftForeArm_parent_Constraint), 2)
        
        temp = mayac.parentConstraint(self.RightShoulder.IK_Dummy_Joint, self.RightForeArm.IK_CTRL_parent_POS_GRP, maintainOffset = True)
        self.RightForeArm_parent_Constraint = temp[0]
        mayac.parentConstraint(self.RightShoulder.Bind_Joint, self.RightForeArm.IK_CTRL_parent_POS_GRP, maintainOffset = True)
        self.RightForeArm_parent_Constraint_Reverse = mayac.createNode( 'reverse', n="RightForeArm_parent_Constraint_Reverse")
        mayac.connectAttr("%s.FollowBody" %(self.RightForeArm.IK_CTRL), "%s.inputX" %(self.RightForeArm_parent_Constraint_Reverse))
        mayac.connectAttr("%s.FollowBody" %(self.RightForeArm.IK_CTRL), "%s.%sW1" %(self.RightForeArm_parent_Constraint, self.RightShoulder.Bind_Joint))
        mayac.connectAttr("%s.outputX" %(self.RightForeArm_parent_Constraint_Reverse), "%s.%sW0" %(self.RightForeArm_parent_Constraint, self.RightShoulder.IK_Dummy_Joint))
        mayac.setAttr("%s.interpType" %(self.RightForeArm_parent_Constraint), 2)
        
        #legs
        temp = mayac.parentConstraint(self.Hips.IK_Dummy_Joint, self.LeftFoot.IK_CTRL_grandparent_POS_GRP, maintainOffset = True)
        self.LeftFoot_grandparent_Constraint = temp[0]
        mayac.parentConstraint(self.Hips.Bind_Joint, self.LeftFoot.IK_CTRL_grandparent_POS_GRP, maintainOffset = True)
        self.LeftFoot_grandparent_Constraint_Reverse = mayac.createNode( 'reverse', n="LeftFoot_grandparent_Constraint_Reverse")
        mayac.connectAttr("%s.FollowBody" %(self.LeftFoot.IK_CTRL), "%s.inputX" %(self.LeftFoot_grandparent_Constraint_Reverse))
        mayac.connectAttr("%s.FollowBody" %(self.LeftFoot.IK_CTRL), "%s.%sW1" %(self.LeftFoot_grandparent_Constraint, self.Hips.Bind_Joint))
        mayac.connectAttr("%s.outputX" %(self.LeftFoot_grandparent_Constraint_Reverse), "%s.%sW0" %(self.LeftFoot_grandparent_Constraint, self.Hips.IK_Dummy_Joint))
        mayac.setAttr("%s.interpType" %(self.LeftFoot_grandparent_Constraint), 2)
        
        temp = mayac.parentConstraint(self.Hips.IK_Dummy_Joint, self.RightFoot.IK_CTRL_grandparent_POS_GRP, maintainOffset = True)
        self.RightFoot_grandparent_Constraint = temp[0]
        mayac.parentConstraint(self.Hips.Bind_Joint, self.RightFoot.IK_CTRL_grandparent_POS_GRP, maintainOffset = True)
        self.RightFoot_grandparent_Constraint_Reverse = mayac.createNode( 'reverse', n="RightFoot_grandparent_Constraint_Reverse")
        mayac.connectAttr("%s.FollowBody" %(self.RightFoot.IK_CTRL), "%s.inputX" %(self.RightFoot_grandparent_Constraint_Reverse))
        mayac.connectAttr("%s.FollowBody" %(self.RightFoot.IK_CTRL), "%s.%sW1" %(self.RightFoot_grandparent_Constraint, self.Hips.Bind_Joint))
        mayac.connectAttr("%s.outputX" %(self.RightFoot_grandparent_Constraint_Reverse), "%s.%sW0" %(self.RightFoot_grandparent_Constraint, self.Hips.IK_Dummy_Joint))
        mayac.setAttr("%s.interpType" %(self.RightFoot_grandparent_Constraint), 2)
        
        temp = mayac.parentConstraint(self.Hips.IK_Dummy_Joint, self.LeftLeg.IK_CTRL_parent_POS_GRP, maintainOffset = True)
        self.LeftLeg_parent_Constraint = temp[0]
        mayac.parentConstraint(self.Hips.Bind_Joint, self.LeftLeg.IK_CTRL_parent_POS_GRP, maintainOffset = True)
        self.LeftLeg_parent_Constraint_Reverse = mayac.createNode( 'reverse', n="LeftLeg_parent_Constraint_Reverse")
        mayac.connectAttr("%s.FollowBody" %(self.LeftLeg.IK_CTRL), "%s.inputX" %(self.LeftLeg_parent_Constraint_Reverse))
        mayac.connectAttr("%s.FollowBody" %(self.LeftLeg.IK_CTRL), "%s.%sW1" %(self.LeftLeg_parent_Constraint, self.Hips.Bind_Joint))
        mayac.connectAttr("%s.outputX" %(self.LeftLeg_parent_Constraint_Reverse), "%s.%sW0" %(self.LeftLeg_parent_Constraint, self.Hips.IK_Dummy_Joint))
        mayac.setAttr("%s.interpType" %(self.LeftLeg_parent_Constraint), 2)
        
        temp = mayac.parentConstraint(self.Hips.IK_Dummy_Joint, self.RightLeg.IK_CTRL_parent_POS_GRP, maintainOffset = True)
        self.RightLeg_parent_Constraint = temp[0]
        mayac.parentConstraint(self.Hips.Bind_Joint, self.RightLeg.IK_CTRL_parent_POS_GRP, maintainOffset = True)
        self.RightLeg_parent_Constraint_Reverse = mayac.createNode( 'reverse', n="RightLeg_parent_Constraint_Reverse")
        mayac.connectAttr("%s.FollowBody" %(self.RightLeg.IK_CTRL), "%s.inputX" %(self.RightLeg_parent_Constraint_Reverse))
        mayac.connectAttr("%s.FollowBody" %(self.RightLeg.IK_CTRL), "%s.%sW1" %(self.RightLeg_parent_Constraint, self.Hips.Bind_Joint))
        mayac.connectAttr("%s.outputX" %(self.RightLeg_parent_Constraint_Reverse), "%s.%sW0" %(self.RightLeg_parent_Constraint, self.Hips.IK_Dummy_Joint))
        mayac.setAttr("%s.interpType" %(self.RightLeg_parent_Constraint), 2)
        
        
        
        #IK Legs and Arms to Global
        temp = mayac.parentConstraint(self.LeftFoot.IK_CTRL_grandparent_POS_GRP, self.LeftFoot.IK_CTRL_grandparent_Global_POS_GRP, maintainOffset = True)
        self.LeftFoot.grandparent_Global_Constraint = temp[0]
        mayac.parentConstraint(self.global_CTRL, self.LeftFoot.IK_CTRL_grandparent_Global_POS_GRP, maintainOffset = True)
        self.LeftFoot.grandparent_Global_Constraint_Reverse = mayac.createNode( 'reverse', n="LeftFoot_grandparent_Global_Constraint_Reverse")
        mayac.connectAttr("%s.ParentToGlobal" %(self.LeftFoot.IK_CTRL), "%s.inputX" %(self.LeftFoot.grandparent_Global_Constraint_Reverse))
        mayac.connectAttr("%s.ParentToGlobal" %(self.LeftFoot.IK_CTRL), "%s.%sW1" %(self.LeftFoot.grandparent_Global_Constraint, self.global_CTRL))
        mayac.connectAttr("%s.outputX" %(self.LeftFoot.grandparent_Global_Constraint_Reverse), "%s.%sW0" %(self.LeftFoot.grandparent_Global_Constraint, self.LeftFoot.IK_CTRL_grandparent_POS_GRP))
        mayac.setAttr("%s.interpType" %(self.LeftFoot.grandparent_Global_Constraint), 0)
        
        temp = mayac.parentConstraint(self.RightFoot.IK_CTRL_grandparent_POS_GRP, self.RightFoot.IK_CTRL_grandparent_Global_POS_GRP, maintainOffset = True)
        self.RightFoot.grandparent_Global_Constraint = temp[0]
        mayac.parentConstraint(self.global_CTRL, self.RightFoot.IK_CTRL_grandparent_Global_POS_GRP, maintainOffset = True)
        self.RightFoot.grandparent_Global_Constraint_Reverse = mayac.createNode( 'reverse', n="RightFoot_grandparent_Global_Constraint_Reverse")
        mayac.connectAttr("%s.ParentToGlobal" %(self.RightFoot.IK_CTRL), "%s.inputX" %(self.RightFoot.grandparent_Global_Constraint_Reverse))
        mayac.connectAttr("%s.ParentToGlobal" %(self.RightFoot.IK_CTRL), "%s.%sW1" %(self.RightFoot.grandparent_Global_Constraint, self.global_CTRL))
        mayac.connectAttr("%s.outputX" %(self.RightFoot.grandparent_Global_Constraint_Reverse), "%s.%sW0" %(self.RightFoot.grandparent_Global_Constraint, self.RightFoot.IK_CTRL_grandparent_POS_GRP))
        mayac.setAttr("%s.interpType" %(self.RightFoot.grandparent_Global_Constraint), 2)
        
        temp = mayac.parentConstraint(self.LeftHand.IK_CTRL_grandparent_POS_GRP, self.LeftHand.IK_CTRL_grandparent_Global_POS_GRP, maintainOffset = True)
        self.LeftHand.grandparent_Global_Constraint = temp[0]
        mayac.parentConstraint(self.global_CTRL, self.LeftHand.IK_CTRL_grandparent_Global_POS_GRP, maintainOffset = True)
        self.LeftHand.grandparent_Global_Constraint_Reverse = mayac.createNode( 'reverse', n="LeftHand_grandparent_Global_Constraint_Reverse")
        mayac.connectAttr("%s.ParentToGlobal" %(self.LeftHand.IK_CTRL), "%s.inputX" %(self.LeftHand.grandparent_Global_Constraint_Reverse))
        mayac.connectAttr("%s.ParentToGlobal" %(self.LeftHand.IK_CTRL), "%s.%sW1" %(self.LeftHand.grandparent_Global_Constraint, self.global_CTRL))
        mayac.connectAttr("%s.outputX" %(self.LeftHand.grandparent_Global_Constraint_Reverse), "%s.%sW0" %(self.LeftHand.grandparent_Global_Constraint, self.LeftHand.IK_CTRL_grandparent_POS_GRP))
        mayac.setAttr("%s.interpType" %(self.LeftHand.grandparent_Global_Constraint), 2)
        
        temp = mayac.parentConstraint(self.RightHand.IK_CTRL_grandparent_POS_GRP, self.RightHand.IK_CTRL_grandparent_Global_POS_GRP, maintainOffset = True)
        self.RightHand.grandparent_Global_Constraint = temp[0]
        mayac.parentConstraint(self.global_CTRL, self.RightHand.IK_CTRL_grandparent_Global_POS_GRP, maintainOffset = True)
        self.RightHand.grandparent_Global_Constraint_Reverse = mayac.createNode( 'reverse', n="RightHand_grandparent_Global_Constraint_Reverse")
        mayac.connectAttr("%s.ParentToGlobal" %(self.RightHand.IK_CTRL), "%s.inputX" %(self.RightHand.grandparent_Global_Constraint_Reverse))
        mayac.connectAttr("%s.ParentToGlobal" %(self.RightHand.IK_CTRL), "%s.%sW1" %(self.RightHand.grandparent_Global_Constraint, self.global_CTRL))
        mayac.connectAttr("%s.outputX" %(self.RightHand.grandparent_Global_Constraint_Reverse), "%s.%sW0" %(self.RightHand.grandparent_Global_Constraint, self.RightHand.IK_CTRL_grandparent_POS_GRP))
        mayac.setAttr("%s.interpType" %(self.RightHand.grandparent_Global_Constraint), 2)
        

        ''' self.IK_CTRL_inRig_CONST_GRP = None
        self.follow_extremity_Constraint = None
        self.follow_extremity_Constraint_Reverse = None'''
        
        #IK Elbows and Knees to Global
        temp = mayac.parentConstraint(self.LeftLeg.IK_CTRL_parent_POS_GRP, self.LeftLeg.IK_CTRL_parent_Global_POS_GRP, maintainOffset = True)
        self.LeftLeg.parent_Global_Constraint = temp[0]
        mayac.parentConstraint(self.global_CTRL, self.LeftLeg.IK_CTRL_parent_Global_POS_GRP, maintainOffset = True)
        self.LeftLeg.parent_Global_Constraint_Reverse = mayac.createNode( 'reverse', n="LeftLeg_parent_Global_Constraint_Reverse")
        mayac.connectAttr("%s.ParentToGlobal" %(self.LeftLeg.IK_CTRL), "%s.inputX" %(self.LeftLeg.parent_Global_Constraint_Reverse))
        mayac.connectAttr("%s.ParentToGlobal" %(self.LeftLeg.IK_CTRL), "%s.%sW1" %(self.LeftLeg.parent_Global_Constraint, self.global_CTRL))
        mayac.connectAttr("%s.outputX" %(self.LeftLeg.parent_Global_Constraint_Reverse), "%s.%sW0" %(self.LeftLeg.parent_Global_Constraint, self.LeftLeg.IK_CTRL_parent_POS_GRP))
        mayac.setAttr("%s.interpType" %(self.LeftLeg.parent_Global_Constraint), 2)
        
        temp = mayac.parentConstraint(self.RightLeg.IK_CTRL_parent_POS_GRP, self.RightLeg.IK_CTRL_parent_Global_POS_GRP, maintainOffset = True)
        self.RightLeg.parent_Global_Constraint = temp[0]
        mayac.parentConstraint(self.global_CTRL, self.RightLeg.IK_CTRL_parent_Global_POS_GRP, maintainOffset = True)
        self.RightLeg.parent_Global_Constraint_Reverse = mayac.createNode( 'reverse', n="RightLeg_parent_Global_Constraint_Reverse")
        mayac.connectAttr("%s.ParentToGlobal" %(self.RightLeg.IK_CTRL), "%s.inputX" %(self.RightLeg.parent_Global_Constraint_Reverse))
        mayac.connectAttr("%s.ParentToGlobal" %(self.RightLeg.IK_CTRL), "%s.%sW1" %(self.RightLeg.parent_Global_Constraint, self.global_CTRL))
        mayac.connectAttr("%s.outputX" %(self.RightLeg.parent_Global_Constraint_Reverse), "%s.%sW0" %(self.RightLeg.parent_Global_Constraint, self.RightLeg.IK_CTRL_parent_POS_GRP))
        mayac.setAttr("%s.interpType" %(self.RightLeg.parent_Global_Constraint), 2)
        
        temp = mayac.parentConstraint(self.LeftForeArm.IK_CTRL_parent_POS_GRP, self.LeftForeArm.IK_CTRL_parent_Global_POS_GRP, maintainOffset = True)
        self.LeftForeArm.parent_Global_Constraint = temp[0]
        mayac.parentConstraint(self.global_CTRL, self.LeftForeArm.IK_CTRL_parent_Global_POS_GRP, maintainOffset = True)
        self.LeftForeArm.parent_Global_Constraint_Reverse = mayac.createNode( 'reverse', n="LeftForeArm_parent_Global_Constraint_Reverse")
        mayac.connectAttr("%s.ParentToGlobal" %(self.LeftForeArm.IK_CTRL), "%s.inputX" %(self.LeftForeArm.parent_Global_Constraint_Reverse))
        mayac.connectAttr("%s.ParentToGlobal" %(self.LeftForeArm.IK_CTRL), "%s.%sW1" %(self.LeftForeArm.parent_Global_Constraint, self.global_CTRL))
        mayac.connectAttr("%s.outputX" %(self.LeftForeArm.parent_Global_Constraint_Reverse), "%s.%sW0" %(self.LeftForeArm.parent_Global_Constraint, self.LeftForeArm.IK_CTRL_parent_POS_GRP))
        mayac.setAttr("%s.interpType" %(self.LeftForeArm.parent_Global_Constraint), 2)
        
        temp = mayac.parentConstraint(self.RightForeArm.IK_CTRL_parent_POS_GRP, self.RightForeArm.IK_CTRL_parent_Global_POS_GRP, maintainOffset = True)
        self.RightForeArm.parent_Global_Constraint = temp[0]
        mayac.parentConstraint(self.global_CTRL, self.RightForeArm.IK_CTRL_parent_Global_POS_GRP, maintainOffset = True)
        self.RightForeArm.parent_Global_Constraint_Reverse = mayac.createNode( 'reverse', n="RightForeArm_parent_Global_Constraint_Reverse")
        mayac.connectAttr("%s.ParentToGlobal" %(self.RightForeArm.IK_CTRL), "%s.inputX" %(self.RightForeArm.parent_Global_Constraint_Reverse))
        mayac.connectAttr("%s.ParentToGlobal" %(self.RightForeArm.IK_CTRL), "%s.%sW1" %(self.RightForeArm.parent_Global_Constraint, self.global_CTRL))
        mayac.connectAttr("%s.outputX" %(self.RightForeArm.parent_Global_Constraint_Reverse), "%s.%sW0" %(self.RightForeArm.parent_Global_Constraint, self.RightForeArm.IK_CTRL_parent_POS_GRP))
        mayac.setAttr("%s.interpType" %(self.RightForeArm.parent_Global_Constraint), 2)
        
        
        
        #IK Elbows and Knees to Hands and feet     
        temp = mayac.parentConstraint(self.LeftFoot.IK_CTRL, self.LeftLeg.Follow_Foot_GRP, maintainOffset = True)
        self.LeftLeg.Follow_Foot_Constraint = temp[0]
        temp = mayac.parentConstraint(self.LeftLeg.IK_CTRL_animData_CONST_GRP, self.LeftLeg.IK_CTRL_inRig_CONST_GRP, maintainOffset = False)
        self.LeftLeg.follow_extremity_Constraint = temp[0]
        mayac.parentConstraint(self.LeftLeg.Follow_Knee_GRP, self.LeftLeg.IK_CTRL_inRig_CONST_GRP, maintainOffset = False)
        self.LeftLeg.follow_extremity_Constraint_Reverse = mayac.createNode( 'reverse', n="LeftLeg_follow_extremity_Constraint_Reverse")
        mayac.connectAttr("%s.FollowFoot" %(self.LeftLeg.IK_CTRL), "%s.inputX" %(self.LeftLeg.follow_extremity_Constraint_Reverse))
        mayac.connectAttr("%s.FollowFoot" %(self.LeftLeg.IK_CTRL), "%s.%sW1" %(self.LeftLeg.follow_extremity_Constraint, self.LeftLeg.Follow_Knee_GRP))
        mayac.connectAttr("%s.outputX" %(self.LeftLeg.follow_extremity_Constraint_Reverse), "%s.%sW0" %(self.LeftLeg.follow_extremity_Constraint, self.LeftLeg.IK_CTRL_animData_CONST_GRP))
        mayac.setAttr("%s.interpType" %(self.LeftLeg.follow_extremity_Constraint), 2)
        
        temp = mayac.parentConstraint(self.RightFoot.IK_CTRL, self.RightLeg.Follow_Foot_GRP, maintainOffset = True)
        self.RightLeg.Follow_Foot_Constraint = temp[0]
        temp = mayac.parentConstraint(self.RightLeg.IK_CTRL_animData_CONST_GRP, self.RightLeg.IK_CTRL_inRig_CONST_GRP, maintainOffset = False)
        self.RightLeg.follow_extremity_Constraint = temp[0]
        mayac.parentConstraint(self.RightLeg.Follow_Knee_GRP, self.RightLeg.IK_CTRL_inRig_CONST_GRP, maintainOffset = False)
        self.RightLeg.follow_extremity_Constraint_Reverse = mayac.createNode( 'reverse', n="RightLeg_follow_extremity_Constraint_Reverse")
        mayac.connectAttr("%s.FollowFoot" %(self.RightLeg.IK_CTRL), "%s.inputX" %(self.RightLeg.follow_extremity_Constraint_Reverse))
        mayac.connectAttr("%s.FollowFoot" %(self.RightLeg.IK_CTRL), "%s.%sW1" %(self.RightLeg.follow_extremity_Constraint, self.RightLeg.Follow_Knee_GRP))
        mayac.connectAttr("%s.outputX" %(self.RightLeg.follow_extremity_Constraint_Reverse), "%s.%sW0" %(self.RightLeg.follow_extremity_Constraint, self.RightLeg.IK_CTRL_animData_CONST_GRP))
        mayac.setAttr("%s.interpType" %(self.RightLeg.follow_extremity_Constraint), 2)
        
        temp = mayac.parentConstraint(self.LeftForeArm.IK_CTRL_animData_CONST_GRP, self.LeftForeArm.IK_CTRL_inRig_CONST_GRP, maintainOffset = True)
        self.LeftForeArm.follow_extremity_Constraint = temp[0]
        mayac.parentConstraint(self.LeftHand.IK_CTRL, self.LeftForeArm.IK_CTRL_inRig_CONST_GRP, maintainOffset = True)
        self.LeftForeArm.follow_extremity_Constraint_Reverse = mayac.createNode( 'reverse', n="LeftForeArm_follow_extremity_Constraint_Reverse")
        mayac.connectAttr("%s.FollowHand" %(self.LeftForeArm.IK_CTRL), "%s.inputX" %(self.LeftForeArm.follow_extremity_Constraint_Reverse))
        mayac.connectAttr("%s.FollowHand" %(self.LeftForeArm.IK_CTRL), "%s.%sW1" %(self.LeftForeArm.follow_extremity_Constraint, self.LeftHand.IK_CTRL))
        mayac.connectAttr("%s.outputX" %(self.LeftForeArm.follow_extremity_Constraint_Reverse), "%s.%sW0" %(self.LeftForeArm.follow_extremity_Constraint, self.LeftForeArm.IK_CTRL_animData_CONST_GRP))
        mayac.setAttr("%s.interpType" %(self.LeftForeArm.follow_extremity_Constraint), 2)
        
        temp = mayac.parentConstraint(self.RightForeArm.IK_CTRL_animData_CONST_GRP, self.RightForeArm.IK_CTRL_inRig_CONST_GRP, maintainOffset = True)
        self.RightForeArm.follow_extremity_Constraint = temp[0]
        mayac.parentConstraint(self.RightHand.IK_CTRL, self.RightForeArm.IK_CTRL_inRig_CONST_GRP, maintainOffset = True)
        self.RightForeArm.follow_extremity_Constraint_Reverse = mayac.createNode( 'reverse', n="RightForeArm_follow_extremity_Constraint_Reverse")
        mayac.connectAttr("%s.FollowHand" %(self.RightForeArm.IK_CTRL), "%s.inputX" %(self.RightForeArm.follow_extremity_Constraint_Reverse))
        mayac.connectAttr("%s.FollowHand" %(self.RightForeArm.IK_CTRL), "%s.%sW1" %(self.RightForeArm.follow_extremity_Constraint, self.RightHand.IK_CTRL))
        mayac.connectAttr("%s.outputX" %(self.RightForeArm.follow_extremity_Constraint_Reverse), "%s.%sW0" %(self.RightForeArm.follow_extremity_Constraint, self.RightForeArm.IK_CTRL_animData_CONST_GRP))
        mayac.setAttr("%s.interpType" %(self.RightForeArm.follow_extremity_Constraint), 2)
        

        
        #IK feet
        self.Left_Ankle_IK_CTRL = DJB_createGroup(transform = None, suffix = None, fullName ="Left_Ankle_IK_CTRL", pivotFrom = self.LeftToeBase.Bind_Joint)
        self.Left_ToeBase_IK_CTRL = DJB_createGroup(transform = None, suffix = None, fullName ="Left_ToeBase_IK_CTRL", pivotFrom = self.LeftToeBase.Bind_Joint)
        self.Left_ToeBase_IK_AnimData_GRP = DJB_createGroup(transform = self.Left_ToeBase_IK_CTRL, suffix = None, fullName ="Left_ToeBase_IK_AnimData_GRP")
        self.Left_Ankle_IK_AnimData_GRP = DJB_createGroup(transform = self.Left_Ankle_IK_CTRL, suffix = None, fullName ="Left_Ankle_IK_AnimData_GRP")
        self.Left_Toe_IK_CTRL = DJB_createGroup(transform = None, suffix = None, fullName ="Left_Toe_End_IK_CTRL", pivotFrom = self.LeftToe_End.Bind_Joint)
        self.Left_Toe_IK_AnimData_GRP = DJB_createGroup(transform = self.Left_Toe_IK_CTRL, suffix = None, fullName ="Left_Toe_IK_AnimData_GRP")   
        #set rotation orders
        mayac.setAttr("%s.rotateOrder" % (self.Left_Ankle_IK_CTRL), self.LeftFoot.rotOrder)
        mayac.setAttr("%s.rotateOrder" % (self.Left_ToeBase_IK_CTRL), self.LeftToeBase.rotOrder)
        mayac.setAttr("%s.rotateOrder" % (self.Left_ToeBase_IK_AnimData_GRP), self.LeftToeBase.rotOrder)
        mayac.setAttr("%s.rotateOrder" % (self.Left_Ankle_IK_AnimData_GRP), self.LeftFoot.rotOrder)
        mayac.setAttr("%s.rotateOrder" % (self.Left_Toe_IK_CTRL), self.LeftToeBase.rotOrder)
        mayac.setAttr("%s.rotateOrder" % (self.Left_Toe_IK_AnimData_GRP), self.LeftToeBase.rotOrder)
        
        
        #handle     
        temp = mayac.ikHandle( n="Left_ToeBase_IkHandle", sj= self.LeftFoot.IK_Joint, ee= self.LeftToeBase.IK_Joint, solver = "ikSCsolver", weight = 1)
        self.Left_ToeBase_IkHandle = temp[0]
        mayac.setAttr("%s.visibility" % (self.Left_ToeBase_IkHandle), 0)

        mayac.parent(self.Left_Toe_IK_AnimData_GRP, self.LeftFoot.IK_CTRL)
        mayac.parent(self.Left_ToeBase_IK_AnimData_GRP, self.Left_Toe_IK_CTRL)
        mayac.parent(self.Left_Ankle_IK_AnimData_GRP, self.Left_Toe_IK_CTRL)
        mayac.parent(self.LeftFoot.IK_Handle, self.Left_Ankle_IK_CTRL)
        mayac.parent(self.Left_ToeBase_IkHandle, self.Left_Ankle_IK_CTRL)
        mayac.orientConstraint(self.Left_Toe_IK_CTRL, self.LeftToe_End.IK_Joint)
        mayac.orientConstraint(self.Left_ToeBase_IK_CTRL, self.LeftToeBase.IK_Joint)
        mayac.delete(self.LeftFoot.IK_Constraint)
        self.LeftFoot.IK_Constraint = None
        mayac.orientConstraint(self.Left_Ankle_IK_CTRL, self.LeftFoot.IK_Joint)
        
        self.Left_IK_ToeBase_animData_MultNode = mayac.createNode( 'multiplyDivide', n="Left_IK_ToeBase_animData_MultNode")
        mayac.connectAttr("%s.rotateX" %(self.LeftToeBase.AnimData_Joint), "%s.input1X" %(self.Left_IK_ToeBase_animData_MultNode), force = True)
        mayac.connectAttr("%s.AnimDataMult" %(self.LeftFoot.IK_CTRL), "%s.input2X" %(self.Left_IK_ToeBase_animData_MultNode), force = True)
        mayac.connectAttr("%s.rotateY" %(self.LeftToeBase.AnimData_Joint), "%s.input1Y" %(self.Left_IK_ToeBase_animData_MultNode), force = True)
        mayac.connectAttr("%s.AnimDataMult" %(self.LeftFoot.IK_CTRL), "%s.input2Y" %(self.Left_IK_ToeBase_animData_MultNode), force = True)
        mayac.connectAttr("%s.rotateZ" %(self.LeftToeBase.AnimData_Joint), "%s.input1Z" %(self.Left_IK_ToeBase_animData_MultNode), force = True)
        mayac.connectAttr("%s.AnimDataMult" %(self.LeftFoot.IK_CTRL), "%s.input2Z" %(self.Left_IK_ToeBase_animData_MultNode), force = True)
        mayac.connectAttr("%s.outputX" %(self.Left_IK_ToeBase_animData_MultNode), "%s.rotateX" %(self.Left_ToeBase_IK_AnimData_GRP), force = True)
        mayac.connectAttr("%s.outputY" %(self.Left_IK_ToeBase_animData_MultNode), "%s.rotateY" %(self.Left_ToeBase_IK_AnimData_GRP), force = True)
        mayac.connectAttr("%s.outputZ" %(self.Left_IK_ToeBase_animData_MultNode), "%s.rotateZ" %(self.Left_ToeBase_IK_AnimData_GRP), force = True)
    
        self.Right_Ankle_IK_CTRL = DJB_createGroup(transform = None, suffix = None, fullName ="Right_Ankle_IK_CTRL", pivotFrom = self.RightToeBase.Bind_Joint)
        self.Right_ToeBase_IK_CTRL = DJB_createGroup(transform = None, suffix = None, fullName ="Right_ToeBase_IK_CTRL", pivotFrom = self.RightToeBase.Bind_Joint)
        self.Right_ToeBase_IK_AnimData_GRP = DJB_createGroup(transform = self.Right_ToeBase_IK_CTRL, suffix = None, fullName ="Right_ToeBase_IK_AnimData_GRP")
        self.Right_Ankle_IK_AnimData_GRP = DJB_createGroup(transform = self.Right_Ankle_IK_CTRL, suffix = None, fullName ="Right_Ankle_IK_AnimData_GRP")
        self.Right_Toe_IK_CTRL = DJB_createGroup(transform = None, suffix = None, fullName ="Right_Toe_End_IK_CTRL", pivotFrom = self.RightToe_End.Bind_Joint)
        self.Right_Toe_IK_AnimData_GRP = DJB_createGroup(transform = self.Right_Toe_IK_CTRL, suffix = None, fullName ="Right_Toe_IK_AnimData_GRP")            
        #set rotation orders
        mayac.setAttr("%s.rotateOrder" % (self.Right_Ankle_IK_CTRL), self.LeftFoot.rotOrder)
        mayac.setAttr("%s.rotateOrder" % (self.Right_ToeBase_IK_CTRL), self.LeftToeBase.rotOrder)
        mayac.setAttr("%s.rotateOrder" % (self.Right_ToeBase_IK_AnimData_GRP), self.LeftToeBase.rotOrder)
        mayac.setAttr("%s.rotateOrder" % (self.Right_Ankle_IK_AnimData_GRP), self.LeftFoot.rotOrder)
        mayac.setAttr("%s.rotateOrder" % (self.Right_Toe_IK_CTRL), self.LeftToeBase.rotOrder)
        mayac.setAttr("%s.rotateOrder" % (self.Right_Toe_IK_AnimData_GRP), self.LeftToeBase.rotOrder)
        #IK Handle
        temp = mayac.ikHandle( n="Right_ToeBase_IkHandle", sj= self.RightFoot.IK_Joint, ee= self.RightToeBase.IK_Joint, solver = "ikSCsolver", weight = 1)
        self.Right_ToeBase_IkHandle = temp[0]
        mayac.setAttr("%s.visibility" % (self.Right_ToeBase_IkHandle), 0)

        
        mayac.parent(self.Right_Toe_IK_AnimData_GRP, self.RightFoot.IK_CTRL)
        mayac.parent(self.Right_ToeBase_IK_AnimData_GRP, self.Right_Toe_IK_CTRL)
        mayac.parent(self.Right_Ankle_IK_AnimData_GRP, self.Right_Toe_IK_CTRL)
        mayac.parent(self.RightFoot.IK_Handle, self.Right_Ankle_IK_CTRL)
        mayac.parent(self.Right_ToeBase_IkHandle, self.Right_Ankle_IK_CTRL)
        mayac.orientConstraint(self.Right_Toe_IK_CTRL, self.RightToe_End.IK_Joint)
        mayac.orientConstraint(self.Right_ToeBase_IK_CTRL, self.RightToeBase.IK_Joint)
        mayac.delete(self.RightFoot.IK_Constraint)
        self.RightFoot.IK_Constraint = None
        mayac.orientConstraint(self.Right_Ankle_IK_CTRL, self.RightFoot.IK_Joint)
        
        self.Right_IK_ToeBase_animData_MultNode = mayac.createNode( 'multiplyDivide', n="Right_IK_ToeBase_animData_MultNode")
        mayac.connectAttr("%s.rotateX" %(self.RightToeBase.AnimData_Joint), "%s.input1X" %(self.Right_IK_ToeBase_animData_MultNode), force = True)
        mayac.connectAttr("%s.AnimDataMult" %(self.RightFoot.IK_CTRL), "%s.input2X" %(self.Right_IK_ToeBase_animData_MultNode), force = True)
        mayac.connectAttr("%s.rotateY" %(self.RightToeBase.AnimData_Joint), "%s.input1Y" %(self.Right_IK_ToeBase_animData_MultNode), force = True)
        mayac.connectAttr("%s.AnimDataMult" %(self.RightFoot.IK_CTRL), "%s.input2Y" %(self.Right_IK_ToeBase_animData_MultNode), force = True)
        mayac.connectAttr("%s.rotateZ" %(self.RightToeBase.AnimData_Joint), "%s.input1Z" %(self.Right_IK_ToeBase_animData_MultNode), force = True)
        mayac.connectAttr("%s.AnimDataMult" %(self.RightFoot.IK_CTRL), "%s.input2Z" %(self.Right_IK_ToeBase_animData_MultNode), force = True)
        mayac.connectAttr("%s.outputX" %(self.Right_IK_ToeBase_animData_MultNode), "%s.rotateX" %(self.Right_ToeBase_IK_AnimData_GRP), force = True)
        mayac.connectAttr("%s.outputY" %(self.Right_IK_ToeBase_animData_MultNode), "%s.rotateY" %(self.Right_ToeBase_IK_AnimData_GRP), force = True)
        mayac.connectAttr("%s.outputZ" %(self.Right_IK_ToeBase_animData_MultNode), "%s.rotateZ" %(self.Right_ToeBase_IK_AnimData_GRP), force = True)

        #Zero offsets on Foot Constraints
        mayac.setAttr("%s.offsetX" % (self.LeftFoot.Constraint), 0)
        mayac.setAttr("%s.offsetY" % (self.LeftFoot.Constraint), 0)
        mayac.setAttr("%s.offsetZ" % (self.LeftFoot.Constraint), 0)
        mayac.setAttr("%s.offsetX" % (self.RightFoot.Constraint), 0)
        mayac.setAttr("%s.offsetY" % (self.RightFoot.Constraint), 0)
        mayac.setAttr("%s.offsetZ" % (self.RightFoot.Constraint), 0)

        #attr connections to foot controls
        if self.rigType == "AutoRig":
            self.LeftFoot_FootRoll_MultNode = mayac.createNode( 'multiplyDivide', n="LeftFoot_FootRoll_MultNode")
            mayac.setAttr("%s.input2X" %(self.LeftFoot_FootRoll_MultNode), -1)
            mayac.connectAttr("%s.FootRoll" %(self.LeftFoot.IK_CTRL), "%s.input1X" %(self.LeftFoot_FootRoll_MultNode), force = True)
            mayac.connectAttr("%s.outputX" %(self.LeftFoot_FootRoll_MultNode), "%s.rotateX" %(self.Left_Ankle_IK_CTRL), force = True)
    
            mayac.connectAttr("%s.ToeTap" %(self.LeftFoot.IK_CTRL), "%s.rotateX" %(self.Left_ToeBase_IK_CTRL), force = True)
            Left_ToeBase_ZAdd = mayac.shadingNode('plusMinusAverage', asUtility=True, n = "Left_ToeBase_ZAdd")
            mayac.connectAttr("%s.ToeSideToSide" %(self.LeftFoot.IK_CTRL), "%s.input1D[0]" %(Left_ToeBase_ZAdd), force = True)
            mayac.connectAttr("%s.output1D" %(Left_ToeBase_ZAdd), "%s.rotateZ" %(self.Left_ToeBase_IK_CTRL), force = True)
            mayac.connectAttr("%s.ToeRotate" %(self.LeftFoot.IK_CTRL), "%s.rotateY" %(self.Left_ToeBase_IK_CTRL), force = True)
            
            self.LeftFoot_ToeRoll_MultNode = mayac.createNode( 'multiplyDivide', n="LeftFoot_ToeRoll_MultNode")
            mayac.setAttr("%s.input2X" %(self.LeftFoot_ToeRoll_MultNode), -1)
            mayac.connectAttr("%s.ToeRoll" %(self.LeftFoot.IK_CTRL), "%s.input1X" %(self.LeftFoot_ToeRoll_MultNode), force = True)
            mayac.connectAttr("%s.outputX" %(self.LeftFoot_ToeRoll_MultNode), "%s.rotateX" %(self.Left_Toe_IK_CTRL), force = True)
            
            mayac.connectAttr("%s.HipPivot" %(self.LeftFoot.IK_CTRL), "%s.rotateY" %(self.LeftFoot.IK_CTRL_grandparent_inRig_CONST_GRP), force = True)
    
            mayac.connectAttr("%s.BallPivot" %(self.LeftFoot.IK_CTRL), "%s.input1D[1]" %(Left_ToeBase_ZAdd), force = True)
            mayac.connectAttr("%s.BallPivot" %(self.LeftFoot.IK_CTRL), "%s.rotateZ" %(self.Left_Ankle_IK_CTRL), force = True)
            
            mayac.connectAttr("%s.ToePivot" %(self.LeftFoot.IK_CTRL), "%s.rotateZ" %(self.Left_Toe_IK_CTRL), force = True)
            
            mayac.connectAttr("%s.HipSideToSide" %(self.LeftFoot.IK_CTRL), "%s.rotateZ" %(self.LeftFoot.IK_CTRL_grandparent_inRig_CONST_GRP), force = True)
    
            mayac.connectAttr("%s.HipBackToFront" %(self.LeftFoot.IK_CTRL), "%s.rotateX" %(self.LeftFoot.IK_CTRL_grandparent_inRig_CONST_GRP), force = True)
        
        
            self.RightFoot_FootRoll_MultNode = mayac.createNode( 'multiplyDivide', n="RightFoot_FootRoll_MultNode")
            mayac.setAttr("%s.input2X" %(self.RightFoot_FootRoll_MultNode), -1)
            mayac.connectAttr("%s.FootRoll" %(self.RightFoot.IK_CTRL), "%s.input1X" %(self.RightFoot_FootRoll_MultNode), force = True)
            mayac.connectAttr("%s.outputX" %(self.RightFoot_FootRoll_MultNode), "%s.rotateX" %(self.Right_Ankle_IK_CTRL), force = True)
    
            mayac.connectAttr("%s.ToeTap" %(self.RightFoot.IK_CTRL), "%s.rotateX" %(self.Right_ToeBase_IK_CTRL), force = True)
            Right_ToeBase_ZAdd = mayac.shadingNode('plusMinusAverage', asUtility=True, n = "Right_ToeBase_ZAdd")
            mayac.connectAttr("%s.ToeSideToSide" %(self.RightFoot.IK_CTRL), "%s.input1D[0]" %(Right_ToeBase_ZAdd), force = True)
            mayac.connectAttr("%s.output1D" %(Right_ToeBase_ZAdd), "%s.rotateZ" %(self.Right_ToeBase_IK_CTRL), force = True)
            mayac.connectAttr("%s.ToeRotate" %(self.RightFoot.IK_CTRL), "%s.rotateY" %(self.Right_ToeBase_IK_CTRL), force = True)
    
            self.RightFoot_ToeRoll_MultNode = mayac.createNode( 'multiplyDivide', n="RightFoot_ToeRoll_MultNode")
            mayac.setAttr("%s.input2X" %(self.RightFoot_ToeRoll_MultNode), -1)
            mayac.connectAttr("%s.ToeRoll" %(self.RightFoot.IK_CTRL), "%s.input1X" %(self.RightFoot_ToeRoll_MultNode), force = True)
            mayac.connectAttr("%s.outputX" %(self.RightFoot_ToeRoll_MultNode), "%s.rotateX" %(self.Right_Toe_IK_CTRL), force = True)
            
            self.RightFoot_HipPivot_MultNode = mayac.createNode( 'multiplyDivide', n="RightFoot_HipPivot_MultNode")
            mayac.setAttr("%s.input2X" %(self.RightFoot_HipPivot_MultNode), -1)
            mayac.connectAttr("%s.HipPivot" %(self.RightFoot.IK_CTRL), "%s.input1X" %(self.RightFoot_HipPivot_MultNode), force = True)
            mayac.connectAttr("%s.outputX" %(self.RightFoot_HipPivot_MultNode), "%s.rotateY" %(self.RightFoot.IK_CTRL_grandparent_inRig_CONST_GRP), force = True)
            
            self.RightFoot_BallPivot_MultNode = mayac.createNode( 'multiplyDivide', n="RightFoot_BallPivot_MultNode")
            mayac.setAttr("%s.input2X" %(self.RightFoot_BallPivot_MultNode), -1)
            mayac.connectAttr("%s.BallPivot" %(self.RightFoot.IK_CTRL), "%s.input1X" %(self.RightFoot_BallPivot_MultNode), force = True)
            mayac.connectAttr("%s.outputX" %(self.RightFoot_BallPivot_MultNode), "%s.input1D[1]" %(Right_ToeBase_ZAdd), force = True)
            mayac.connectAttr("%s.outputX" %(self.RightFoot_BallPivot_MultNode), "%s.rotateZ" %(self.Right_Ankle_IK_CTRL), force = True)
            
            self.RightFoot_ToePivot_MultNode = mayac.createNode( 'multiplyDivide', n="RightFoot_ToePivot_MultNode")
            mayac.setAttr("%s.input2X" %(self.RightFoot_ToePivot_MultNode), -1)
            mayac.connectAttr("%s.ToePivot" %(self.RightFoot.IK_CTRL), "%s.input1X" %(self.RightFoot_ToePivot_MultNode), force = True)
            mayac.connectAttr("%s.outputX" %(self.RightFoot_ToePivot_MultNode), "%s.rotateZ" %(self.Right_Toe_IK_CTRL), force = True)
            
            self.RightFoot_HipSideToSide_MultNode = mayac.createNode( 'multiplyDivide', n="RightFoot_HipSideToSide_MultNode")
            mayac.setAttr("%s.input2X" %(self.RightFoot_HipSideToSide_MultNode), -1)
            mayac.connectAttr("%s.HipSideToSide" %(self.RightFoot.IK_CTRL), "%s.input1X" %(self.RightFoot_HipSideToSide_MultNode), force = True)
            mayac.connectAttr("%s.outputX" %(self.RightFoot_HipSideToSide_MultNode), "%s.rotateZ" %(self.RightFoot.IK_CTRL_grandparent_inRig_CONST_GRP), force = True)
            
            mayac.connectAttr("%s.HipBackToFront" %(self.RightFoot.IK_CTRL), "%s.rotateX" %(self.RightFoot.IK_CTRL_grandparent_inRig_CONST_GRP), force = True)
        
        
        
        
        elif self.rigType == "World":
            self.LeftFoot_FootRoll_MultNode = mayac.createNode( 'multiplyDivide', n="LeftFoot_FootRoll_MultNode")
            mayac.setAttr("%s.input2X" %(self.LeftFoot_FootRoll_MultNode), 1)
            mayac.connectAttr("%s.FootRoll" %(self.LeftFoot.IK_CTRL), "%s.input1X" %(self.LeftFoot_FootRoll_MultNode), force = True)
            mayac.connectAttr("%s.outputX" %(self.LeftFoot_FootRoll_MultNode), "%s.rotateX" %(self.Left_Ankle_IK_CTRL), force = True)
    
            LeftFoot_ToeTap_MultNode = mayac.createNode( 'multiplyDivide', n="LeftFoot_ToeTap_MultNode")
            mayac.setAttr("%s.input2X" %(LeftFoot_ToeTap_MultNode), -1)
            mayac.connectAttr("%s.ToeTap" %(self.LeftFoot.IK_CTRL), "%s.input1X" %(LeftFoot_ToeTap_MultNode), force = True)
            mayac.connectAttr("%s.outputX" %(LeftFoot_ToeTap_MultNode), "%s.rotateX" %(self.Left_ToeBase_IK_CTRL), force = True)
            
            Left_ToeBase_ZAdd = mayac.shadingNode('plusMinusAverage', asUtility=True, n = "Left_ToeBase_ZAdd")
            mayac.connectAttr("%s.ToeSideToSide" %(self.LeftFoot.IK_CTRL), "%s.input1D[0]" %(Left_ToeBase_ZAdd), force = True)
            mayac.connectAttr("%s.output1D" %(Left_ToeBase_ZAdd), "%s.rotateY" %(self.Left_ToeBase_IK_CTRL), force = True)
            mayac.connectAttr("%s.ToeRotate" %(self.LeftFoot.IK_CTRL), "%s.rotateZ" %(self.Left_ToeBase_IK_CTRL), force = True)
            
            self.LeftFoot_ToeRoll_MultNode = mayac.createNode( 'multiplyDivide', n="LeftFoot_ToeRoll_MultNode")
            mayac.setAttr("%s.input2X" %(self.LeftFoot_ToeRoll_MultNode), 1)
            mayac.connectAttr("%s.ToeRoll" %(self.LeftFoot.IK_CTRL), "%s.input1X" %(self.LeftFoot_ToeRoll_MultNode), force = True)
            mayac.connectAttr("%s.outputX" %(self.LeftFoot_ToeRoll_MultNode), "%s.rotateX" %(self.Left_Toe_IK_CTRL), force = True)
            
            mayac.connectAttr("%s.HipPivot" %(self.LeftFoot.IK_CTRL), "%s.rotateY" %(self.LeftFoot.IK_CTRL_grandparent_inRig_CONST_GRP), force = True)
    
            mayac.connectAttr("%s.BallPivot" %(self.LeftFoot.IK_CTRL), "%s.input1D[1]" %(Left_ToeBase_ZAdd), force = True)
            mayac.connectAttr("%s.BallPivot" %(self.LeftFoot.IK_CTRL), "%s.rotateY" %(self.Left_Ankle_IK_CTRL), force = True)
            
            mayac.connectAttr("%s.ToePivot" %(self.LeftFoot.IK_CTRL), "%s.rotateY" %(self.Left_Toe_IK_CTRL), force = True)
            
            mayac.connectAttr("%s.HipSideToSide" %(self.LeftFoot.IK_CTRL), "%s.rotateZ" %(self.LeftFoot.IK_CTRL_grandparent_inRig_CONST_GRP), force = True)
    
            mayac.connectAttr("%s.HipBackToFront" %(self.LeftFoot.IK_CTRL), "%s.rotateX" %(self.LeftFoot.IK_CTRL_grandparent_inRig_CONST_GRP), force = True)
            
            
            self.RightFoot_FootRoll_MultNode = mayac.createNode( 'multiplyDivide', n="RightFoot_FootRoll_MultNode")
            mayac.setAttr("%s.input2X" %(self.RightFoot_FootRoll_MultNode), 1)
            mayac.connectAttr("%s.FootRoll" %(self.RightFoot.IK_CTRL), "%s.input1X" %(self.RightFoot_FootRoll_MultNode), force = True)
            mayac.connectAttr("%s.outputX" %(self.RightFoot_FootRoll_MultNode), "%s.rotateX" %(self.Right_Ankle_IK_CTRL), force = True)
    
            RightFoot_ToeTap_MultNode = mayac.createNode( 'multiplyDivide', n="RightFoot_ToeTap_MultNode")
            mayac.setAttr("%s.input2X" %(RightFoot_ToeTap_MultNode), -1)
            mayac.connectAttr("%s.ToeTap" %(self.RightFoot.IK_CTRL), "%s.input1X" %(RightFoot_ToeTap_MultNode), force = True)
            mayac.connectAttr("%s.outputX" %(RightFoot_ToeTap_MultNode), "%s.rotateX" %(self.Right_ToeBase_IK_CTRL), force = True)
            
            Right_ToeBase_ZAdd = mayac.shadingNode('plusMinusAverage', asUtility=True, n = "Right_ToeBase_ZAdd")
            mayac.connectAttr("%s.ToeSideToSide" %(self.RightFoot.IK_CTRL), "%s.input1D[0]" %(Right_ToeBase_ZAdd), force = True)
            mayac.connectAttr("%s.output1D" %(Right_ToeBase_ZAdd), "%s.rotateY" %(self.Right_ToeBase_IK_CTRL), force = True)
            mayac.connectAttr("%s.ToeRotate" %(self.RightFoot.IK_CTRL), "%s.rotateZ" %(self.Right_ToeBase_IK_CTRL), force = True)
    
            self.RightFoot_ToeRoll_MultNode = mayac.createNode( 'multiplyDivide', n="RightFoot_ToeRoll_MultNode")
            mayac.setAttr("%s.input2X" %(self.RightFoot_ToeRoll_MultNode), 1)
            mayac.connectAttr("%s.ToeRoll" %(self.RightFoot.IK_CTRL), "%s.input1X" %(self.RightFoot_ToeRoll_MultNode), force = True)
            mayac.connectAttr("%s.outputX" %(self.RightFoot_ToeRoll_MultNode), "%s.rotateX" %(self.Right_Toe_IK_CTRL), force = True)
            
            self.RightFoot_HipPivot_MultNode = mayac.createNode( 'multiplyDivide', n="RightFoot_HipPivot_MultNode")
            mayac.setAttr("%s.input2X" %(self.RightFoot_HipPivot_MultNode), -1)
            mayac.connectAttr("%s.HipPivot" %(self.RightFoot.IK_CTRL), "%s.input1X" %(self.RightFoot_HipPivot_MultNode), force = True)
            mayac.connectAttr("%s.outputX" %(self.RightFoot_HipPivot_MultNode), "%s.rotateY" %(self.RightFoot.IK_CTRL_grandparent_inRig_CONST_GRP), force = True)
            
            self.RightFoot_BallPivot_MultNode = mayac.createNode( 'multiplyDivide', n="RightFoot_BallPivot_MultNode")
            mayac.setAttr("%s.input2X" %(self.RightFoot_BallPivot_MultNode), -1)
            mayac.connectAttr("%s.BallPivot" %(self.RightFoot.IK_CTRL), "%s.input1X" %(self.RightFoot_BallPivot_MultNode), force = True)
            mayac.connectAttr("%s.outputX" %(self.RightFoot_BallPivot_MultNode), "%s.input1D[1]" %(Right_ToeBase_ZAdd), force = True)
            mayac.connectAttr("%s.outputX" %(self.RightFoot_BallPivot_MultNode), "%s.rotateY" %(self.Right_Ankle_IK_CTRL), force = True)
            
            self.RightFoot_ToePivot_MultNode = mayac.createNode( 'multiplyDivide', n="RightFoot_ToePivot_MultNode")
            mayac.setAttr("%s.input2X" %(self.RightFoot_ToePivot_MultNode), -1)
            mayac.connectAttr("%s.ToePivot" %(self.RightFoot.IK_CTRL), "%s.input1X" %(self.RightFoot_ToePivot_MultNode), force = True)
            mayac.connectAttr("%s.outputX" %(self.RightFoot_ToePivot_MultNode), "%s.rotateY" %(self.Right_Toe_IK_CTRL), force = True)
            
            self.RightFoot_HipSideToSide_MultNode = mayac.createNode( 'multiplyDivide', n="RightFoot_HipSideToSide_MultNode")
            mayac.setAttr("%s.input2X" %(self.RightFoot_HipSideToSide_MultNode), -1)
            mayac.connectAttr("%s.HipSideToSide" %(self.RightFoot.IK_CTRL), "%s.input1X" %(self.RightFoot_HipSideToSide_MultNode), force = True)
            mayac.connectAttr("%s.outputX" %(self.RightFoot_HipSideToSide_MultNode), "%s.rotateZ" %(self.RightFoot.IK_CTRL_grandparent_inRig_CONST_GRP), force = True)
            
            mayac.connectAttr("%s.HipBackToFront" %(self.RightFoot.IK_CTRL), "%s.rotateX" %(self.RightFoot.IK_CTRL_grandparent_inRig_CONST_GRP), force = True)


        
        
        #finger SDKs
        if self.rigType == "AutoRig":
            if self.LeftHandIndex1.Bind_Joint:
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandIndex2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandIndex2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandIndex2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandIndex3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandIndex3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandIndex3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 45.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -45.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = -30.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = 12.0)
            else:
                mayac.deleteAttr("%s.IndexCurl"  % (self.LeftHand.Options_CTRL))
            if self.LeftHandMiddle1.Bind_Joint:
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandMiddle2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandMiddle2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandMiddle2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandMiddle3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandMiddle3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandMiddle3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 45.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -45.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = -10.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = 3.0)
            else:
                mayac.deleteAttr("%s.MiddleCurl"  % (self.LeftHand.Options_CTRL))    
            if self.LeftHandRing1.Bind_Joint:
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandRing2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandRing2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandRing2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandRing3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandRing3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandRing3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 45.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -45.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 15.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -5.0)
            else:
                mayac.deleteAttr("%s.RingCurl"  % (self.LeftHand.Options_CTRL))      
            if self.LeftHandPinky1.Bind_Joint:
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandPinky2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandPinky2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandPinky2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandPinky3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandPinky3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.LeftHandPinky3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 45.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -45.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 30.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -13.0)
            else:
                mayac.deleteAttr("%s.PinkyCurl"  % (self.LeftHand.Options_CTRL))    
            if self.LeftHandThumb1.Bind_Joint:
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandThumb1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandThumb1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 25.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandThumb1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -25.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandThumb2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandThumb2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 60.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandThumb2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -60.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandThumb3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandThumb3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandThumb3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandThumb1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandThumb2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandThumb1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = -15.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandThumb1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = 15.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandThumb2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = 30.0)
            else:
                mayac.deleteAttr("%s.ThumbCurl"  % (self.LeftHand.Options_CTRL))
            if not self.LeftHandPinky1.Bind_Joint and not self.LeftHandRing1.Bind_Joint and not self.LeftHandMiddle1.Bind_Joint and not self.LeftHandIndex1.Bind_Joint:
                mayac.deleteAttr("%s.Sway"  % (self.LeftHand.Options_CTRL))
                if not self.LeftHandThumb1.Bind_Joint:
                    mayac.deleteAttr("%s.Spread"  % (self.LeftHand.Options_CTRL))
                    
                    
            if self.RightHandIndex1.Bind_Joint:
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandIndex2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandIndex2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandIndex2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandIndex3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandIndex3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandIndex3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = -45.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = 45.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 30.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -12.0)
            else:
                mayac.deleteAttr("%s.IndexCurl"  % (self.RightHand.Options_CTRL))
            if self.RightHandMiddle1.Bind_Joint:
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandMiddle2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandMiddle2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandMiddle2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandMiddle3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandMiddle3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandMiddle3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = -45.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = 45.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 10.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -3.0)
            else:
                mayac.deleteAttr("%s.MiddleCurl"  % (self.RightHand.Options_CTRL))    
            if self.RightHandRing1.Bind_Joint:
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandRing2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandRing2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandRing2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandRing3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandRing3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandRing3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = -45.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = 45.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = -15.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = 5.0)
            else:
                mayac.deleteAttr("%s.RingCurl"  % (self.RightHand.Options_CTRL))      
            if self.RightHandPinky1.Bind_Joint:
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandPinky2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandPinky2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandPinky2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandPinky3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandPinky3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateX" % (self.RightHandPinky3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = -45.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = 45.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = -30.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = 13.0)
            else:
                mayac.deleteAttr("%s.PinkyCurl"  % (self.RightHand.Options_CTRL))    
            if self.RightHandThumb1.Bind_Joint:
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandThumb1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandThumb1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = -25.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandThumb1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = 25.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandThumb2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandThumb2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = -60.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandThumb2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = 60.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandThumb3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandThumb3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandThumb3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandThumb1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandThumb2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandThumb1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 15.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandThumb1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -15.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandThumb2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -30.0)
            else:
                mayac.deleteAttr("%s.ThumbCurl"  % (self.RightHand.Options_CTRL))
            if not self.RightHandPinky1.Bind_Joint and not self.RightHandRing1.Bind_Joint and not self.RightHandMiddle1.Bind_Joint and not self.RightHandIndex1.Bind_Joint:
                mayac.deleteAttr("%s.Sway"  % (self.RightHand.Options_CTRL))
                if not self.RightHandThumb1.Bind_Joint:
                    mayac.deleteAttr("%s.Spread"  % (self.RightHand.Options_CTRL))

        elif self.rigType == "World":
            if self.LeftHandIndex1.Bind_Joint:
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandIndex2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandIndex2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandIndex2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandIndex3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandIndex3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandIndex3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 45.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -45.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = -30.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = 12.0)
            else:
                mayac.deleteAttr("%s.IndexCurl"  % (self.LeftHand.Options_CTRL))
            if self.LeftHandMiddle1.Bind_Joint:
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandMiddle2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandMiddle2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandMiddle2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandMiddle3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandMiddle3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandMiddle3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 45.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -45.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = -10.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = 3.0)
            else:
                mayac.deleteAttr("%s.MiddleCurl"  % (self.LeftHand.Options_CTRL))    
            if self.LeftHandRing1.Bind_Joint:
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandRing2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandRing2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandRing2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandRing3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandRing3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandRing3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 45.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -45.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 15.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -5.0)
            else:
                mayac.deleteAttr("%s.RingCurl"  % (self.LeftHand.Options_CTRL))      
            if self.LeftHandPinky1.Bind_Joint:
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandPinky2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandPinky2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandPinky2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandPinky3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandPinky3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.LeftHandPinky3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 45.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -45.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 30.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -13.0)
            else:
                mayac.deleteAttr("%s.PinkyCurl"  % (self.LeftHand.Options_CTRL))    
            if self.LeftHandThumb1.Bind_Joint:
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandThumb1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandThumb1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 25.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandThumb1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -25.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandThumb2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandThumb2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 60.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandThumb2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -60.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandThumb3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandThumb3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandThumb3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandThumb1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandThumb2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandThumb1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = 10.0, value = -15.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandThumb1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = 15.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.LeftHandThumb2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.LeftHand.Options_CTRL), driverValue = -10.0, value = 30.0)
            else:
                mayac.deleteAttr("%s.ThumbCurl"  % (self.LeftHand.Options_CTRL))
            if not self.LeftHandPinky1.Bind_Joint and not self.LeftHandRing1.Bind_Joint and not self.LeftHandMiddle1.Bind_Joint and not self.LeftHandIndex1.Bind_Joint:
                mayac.deleteAttr("%s.Sway"  % (self.LeftHand.Options_CTRL))
                if not self.LeftHandThumb1.Bind_Joint:
                    mayac.deleteAttr("%s.Spread"  % (self.LeftHand.Options_CTRL))
                    
                    
            if self.RightHandIndex1.Bind_Joint:
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandIndex2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandIndex2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandIndex2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandIndex3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandIndex3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandIndex3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.IndexCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = -45.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = 45.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 30.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandIndex1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -12.0)
            else:
                mayac.deleteAttr("%s.IndexCurl"  % (self.RightHand.Options_CTRL))
            if self.RightHandMiddle1.Bind_Joint:
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandMiddle2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandMiddle2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandMiddle2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandMiddle3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandMiddle3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandMiddle3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.MiddleCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = -45.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = 45.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 10.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandMiddle1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -3.0)
            else:
                mayac.deleteAttr("%s.MiddleCurl"  % (self.RightHand.Options_CTRL))    
            if self.RightHandRing1.Bind_Joint:
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandRing2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandRing2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandRing2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandRing3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandRing3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandRing3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.RingCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = -45.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = 45.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = -15.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandRing1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = 5.0)
            else:
                mayac.deleteAttr("%s.RingCurl"  % (self.RightHand.Options_CTRL))      
            if self.RightHandPinky1.Bind_Joint:
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandPinky2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandPinky2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandPinky2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandPinky3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandPinky3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateZ" % (self.RightHandPinky3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.PinkyCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = -45.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Sway"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = 45.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = -30.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandPinky1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = 13.0)
            else:
                mayac.deleteAttr("%s.PinkyCurl"  % (self.RightHand.Options_CTRL))    
            if self.RightHandThumb1.Bind_Joint:
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandThumb1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandThumb1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = -25.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandThumb1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = 25.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandThumb2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandThumb2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = -60.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandThumb2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = 60.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandThumb3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandThumb3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = -90.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandThumb3.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.ThumbCurl"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = 90.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandThumb1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandThumb2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = 0.0, value = 0.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandThumb1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = 10.0, value = 15.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandThumb1.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -15.0)
                mayac.setDrivenKeyframe( "%s.rotateY" % (self.RightHandThumb2.FK_CTRL_inRig_CONST_GRP), currentDriver="%s.Spread"  % (self.RightHand.Options_CTRL), driverValue = -10.0, value = -30.0)
            else:
                mayac.deleteAttr("%s.ThumbCurl"  % (self.RightHand.Options_CTRL))
            if not self.RightHandPinky1.Bind_Joint and not self.RightHandRing1.Bind_Joint and not self.RightHandMiddle1.Bind_Joint and not self.RightHandIndex1.Bind_Joint:
                mayac.deleteAttr("%s.Sway"  % (self.RightHand.Options_CTRL))
                if not self.RightHandThumb1.Bind_Joint:
                    mayac.deleteAttr("%s.Spread"  % (self.RightHand.Options_CTRL))
            
            

        
        #global scale
        mayac.scaleConstraint(self.global_CTRL, self.Joint_GRP, name = "Global_Scale_Constraint")
        
        #IKFK switches
        self.LeftArm_Switch_Reverse = mayac.createNode( 'reverse', n="LeftArm_Switch_Reverse")
        self.RightArm_Switch_Reverse = mayac.createNode( 'reverse', n="RightArm_Switch_Reverse")
        self.LeftLeg_Switch_Reverse = mayac.createNode( 'reverse', n="LeftLeg_Switch_Reverse")
        self.RightLeg_Switch_Reverse = mayac.createNode( 'reverse', n="RightLeg_Switch_Reverse")
        mayac.connectAttr("%s.FK_IK" %(self.LeftHand.Options_CTRL), "%s.inputX" %(self.LeftArm_Switch_Reverse))
        mayac.connectAttr("%s.FK_IK" %(self.RightHand.Options_CTRL), "%s.inputX" %(self.RightArm_Switch_Reverse))
        mayac.connectAttr("%s.FK_IK" %(self.LeftFoot.Options_CTRL), "%s.inputX" %(self.LeftLeg_Switch_Reverse))
        mayac.connectAttr("%s.FK_IK" %(self.RightFoot.Options_CTRL), "%s.inputX" %(self.RightLeg_Switch_Reverse))
        
        mayac.setAttr("%s.interpType" %(self.LeftArm.Constraint), 2)
        mayac.setAttr("%s.interpType" %(self.LeftForeArm.Constraint), 2)
        mayac.setAttr("%s.interpType" %(self.LeftHand.Constraint), 2)
        mayac.setAttr("%s.interpType" %(self.RightArm.Constraint), 2)
        mayac.setAttr("%s.interpType" %(self.RightForeArm.Constraint), 2)
        mayac.setAttr("%s.interpType" %(self.RightHand.Constraint), 2)
        mayac.setAttr("%s.interpType" %(self.LeftUpLeg.Constraint), 2)
        mayac.setAttr("%s.interpType" %(self.LeftLeg.Constraint), 2)
        mayac.setAttr("%s.interpType" %(self.LeftFoot.Constraint), 2)
        mayac.setAttr("%s.interpType" %(self.LeftToeBase.Constraint), 2)
        mayac.setAttr("%s.interpType" %(self.RightUpLeg.Constraint), 2)
        mayac.setAttr("%s.interpType" %(self.RightLeg.Constraint), 2)
        mayac.setAttr("%s.interpType" %(self.RightFoot.Constraint), 2)
        mayac.setAttr("%s.interpType" %(self.RightToeBase.Constraint), 2)
        
        mayac.connectAttr("%s.FK_IK" %(self.LeftHand.Options_CTRL), "%s.%sW1" %(self.LeftArm.Constraint, self.LeftArm.IK_Joint))
        mayac.connectAttr("%s.outputX" %(self.LeftArm_Switch_Reverse), "%s.%sW0" %(self.LeftArm.Constraint, self.LeftArm.FK_Joint))
        mayac.connectAttr("%s.FK_IK" %(self.LeftHand.Options_CTRL), "%s.%sW1" %(self.LeftForeArm.Constraint, self.LeftForeArm.IK_Joint))
        mayac.connectAttr("%s.outputX" %(self.LeftArm_Switch_Reverse), "%s.%sW0" %(self.LeftForeArm.Constraint, self.LeftForeArm.FK_Joint))
        mayac.connectAttr("%s.FK_IK" %(self.LeftHand.Options_CTRL), "%s.%sW1" %(self.LeftHand.Constraint, self.LeftHand.IK_Joint))
        mayac.connectAttr("%s.outputX" %(self.LeftArm_Switch_Reverse), "%s.%sW0" %(self.LeftHand.Constraint, self.LeftHand.FK_Joint))
        mayac.connectAttr("%s.FK_IK" %(self.RightHand.Options_CTRL), "%s.%sW1" %(self.RightArm.Constraint, self.RightArm.IK_Joint))
        mayac.connectAttr("%s.outputX" %(self.RightArm_Switch_Reverse), "%s.%sW0" %(self.RightArm.Constraint, self.RightArm.FK_Joint))
        mayac.connectAttr("%s.FK_IK" %(self.RightHand.Options_CTRL), "%s.%sW1" %(self.RightForeArm.Constraint, self.RightForeArm.IK_Joint))
        mayac.connectAttr("%s.outputX" %(self.RightArm_Switch_Reverse), "%s.%sW0" %(self.RightForeArm.Constraint, self.RightForeArm.FK_Joint))
        mayac.connectAttr("%s.FK_IK" %(self.RightHand.Options_CTRL), "%s.%sW1" %(self.RightHand.Constraint, self.RightHand.IK_Joint))
        mayac.connectAttr("%s.outputX" %(self.RightArm_Switch_Reverse), "%s.%sW0" %(self.RightHand.Constraint, self.RightHand.FK_Joint))
        
        mayac.connectAttr("%s.FK_IK" %(self.LeftFoot.Options_CTRL), "%s.%sW1" %(self.LeftUpLeg.Constraint, self.LeftUpLeg.IK_Joint))
        mayac.connectAttr("%s.outputX" %(self.LeftLeg_Switch_Reverse), "%s.%sW0" %(self.LeftUpLeg.Constraint, self.LeftUpLeg.FK_Joint))
        mayac.connectAttr("%s.FK_IK" %(self.LeftFoot.Options_CTRL), "%s.%sW1" %(self.LeftLeg.Constraint, self.LeftLeg.IK_Joint))
        mayac.connectAttr("%s.outputX" %(self.LeftLeg_Switch_Reverse), "%s.%sW0" %(self.LeftLeg.Constraint, self.LeftLeg.FK_Joint))
        mayac.connectAttr("%s.FK_IK" %(self.LeftFoot.Options_CTRL), "%s.%sW1" %(self.LeftFoot.Constraint, self.LeftFoot.IK_Joint))
        mayac.connectAttr("%s.outputX" %(self.LeftLeg_Switch_Reverse), "%s.%sW0" %(self.LeftFoot.Constraint, self.LeftFoot.FK_Joint))
        mayac.connectAttr("%s.FK_IK" %(self.LeftFoot.Options_CTRL), "%s.%sW1" %(self.LeftToeBase.Constraint, self.LeftToeBase.IK_Joint))
        mayac.connectAttr("%s.outputX" %(self.LeftLeg_Switch_Reverse), "%s.%sW0" %(self.LeftToeBase.Constraint, self.LeftToeBase.FK_Joint))
        mayac.connectAttr("%s.FK_IK" %(self.RightFoot.Options_CTRL), "%s.%sW1" %(self.RightUpLeg.Constraint, self.RightUpLeg.IK_Joint))
        mayac.connectAttr("%s.outputX" %(self.RightLeg_Switch_Reverse), "%s.%sW0" %(self.RightUpLeg.Constraint, self.RightUpLeg.FK_Joint))
        mayac.connectAttr("%s.FK_IK" %(self.RightFoot.Options_CTRL), "%s.%sW1" %(self.RightLeg.Constraint, self.RightLeg.IK_Joint))
        mayac.connectAttr("%s.outputX" %(self.RightLeg_Switch_Reverse), "%s.%sW0" %(self.RightLeg.Constraint, self.RightLeg.FK_Joint))
        mayac.connectAttr("%s.FK_IK" %(self.RightFoot.Options_CTRL), "%s.%sW1" %(self.RightFoot.Constraint, self.RightFoot.IK_Joint))
        mayac.connectAttr("%s.outputX" %(self.RightLeg_Switch_Reverse), "%s.%sW0" %(self.RightFoot.Constraint, self.RightFoot.FK_Joint))
        mayac.connectAttr("%s.FK_IK" %(self.RightFoot.Options_CTRL), "%s.%sW1" %(self.RightToeBase.Constraint, self.RightToeBase.IK_Joint))
        mayac.connectAttr("%s.outputX" %(self.RightLeg_Switch_Reverse), "%s.%sW0" %(self.RightToeBase.Constraint, self.RightToeBase.FK_Joint))
        
        #FKIK Visibilities
        DJB_Unlock_Connect_Lock("%s.FK_IK" %(self.LeftHand.Options_CTRL), "%s.visibility" %(self.LeftArm.IK_Joint))
        DJB_Unlock_Connect_Lock("%s.FK_IK" %(self.LeftHand.Options_CTRL), "%s.visibility" %(self.LeftForeArm.IK_CTRL_POS_GRP))
        DJB_Unlock_Connect_Lock("%s.FK_IK" %(self.LeftHand.Options_CTRL), "%s.visibility" %(self.LeftHand.IK_CTRL_POS_GRP))
        DJB_Unlock_Connect_Lock("%s.FK_IK" %(self.RightHand.Options_CTRL), "%s.visibility" %(self.RightArm.IK_Joint))
        DJB_Unlock_Connect_Lock("%s.FK_IK" %(self.RightHand.Options_CTRL), "%s.visibility" %(self.RightForeArm.IK_CTRL_POS_GRP))
        DJB_Unlock_Connect_Lock("%s.FK_IK" %(self.RightHand.Options_CTRL), "%s.visibility" %(self.RightHand.IK_CTRL_POS_GRP))

        DJB_Unlock_Connect_Lock("%s.FK_IK" %(self.LeftFoot.Options_CTRL), "%s.visibility" %(self.LeftUpLeg.IK_Joint))
        DJB_Unlock_Connect_Lock("%s.FK_IK" %(self.LeftFoot.Options_CTRL), "%s.visibility" %(self.LeftLeg.IK_CTRL_POS_GRP))
        DJB_Unlock_Connect_Lock("%s.FK_IK" %(self.LeftFoot.Options_CTRL), "%s.visibility" %(self.LeftFoot.IK_CTRL_POS_GRP))
        DJB_Unlock_Connect_Lock("%s.FK_IK" %(self.RightFoot.Options_CTRL), "%s.visibility" %(self.RightUpLeg.IK_Joint))
        DJB_Unlock_Connect_Lock("%s.FK_IK" %(self.RightFoot.Options_CTRL), "%s.visibility" %(self.RightLeg.IK_CTRL_POS_GRP))
        DJB_Unlock_Connect_Lock("%s.FK_IK" %(self.RightFoot.Options_CTRL), "%s.visibility" %(self.RightFoot.IK_CTRL_POS_GRP))
     
        DJB_Unlock_Connect_Lock("%s.outputX" %(self.LeftArm_Switch_Reverse), "%s.visibility" %(self.LeftArm.FK_Joint))
        DJB_Unlock_Connect_Lock("%s.outputX" %(self.LeftArm_Switch_Reverse), "%s.visibility" %(self.LeftArm.FK_CTRL_POS_GRP))
        DJB_Unlock_Connect_Lock("%s.outputX" %(self.RightArm_Switch_Reverse), "%s.visibility" %(self.RightArm.FK_Joint))
        DJB_Unlock_Connect_Lock("%s.outputX" %(self.RightArm_Switch_Reverse), "%s.visibility" %(self.RightArm.FK_CTRL_POS_GRP))
        
        DJB_Unlock_Connect_Lock("%s.outputX" %(self.LeftLeg_Switch_Reverse), "%s.visibility" %(self.LeftUpLeg.FK_Joint))
        DJB_Unlock_Connect_Lock("%s.outputX" %(self.LeftLeg_Switch_Reverse), "%s.visibility" %(self.LeftUpLeg.FK_CTRL_POS_GRP))
        DJB_Unlock_Connect_Lock("%s.outputX" %(self.RightLeg_Switch_Reverse), "%s.visibility" %(self.RightUpLeg.FK_Joint))
        DJB_Unlock_Connect_Lock("%s.outputX" %(self.RightLeg_Switch_Reverse), "%s.visibility" %(self.RightUpLeg.FK_CTRL_POS_GRP))
        
        mayac.select(clear = True)
        self.Misc_GRP = mayac.group(em = True, name = "Misc_GRP", world = True)
        DJB_movePivotToObject(self.Misc_GRP, self.global_CTRL)
        mayac.parent(self.Misc_GRP, self.Character_GRP)
        self.LeftForeArm.createGuideCurve(self.Misc_GRP, optionsCTRL = self.LeftHand.Options_CTRL)
        self.RightForeArm.createGuideCurve(self.Misc_GRP, optionsCTRL = self.RightHand.Options_CTRL)
        self.LeftLeg.createGuideCurve(self.Misc_GRP, optionsCTRL = self.LeftFoot.Options_CTRL)
        self.RightLeg.createGuideCurve(self.Misc_GRP, optionsCTRL = self.RightFoot.Options_CTRL)
        
        if self.LeftEye.Bind_Joint and self.RightEye.Bind_Joint:
            mayac.addAttr(self.Head.FK_CTRL, longName='EyesFollowAim', defaultValue=1.0, min = 0.0, max = 1.0, keyable = True)
            self.FacialMiscGRP = mayac.group(em=True, n="Facial_Misc_GRP")
            mayac.parent(self.FacialMiscGRP, self.Character_GRP)
            self.LeftEye.createGuideCurve(self.FacialMiscGRP, optionsCTRL = self.Head.FK_CTRL, attr="EyesFollowAim")
            self.RightEye.createGuideCurve(self.FacialMiscGRP, optionsCTRL = self.Head.FK_CTRL, attr="EyesFollowAim")
            mayac.connectAttr("%s.EyesFollowAim"%self.Head.FK_CTRL, "%s.visibility"%self.FacialControls.Eyes_CTRL.Aim_CTRL)
            EyesFollowAimReverse = mayac.createNode( 'reverse', n="EyesFollowAimReverse")
            mayac.connectAttr("%s.EyesFollowAim"%self.Head.FK_CTRL, "%s.inputX" %EyesFollowAimReverse)
            DJB_Unlock_Connect_Lock("%s.outputX" %EyesFollowAimReverse, "%s.visibility"%self.LeftEye.FK_CTRL)
            DJB_Unlock_Connect_Lock("%s.outputX" %EyesFollowAimReverse, "%s.visibility"%self.RightEye.FK_CTRL)
            DJB_LockNHide(self.FacialControls.Eyes_CTRL.Aim_CTRL, tx = False, ty = False, tz = False, rx = False, ry = False, rz = False)
            for Eye in [self.LeftEye, self.RightEye]:
                for attr in mayac.listAttr(Eye.Constraint, ud=True):
                    if "IK" in attr:
                        mayac.connectAttr("%s.EyesFollowAim"%self.Head.FK_CTRL, "%s.%s" %(Eye.Constraint,attr))
                    elif "FK" in attr:
                        mayac.connectAttr("%s.outputX" %EyesFollowAimReverse, "%s.%s" %(Eye.Constraint,attr))
            

        #Layers
        mayac.select(clear = True)
        self.Mesh_Layer = mayac.createDisplayLayer(name = "MeshLayer", number = 1)
        mayac.editDisplayLayerMembers(self.Mesh_Layer, self.Mesh_GRP)
        self.Bind_Joint_Layer = mayac.createDisplayLayer(name = "BindJointLayer", number = 2)
        mayac.editDisplayLayerMembers(self.Bind_Joint_Layer, self.Bind_Joint_GRP)
        #self.AnimData_Joint_Layer = mayac.createDisplayLayer(name = "AnimDataJointLayer", number = 3)
        #mayac.editDisplayLayerMembers(self.AnimData_Joint_Layer, self.AnimData_Joint_GRP)
        mayac.setAttr("%s.visibility" % (self.AnimData_Joint_GRP), 0)
        self.Control_Layer = mayac.createDisplayLayer(name = "ControlLayer", number = 4)
        mayac.editDisplayLayerMembers(self.Control_Layer, self.CTRL_GRP)
        mayac.editDisplayLayerMembers(self.Control_Layer, self.Misc_GRP)
        mayac.setAttr("%s.visibility" %(self.Mesh_Layer), 1)
        mayac.setAttr("%s.displayType" %(self.Mesh_Layer), 2)
        mayac.setAttr("%s.visibility" %(self.Bind_Joint_Layer), 0)
        mayac.setAttr("%s.displayType" %(self.Bind_Joint_Layer), 2)
        #mayac.setAttr("%s.visibility" %(self.AnimData_Joint_Layer), 0)
        #mayac.setAttr("%s.displayType" %(self.AnimData_Joint_Layer), 2)
        
        for bodyPart in self.bodyParts:
            if "Eye" not in bodyPart.nodeName:
                bodyPart.fixAllLayerOverrides(self.Control_Layer)
            else:
                bodyPart.fixAllLayerOverrides(self.FacialControl_Layer)
        self.Hips.fixLayerOverrides(self.global_CTRL, "black", self.Control_Layer)
        self.Hips.fixLayerOverrides(self.LeftForeArm.Guide_Curve, "black", self.Control_Layer, referenceAlways = True)
        self.Hips.fixLayerOverrides(self.RightForeArm.Guide_Curve, "black", self.Control_Layer, referenceAlways = True)
        self.Hips.fixLayerOverrides(self.LeftLeg.Guide_Curve, "black", self.Control_Layer, referenceAlways = True)
        self.Hips.fixLayerOverrides(self.RightLeg.Guide_Curve, "black", self.Control_Layer, referenceAlways = True)
        if self.LeftEye.Bind_Joint and self.RightEye.Bind_Joint:
            self.Hips.fixLayerOverrides(self.LeftEye.Guide_Curve, "black", self.FacialControl_Layer, referenceAlways = True)
            self.Hips.fixLayerOverrides(self.RightEye.Guide_Curve, "black", self.FacialControl_Layer, referenceAlways = True)
         
         
        #quick select sets
        mayac.select(clear = True)
        for bodyPart in self.bodyParts:
            if bodyPart.Bind_Joint:
                mayac.select(bodyPart.Bind_Joint, add = True)
        self.Bind_Joint_SelectSet = mayac.sets(text = "gCharacterSet", name = "Bind_Joint_SelectSet")
        #mayac.select(clear = True)
        #for bodyPart in self.bodyParts:
            #if bodyPart.AnimData_Joint:
                #mayac.select(bodyPart.AnimData_Joint, add = True)
        #self.AnimData_Joint_SelectSet = mayac.sets(text = "gCharacterSet", name = "AnimData_Joint_SelectSet")
        mayac.select(clear = True)
        for bodyPart in self.bodyParts:
            if bodyPart.FK_CTRL:
                mayac.select(bodyPart.FK_CTRL, add = True)
            if bodyPart.IK_CTRL:
                mayac.select(bodyPart.IK_CTRL, add = True)
            if bodyPart.Options_CTRL:
                mayac.select(bodyPart.Options_CTRL, add = True)
        mayac.select(self.global_CTRL, add = True)
        self.Controls_SelectSet = mayac.sets(text = "gCharacterSet", name = "Controls_SelectSet")
        mayac.select(clear = True)
        for geo in self.mesh:
            mayac.select(geo, add = True)
        self.Geo_SelectSet = mayac.sets(text = "gCharacterSet", name = "Geo_SelectSet")
        mayac.select(clear = True)
        
        #Cleanup
        mayac.delete(self.LeftFoot.footRotateLOC)
        mayac.delete(self.RightFoot.footRotateLOC)
        DJB_LockNHide(self.Character_GRP)
        DJB_LockNHide(self.CTRL_GRP)
        DJB_LockNHide(self.Joint_GRP)
        DJB_LockNHide(self.Bind_Joint_GRP)
        DJB_LockNHide(self.AnimData_Joint_GRP)
        DJB_LockNHide(self.Mesh_GRP)
        DJB_LockNHide(self.Misc_GRP)
        mayac.setAttr("%s.visibility" % (self.IK_Dummy_Joint_GRP), 0)
        DJB_LockNHide(self.IK_Dummy_Joint_GRP)
        
        DJB_LockNHide(self.Left_ToeBase_IkHandle)
        DJB_LockNHide(self.Right_ToeBase_IkHandle)
        DJB_LockNHide(self.Left_Ankle_IK_CTRL)
        DJB_LockNHide(self.Left_ToeBase_IK_CTRL)
        DJB_LockNHide(self.Left_ToeBase_IK_AnimData_GRP)
        DJB_LockNHide(self.Left_Ankle_IK_AnimData_GRP)
        DJB_LockNHide(self.Left_Toe_IK_CTRL)
        DJB_LockNHide(self.Left_Toe_IK_AnimData_GRP)
        DJB_LockNHide(self.Right_Ankle_IK_CTRL)
        DJB_LockNHide(self.Right_ToeBase_IK_CTRL)
        DJB_LockNHide(self.Right_ToeBase_IK_AnimData_GRP)
        DJB_LockNHide(self.Right_Ankle_IK_AnimData_GRP)
        DJB_LockNHide(self.Right_Toe_IK_CTRL)
        DJB_LockNHide(self.Right_Toe_IK_AnimData_GRP)

        
        
        
        #lock CTRLS
        for bodyPart in self.bodyParts:
            bodyPart.lockUpCTRLs()
        
        #defaultValues
        mayac.setAttr("%s.FK_IK" % (self.LeftFoot.Options_CTRL), 1)
        mayac.setAttr("%s.FK_IK" % (self.RightFoot.Options_CTRL), 1)
        mayac.setAttr("%s.FK_IK" % (self.LeftHand.Options_CTRL), 0)
        mayac.setAttr("%s.FK_IK" % (self.RightHand.Options_CTRL), 0)
        
        mayac.setAttr("%s.FollowBody" % (self.LeftHand.IK_CTRL), 0)
        mayac.setAttr("%s.FollowBody" % (self.RightHand.IK_CTRL), 0)
        mayac.setAttr("%s.FollowBody" % (self.LeftForeArm.IK_CTRL), 0)
        mayac.setAttr("%s.FollowBody" % (self.RightForeArm.IK_CTRL), 0)
        mayac.setAttr("%s.FollowBody" % (self.LeftFoot.IK_CTRL), 0)
        mayac.setAttr("%s.FollowBody" % (self.RightFoot.IK_CTRL), 0)
        mayac.setAttr("%s.FollowBody" % (self.LeftLeg.IK_CTRL), 0)
        mayac.setAttr("%s.FollowBody" % (self.RightLeg.IK_CTRL), 0)
        
        selfPOS = mayac.xform(self.LeftLeg.Bind_Joint, query = True, absolute = True, worldSpace = True, translation = True)
        parentPOS = mayac.xform(self.LeftLeg.parent.Bind_Joint, query = True, absolute = True, worldSpace = True, translation = True)
        tempDistance = math.sqrt((selfPOS[0]-parentPOS[0])*(selfPOS[0]-parentPOS[0]) + (selfPOS[1]-parentPOS[1])*(selfPOS[1]-parentPOS[1]) + (selfPOS[2]-parentPOS[2])*(selfPOS[2]-parentPOS[2]))
        mayac.setAttr("%s.translateZ" % (self.LeftLeg.IK_CTRL), tempDistance / 2)
        mayac.setAttr("%s.translateZ" % (self.RightLeg.IK_CTRL), tempDistance / 2)
        if self.rigType == "AutoRig":
            mayac.setAttr("%s.translateX" % (self.LeftForeArm.IK_CTRL), tempDistance / 2)
            mayac.setAttr("%s.translateX" % (self.RightForeArm.IK_CTRL), tempDistance / -2)
        elif self.rigType == "World":
            mayac.setAttr("%s.translateZ" % (self.LeftForeArm.IK_CTRL), tempDistance / -2)
            mayac.setAttr("%s.translateZ" % (self.RightForeArm.IK_CTRL), tempDistance / -2)
        DJB_LockNHide(self.global_CTRL, tx = False, ty = False, tz = False, rx = False, ry = False, rz = False, s = False, v = True)
        
        #wiggle ik controls
        mayac.refresh()
        for ctrl in [self.LeftHand.IK_CTRL, self.RightHand.IK_CTRL, self.LeftFoot.IK_CTRL, self.RightFoot.IK_CTRL]:
            mayac.setAttr("%s.ty" % (ctrl), 2.0)
        mayac.refresh()
        for ctrl in [self.LeftHand.IK_CTRL, self.RightHand.IK_CTRL, self.LeftFoot.IK_CTRL, self.RightFoot.IK_CTRL]:
            mayac.setAttr("%s.ty" % (ctrl), 0.0)
        mayac.refresh()
        
        mel.eval("escapeCurrentTool;")
        OpenMaya.MGlobal.displayInfo("Rig Complete")

        
    def checkSkeletonProportions(self, incomingDataRootJoint):
        return True
        proportionCheckTolerance = .03
        success = True
        New_joint_Namespace = DJB_findBeforeSeparator(incomingDataRootJoint, ':')
        if not self.hulaOption and "Root" in incomingDataRootJoint:
            print "failing because of hula"
            success = False
        for bodyPart in self.bodyParts:
            if bodyPart.children and bodyPart.nodeName != "Root" and bodyPart.Bind_Joint:
                selfPOS = mayac.xform(bodyPart.Bind_Joint, query = True, absolute = True, worldSpace = True, translation = True)
                if not mayac.objExists("%s%s" % (New_joint_Namespace, bodyPart.nodeName)):
                    print "failing becuase of %s%s not existing"%(New_joint_Namespace, bodyPart.nodeName)
                    success = False
                    break
                else:
                    DataSelfPOS = mayac.xform("%s%s" % (New_joint_Namespace, bodyPart.nodeName), query = True, absolute = True, worldSpace = True, translation = True)
                    for child in bodyPart.children:
                        if child in self.bodyParts:
                            if child.Bind_Joint and "End" not in child.nodeName:
                                childPOS = mayac.xform(child.Bind_Joint, query = True, absolute = True, worldSpace = True, translation = True)
                                if not mayac.objExists("%s%s" % (New_joint_Namespace, child.nodeName)):
                                    print "failing becuase of %s%s not existing"%(New_joint_Namespace, child.nodeName)
                                    success = False
                                    break
                                else:
                                    DataChildPOS = mayac.xform("%s%s" % (New_joint_Namespace, child.nodeName), query = True, absolute = True, worldSpace = True, translation = True)
                                    correctDistance = math.sqrt((selfPOS[0]-childPOS[0])*(selfPOS[0]-childPOS[0]) + (selfPOS[1]-childPOS[1])*(selfPOS[1]-childPOS[1]) + (selfPOS[2]-childPOS[2])*(selfPOS[2]-childPOS[2])) / mayac.getAttr("%s.scaleX" % (self.global_CTRL))
                                    distanceInQuestion = math.sqrt((DataSelfPOS[0]-DataChildPOS[0])*(DataSelfPOS[0]-DataChildPOS[0]) + (DataSelfPOS[1]-DataChildPOS[1])*(DataSelfPOS[1]-DataChildPOS[1]) + (DataSelfPOS[2]-DataChildPOS[2])*(DataSelfPOS[2]-DataChildPOS[2]))
                                    if not math.fabs(distanceInQuestion/correctDistance) > 1 - proportionCheckTolerance or not math.fabs(distanceInQuestion/correctDistance) < 1 + proportionCheckTolerance:
                                        print "Failing because proportions are incorrect for %s%s"%(New_joint_Namespace, bodyPart.nodeName)
                                        success = False
                                        break
                                if bodyPart.rotOrder != mayac.getAttr("%s.rotateOrder" % (New_joint_Namespace + bodyPart.nodeName)):
                                    print "Failing because rotation Orders are incorrect for %s%s"%(New_joint_Namespace, bodyPart.nodeName)
                                    success = False
                                    break
        return success
        
        
    def connectMotionToAnimDataJoints(self, incomingDataRootJoint): 
        mayac.currentTime(1)
        New_joint_Namespace = DJB_findBeforeSeparator(incomingDataRootJoint, ':')
        curJoint = 0.0
        objectsOfInterest = []
        for bodyPart in self.bodyParts:
            if bodyPart.nodeName == "Root" and self.hulaOption:
                if mayac.objExists("%sRoot" % (New_joint_Namespace)):
                    objectsOfInterest.append("%sRoot" % (New_joint_Namespace))
                    DJB_ConnectAll("%sRoot" % (New_joint_Namespace), bodyPart.AnimData_Joint)
                else:
                    objectsOfInterest.append("%sHips" % (New_joint_Namespace))
                    DJB_ConnectAll("%sHips" % (New_joint_Namespace), bodyPart.AnimData_Joint)
            elif bodyPart.nodeName == "Hips" and self.hulaOption and mayac.objExists("%sRoot" % (New_joint_Namespace)):
                objectsOfInterest.append("%sHips" % (New_joint_Namespace))
                DJB_ConnectAll("%sHips" % (New_joint_Namespace), bodyPart.AnimData_Joint)
            elif bodyPart.nodeName == "Hips" and not self.hulaOption:
                objectsOfInterest.append("%sHips" % (New_joint_Namespace))
                DJB_ConnectAll("%sHips" % (New_joint_Namespace), bodyPart.AnimData_Joint)
            elif bodyPart.nodeName not in ["Hips", "HeadTop_End", "LeftHandThumb4", "LeftHandIndex4", "LeftHandMiddle4", "LeftHandRing4", "LeftHandPinky4", "LeftToe_End", "RightHandThumb4", "RightHandIndex4", "RightHandMiddle4", "RightHandRing4", "RightHandPinky4", "RightToe_End"]:
                newAnimDataJoint = "%s%s" % (New_joint_Namespace, bodyPart.nodeName)
                if mayac.objExists(newAnimDataJoint):
                    objectsOfInterest.append(newAnimDataJoint)
                    DJB_ConnectAll(newAnimDataJoint, bodyPart.AnimData_Joint)
            curJoint += 1
        
        ##adjust timeline to fit animation
        #find first and last frames
        howManyKeys = []
        last = 0
        highestTime = -999999999
        lowestTime = 99999999
        for obj in objectsOfInterest:
            myKeys = mayac.keyframe(obj, query = True, name = True)
            if myKeys:
                howManyKeys = mayac.keyframe(myKeys[0], query = True, timeChange = True)
                last = len(howManyKeys)-1
                if howManyKeys[last] > highestTime:
                    highestTime = howManyKeys[last]
                if howManyKeys[0] < lowestTime:
                    lowestTime = howManyKeys[0]
        
        startTime = lowestTime
        endTime = highestTime
        if startTime != 99999999 and endTime != -999999999:
            mayac.playbackOptions(minTime = startTime, maxTime = highestTime)
        
        OpenMaya.MGlobal.displayInfo("Animation Data Connected")
        
        
        
        
    def transferMotionToAnimDataJoints(self, incomingDataRootJoint, newStartTime = 0, mixMethod = "insert", directConnect_ = False): #mixMethod - insert or merge
        mayac.currentTime(1)
        New_joint_Namespace = DJB_findBeforeSeparator(incomingDataRootJoint, ':')
        keyList = mayac.keyframe("%s.translateX"%(incomingDataRootJoint),query = True, timeChange = True)
        if keyList:
            lastFrame = keyList[len(keyList)-1]
            curJoint = 0.0
            gMainProgressBar = mel.eval('$tmp = $gMainProgressBar');
            if not directConnect_:
                mayac.progressBar( gMainProgressBar,
                               edit=True,
                               beginProgress=True,
                               isInterruptable=True,
                               status='Copying Keyframes for joint %d/%d ...' % (curJoint, len(self.bodyParts)-1),
                               maxValue=lastFrame )
                for bodyPart in self.bodyParts:
                    if mayac.progressBar(gMainProgressBar, query=True, isCancelled=True ) :
                        break
                    if bodyPart.nodeName == "Root" and self.hulaOption:
                        if mayac.objExists("%sRoot" % (New_joint_Namespace)):
                            mayac.copyKey("%sRoot" % (New_joint_Namespace), time = (0,lastFrame), hierarchy = "none", controlPoints = 0, shape = 1)
                            mayac.pasteKey(bodyPart.AnimData_Joint, option = mixMethod, connect = 1, timeOffset = newStartTime, valueOffset = 0)
                        else:
                            mayac.copyKey("%sHips" % (New_joint_Namespace), time = (0,lastFrame), hierarchy = "none", controlPoints = 0, shape = 1)
                            mayac.pasteKey(bodyPart.AnimData_Joint, option = mixMethod, connect = 1, timeOffset = newStartTime, valueOffset = 0)
                    elif bodyPart.nodeName == "Hips" and self.hulaOption and mayac.objExists("%sRoot" % (New_joint_Namespace)):
                        mayac.copyKey("%sHips" % (New_joint_Namespace), time = (0,lastFrame), hierarchy = "none", controlPoints = 0, shape = 1)
                        mayac.pasteKey(bodyPart.AnimData_Joint, option = mixMethod, connect = 1, timeOffset = newStartTime, valueOffset = 0)
                    elif bodyPart.nodeName == "Hips" and not self.hulaOption:
                        mayac.copyKey("%sHips" % (New_joint_Namespace), time = (0,lastFrame), hierarchy = "none", controlPoints = 0, shape = 1)
                        mayac.pasteKey(bodyPart.AnimData_Joint, option = mixMethod, connect = 1, timeOffset = newStartTime, valueOffset = 0)
                    elif bodyPart.nodeName not in ["Hips", "HeadTop_End", "LeftHandThumb4", "LeftHandIndex4", "LeftHandMiddle4", "LeftHandRing4", "LeftHandPinky4", "LeftToe_End", "RightHandThumb4", "RightHandIndex4", "RightHandMiddle4", "RightHandRing4", "RightHandPinky4", "RightToe_End"]:
                        newAnimDataJoint = "%s%s" % (New_joint_Namespace, bodyPart.nodeName)
                        if mayac.objExists(newAnimDataJoint):
                            numCurves = mayac.copyKey(newAnimDataJoint, time = (0,lastFrame), hierarchy = "none", controlPoints = 0, shape = 1)
                            if numCurves:
                                mayac.pasteKey(bodyPart.AnimData_Joint, option = mixMethod, connect = 1, timeOffset = newStartTime, valueOffset = 0)
                    mayac.progressBar(gMainProgressBar, edit=True, step=1)    
                    curJoint += 1
            mayac.progressBar(gMainProgressBar, edit=True, endProgress=True)
        sClusters = []
        sClusters = mayac.listConnections(incomingDataRootJoint, destination = True, type = "skinCluster")
        for joint in mayac.listRelatives(incomingDataRootJoint, allDescendents = True, type = 'joint'):
            checkClusterList = mayac.listConnections(joint, destination = True, type = "skinCluster")
            if checkClusterList:
                for checkCluster in checkClusterList:
                    if checkCluster not in sClusters:
                        sClusters.append(checkCluster)
        self.origAnim = mayac.group(incomingDataRootJoint, name = "Original_Animation_GRP")
        if sClusters:
            for sCluster in sClusters:
                shapes =  mayac.listConnections(sCluster, destination = True, type = "mesh")
                if shapes:
                    for shape in shapes:
                        parent = mayac.listRelatives(shape, parent = True)
                        if parent and self.origAnim not in parent:
                            DJB_Unlock(shape)
                            while "Original_Animation_" not in shape:
                                shape = mayac.rename(shape, "Original_Animation_%s" % (shape))
                            shape = mayac.parent(shape, self.origAnim)[0]
                        if not parent:
                            DJB_Unlock(shape)
                            while "Original_Animation_" not in shape:
                                shape = mayac.rename(shape, "Original_Animation_%s" % (shape))
                            shape = mayac.parent(shape, self.origAnim)[0]
                        #see if there are blendshapes
                        meshShapes = mayac.listRelatives(shape, children=True, shapes=True)
                        blendShapeNodes = set()
                        for meshShape in meshShapes:
                            print meshShape
                            connections = mayac.listConnections(meshShape)
                            for con in connections:
                                if mayac.nodeType(con) == "blendShape":
                                    blendShapeNodes.add(con)
                                concons = mayac.listConnections(con)
                                for concon in concons:
                                    if mayac.nodeType(concon) == "blendShape":
                                        blendShapeNodes.add(concon)
                        if blendShapeNodes:
                            for blendShapeNode in list(blendShapeNodes):
                                blendShapeNode = mayac.rename(blendShapeNode, "Original_Animation_%s"%blendShapeNode)
                                connections = mayac.listConnections(blendShapeNode, s=True)
                                for con in connections:
                                    if mayac.nodeType(con) == "transform":
                                        DJB_Unlock(con)
                                        while "Original_Animation_" not in con:
                                            con = mayac.rename(con, "Original_Animation_%s" % (con))
                                        try:
                                            mayac.parent(con, self.origAnim)
                                        except:
                                            pass
        
        if not directConnect_:
            #rename orig anim joints
            for bodyPart in self.bodyParts:
                if mayac.objExists("%s%s" % (New_joint_Namespace, bodyPart.nodeName)):
                    mayac.rename("%s%s" % (New_joint_Namespace, bodyPart.nodeName), "Original_Animation_%s" % (bodyPart.nodeName))
            if self.ExtraJoints:
                for extraJoint in self.ExtraJoints:
                    if mayac.objExists("%s%s" % (New_joint_Namespace, extraJoint.nodeName)):
                        mayac.rename("%s%s" % (New_joint_Namespace, extraJoint.nodeName), "Original_Animation_%s" % (extraJoint.nodeName))
            
            mayac.parent(self.origAnim, self.Character_GRP)
            self.origAnimation_Layer = mayac.createDisplayLayer(name = "OrigAnimationLayer", number = 1)
            mayac.editDisplayLayerMembers(self.origAnimation_Layer, self.origAnim)
            mayac.setAttr("%s.visibility" %(self.origAnimation_Layer), 0)
            mayac.setAttr("%s.displayType" %(self.origAnimation_Layer), 2)
            #update infoNode
            pyToAttr("%s.origAnim" % (self.infoNode), self.origAnim)
            pyToAttr("%s.origAnimation_Layer" % (self.infoNode), self.origAnimation_Layer)
        
        
        ##adjust timeline to fit animation
        #find first and last frames
        howManyKeys = []
        last = 0
        highestTime = -999999999
        lowestTime = 99999999
        objectsOfInterest = []
        for bodyPart in self.bodyParts:
            if "4" not in bodyPart.nodeName and "End" not in bodyPart.nodeName:
                if bodyPart.FK_CTRL:
                    objectsOfInterest.append(bodyPart.FK_CTRL)
                if bodyPart.IK_CTRL:
                    objectsOfInterest.append(bodyPart.IK_CTRL)
                if bodyPart.Options_CTRL:
                    objectsOfInterest.append(bodyPart.Options_CTRL)
                if bodyPart.AnimData_Joint:
                    objectsOfInterest.append(bodyPart.AnimData_Joint)
        objectsOfInterest.append(self.global_CTRL)
        if self.FacialControl_Mover:
            blendshapeNodes = mayac.ls(type='blendShape')
            if blendshapeNodes:
                for node in blendshapeNodes:
                    objectsOfInterest.append(node)
        for obj in objectsOfInterest:
            myKeys = mayac.keyframe(obj, query = True, name = True)
            if myKeys:
                howManyKeys = mayac.keyframe(myKeys[0], query = True, timeChange = True)
                last = len(howManyKeys)-1
                if howManyKeys[last] > highestTime:
                    highestTime = howManyKeys[last]
                if howManyKeys[0] < lowestTime:
                    lowestTime = howManyKeys[0]
        
        startTime = lowestTime
        endTime = highestTime
        if startTime != 99999999 and endTime != -999999999:
            mayac.playbackOptions(minTime = startTime, maxTime = highestTime)
        
        #transfer facial anim
        if self.FacialControl_Mover:
            FacePlus.copyBlendshapeAnimationToRig(self.origAnim, self.FacialControl_Mover, startTime, endTime)
            mayac.setAttr("%s.EyesFollowAim"%self.Head.FK_CTRL, 0.0)
        
        OpenMaya.MGlobal.displayInfo("Animation Data Attached")
        
        
    def deleteOriginalAnimation(self):
        mayac.delete(self.origAnim, self.origAnimation_Layer)
        self.origAnim = None
        self.origAnimation_Layer = None
        pyToAttr("%s.origAnim" % (self.infoNode), self.origAnim)
        pyToAttr("%s.origAnimation_Layer" % (self.infoNode), self.origAnimation_Layer)
        
        OpenMaya.MGlobal.displayInfo("Original Animation Deleted")
        
    
    
    def bakeAnimationToControls(self, bodyPart_ = "all"):
        #find first and last frames
        howManyKeys = []
        last = 0
        highestTime = -999999999
        lowestTime = 99999999
        objectsOfInterest = []
        for bodyPart in self.bodyParts:
            if "4" not in bodyPart.nodeName and "End" not in bodyPart.nodeName:
                if bodyPart.FK_CTRL:
                    objectsOfInterest.append(bodyPart.FK_CTRL)
                if bodyPart.IK_CTRL:
                    objectsOfInterest.append(bodyPart.IK_CTRL)
                if bodyPart.Options_CTRL:
                    objectsOfInterest.append(bodyPart.Options_CTRL)
                if bodyPart.AnimData_Joint:
                    objectsOfInterest.append(bodyPart.AnimData_Joint)
        objectsOfInterest.append(self.global_CTRL)
        for obj in objectsOfInterest:
            myKeys = mayac.keyframe(obj, query = True, name = True)
            if myKeys:
                howManyKeys = mayac.keyframe(myKeys[0], query = True, timeChange = True)
                last = len(howManyKeys)-1
                if howManyKeys[last] > highestTime:
                    highestTime = howManyKeys[last]
                if howManyKeys[0] < lowestTime:
                    lowestTime = howManyKeys[0]
        
        startTime = lowestTime
        endTime = highestTime
        
        if startTime == 99999999 and endTime == -999999999:
            OpenMaya.MGlobal.displayError("No Keyframes found on Character to bake!")
            return None
        
        #create locators
        locators = []
        for bodyPart in self.bodyParts:
            if "LeftLeg" in bodyPart.nodeName or "RightLeg" in bodyPart.nodeName or "ForeArm" in bodyPart.nodeName:
                temp = mayac.spaceLocator(n = "%s_locator1" % (bodyPart.nodeName))
                bodyPart.locator1 = temp[0]
                mayac.setAttr("%s.rotateOrder" % (bodyPart.locator1), bodyPart.rotOrder)
                mayac.setAttr("%s.visibility"%(bodyPart.locator1), 0)
                mayac.parent(bodyPart.locator1, self.global_CTRL)
                locators.append(bodyPart.locator1)
                temp = mayac.pointConstraint(bodyPart.IK_BakingLOC, bodyPart.locator1)
                bodyPart.locatorConstraint1 = temp[0]
            if "Foot" not in bodyPart.nodeName:
                temp = mayac.spaceLocator(n = "%s_locator" % (bodyPart.nodeName))
                bodyPart.locator = temp[0]
                mayac.setAttr("%s.rotateOrder" % (bodyPart.locator), bodyPart.rotOrder)
                mayac.setAttr("%s.visibility"%(bodyPart.locator), 0)
                mayac.parent(bodyPart.locator, self.global_CTRL)
                locators.append(bodyPart.locator)
                temp = mayac.parentConstraint(bodyPart.Bind_Joint, bodyPart.locator)
                bodyPart.locatorConstraint = temp[0]
            else:
                temp = mayac.spaceLocator(n = "%s_locator1" % (bodyPart.nodeName))
                bodyPart.locator1 = temp[0]
                mayac.setAttr("%s.rotateOrder" % (bodyPart.locator1), bodyPart.rotOrder)
                mayac.setAttr("%s.visibility"%(bodyPart.locator1), 0)
                mayac.parent(bodyPart.locator1, self.global_CTRL)
                mayac.delete(mayac.parentConstraint(bodyPart.Bind_Joint, bodyPart.locator1))
                temp = mayac.spaceLocator(n = "%s_locator" % (bodyPart.nodeName))
                bodyPart.locator = temp[0]
                mayac.setAttr("%s.rotateOrder" % (bodyPart.locator), bodyPart.rotOrder)
                mayac.setAttr("%s.visibility"%(bodyPart.locator), 0)
                mayac.parent(bodyPart.locator, self.global_CTRL)
                mayac.delete(mayac.parentConstraint(bodyPart.IK_BakingLOC, bodyPart.locator))
                temp = mayac.parentConstraint(bodyPart.locator1, bodyPart.locator, maintainOffset = True)
                bodyPart.locatorConstraint1 = temp[0]
                
                locators.append(bodyPart.locator)
                locators.append(bodyPart.locator1)
                temp = mayac.parentConstraint(bodyPart.Bind_Joint, bodyPart.locator1)
                bodyPart.locatorConstraint = temp[0]
                
        #bake onto locators
        mayac.select(clear = True)
        mayac.bakeResults(locators, simulation = True, time = (startTime, endTime))
        for bodyPart in self.bodyParts:
            mayac.delete(bodyPart.locatorConstraint)
            bodyPart.locatorConstraint = None
            if bodyPart.locatorConstraint1:
                mayac.delete(bodyPart.locatorConstraint1)
                bodyPart.locatorConstraint1 = None
        
        #zero out controls, animJoints
        for bodyPart in self.bodyParts:
            if bodyPart.AnimData_Joint:
                bodyPart.zeroToOrig(bodyPart.AnimData_Joint)
            if bodyPart.FK_CTRL:
                DJB_ZeroOut(bodyPart.FK_CTRL)
                DJB_ZeroOutAtt(bodyPart.FK_CTRL + ".AnimDataMult", value = 1)
                if "Root" in bodyPart.nodeName and self.hulaOption:
                    DJB_ZeroOutAtt(bodyPart.FK_CTRL + ".AnimDataMultTrans", value = 1)
                elif "Hips" in bodyPart.nodeName and not self.hulaOption:
                    DJB_ZeroOutAtt(bodyPart.FK_CTRL + ".AnimDataMultTrans", value = 1)
                if "Head" in bodyPart.nodeName:
                    DJB_ZeroOutAtt(bodyPart.FK_CTRL + ".InheritRotation", value = 1)
            if bodyPart.IK_CTRL:
                DJB_ZeroOut(bodyPart.IK_CTRL)
                DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".AnimDataMult", value = 1)
                DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".ParentToGlobal")
                DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".FollowBody")
                if "Leg" in bodyPart.nodeName:
                    DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".FollowFoot")
                if "ForeArm" in bodyPart.nodeName:
                    DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".FollowHand")
                if "Foot" in bodyPart.nodeName:
                    DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".FootRoll")
                    DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".ToeTap")
                    DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".ToeSideToSide")
                    DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".ToeRotate")
                    DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".ToeRoll")
                    DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".HipPivot")
                    DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".BallPivot")
                    DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".ToePivot")
                    DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".HipSideToSide")
                    DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".HipBackToFront")
            if bodyPart.Options_CTRL:
                if "Hand" in bodyPart.nodeName:
                    DJB_ZeroOutAtt(bodyPart.Options_CTRL + ".FollowHand")
                    DJB_ZeroOutAtt(bodyPart.Options_CTRL + ".ThumbCurl")
                    DJB_ZeroOutAtt(bodyPart.Options_CTRL + ".IndexCurl")
                    DJB_ZeroOutAtt(bodyPart.Options_CTRL + ".MiddleCurl")
                    DJB_ZeroOutAtt(bodyPart.Options_CTRL + ".RingCurl")
                    DJB_ZeroOutAtt(bodyPart.Options_CTRL + ".PinkyCurl")
                    DJB_ZeroOutAtt(bodyPart.Options_CTRL + ".Sway")
                    DJB_ZeroOutAtt(bodyPart.Options_CTRL + ".Spread")
                   
            
    
        #constraints
        bakeConstraintList = []
        bakeCTRLList = []
        EulerList = []
        for bodyPart in self.bodyParts:
            if bodyPart.FK_CTRL:
                if "Root" in bodyPart.nodeName:
                    temp = mayac.parentConstraint(bodyPart.locator, bodyPart.FK_CTRL)
                    bakeConstraintList.append(temp[0])
                    bakeCTRLList.append(bodyPart.FK_CTRL + ".translateX")
                    bakeCTRLList.append(bodyPart.FK_CTRL + ".translateY")
                    bakeCTRLList.append(bodyPart.FK_CTRL + ".translateZ")
                    bakeCTRLList.append(bodyPart.FK_CTRL + ".rotateX")
                    bakeCTRLList.append(bodyPart.FK_CTRL + ".rotateY")
                    bakeCTRLList.append(bodyPart.FK_CTRL + ".rotateZ")
                    
                elif "Hips" in bodyPart.nodeName and not self.hulaOption:
                    temp = mayac.parentConstraint(bodyPart.locator, bodyPart.FK_CTRL)
                    bakeConstraintList.append(temp[0])
                    bakeCTRLList.append(bodyPart.FK_CTRL + ".translateX")
                    bakeCTRLList.append(bodyPart.FK_CTRL + ".translateY")
                    bakeCTRLList.append(bodyPart.FK_CTRL + ".translateZ")
                    bakeCTRLList.append(bodyPart.FK_CTRL + ".rotateX")
                    bakeCTRLList.append(bodyPart.FK_CTRL + ".rotateY")
                    bakeCTRLList.append(bodyPart.FK_CTRL + ".rotateZ")
                   
                elif "Foot" in bodyPart.nodeName:
                    temp = mayac.orientConstraint(bodyPart.locator1, bodyPart.FK_CTRL)
                    bakeConstraintList.append(temp[0])
                    bakeCTRLList.append(bodyPart.FK_CTRL + ".rotateX")
                    bakeCTRLList.append(bodyPart.FK_CTRL + ".rotateY")
                    bakeCTRLList.append(bodyPart.FK_CTRL + ".rotateZ")
                    
                else:
                    temp = mayac.orientConstraint(bodyPart.locator, bodyPart.FK_CTRL)
                    bakeConstraintList.append(temp[0])
                    bakeCTRLList.append(bodyPart.FK_CTRL + ".rotateX")
                    bakeCTRLList.append(bodyPart.FK_CTRL + ".rotateY")
                    bakeCTRLList.append(bodyPart.FK_CTRL + ".rotateZ")

            if bodyPart.IK_CTRL:
                
                if "ForeArm" in bodyPart.nodeName or "Leg" in bodyPart.nodeName:
                    temp = mayac.pointConstraint(bodyPart.locator1, bodyPart.IK_CTRL)
                    bakeConstraintList.append(temp[0])
                    bakeCTRLList.append(bodyPart.IK_CTRL + ".translateX")
                    bakeCTRLList.append(bodyPart.IK_CTRL + ".translateY")
                    bakeCTRLList.append(bodyPart.IK_CTRL + ".translateZ")
                else:
                    temp = mayac.parentConstraint(bodyPart.locator, bodyPart.IK_CTRL)
                    bakeConstraintList.append(temp[0])
                    bakeCTRLList.append(bodyPart.IK_CTRL + ".translateX")
                    bakeCTRLList.append(bodyPart.IK_CTRL + ".translateY")
                    bakeCTRLList.append(bodyPart.IK_CTRL + ".translateZ")
                    bakeCTRLList.append(bodyPart.IK_CTRL + ".rotateX")
                    bakeCTRLList.append(bodyPart.IK_CTRL + ".rotateY")
                    bakeCTRLList.append(bodyPart.IK_CTRL + ".rotateZ")

                
        #bake onto controls
        mayac.bakeResults(bakeCTRLList, simulation = True, time = (startTime, endTime))
        mayac.delete(bakeConstraintList)

        
        #Euler filter
        for bodyPart in self.bodyParts:
            if bodyPart.FK_CTRL:
                mayac.filterCurve( '%s_rotateX'%(bodyPart.FK_CTRL), '%s_rotateY'%(bodyPart.FK_CTRL), '%s_rotateZ'%(bodyPart.FK_CTRL))
            if bodyPart.nodeName  == "LeftHand" or bodyPart.nodeName  == "RightHand" or bodyPart.nodeName  == "LeftFoot" or bodyPart.nodeName  == "RightFoot":
                mayac.filterCurve( '%s_rotateX'%(bodyPart.IK_CTRL), '%s_rotateY'%(bodyPart.IK_CTRL), '%s_rotateZ'%(bodyPart.IK_CTRL))
            
        
        #delete garbage
        for bodyPart in self.bodyParts:
            mayac.delete(bodyPart.locator)
            bodyPart.locator = None
            if bodyPart.locator1:
                mayac.delete(bodyPart.locator1)
                bodyPart.locator1 = None
                
        #make sure animLayer1 is active
        baseLayer = mayac.animLayer(query = True, root = True)
        if baseLayer:
            layers = mayac.ls(type = 'animLayer')
            for layer in layers:
                mel.eval('animLayerEditorOnSelect "%s" 0;'%(layer))
            mel.eval('animLayerEditorOnSelect "%s" 1;'%(baseLayer))
             
        #IK Toe Tap
        if self.rigType == "AutoRig":
            mayac.copyKey(self.LeftToeBase.FK_CTRL, time = (startTime, endTime), hierarchy = "none", controlPoints = 0, shape = 1, attribute = "rotateX")
            mayac.pasteKey(self.LeftFoot.IK_CTRL, connect = 1, attribute = "ToeTap")
            mayac.copyKey(self.LeftToeBase.FK_CTRL, time = (startTime, endTime), hierarchy = "none", controlPoints = 0, shape = 1, attribute = "rotateY")
            mayac.pasteKey(self.LeftFoot.IK_CTRL, connect = 1, attribute = "ToeRotate")
            mayac.copyKey(self.LeftToeBase.FK_CTRL, time = (startTime, endTime), hierarchy = "none", controlPoints = 0, shape = 1, attribute = "rotateZ")
            mayac.pasteKey(self.LeftFoot.IK_CTRL, connect = 1, attribute = "ToeSideToSide")
            mayac.copyKey(self.RightToeBase.FK_CTRL, time = (startTime, endTime), hierarchy = "none", controlPoints = 0, shape = 1, attribute = "rotateX")
            mayac.pasteKey(self.RightFoot.IK_CTRL, connect = 1, attribute = "ToeTap")
            mayac.copyKey(self.RightToeBase.FK_CTRL, time = (startTime, endTime), hierarchy = "none", controlPoints = 0, shape = 1, attribute = "rotateY")
            mayac.pasteKey(self.RightFoot.IK_CTRL, connect = 1, attribute = "ToeRotate")
            mayac.copyKey(self.RightToeBase.FK_CTRL, time = (startTime, endTime), hierarchy = "none", controlPoints = 0, shape = 1, attribute = "rotateZ")
            mayac.pasteKey(self.RightFoot.IK_CTRL, connect = 1, attribute = "ToeSideToSide")
        elif self.rigType == "World":
            mayac.copyKey(self.LeftToeBase.FK_CTRL, time = (startTime, endTime), hierarchy = "none", controlPoints = 0, shape = 1, attribute = "rotateX")
            mayac.pasteKey(self.LeftFoot.IK_CTRL, connect = 1, attribute = "ToeTap")
            mayac.scaleKey(self.LeftFoot.IK_CTRL, at='ToeTap', time=(startTime, endTime), valueScale = -1, valuePivot=0 )
            
            mayac.copyKey(self.LeftToeBase.FK_CTRL, time = (startTime, endTime), hierarchy = "none", controlPoints = 0, shape = 1, attribute = "rotateY")
            mayac.pasteKey(self.LeftFoot.IK_CTRL, connect = 1, attribute = "ToeSideToSide")
            mayac.copyKey(self.LeftToeBase.FK_CTRL, time = (startTime, endTime), hierarchy = "none", controlPoints = 0, shape = 1, attribute = "rotateZ")
            mayac.pasteKey(self.LeftFoot.IK_CTRL, connect = 1, attribute = "ToeRotate")
            mayac.copyKey(self.RightToeBase.FK_CTRL, time = (startTime, endTime), hierarchy = "none", controlPoints = 0, shape = 1, attribute = "rotateX")
            mayac.pasteKey(self.RightFoot.IK_CTRL, connect = 1, attribute = "ToeTap")
            mayac.scaleKey(self.RightFoot.IK_CTRL, at='ToeTap', time=(startTime, endTime), valueScale = -1, valuePivot=0 )
            
            mayac.copyKey(self.RightToeBase.FK_CTRL, time = (startTime, endTime), hierarchy = "none", controlPoints = 0, shape = 1, attribute = "rotateY")
            mayac.pasteKey(self.RightFoot.IK_CTRL, connect = 1, attribute = "ToeSideToSide")
            mayac.copyKey(self.RightToeBase.FK_CTRL, time = (startTime, endTime), hierarchy = "none", controlPoints = 0, shape = 1, attribute = "rotateZ")
            mayac.pasteKey(self.RightFoot.IK_CTRL, connect = 1, attribute = "ToeRotate")
            
        OpenMaya.MGlobal.displayInfo("Bake Successful")


    def clearAnimationControls(self, bodyPart_ = "all"):
        #find first and last frames
        #find first and last frames
        howManyKeys = []
        last = 0
        highestTime = -999999999
        lowestTime = 99999999
        objectsOfInterest = []
        for bodyPart in self.bodyParts:
            if "4" not in bodyPart.nodeName and "End" not in bodyPart.nodeName:
                if bodyPart.FK_CTRL:
                    objectsOfInterest.append(bodyPart.FK_CTRL)
                if bodyPart.IK_CTRL:
                    objectsOfInterest.append(bodyPart.IK_CTRL)
                if bodyPart.Options_CTRL:
                    objectsOfInterest.append(bodyPart.Options_CTRL)
                if bodyPart.AnimData_Joint:
                    objectsOfInterest.append(bodyPart.AnimData_Joint)
        objectsOfInterest.append(self.global_CTRL)
        for object in objectsOfInterest:
            myKeys = mayac.keyframe(object, query = True, name = True)
            if myKeys:
                howManyKeys = mayac.keyframe(myKeys[0], query = True, timeChange = True)
                last = len(howManyKeys)-1
                if howManyKeys[last] > highestTime:
                    highestTime = howManyKeys[last]
                if howManyKeys[0] < lowestTime:
                    lowestTime = howManyKeys[0]
        
        startTime = lowestTime
        endTime = highestTime
        
        if startTime == 99999999 and endTime == -999999999:
            OpenMaya.MGlobal.displayError("No Keyframes found on Character to clear!")
            return None
        
            
            
            
            
        #create locators
        locators = []
        temp = mayac.duplicate(self.global_CTRL, parentOnly = True)
        fakeGlobal = temp[0]
        mayac.setAttr("%s.translateX"%(fakeGlobal), 0)
        mayac.setAttr("%s.translateY"%(fakeGlobal), 0)
        mayac.setAttr("%s.translateZ"%(fakeGlobal), 0)
        mayac.setAttr("%s.rotateX"%(fakeGlobal), 0)
        mayac.setAttr("%s.rotateY"%(fakeGlobal), 0)
        mayac.setAttr("%s.rotateZ"%(fakeGlobal), 0)
        mayac.connectAttr("%s.scaleX"%(self.global_CTRL), "%s.scaleX"%(fakeGlobal))
        mayac.connectAttr("%s.scaleY"%(self.global_CTRL), "%s.scaleY"%(fakeGlobal))
        mayac.connectAttr("%s.scaleZ"%(self.global_CTRL), "%s.scaleZ"%(fakeGlobal))
        mayac.setAttr("%s.visibility"%(fakeGlobal), lock = False, keyable = True)
        mayac.setAttr("%s.visibility"%(fakeGlobal), 0)
        for bodyPart in self.bodyParts:
            temp = mayac.spaceLocator(n = "%s_locator" % (bodyPart.nodeName))
            bodyPart.locator = temp[0]
            locators.append(bodyPart.locator)
            mayac.setAttr("%s.visibility"%(bodyPart.locator), 0)
            mayac.parent(bodyPart.locator, self.global_CTRL)
            temp = mayac.parentConstraint(bodyPart.Bind_Joint, bodyPart.locator)
            bodyPart.locatorConstraint = temp[0]
            if "LeftLeg" in bodyPart.nodeName or "RightLeg" in bodyPart.nodeName or "ForeArm" in bodyPart.nodeName:
                temp = mayac.spaceLocator(n = "%s_locator2" % (bodyPart.nodeName))
                bodyPart.locator2 = temp[0]
                locators.append(bodyPart.locator2)
                mayac.setAttr("%s.visibility"%(bodyPart.locator2), 0)
                mayac.parent(bodyPart.locator2, self.global_CTRL)
                temp = mayac.parentConstraint(bodyPart.IK_BakingLOC, bodyPart.locator2)
                bodyPart.locatorConstraint2 = temp[0]
                temp = mayac.spaceLocator(n = "%s_locator3" % (bodyPart.nodeName))
                bodyPart.locator3 = temp[0]
                mayac.parent(bodyPart.locator3, fakeGlobal)
                mayac.setAttr("%s.visibility"%(bodyPart.locator3), 0)
                locators.append(bodyPart.locator3)
                mayac.connectAttr("%s.translateX" % (bodyPart.locator2), "%s.translateX" % (bodyPart.locator3))
                mayac.connectAttr("%s.translateY" % (bodyPart.locator2), "%s.translateY" % (bodyPart.locator3))
                mayac.connectAttr("%s.translateZ" % (bodyPart.locator2), "%s.translateZ" % (bodyPart.locator3))
                mayac.connectAttr("%s.rotateX" % (bodyPart.locator2), "%s.rotateX" % (bodyPart.locator3))
                mayac.connectAttr("%s.rotateY" % (bodyPart.locator2), "%s.rotateY" % (bodyPart.locator3))
                mayac.connectAttr("%s.rotateZ" % (bodyPart.locator2), "%s.rotateZ" % (bodyPart.locator3))
           
            temp = mayac.spaceLocator(n = "%s_locator1" % (bodyPart.nodeName))
            bodyPart.locator1 = temp[0]
            mayac.setAttr("%s.visibility"%(bodyPart.locator1), 0)
            locators.append(bodyPart.locator1)
            mayac.parent(bodyPart.locator1, fakeGlobal)
            mayac.connectAttr("%s.translateX" % (bodyPart.locator), "%s.translateX" % (bodyPart.locator1))
            mayac.connectAttr("%s.translateY" % (bodyPart.locator), "%s.translateY" % (bodyPart.locator1))
            mayac.connectAttr("%s.translateZ" % (bodyPart.locator), "%s.translateZ" % (bodyPart.locator1))
            mayac.connectAttr("%s.rotateX" % (bodyPart.locator), "%s.rotateX" % (bodyPart.locator1))
            mayac.connectAttr("%s.rotateY" % (bodyPart.locator), "%s.rotateY" % (bodyPart.locator1))
            mayac.connectAttr("%s.rotateZ" % (bodyPart.locator), "%s.rotateZ" % (bodyPart.locator1))
        mayac.select(clear = True)
            
                
        
        #bake onto locators
        mayac.bakeResults(locators, simulation = True, time = (startTime, endTime))
        for bodyPart in self.bodyParts:
            mayac.delete(bodyPart.locatorConstraint)
            bodyPart.locatorConstraint = None
            if bodyPart.locatorConstraint1:
                mayac.delete(bodyPart.locatorConstraint1)
                bodyPart.locatorConstraint1 = None
            if bodyPart.locatorConstraint2:
                mayac.delete(bodyPart.locatorConstraint2)
                bodyPart.locatorConstraint2 = None
            if bodyPart.locatorConstraint3:
                mayac.delete(bodyPart.locatorConstraint3)
                bodyPart.locatorConstraint3 = None
                
        
        bakeConstraintList = []
        bakeJointList = []
        #zero out controls, animJoints
        for bodyPart in self.bodyParts:
            if bodyPart.AnimData_Joint:
                bodyPart.zeroToOrig(bodyPart.AnimData_Joint)
            if bodyPart.FK_CTRL:
                DJB_ZeroOut(bodyPart.FK_CTRL)
                DJB_ZeroOutAtt(bodyPart.FK_CTRL + ".AnimDataMult", value = 1)
                if "Root" in bodyPart.nodeName:
                    DJB_ZeroOutAtt(bodyPart.FK_CTRL + ".AnimDataMultTrans", value = 1)
                elif "Hips" in bodyPart.nodeName and not self.hulaOption:
                    DJB_ZeroOutAtt(bodyPart.FK_CTRL + ".AnimDataMultTrans", value = 1)
                if "Head" in bodyPart.nodeName:
                    DJB_ZeroOutAtt(bodyPart.FK_CTRL + ".InheritRotation", value = 1)
            if bodyPart.IK_CTRL:
                DJB_ZeroOut(bodyPart.IK_CTRL)
                DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".AnimDataMult", value = 1)
                DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".ParentToGlobal")
                DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".FollowBody")
                if "LeftLeg" in bodyPart.nodeName or "RightLeg" in bodyPart.nodeName or "ForeArm" in bodyPart.nodeName:
                    temp = mayac.pointConstraint(bodyPart.IK_CTRL, bodyPart.locator1)
                    bodyPart.locatorConstraint1 = temp[0]
                if "Leg" in bodyPart.nodeName:
                    DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".FollowFoot")
                if "ForeArm" in bodyPart.nodeName:
                    DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".FollowHand")
                if "Foot" in bodyPart.nodeName:
                    DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".FootRoll")
                    DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".ToeTap")
                    DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".ToeSideToSide")
                    DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".ToeRotate")
                    DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".ToeRoll")
                    DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".HipPivot")
                    DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".BallPivot")
                    DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".ToePivot")
                    DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".HipSideToSide")
                    DJB_ZeroOutAtt(bodyPart.IK_CTRL + ".HipBackToFront")
            if bodyPart.Options_CTRL:
                if "Hand" in bodyPart.nodeName:
                    DJB_ZeroOutAtt(bodyPart.Options_CTRL + ".FollowHand")
                    DJB_ZeroOutAtt(bodyPart.Options_CTRL + ".ThumbCurl")
                    DJB_ZeroOutAtt(bodyPart.Options_CTRL + ".IndexCurl")
                    DJB_ZeroOutAtt(bodyPart.Options_CTRL + ".MiddleCurl")
                    DJB_ZeroOutAtt(bodyPart.Options_CTRL + ".RingCurl")
                    DJB_ZeroOutAtt(bodyPart.Options_CTRL + ".PinkyCurl")
                    DJB_ZeroOutAtt(bodyPart.Options_CTRL + ".Sway")
                    DJB_ZeroOutAtt(bodyPart.Options_CTRL + ".Spread")
                    
            
        
        #constraints
        for bodyPart in self.bodyParts:
            if "Root" in bodyPart.nodeName and self.hulaOption:
                temp = mayac.parentConstraint(bodyPart.locator1, bodyPart.AnimData_Joint)
                bakeConstraintList.append(temp[0])
                bakeJointList.append(bodyPart.AnimData_Joint + ".translateX")
                bakeJointList.append(bodyPart.AnimData_Joint + ".translateY")
                bakeJointList.append(bodyPart.AnimData_Joint + ".translateZ")
                bakeJointList.append(bodyPart.AnimData_Joint + ".rotateX")
                bakeJointList.append(bodyPart.AnimData_Joint + ".rotateY")
                bakeJointList.append(bodyPart.AnimData_Joint + ".rotateZ")   
            elif "Hips" in  bodyPart.nodeName and not self.hulaOption:
                temp = mayac.parentConstraint(bodyPart.locator1, bodyPart.AnimData_Joint)
                bakeConstraintList.append(temp[0])
                bakeJointList.append(bodyPart.AnimData_Joint + ".translateX")
                bakeJointList.append(bodyPart.AnimData_Joint + ".translateY")
                bakeJointList.append(bodyPart.AnimData_Joint + ".translateZ")
                bakeJointList.append(bodyPart.AnimData_Joint + ".rotateX")
                bakeJointList.append(bodyPart.AnimData_Joint + ".rotateY")
                bakeJointList.append(bodyPart.AnimData_Joint + ".rotateZ")            
            else:
                temp = mayac.orientConstraint(bodyPart.locator1, bodyPart.AnimData_Joint)
                bakeConstraintList.append(temp[0])
                bakeJointList.append(bodyPart.AnimData_Joint + ".rotateX")
                bakeJointList.append(bodyPart.AnimData_Joint + ".rotateY")
                bakeJointList.append(bodyPart.AnimData_Joint + ".rotateZ")

                
        #bake onto joints
        mayac.bakeResults(bakeJointList, simulation = True, time = (startTime, endTime))
        mayac.delete(bakeConstraintList)
        
                
        #Euler filter
        for bodyPart in self.bodyParts:
            if bodyPart.AnimData_Joint:
                mayac.filterCurve( '%s_rotateX'%(bodyPart.AnimData_Joint), '%s_rotateY'%(bodyPart.AnimData_Joint), '%s_rotateZ'%(bodyPart.AnimData_Joint))

        
        #delete garbage
        for bodyPart in self.bodyParts:
            mayac.delete(bodyPart.locator)
            bodyPart.locator = None
            if bodyPart.locator1:
                mayac.delete(bodyPart.locator1)
                bodyPart.locator1 = None
            if bodyPart.locator2:
                mayac.delete(bodyPart.locator2)
                bodyPart.locator2 = None
            if bodyPart.locator3:
                mayac.delete(bodyPart.locator3)
                bodyPart.locator3 = None
        #mayac.delete(fakeGlobal)
            
        #move PVs out a bit
        DJB_ZeroOut(self.LeftForeArm.IK_BakingLOC)
        DJB_ZeroOut(self.RightForeArm.IK_BakingLOC)
        DJB_ZeroOut(self.LeftLeg.IK_BakingLOC)
        DJB_ZeroOut(self.RightLeg.IK_BakingLOC)
        DJB_ZeroOut(self.LeftForeArm.IK_CTRL)
        DJB_ZeroOut(self.RightForeArm.IK_CTRL)
        DJB_ZeroOut(self.LeftLeg.IK_CTRL)
        DJB_ZeroOut(self.RightLeg.IK_CTRL)

        selfPOS = mayac.xform(self.LeftLeg.Bind_Joint, query = True, absolute = True, worldSpace = True, translation = True)
        parentPOS = mayac.xform(self.LeftLeg.parent.Bind_Joint, query = True, absolute = True, worldSpace = True, translation = True)
        tempDistance = math.sqrt((selfPOS[0]-parentPOS[0])*(selfPOS[0]-parentPOS[0]) + (selfPOS[1]-parentPOS[1])*(selfPOS[1]-parentPOS[1]) + (selfPOS[2]-parentPOS[2])*(selfPOS[2]-parentPOS[2]))
        mayac.setAttr("%s.translateZ" % (self.LeftLeg.IK_CTRL), tempDistance / 2)
        mayac.setAttr("%s.translateZ" % (self.RightLeg.IK_CTRL), tempDistance / 2)
        mayac.setAttr("%s.translateZ" % (self.LeftLeg.IK_BakingLOC), tempDistance / 2)
        mayac.setAttr("%s.translateZ" % (self.RightLeg.IK_BakingLOC), tempDistance / 2)
        selfPOS = mayac.xform(self.LeftForeArm.Bind_Joint, query = True, absolute = True, worldSpace = True, translation = True)
        parentPOS = mayac.xform(self.LeftForeArm.parent.Bind_Joint, query = True, absolute = True, worldSpace = True, translation = True)
        tempDistance = math.sqrt((selfPOS[0]-parentPOS[0])*(selfPOS[0]-parentPOS[0]) + (selfPOS[1]-parentPOS[1])*(selfPOS[1]-parentPOS[1]) + (selfPOS[2]-parentPOS[2])*(selfPOS[2]-parentPOS[2]))
        if self.rigType == "AutoRig":
            mayac.setAttr("%s.translateX" % (self.LeftForeArm.IK_CTRL), tempDistance / 2)
            mayac.setAttr("%s.translateX" % (self.RightForeArm.IK_CTRL), tempDistance / -2)
            mayac.setAttr("%s.translateX" % (self.LeftForeArm.IK_BakingLOC), tempDistance / 2)
            mayac.setAttr("%s.translateX" % (self.RightForeArm.IK_BakingLOC), tempDistance / -2)
        elif self.rigType == "World":
            mayac.setAttr("%s.translateZ" % (self.LeftForeArm.IK_CTRL), tempDistance / -2)
            mayac.setAttr("%s.translateZ" % (self.RightForeArm.IK_CTRL), tempDistance / -2)
            mayac.setAttr("%s.translateZ" % (self.LeftForeArm.IK_BakingLOC), tempDistance / -2)
            mayac.setAttr("%s.translateZ" % (self.RightForeArm.IK_BakingLOC), tempDistance / -2)
        
        OpenMaya.MGlobal.displayInfo("Un-Bake Successful")
        


    def createExportSkeleton(self, keepMesh_ = False, dynamicsToFK = 0, reduceNonEssential = False, start=None, end=None, removeEndJoints=False):
        anythingToBakeBlends = False
        #copy joints and mesh
        if self.exportList:
            for obj in self.exportList:
                if mayac.objExists(obj):
                    mayac.delete(obj)
        self.exportList = []
        self.exportListDropFrames = []
        translateOpenList = []
        #go to bind pose first
        bindJoints = []
        for bodyPart in self.bodyParts:
            if bodyPart.Bind_Joint:
                bindJoints.append(bodyPart.Bind_Joint)
        if self.ExtraJoints:
            for extra in self.ExtraJoints:
                if extra.Bind_Joint:
                    bindJoints.append(extra.Bind_Joint)
        for bodyPart in self.bodyParts:
            if bodyPart.children:
                if "Root" in bodyPart.nodeName or "Hips" in bodyPart.nodeName or "Leg" in bodyPart.nodeName or "Foot" in bodyPart.nodeName or "Toe" in bodyPart.nodeName or "Spine" in bodyPart.nodeName or "Shoulder" in bodyPart.nodeName or "Arm" in bodyPart.nodeName or bodyPart.nodeName == "LeftHand" or bodyPart.nodeName == "RightHand":
                    bodyPart.duplicateJoint("ExportSkeleton")
                    self.exportList.append(bodyPart.Export_Joint)
                else:
                    bodyPart.duplicateJoint("ExportSkeleton")
                    self.exportListDropFrames.append(bodyPart.Export_Joint)
            elif not removeEndJoints:
                bodyPart.duplicateJoint("ExportSkeleton")
                self.exportListDropFrames.append(bodyPart.Export_Joint)
            if bodyPart.translateOpen:
                translateOpenList.append(bodyPart.Export_Joint)
        
        if self.ExtraJoints:
            for node in self.ExtraJoints:
                if node.children:
                    node.duplicateJoint("ExportSkeleton")
                    node.Export_Joint = mayac.rename(node.Export_Joint, node.nodeName)
                    node.Export_Joint = mayac.rename(node.Export_Joint, DJB_findAfterSeperator(node.Export_Joint,":"))
                    self.exportListDropFrames.append(node.Export_Joint)
                    if node.translateOpen:
                        translateOpenList.append(node.Export_Joint)
                elif node.translateOpen:
                    node.duplicateJoint("ExportSkeleton")
                    node.Export_Joint = mayac.rename(node.Export_Joint, node.nodeName)
                    node.Export_Joint = mayac.rename(node.Export_Joint, DJB_findAfterSeperator(node.Export_Joint,":"))
                    self.exportListDropFrames.append(node.Export_Joint)
                    translateOpenList.append(node.Export_Joint)
                elif node.twistJoint:
                    node.duplicateJoint("ExportSkeleton")
                    node.Export_Joint = mayac.rename(node.Export_Joint, node.nodeName)
                    node.Export_Joint = mayac.rename(node.Export_Joint, DJB_findAfterSeperator(node.Export_Joint,":"))
                    self.exportListDropFrames.append(node.Export_Joint)
        pyToAttr("%s.exportList" % (self.infoNode), self.exportList)
        
        #lock unneeded attributes:
        for joint in (self.exportList + self.exportListDropFrames):
            if "Root" not in joint and "FacialAnim" not in joint and "Hips" not in joint and joint not in translateOpenList:
                DJB_LockNHide(joint, tx = True, ty = True, tz = True, rx = False, ry = False, rz = False, s = True, v = True, other = ("jointOrientX", "jointOrientY", "jointOrientZ", "lockInfluenceWeights", "liw"))
            elif joint in translateOpenList:
                DJB_LockNHide(joint, tx = False, ty = False, tz = False, rx = False, ry = False, rz = False, s = True, v = True, other = ("jointOrientX", "jointOrientY", "jointOrientZ", "lockInfluenceWeights", "liw"))
            else:
                DJB_LockNHide(joint, tx = False, ty = False, tz = False, rx = False, ry = False, rz = False, s = True, v = True, other = ("lockInfluenceWeights", "liw"))
        
        #create Constraints
        constraintList = []
        for bodyPart in self.bodyParts:
            if bodyPart.Bind_Joint and bodyPart.children and "Root" not in bodyPart.nodeName and "Hips" not in bodyPart.nodeName:
                if not bodyPart.translateOpen:
                    constraintList.append(mayac.orientConstraint(bodyPart.Bind_Joint, bodyPart.Export_Joint))
                else:
                    constraintList.append(mayac.parentConstraint(bodyPart.Bind_Joint, bodyPart.Export_Joint))
            elif bodyPart.Bind_Joint and bodyPart.children:
                constraintList.append(mayac.parentConstraint(bodyPart.Bind_Joint, bodyPart.Export_Joint))
            elif "Eye" in bodyPart.nodeName:
                constraintList.append(mayac.orientConstraint(bodyPart.Bind_Joint, bodyPart.Export_Joint))
        if self.ExtraJoints:
            for node in self.ExtraJoints:
                if node.children and not node.translateOpen:
                    constraintList.append(mayac.orientConstraint(node.Bind_Joint, node.Export_Joint))
                elif node.translateOpen:
                    print node.nodeName
                    constraintList.append(mayac.parentConstraint(node.Bind_Joint, node.Export_Joint))
                elif node.twistJoint:
                    constraintList.append(mayac.orientConstraint(node.Bind_Joint, node.Export_Joint))
        
        
        #find first and last frames
        startTime = start
        endTime = end
        if startTime == None:
            howManyKeys = []
            last = 0
            highestTime = -999999999
            lowestTime = 99999999
            objectsOfInterest = []
            for bodyPart in self.bodyParts:
                if "4" not in bodyPart.nodeName and "End" not in bodyPart.nodeName:
                    if bodyPart.FK_CTRL:
                        objectsOfInterest.append(bodyPart.FK_CTRL)
                    if bodyPart.IK_CTRL:
                        objectsOfInterest.append(bodyPart.IK_CTRL)
                    if bodyPart.Options_CTRL:
                        objectsOfInterest.append(bodyPart.Options_CTRL)
                    if bodyPart.AnimData_Joint:
                        objectsOfInterest.append(bodyPart.AnimData_Joint)
            objectsOfInterest.append(self.global_CTRL)
            for obj in objectsOfInterest:
                myKeys = mayac.keyframe(obj, query = True, name = True)
                if myKeys:
                    howManyKeys = mayac.keyframe(myKeys[0], query = True, timeChange = True)
                    last = len(howManyKeys)-1
                    if howManyKeys[last] > highestTime:
                        highestTime = howManyKeys[last]
                    if howManyKeys[0] < lowestTime:
                        lowestTime = howManyKeys[0]
            
            startTime = lowestTime
            endTime = highestTime
        highestTime = endTime
        lowestTime = startTime
        
        anythingToBake = True
        
        if startTime == 99999999 and endTime == -999999999:
            anythingToBake = False
        else:
            mayac.currentTime( lowestTime, edit=True )
        
            #control layer must be visible
            controlLayer = DJB_addNameSpace(self.characterNameSpace, "SecondaryControlLayer")
            if mayac.objExists(controlLayer):
                mayac.setAttr("%s.visibility" %(controlLayer), 1)
            if dynamicsToFK:
                if self.ExtraJoints:
                    for node in self.ExtraJoints:
                        if node.Options_CTRL:
                            mayac.setKeyframe(node.Options_CTRL, attribute='FK_Dyn', t=[lowestTime + dynamicsToFK, highestTime - dynamicsToFK])
                            mayac.setKeyframe(node.Options_CTRL, attribute='FK_Dyn', v = 0, t=[lowestTime, highestTime])
            for i in range(int(lowestTime-.5),int(lowestTime-.5)+15):
                mayac.currentTime( i, edit=True )
        
        
        #bake animation to joints
        mayac.select(clear = True)
        if anythingToBake and self.exportList:
            mayac.bakeResults(self.exportList + self.exportListDropFrames, simulation = True, time = (startTime, endTime), sampleBy = 1.0)
        for constraint in constraintList:
            mayac.delete(constraint)
        
        if anythingToBake:
        
            if self.exportListDropFrames:
                if reduceNonEssential:
                    for jointNum in self.exportListDropFrames:
                        animCurves = []
                        temp = mayac.listConnections( '%s.tx' % (jointNum), d=False, s=True )
                        if temp:
                            animCurves.append(temp[0])
                        temp = mayac.listConnections( '%s.ty' % (jointNum), d=False, s=True )
                        if temp:
                            animCurves.append(temp[0])
                        temp = mayac.listConnections( '%s.tz' % (jointNum), d=False, s=True )
                        if temp:
                            animCurves.append(temp[0])
                        temp = mayac.listConnections( '%s.rx' % (jointNum), d=False, s=True )
                        if temp:
                            animCurves.append(temp[0])
                        temp = mayac.listConnections( '%s.ry' % (jointNum), d=False, s=True )
                        if temp:
                            animCurves.append(temp[0])
                        temp = mayac.listConnections( '%s.rz' % (jointNum), d=False, s=True )
                        if temp:
                            animCurves.append(temp[0])
                        if animCurves:
                            for curve in animCurves:
                                mayac.filterCurve(curve, f = "simplify", tol = .015, timeTolerance = .05)
            self.exportList += self.exportListDropFrames
        
        
        #unlock all attributes:
        for joint in (self.exportList+self.exportListDropFrames):
            for attr in ["filmboxTypeID"]:
                if mayac.objExists("%s.%s"%(joint,attr)):
                    mayac.setAttr("%s.%s"%(joint,attr), lock = False, keyable = True)
                    mayac.deleteAttr("%s.%s"%(joint,attr))
            for attr in ["lockInfluenceWeights","liw"]:
                if mayac.objExists("%s.%s"%(joint,attr)):
                    mayac.setAttr("%s.%s"%(joint,attr), lock = False, keyable = True)
            DJB_Unlock(joint)
            mayac.setAttr("%s.jointOrientX" % (joint), lock = False, keyable = True)
            mayac.setAttr("%s.jointOrientY" % (joint), lock = False, keyable = True)
            mayac.setAttr("%s.jointOrientZ" % (joint), lock = False, keyable = True)
            
        #add mesh
        if keepMesh_:
            print "KEEPING MESH!!!"
            #clean up attrs on joints that may cause issues
            
            self.blendShapeTrackers = [] 
            for i in range(len(self.mesh)):
                oldSkin = mayac.listConnections(self.characterNameSpace + self.mesh[i], destination = True, type = "skinCluster")
                if oldSkin:
                    oldSkin = oldSkin[0]
                    #find bind pose
                    bindPose = mayac.listConnections(oldSkin, s=True, type="dagPose")
                    if bindPose:
                        try:
                            mayac.dagPose(bindPose[0], restore=True, g=True)
                            numMembers = mayac.getAttr("%s.members"%bindPose[0], mi=True)
                            for j in range(len(numMembers)):
                                bindJoint = mayac.listConnections("%s.members[%d]"%(bindPose[0], j), s=True)[0]
                                exportJoint = None
                                for bodyPart in self.bodyParts:
                                    if bindJoint == self.characterNameSpace+bodyPart.Bind_Joint:
                                        exportJoint = bodyPart.Export_Joint
                                if not exportJoint and self.ExtraJoints:
                                    for extra in self.ExtraJoints:
                                        if bindJoint == self.characterNameSpace+extra.Bind_Joint:
                                            exportJoint = extra.Export_Joint
                                if exportJoint:
                                    xformMatrix = mayac.getAttr("%s.xformMatrix[%d]"%(bindPose[0], j))
                                    mayac.xform(exportJoint, m=xformMatrix, os=True)
                        except:
                            mayac.warning("Cannot get %s back to bind pose"%bindPose[0])
                else:  #special case if there are deformers on top of rig and skinCluster is no longer directly connected
                    connections = mayac.listConnections((self.characterNameSpace + self.mesh[i]), destination = True)
                    for connection in connections:
                        if "skinCluster" in connection:
                            oldSkin = connection[:-3]
                
                blendshapeTrack = None
                meshName = "%s%s"%(self.characterNameSpace,self.mesh[i])
                isBlendShape = mayac.listConnections(meshName, d=True, type='blendShape')
                if not isBlendShape:   
                    #Keep track of blendshapes and zero out
                    meshConnections = mayac.listConnections(meshName, type = "objectSet")
                    if meshConnections:
                        meshConnections = set(meshConnections)
                        autoKeyframeState = mayac.autoKeyframe(q=True, state=True)
                        mayac.autoKeyframe(state=False)   
                        for con in meshConnections:
                            blendShapeCons = mayac.listConnections(con, type = "blendShape")
                            if blendShapeCons:
                                for blendShapeNode in blendShapeCons:
                                    blendshapeTrack = blendShapeTracker(blendShapeNode, meshName)
                                    self.blendShapeTrackers.append(blendshapeTrack)              
                    duplicatedMesh = mayac.duplicate(meshName, renameChildren = True)[0]
                    shapeNode = mayac.listRelatives(duplicatedMesh, children = True, type = "shape", fullPath = True)[0]
                    oldTransform = mayac.listRelatives(meshName, parent = True)[0]
                    DJB_Unlock(duplicatedMesh)
                    #DJB_Unlock(oldTransform)
                    isItLocked = mayac.getAttr("%s.visibility" % (oldTransform))
                    #mayac.setAttr("%s.visibility" % (oldTransform), 1)
                    mayac.setAttr("%s.visibility" % (meshName), 1)
                    mayac.setAttr("%s.visibility" % (duplicatedMesh), 1)
                    mayac.setAttr("%s.visibility" % (shapeNode), 1)
                    mayac.parent(duplicatedMesh, world = True)
                    duplicatedMesh = mayac.rename(duplicatedMesh, self.original_Mesh_Names[i])
                    self.exportList.append(duplicatedMesh)
                    mayac.disconnectAttr("%s.drawInfo" % (self.Mesh_Layer), "%s.drawOverride" % (duplicatedMesh))
                    shapeNode = mayac.listRelatives(duplicatedMesh, children = True, type = "shape", fullPath = True)[0]
                    mayac.disconnectAttr("%s.drawInfo" % (self.Mesh_Layer), "%s.drawOverride" % (shapeNode))
                    
                    if oldSkin:
                        newSkin = None
                        if self.hulaOption:
                            newSkin = mayac.skinCluster( self.Root.Export_Joint, duplicatedMesh)[0]
                        else:
                            newSkin = mayac.skinCluster( self.Hips.Export_Joint, duplicatedMesh)[0]
                        mayac.copySkinWeights( ss= oldSkin, ds= newSkin, noMirror=True )
                    else:
                        connections = mayac.listConnections("%s.instObjGroups[0]" % (shapeNode), destination=True, plugs=True)
                        if connections:
                            mayac.disconnectAttr("%s.instObjGroups[0]" % (shapeNode), connections[0])
                    #mayac.setAttr("%s.visibility" % (oldTransform), isItLocked)
                    mayac.setAttr("%s.visibility" % (meshName), isItLocked)
                    mayac.setAttr("%s.visibility" % (duplicatedMesh), isItLocked)
                    mayac.setAttr("%s.visibility" % (shapeNode), isItLocked)
                    autoKeyframeState = mayac.autoKeyframe(q=True, state=True)
                    mayac.autoKeyframe(state=False)
                    #Handle Blendshape creation and connections
                    if blendshapeTrack:
                        blendshapeTrack.duplicate(duplicatedMesh)                                
                    #restore orients
                    for bodyPart in self.bodyParts:
                        if bodyPart.Export_Joint:
                            ornt = mayac.getAttr("%s.jointOrient"%bodyPart.Bind_Joint)[0]
                            mayac.setAttr("%s.jointOrient"%bodyPart.Export_Joint, ornt[0], ornt[1], ornt[2])
                            rotation = mayac.getAttr("%s.rotate"%bodyPart.Bind_Joint)[0]
                            mayac.setAttr("%s.rotate"%bodyPart.Export_Joint, rotation[0], rotation[1], rotation[2])
                    if self.ExtraJoints:
                        for extra in self.ExtraJoints:
                            if extra.Export_Joint:
                                ornt = mayac.getAttr("%s.jointOrient"%extra.Bind_Joint)[0]
                                mayac.setAttr("%s.jointOrient"%extra.Export_Joint, ornt[0], ornt[1], ornt[2])
                                rotation = mayac.getAttr("%s.rotate"%extra.Bind_Joint)[0]
                                mayac.setAttr("%s.rotate"%extra.Export_Joint, rotation[0], rotation[1], rotation[2])
                    mayac.autoKeyframe(state=autoKeyframeState)
            #Bake Blendshapes and add to exportList
            if self.blendShapeTrackers:
                bakeList = []
                for tracker in self.blendShapeTrackers:
                    bakeList += tracker.bakeAttrs
                    for attrTracker in tracker.blendShapeAttrTrackers:
                        self.exportList.append(attrTracker.newGeo)
                        
                #check bake frames separately for facial animation
                #find first and last frames
                howManyKeys = []
                last = 0
                highestTime = -999999999
                lowestTime = 99999999
                objectsOfInterest = []
                mover = self.FacialControl_Mover
                if mover:
                    children = mayac.listRelatives(mover, type='transform')
                    if children:
                        for child in children:
                            grandchildren = mayac.listRelatives(child, type='transform')
                            if grandchildren:
                                for grandchild in grandchildren:
                                    greatgrandchildren = mayac.listRelatives(grandchild, type='transform')
                                    if greatgrandchildren:
                                        for greatgrandchild in greatgrandchildren:
                                            if "CTRL" in greatgrandchild:
                                                objectsOfInterest.append(greatgrandchild)
                for obj in objectsOfInterest:
                    myKeys = mayac.keyframe(obj, query = True, name = True)
                    if myKeys:
                        howManyKeys = mayac.keyframe(myKeys[0], query = True, timeChange = True)
                        last = len(howManyKeys)-1
                        if howManyKeys[last] > highestTime:
                            highestTime = howManyKeys[last]
                        if howManyKeys[0] < lowestTime:
                            lowestTime = howManyKeys[0]
                mayac.select(clear=True)
                startTimeBlends = lowestTime
                endTime = highestTime
                
                anythingToBakeBlends = True
                
                if startTimeBlends == 99999999 and endTime == -999999999:
                    anythingToBakeBlends = False
                else:
                    mayac.currentTime( lowestTime, edit=True )
                        
                if anythingToBakeBlends:
                    mayac.bakeResults(bakeList, simulation = True, time = (startTimeBlends, endTime), sampleBy = 1.0)
                else:
                    for tracker in self.blendShapeTrackers:
                        for attrTracker in tracker.blendShapeAttrTrackers:
                            attrTracker.disconnectNewBlendShape()
        if anythingToBake:
            mayac.currentTime( startTime, edit=True )
        if anythingToBakeBlends:
            mayac.currentTime( startTimeBlends, edit=True )
        pyToAttr("%s.exportList" % (self.infoNode), self.exportList)
        return self.exportList
        
        
    def exportSkeleton(self, fileName = None):
        mayac.select(self.exportList+self.exportListDropFrames, replace = True)
        for element in self.exportList+self.exportListDropFrames:
            print element
        if not fileName:
            mayac.ExportSelection()
        else:
            melLine = 'FBXExport -f "%s.fbx" -s' % (fileName)
            mel.eval(melLine)
        mayac.delete(self.exportList)
        self.exportList = []
        if self.blendShapeTrackers:
            for tracker in self.blendShapeTrackers:
                tracker.restoreScene()
    
    def dynamicsStartEndPoseKeys(self, dynamicsToFK = 0):
        highestTime = -999999999
        lowestTime = 99999999
        objectsOfInterest = []
        for bodyPart in self.bodyParts:
            if "4" not in bodyPart.nodeName and "End" not in bodyPart.nodeName:
                if bodyPart.FK_CTRL:
                    objectsOfInterest.append(bodyPart.FK_CTRL)
                if bodyPart.IK_CTRL:
                    objectsOfInterest.append(bodyPart.IK_CTRL)
                if bodyPart.Options_CTRL:
                    objectsOfInterest.append(bodyPart.Options_CTRL)
                if bodyPart.AnimData_Joint:
                    objectsOfInterest.append(bodyPart.AnimData_Joint)
        objectsOfInterest.append(self.global_CTRL)
        for obj in objectsOfInterest:
            myKeys = mayac.keyframe(obj, query = True, name = True)
            if myKeys:
                howManyKeys = mayac.keyframe(myKeys[0], query = True, timeChange = True)
                last = len(howManyKeys)-1
                if howManyKeys[last] > highestTime:
                    highestTime = howManyKeys[last]
                if howManyKeys[0] < lowestTime:
                    lowestTime = howManyKeys[0]
        
        startTime = lowestTime
        endTime = highestTime
        
        if dynamicsToFK:
            if self.ExtraJoints:
                for node in self.ExtraJoints:
                    if node.Options_CTRL:
                        mayac.setKeyframe(node.Options_CTRL, attribute='FK_Dyn', t=[lowestTime + dynamicsToFK, highestTime - dynamicsToFK])
                        mayac.setKeyframe(node.Options_CTRL, attribute='FK_Dyn', v = 0, t=[lowestTime, highestTime])
    
    #for early version
    def deleteExportSkeleton(self):
        if self.exportList:
            mayac.select(self.exportList, replace = True)
            mayac.delete()
        self.exportList = None
        pyToAttr("%s.exportList" % (self.infoNode), self.exportList)



    def writeInfoNode(self):
        self.infoNode = mayac.createNode("transform", name = "MIXAMO_CHARACTER_infoNode")
        pyToAttr("%s.ExtraJoints" % (self.infoNode), self.ExtraJoints)
        pyToAttr("%s.numExtraJointChains" % (self.infoNode), self.numExtraJointChains)
        
        
        pyToAttr("%s.name" % (self.infoNode), self.name)
        pyToAttr("%s.mesh" % (self.infoNode), self.mesh)
        pyToAttr("%s.original_Mesh_Names" % (self.infoNode), self.original_Mesh_Names)
        pyToAttr("%s.joint_namespace" % (self.infoNode), self.joint_namespace)
        pyToAttr("%s.rigType" % (self.infoNode), self.rigType)
        pyToAttr("%s.BoundingBox" % (self.infoNode), self.BoundingBox)
        pyToAttr("%s.Root" % (self.infoNode), self.Root.writeInfoNode())
        pyToAttr("%s.Hips" % (self.infoNode), self.Hips.writeInfoNode())
        pyToAttr("%s.Spine" % (self.infoNode), self.Spine.writeInfoNode())
        pyToAttr("%s.Spine1" % (self.infoNode), self.Spine1.writeInfoNode())
        pyToAttr("%s.Spine2" % (self.infoNode), self.Spine2.writeInfoNode())
        if self.Spine3:
            pyToAttr("%s.Spine3" % (self.infoNode), self.Spine3.writeInfoNode())
        pyToAttr("%s.Neck" % (self.infoNode), self.Neck.writeInfoNode())
        pyToAttr("%s.Neck1" % (self.infoNode), self.Neck1.writeInfoNode())
        pyToAttr("%s.Head" % (self.infoNode), self.Head.writeInfoNode())
        pyToAttr("%s.HeadTop_End" % (self.infoNode), self.HeadTop_End.writeInfoNode())
        pyToAttr("%s.LeftShoulder" % (self.infoNode), self.LeftShoulder.writeInfoNode())
        pyToAttr("%s.LeftArm" % (self.infoNode), self.LeftArm.writeInfoNode())
        pyToAttr("%s.LeftForeArm" % (self.infoNode), self.LeftForeArm.writeInfoNode())
        pyToAttr("%s.LeftHand" % (self.infoNode), self.LeftHand.writeInfoNode())
        pyToAttr("%s.LeftHandThumb1" % (self.infoNode), self.LeftHandThumb1.writeInfoNode())
        pyToAttr("%s.LeftHandThumb2" % (self.infoNode), self.LeftHandThumb2.writeInfoNode())
        pyToAttr("%s.LeftHandThumb3" % (self.infoNode), self.LeftHandThumb3.writeInfoNode())
        pyToAttr("%s.LeftHandThumb4" % (self.infoNode), self.LeftHandThumb4.writeInfoNode())
        pyToAttr("%s.LeftHandIndex1" % (self.infoNode), self.LeftHandIndex1.writeInfoNode())
        pyToAttr("%s.LeftHandIndex2" % (self.infoNode), self.LeftHandIndex2.writeInfoNode())
        pyToAttr("%s.LeftHandIndex3" % (self.infoNode), self.LeftHandIndex3.writeInfoNode())
        pyToAttr("%s.LeftHandIndex4" % (self.infoNode), self.LeftHandIndex4.writeInfoNode())
        pyToAttr("%s.LeftHandMiddle1" % (self.infoNode), self.LeftHandMiddle1.writeInfoNode())
        pyToAttr("%s.LeftHandMiddle2" % (self.infoNode), self.LeftHandMiddle2.writeInfoNode())
        pyToAttr("%s.LeftHandMiddle3" % (self.infoNode), self.LeftHandMiddle3.writeInfoNode())
        pyToAttr("%s.LeftHandMiddle4" % (self.infoNode), self.LeftHandMiddle4.writeInfoNode())
        pyToAttr("%s.LeftHandRing1" % (self.infoNode), self.LeftHandRing1.writeInfoNode())
        pyToAttr("%s.LeftHandRing2" % (self.infoNode), self.LeftHandRing2.writeInfoNode())
        pyToAttr("%s.LeftHandRing3" % (self.infoNode), self.LeftHandRing3.writeInfoNode())
        pyToAttr("%s.LeftHandRing4" % (self.infoNode), self.LeftHandRing4.writeInfoNode())
        pyToAttr("%s.LeftHandPinky1" % (self.infoNode), self.LeftHandPinky1.writeInfoNode())
        pyToAttr("%s.LeftHandPinky2" % (self.infoNode), self.LeftHandPinky2.writeInfoNode())
        pyToAttr("%s.LeftHandPinky3" % (self.infoNode), self.LeftHandPinky3.writeInfoNode())
        pyToAttr("%s.LeftHandPinky4" % (self.infoNode), self.LeftHandPinky4.writeInfoNode())
        pyToAttr("%s.RightShoulder" % (self.infoNode), self.RightShoulder.writeInfoNode())
        pyToAttr("%s.RightArm" % (self.infoNode), self.RightArm.writeInfoNode())
        pyToAttr("%s.RightForeArm" % (self.infoNode), self.RightForeArm.writeInfoNode())
        pyToAttr("%s.RightHand" % (self.infoNode), self.RightHand.writeInfoNode())
        pyToAttr("%s.RightHandThumb1" % (self.infoNode), self.RightHandThumb1.writeInfoNode())
        pyToAttr("%s.RightHandThumb2" % (self.infoNode), self.RightHandThumb2.writeInfoNode())
        pyToAttr("%s.RightHandThumb3" % (self.infoNode), self.RightHandThumb3.writeInfoNode())
        pyToAttr("%s.RightHandThumb4" % (self.infoNode), self.RightHandThumb4.writeInfoNode())
        pyToAttr("%s.RightHandIndex1" % (self.infoNode), self.RightHandIndex1.writeInfoNode())
        pyToAttr("%s.RightHandIndex2" % (self.infoNode), self.RightHandIndex2.writeInfoNode())
        pyToAttr("%s.RightHandIndex3" % (self.infoNode), self.RightHandIndex3.writeInfoNode())
        pyToAttr("%s.RightHandIndex4" % (self.infoNode), self.RightHandIndex4.writeInfoNode())
        pyToAttr("%s.RightHandMiddle1" % (self.infoNode), self.RightHandMiddle1.writeInfoNode())
        pyToAttr("%s.RightHandMiddle2" % (self.infoNode), self.RightHandMiddle2.writeInfoNode())
        pyToAttr("%s.RightHandMiddle3" % (self.infoNode), self.RightHandMiddle3.writeInfoNode())
        pyToAttr("%s.RightHandMiddle4" % (self.infoNode), self.RightHandMiddle4.writeInfoNode())
        pyToAttr("%s.RightHandRing1" % (self.infoNode), self.RightHandRing1.writeInfoNode())
        pyToAttr("%s.RightHandRing2" % (self.infoNode), self.RightHandRing2.writeInfoNode())
        pyToAttr("%s.RightHandRing3" % (self.infoNode), self.RightHandRing3.writeInfoNode())
        pyToAttr("%s.RightHandRing4" % (self.infoNode), self.RightHandRing4.writeInfoNode())
        pyToAttr("%s.RightHandPinky1" % (self.infoNode), self.RightHandPinky1.writeInfoNode())
        pyToAttr("%s.RightHandPinky2" % (self.infoNode), self.RightHandPinky2.writeInfoNode())
        pyToAttr("%s.RightHandPinky3" % (self.infoNode), self.RightHandPinky3.writeInfoNode())
        pyToAttr("%s.RightHandPinky4" % (self.infoNode), self.RightHandPinky4.writeInfoNode())
        pyToAttr("%s.LeftUpLeg" % (self.infoNode), self.LeftUpLeg.writeInfoNode())
        pyToAttr("%s.LeftLeg" % (self.infoNode), self.LeftLeg.writeInfoNode())
        pyToAttr("%s.LeftFoot" % (self.infoNode), self.LeftFoot.writeInfoNode())
        pyToAttr("%s.LeftToeBase" % (self.infoNode), self.LeftToeBase.writeInfoNode())
        pyToAttr("%s.LeftToe_End" % (self.infoNode), self.LeftToe_End.writeInfoNode())
        pyToAttr("%s.RightUpLeg" % (self.infoNode), self.RightUpLeg.writeInfoNode())
        pyToAttr("%s.RightLeg" % (self.infoNode), self.RightLeg.writeInfoNode())
        pyToAttr("%s.RightFoot" % (self.infoNode), self.RightFoot.writeInfoNode())
        pyToAttr("%s.RightToeBase" % (self.infoNode), self.RightToeBase.writeInfoNode())
        pyToAttr("%s.RightToe_End" % (self.infoNode), self.RightToe_End.writeInfoNode())
        pyToAttr("%s.LeftEye" % (self.infoNode), self.LeftEye.writeInfoNode())
        pyToAttr("%s.RightEye" % (self.infoNode), self.RightEye.writeInfoNode())
        
        mayac.parent(self.infoNode, self.Misc_GRP)
        DJB_LockNHide(self.infoNode)
        for bodyPart in (self.Root, self.Hips, self.Spine, self.Spine1, self.Spine2, self.Spine3, self.Neck, self.Neck1, self.Head, self.HeadTop_End, self.LeftShoulder, 
                              self.LeftArm, self.LeftForeArm, self.LeftHand, self.LeftHandThumb1, self.LeftHandThumb2, self.LeftHandThumb3, 
                              self.LeftHandThumb4, self.LeftHandIndex1, self.LeftHandIndex2, self.LeftHandIndex3, self.LeftHandIndex4,
                              self.LeftHandMiddle1, self.LeftHandMiddle2, self.LeftHandMiddle3, self.LeftHandMiddle4, self.LeftHandRing1,
                              self.LeftHandRing2, self.LeftHandRing3, self.LeftHandRing4, self.LeftHandPinky1, self.LeftHandPinky2, 
                              self.LeftHandPinky3, self.LeftHandPinky4, self.RightShoulder, self.RightArm, self.RightForeArm, 
                              self.RightHand, self.RightHandThumb1, self.RightHandThumb2, self.RightHandThumb3, 
                              self.RightHandThumb4, self.RightHandIndex1, self.RightHandIndex2, self.RightHandIndex3, self.RightHandIndex4,
                              self.RightHandMiddle1, self.RightHandMiddle2, self.RightHandMiddle3, self.RightHandMiddle4, self.RightHandRing1,
                              self.RightHandRing2, self.RightHandRing3, self.RightHandRing4, self.RightHandPinky1, self.RightHandPinky2, 
                              self.RightHandPinky3, self.RightHandPinky4, self.LeftUpLeg, self.LeftLeg, self.LeftFoot, self.LeftToeBase,
                              self.LeftToe_End, self.RightUpLeg, self.RightLeg, self.RightFoot, self.RightToeBase, self.RightToe_End,
                              self.LeftEye, self.RightEye):
            mayac.parent(bodyPart.infoNode, self.Misc_GRP)
            DJB_LockNHide(bodyPart.infoNode)

        pyToAttr("%s.proportions" % (self.infoNode), self.proportions)
        pyToAttr("%s.defaultControlScale" % (self.infoNode), self.defaultControlScale)
        pyToAttr("%s.Character_GRP" % (self.infoNode), self.Character_GRP)
        pyToAttr("%s.global_CTRL" % (self.infoNode), self.global_CTRL)
        pyToAttr("%s.CTRL_GRP" % (self.infoNode), self.CTRL_GRP)
        pyToAttr("%s.Joint_GRP" % (self.infoNode), self.Joint_GRP)
        pyToAttr("%s.AnimData_Joint_GRP" % (self.infoNode), self.AnimData_Joint_GRP)
        pyToAttr("%s.Bind_Joint_GRP" % (self.infoNode), self.Bind_Joint_GRP)
        pyToAttr("%s.Mesh_GRP" % (self.infoNode), self.Mesh_GRP)
        pyToAttr("%s.Misc_GRP" % (self.infoNode), self.Misc_GRP)
        pyToAttr("%s.LeftArm_Switch_Reverse" % (self.infoNode), self.LeftArm_Switch_Reverse)
        pyToAttr("%s.RightArm_Switch_Reverse" % (self.infoNode), self.RightArm_Switch_Reverse)
        pyToAttr("%s.LeftLeg_Switch_Reverse" % (self.infoNode), self.LeftLeg_Switch_Reverse)
        pyToAttr("%s.RightLeg_Switch_Reverse" % (self.infoNode), self.RightLeg_Switch_Reverse)
        pyToAttr("%s.Bind_Joint_SelectSet" % (self.infoNode), self.Bind_Joint_SelectSet)
        pyToAttr("%s.AnimData_Joint_SelectSet" % (self.infoNode), self.AnimData_Joint_SelectSet)
        pyToAttr("%s.Controls_SelectSet" % (self.infoNode), self.Controls_SelectSet)
        pyToAttr("%s.Geo_SelectSet" % (self.infoNode), self.Geo_SelectSet)
        pyToAttr("%s.Left_Toe_IK_AnimData_GRP" % (self.infoNode), self.Left_Toe_IK_AnimData_GRP)
        pyToAttr("%s.Left_Toe_IK_CTRL" % (self.infoNode), self.Left_Toe_IK_CTRL)
        pyToAttr("%s.Left_ToeBase_IK_AnimData_GRP" % (self.infoNode), self.Left_ToeBase_IK_AnimData_GRP)
        pyToAttr("%s.Left_IK_ToeBase_animData_MultNode" % (self.infoNode), self.Left_IK_ToeBase_animData_MultNode)
        pyToAttr("%s.Left_ToeBase_IK_CTRL" % (self.infoNode), self.Left_ToeBase_IK_CTRL)
        pyToAttr("%s.Left_Ankle_IK_AnimData_GRP" % (self.infoNode), self.Left_Ankle_IK_AnimData_GRP)
        pyToAttr("%s.Left_Ankle_IK_CTRL" % (self.infoNode), self.Left_Ankle_IK_CTRL)
        pyToAttr("%s.Left_ToeBase_IkHandle" % (self.infoNode), self.Left_ToeBase_IkHandle)
        pyToAttr("%s.Left_ToeEnd_IkHandle" % (self.infoNode), self.Left_ToeEnd_IkHandle)
        pyToAttr("%s.Right_Toe_IK_AnimData_GRP" % (self.infoNode), self.Right_Toe_IK_AnimData_GRP)
        pyToAttr("%s.Right_Toe_IK_CTRL" % (self.infoNode), self.Right_Toe_IK_CTRL)
        pyToAttr("%s.Right_ToeBase_IK_AnimData_GRP" % (self.infoNode), self.Right_ToeBase_IK_AnimData_GRP)
        pyToAttr("%s.Right_IK_ToeBase_animData_MultNode" % (self.infoNode), self.Right_IK_ToeBase_animData_MultNode)
        pyToAttr("%s.Right_ToeBase_IK_CTRL" % (self.infoNode), self.Right_ToeBase_IK_CTRL)
        pyToAttr("%s.Right_Ankle_IK_AnimData_GRP" % (self.infoNode), self.Right_Ankle_IK_AnimData_GRP)
        pyToAttr("%s.Right_Ankle_IK_CTRL" % (self.infoNode), self.Right_Ankle_IK_CTRL)
        pyToAttr("%s.Right_ToeBase_IkHandle" % (self.infoNode), self.Right_ToeBase_IkHandle)
        pyToAttr("%s.Right_ToeEnd_IkHandle" % (self.infoNode), self.Right_ToeEnd_IkHandle)
        pyToAttr("%s.LeftHand_CTRLs_GRP" % (self.infoNode), self.LeftHand_CTRLs_GRP)
        pyToAttr("%s.RightHand_CTRLs_GRP" % (self.infoNode), self.RightHand_CTRLs_GRP)
        pyToAttr("%s.LeftFoot_FootRoll_MultNode" % (self.infoNode), self.LeftFoot_FootRoll_MultNode)
        pyToAttr("%s.LeftFoot_ToeRoll_MultNode" % (self.infoNode), self.LeftFoot_ToeRoll_MultNode)
        pyToAttr("%s.RightFoot_FootRoll_MultNode" % (self.infoNode), self.RightFoot_FootRoll_MultNode)
        pyToAttr("%s.RightFoot_ToeRoll_MultNode" % (self.infoNode), self.RightFoot_ToeRoll_MultNode)
        pyToAttr("%s.RightFoot_HipPivot_MultNode" % (self.infoNode), self.RightFoot_HipPivot_MultNode)
        pyToAttr("%s.RightFoot_BallPivot_MultNode" % (self.infoNode), self.RightFoot_BallPivot_MultNode)
        pyToAttr("%s.RightFoot_ToePivot_MultNode" % (self.infoNode), self.RightFoot_ToePivot_MultNode)
        pyToAttr("%s.RightFoot_HipSideToSide_MultNode" % (self.infoNode), self.RightFoot_HipSideToSide_MultNode)
        pyToAttr("%s.RightFoot_ToeRotate_MultNode" % (self.infoNode), self.RightFoot_ToeRotate_MultNode)
        pyToAttr("%s.IK_Dummy_Joint_GRP" % (self.infoNode), self.IK_Dummy_Joint_GRP)
        pyToAttr("%s.LeftHand_grandparent_Constraint" % (self.infoNode), self.LeftHand_grandparent_Constraint)
        pyToAttr("%s.LeftHand_grandparent_Constraint_Reverse" % (self.infoNode), self.LeftHand_grandparent_Constraint_Reverse)
        pyToAttr("%s.RightHand_grandparent_Constraint" % (self.infoNode), self.RightHand_grandparent_Constraint)
        pyToAttr("%s.RightHand_grandparent_Constraint_Reverse" % (self.infoNode), self.RightHand_grandparent_Constraint_Reverse)
        pyToAttr("%s.LeftForeArm_grandparent_Constraint" % (self.infoNode), self.LeftForeArm_grandparent_Constraint)
        pyToAttr("%s.LeftForeArm_grandparent_Constraint_Reverse" % (self.infoNode), self.LeftForeArm_grandparent_Constraint_Reverse)
        pyToAttr("%s.RightForeArm_grandparent_Constraint" % (self.infoNode), self.RightForeArm_grandparent_Constraint)
        pyToAttr("%s.RightForeArm_grandparent_Constraint_Reverse" % (self.infoNode), self.RightForeArm_grandparent_Constraint_Reverse)
        pyToAttr("%s.origAnim" % (self.infoNode), self.origAnim)
        pyToAttr("%s.origAnimation_Layer" % (self.infoNode), self.origAnimation_Layer)
        pyToAttr("%s.Mesh_Layer" % (self.infoNode), self.Mesh_Layer)
        pyToAttr("%s.Bind_Joint_Layer" % (self.infoNode), self.Bind_Joint_Layer)
        pyToAttr("%s.hulaOption" % (self.infoNode), self.hulaOption)
        pyToAttr("%s.exportList" % (self.infoNode), self.exportList)
        pyToAttr("%s.fingerFlip" % (self.infoNode), self.fingerFlip)
        pyToAttr("%s.FacialControl_Layer" % (self.infoNode), self.FacialControl_Layer)
        pyToAttr("%s.FacialControl_Mover"%(self.infoNode), self.FacialControl_Mover)
        
    
    def remakeMeshInfoNode(self):
        joints = []
        for bodyPart in self.bodyParts:
            if bodyPart.Bind_Joint:
                if mayac.objExists(bodyPart.Bind_Joint):
                    joints.append(bodyPart.Bind_Joint)
        if self.ExtraJoints:
            for ExtraJoint in self.ExtraJoints:
                if ExtraJoint.Bind_Joint:
                    if mayac.objExists(ExtraJoint.Bind_Joint):
                        joints.append(ExtraJoint.Bind_Joint)
        meshes = []
        skins = mayac.listConnections(joints,type='skinCluster')
        if skins:
            for skin in skins:
                if skin:  
                    geos = mayac.skinCluster(skin,query=True,geometry=True)
                    for geo in geos:
                        if geo not in meshes:
                            meshes.append(geo)
        transformNames = []
        if meshes:
            for geo in meshes:
                if "ShapeOrig" not in geo and "Bounding_Box_Override_Cube" not in geo:
                    transform = mayac.listRelatives(geo, parent = True)[0]
                    while transform.find("Mesh_"[0]) != -1:
                        transform = transform[5:len(transform)] #...hopefully they shouldn't start with Mesh_
                    transformNames.append(transform)
            self.mesh = meshes
            self.original_Mesh_Names = transformNames
            pyToAttr("%s.mesh" % (self.infoNode), self.mesh)
            pyToAttr("%s.original_Mesh_Names" % (self.infoNode), self.original_Mesh_Names)
            OpenMaya.MGlobal.displayInfo("Process Complete")
        else:
            mayac.warning("No skinClusters found on known skeleton")
        
        
        
    def makeExtraJointsInfoNode(self, joints):
        
        newExtraJoints = []
        #new characterNode for each joint
        if self.numExtraJointChains:
            self.numExtraJointChains += 1
        else:
            self.numExtraJointChains = 1
        for i in range(len(joints)):
            parentJoint = mayac.listRelatives(joints[i], parent = True)[0]
            if i == 0:
                ParentBodyPart = None
                for bodyPart in self.bodyParts:
                    if parentJoint == bodyPart.Bind_Joint:
                        ParentBodyPart = bodyPart
                if not ParentBodyPart:
                    for extraJoint in self.ExtraJoints:
                        if parentJoint == extraJoint.Bind_Joint:
                            ParentBodyPart = extraJoint
                newExtraJoints.append(DJB_CharacterNode(joints[i], parent = ParentBodyPart, twistJoint_ = True, translateOpen_ = True))
                jointIndex = len(newExtraJoints)-1
            else:
                newExtraJoints.append(DJB_CharacterNode(joints[i], parent = newExtraJoints[jointIndex], twistJoint_ = True, translateOpen_ = True))
                jointIndex = len(newExtraJoints)-1

        #infoNode stuff
        for i in range(len(joints)):
            newExtraJoints[i].writeInfoNode()
            mayac.parent(newExtraJoints[i].infoNode, self.Misc_GRP)
        infoNodes = []
        if not self.ExtraJoints:
            self.ExtraJoints = []
        else:
            infoNodes = attrToPy("%s.ExtraJoints" % (self.infoNode))
        if not infoNodes:
            infoNodes = []
        for joint in newExtraJoints:
            self.ExtraJoints.append(joint)
            infoNodes.append(joint.infoNode)
        pyToAttr("%s.ExtraJoints" % (self.infoNode), infoNodes)
        OpenMaya.MGlobal.displayInfo("Process Complete")
        
    def makeDynamicChainRig(self, joints, dynamic_ = "ZV", control_ = "FK"):
        newExtraJoints = []
        #new characterNode for each joint
        if self.numExtraJointChains:
            self.numExtraJointChains += 1
        else:
            self.numExtraJointChains = 1
        for i in range(len(joints)):
            parentJoint = mayac.listRelatives(joints[i], parent = True)[0]
            if i == 0:
                ParentBodyPart = None
                for bodyPart in self.bodyParts:
                    if parentJoint == bodyPart.Bind_Joint:
                        ParentBodyPart = bodyPart
                if not ParentBodyPart:
                    for extraJoint in self.ExtraJoints:
                        if parentJoint == extraJoint.Bind_Joint:
                            ParentBodyPart = extraJoint
                newExtraJoints.append(DJB_CharacterNode(joints[i], parent = ParentBodyPart, dynamic_ = dynamic_))
                jointIndex = len(newExtraJoints)-1
                newExtraJoints[jointIndex].duplicateJoint(control_, parent_ = "Bind_Joint")
                newExtraJoints[jointIndex].duplicateJoint(dynamic_, parent_ = "Bind_Joint")
                newExtraJoints[jointIndex].duplicateJoint("AnimData")
            else:
                newExtraJoints.append(DJB_CharacterNode(joints[i], parent = newExtraJoints[jointIndex], dynamic_ = dynamic_))
                jointIndex = len(newExtraJoints)-1
                newExtraJoints[jointIndex].duplicateJoint(control_)
                newExtraJoints[jointIndex].duplicateJoint(dynamic_)
                newExtraJoints[jointIndex].duplicateJoint("AnimData")
            
            #FK controls
            if i < len(joints)-1 and len(joints) > 1:
                newExtraJoints[jointIndex].createControl(type = "FK", rigType = "Dyn",
                                    style = "circle", 
                                    scale = (self.proportions["depth"]*0.10, self.proportions["depth"]*0.10, self.proportions["depth"]*0.10),
                                    offset = (self.proportions["depth"]*0.05, 0, 0),
                                    rotate = (0, 0, 90),
                                    color_ = "white")
            elif len(joints) == 1:
                newExtraJoints[jointIndex].createControl(type = "FK", rigType = "Dyn",
                                    style = "circle", 
                                    scale = (self.proportions["depth"]*0.10, self.proportions["depth"]*0.10, self.proportions["depth"]*0.10),
                                    offset = (self.proportions["depth"]*0.05, 0, 0),
                                    rotate = (0, 0, 90),
                                    color_ = "white")
                
                
            #Options CTRL
            if i == len(joints)-1:
                newExtraJoints[jointIndex].createControl(type = "options", 
                                    style = "options",
                                    scale = (self.proportions["depth"]*0.06, self.proportions["depth"]*0.06, self.proportions["depth"]*-0.06),
                                    rotate = (-90, 0, 90),
                                    offset = (0, self.proportions["depth"]*.15, 0),  
                                    partialConstraint = 0,
                                    color_ = "white",
                                    name_ = "%s_Options"%(newExtraJoints[0].nodeName))
                
        #ZV controls
        #one joint
        if len(joints) == 1:
            newExtraJoints[0].translateOpen = True
            FullName = newExtraJoints[0].nodeName
            newExtraJoints[0].IK_Handle = DJB_createGroup(pivotFrom = newExtraJoints[0].Bind_Joint, fullName = "%s_Dyn_NULL"%(FullName))
            newExtraJoints[0].IK_CTRL_POS_GRP = DJB_createGroup(newExtraJoints[0].IK_Handle)
            mayac.parent(newExtraJoints[i].IK_CTRL_POS_GRP, self.global_CTRL)
            mayac.setAttr("%s.visibility"%(newExtraJoints[i].IK_Handle), 0)
            mayac.parentConstraint(newExtraJoints[0].parent.Bind_Joint, newExtraJoints[0].IK_CTRL_POS_GRP, maintainOffset = True)
            newExtraJoints[0].Dyn_Node = nParticleMethod(newExtraJoints[0].IK_Handle, weight=0.7, conserve=1.0, transfShapes=False)
            newExtraJoints[0].createControl(type = "Dyn",
                                    style = "box1",
                                    scale = (self.proportions["depth"]*0.1, self.proportions["depth"]*0.1, self.proportions["depth"]*0.1),
                                    offset = (0, 0, 0),
                                    color_ = "white",
                                    name_ = "%s_Dyn_CTRL"%(newExtraJoints[0].nodeName))
            mayac.parent(newExtraJoints[0].Dyn_CTRL, self.global_CTRL)
            mayac.parentConstraint(newExtraJoints[0].Bind_Joint, newExtraJoints[0].Dyn_CTRL)
            mayac.parentConstraint(newExtraJoints[0].IK_Handle, newExtraJoints[0].Dyn_Joint)
            
            
            
        endJointIndex = len(newExtraJoints)-1
        if dynamic_ == "ZV" and jointIndex > 0: #more than one dynamic joint  
            for i in range(1, endJointIndex+1): 
                temp = mayac.ikHandle( sj=newExtraJoints[i].parent.Dyn_Joint, ee=newExtraJoints[i].Dyn_Joint, n = "%s_DYN_IKHandle"%(newExtraJoints[i-1].nodeName))
                newExtraJoints[i].IK_Handle = temp[0]
                mayac.rename(temp[1], "%s_DYN_IKEffector"%(newExtraJoints[i].nodeName))
                mayac.setAttr("%s.visibility"%(newExtraJoints[i].IK_Handle), 0)
                newExtraJoints[i].IK_CTRL_POS_GRP = DJB_createGroup(newExtraJoints[i].IK_Handle)
                if i==1:
                    mayac.parent(newExtraJoints[i].IK_CTRL_POS_GRP, self.global_CTRL)
                    mayac.parentConstraint(newExtraJoints[0].parent.Bind_Joint, newExtraJoints[i].IK_CTRL_POS_GRP, maintainOffset = True)
                else:
                    mayac.parent(newExtraJoints[i].IK_CTRL_POS_GRP, newExtraJoints[i-1].IK_Handle)
                newExtraJoints[i].Dyn_Node = nParticleMethod(newExtraJoints[i].IK_Handle, weight=0.7, conserve=1.0, transfShapes=False)
            newExtraJoints[endJointIndex].createControl(type = "Dyn",
                                    style = "box1",
                                    scale = (self.proportions["depth"]*0.1, self.proportions["depth"]*0.1, self.proportions["depth"]*0.1),
                                    offset = (0, 0, 0),
                                    color_ = "white",
                                    name_ = "%s_Dyn_CTRL"%(newExtraJoints[0].nodeName))
            mayac.parent(newExtraJoints[endJointIndex].Dyn_CTRL, self.global_CTRL)
            mayac.parentConstraint(newExtraJoints[endJointIndex].Bind_Joint, newExtraJoints[endJointIndex].Dyn_CTRL)
                

        for i in range(len(joints)):
            #Hook up controls
            newExtraJoints[i].finalizeCTRLs()
            newExtraJoints[i].lockUpCTRLs()
        mayac.parent(newExtraJoints[len(newExtraJoints)-1].Options_CTRL, self.global_CTRL)
        #Hook up Attrs
        for i in range(len(joints)):
            if newExtraJoints[i].Dyn_Node:
                mayac.connectAttr("%s.weight" %(newExtraJoints[len(newExtraJoints)-1].Dyn_CTRL), "%s.weight" %(newExtraJoints[i].Dyn_Node))
                mayac.connectAttr("%s.conserve" %(newExtraJoints[len(newExtraJoints)-1].Dyn_CTRL), "%s.conserve" %(newExtraJoints[i].Dyn_Node))
            if newExtraJoints[i].Dyn_Joint:
                mayac.connectAttr("%s.multiplier" %(newExtraJoints[len(newExtraJoints)-1].Dyn_CTRL), "%s.input2X" %(newExtraJoints[i].Dyn_Mult))
                mayac.connectAttr("%s.multiplier" %(newExtraJoints[len(newExtraJoints)-1].Dyn_CTRL), "%s.input2Y" %(newExtraJoints[i].Dyn_Mult))
                mayac.connectAttr("%s.multiplier" %(newExtraJoints[len(newExtraJoints)-1].Dyn_CTRL), "%s.input2Z" %(newExtraJoints[i].Dyn_Mult))
                if newExtraJoints[i].translateOpen:
                    jointPosHolder = mayac.shadingNode ('multiplyDivide', asUtility = True, name = "%s_JointPos"%(newExtraJoints[i].Dyn_Mult1))
                    jointPosHolder1 = mayac.shadingNode ('multiplyDivide', asUtility = True, name = "%s_JointPos"%(newExtraJoints[i].Dyn_Mult1))
                    trans = mayac.getAttr("%s.translate"%(newExtraJoints[i].Bind_Joint))[0]
                    mayac.setAttr("%s.input1X"%(jointPosHolder), trans[0])
                    mayac.setAttr("%s.input1Y"%(jointPosHolder), trans[1])
                    mayac.setAttr("%s.input1Z"%(jointPosHolder), trans[2])
                    mayac.setAttr("%s.input1X"%(jointPosHolder1), trans[0])
                    mayac.setAttr("%s.input1Y"%(jointPosHolder1), trans[1])
                    mayac.setAttr("%s.input1Z"%(jointPosHolder1), trans[2])
                    subtract1 = mayac.shadingNode ('plusMinusAverage', asUtility = True, name = "%s_Subtract"%(newExtraJoints[i].Dyn_Mult1))
                    mel.eval('AEnewNonNumericMultiAddNewItem("%s", "input3D");'%(subtract1))
                    mel.eval('AEnewNonNumericMultiAddNewItem("%s", "input3D");'%(subtract1))
                    mayac.setAttr("%s.operation"%(subtract1), 2)
                    mayac.connectAttr("%s.output"%(jointPosHolder), "%s.input3D[0]"%(subtract1), force = True)
                    mayac.connectAttr("%s.translate"%(newExtraJoints[i].Dyn_Joint), "%s.input3D[1]"%(subtract1), force = True)
                    mayac.connectAttr("%s.output3D"%(subtract1), "%s.input1"%(newExtraJoints[i].Dyn_Mult1), force = True)
                    add1 = mayac.shadingNode ('plusMinusAverage', asUtility = True, name = "%s_Add"%(newExtraJoints[i].Dyn_Mult1))
                    mel.eval('AEnewNonNumericMultiAddNewItem("%s", "input3D");'%(add1))
                    mel.eval('AEnewNonNumericMultiAddNewItem("%s", "input3D");'%(add1))
                    mayac.connectAttr("%s.output"%(newExtraJoints[i].Dyn_Mult1), "%s.input3D[0]"%(add1), force = True)
                    mayac.connectAttr("%s.output"%(jointPosHolder1), "%s.input3D[1]"%(add1), force = True)
                    mayac.connectAttr("%s.output3D"%(add1), "%s.translate"%(newExtraJoints[i].DynMult_Joint), force = True)
                    mayac.connectAttr("%s.multiplier" %(newExtraJoints[len(newExtraJoints)-1].Dyn_CTRL), "%s.input2Y" %(newExtraJoints[i].Dyn_Mult1))
                    mayac.connectAttr("%s.multiplier" %(newExtraJoints[len(newExtraJoints)-1].Dyn_CTRL), "%s.input2Z" %(newExtraJoints[i].Dyn_Mult1))
        #Contraint Reverses
        reverseNode = mayac.createNode( 'reverse', n="%s_Switch_Reverse" %(newExtraJoints[0].nodeName))
        typeName = ""
        if dynamic_ == "ZV" and control_ == "FK":
            typeName = "FK_Dyn"
        mayac.setAttr("%s.weight" %(newExtraJoints[len(joints)-1].Dyn_CTRL), 0.8)
        mayac.setAttr("%s.conserve" %(newExtraJoints[len(joints)-1].Dyn_CTRL), 1.0)
        mayac.setAttr("%s.%s" %(newExtraJoints[len(newExtraJoints)-1].Options_CTRL, typeName), 1.0)
        mayac.connectAttr("%s.%s" %(newExtraJoints[len(joints)-1].Options_CTRL, typeName), "%s.inputX" %(reverseNode))
        for i in range(len(joints)):
            if newExtraJoints[i].Constraint:
                mayac.setAttr("%s.interpType" %(newExtraJoints[i].Constraint), 2)
                mayac.connectAttr("%s.%s" %(newExtraJoints[len(joints)-1].Options_CTRL, typeName), "%s.%sW1" %(newExtraJoints[i].Constraint, newExtraJoints[i].DynMult_Joint))
                mayac.connectAttr("%s.outputX" %(reverseNode), "%s.%sW0" %(newExtraJoints[i].Constraint, newExtraJoints[i].FK_Joint))
            DJB_Unlock_Connect_Lock("%s.%s" %(newExtraJoints[len(joints)-1].Options_CTRL, typeName), "%s.visibility" %(newExtraJoints[i].DynMult_Joint))
            DJB_Unlock_Connect_Lock("%s.outputX" %(reverseNode), "%s.visibility" %(newExtraJoints[i].FK_Joint))
            if newExtraJoints[i].FK_CTRL:
                DJB_Unlock_Connect_Lock("%s.outputX" %(reverseNode), "%s.visibility" %(newExtraJoints[i].FK_CTRL))
            if newExtraJoints[i].Dyn_CTRL:
                DJB_Unlock_Connect_Lock("%s.%s" %(newExtraJoints[len(joints)-1].Options_CTRL, typeName), "%s.visibility" %(newExtraJoints[i].Dyn_CTRL))
        #infoNode stuff
        for i in range(len(joints)):
            newExtraJoints[i].writeInfoNode()
            mayac.parent(newExtraJoints[i].infoNode, self.Misc_GRP)
        infoNodes = []
        if not self.ExtraJoints:
            self.ExtraJoints = []
        else:
            infoNodes = attrToPy("%s.ExtraJoints" % (self.infoNode))
        if not infoNodes:
            infoNodes = []
        for joint in newExtraJoints:
            self.ExtraJoints.append(joint)
            infoNodes.append(joint.infoNode)
        pyToAttr("%s.ExtraJoints" % (self.infoNode), infoNodes)