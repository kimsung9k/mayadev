'''
DJB_Character.FacialControls
Handles:
    Class for Fuse Facial Controls
'''
import maya.cmds as mayac
from MixamoAutoRig.Utils.General import *
import FacePlusRig
import os


def findNode(nodeName):
        all = mayac.ls(type = "transform")
        for cur in all:
            if nodeName in cur:
                return cur
        return ''

def CreateSwitch(object, objectConst0, objectConst1, switchAttr = "", type = "parentConstraint"):
    return None
    constraint = None
    if type == "parentConstraint":
        constraint = mayac.parentConstraint(objectConst0, objectConst1, object, mo=True)[0]
    
    obj0Attr = ''
    obj1Attr = ''
    attrs = mayac.listAttr(constraint, k=True, u=True, ud=True)
    for attr in attrs:
        if objectConst0 in attr:
            obj0Attr = "%s.%s"%(constraint,attr)
        elif objectConst1 in attr:
            obj1Attr = "%s.%s"%(constraint,attr)
    
    reverseNode = mayac.shadingNode('reverse', asUtility=True, n="%s_Reverse"%switchAttr.replace(".","_"))
    
    print switchAttr, obj1Attr
    mayac.connectAttr(switchAttr, obj1Attr)
    mayac.connectAttr(switchAttr, "%s.inputX"%reverseNode)
    mayac.connectAttr("%s.outputX"%reverseNode, obj0Attr)
   
   
class Eyes_CTRL(object):
    def __init__(self, L_Eye_CTRL, R_Eye_CTRL, Head_CTRL, Global_CTRL):
        self.L_Eye_CTRL = L_Eye_CTRL
        self.R_Eye_CTRL = R_Eye_CTRL
        self.Aim_CTRL = mayac.circle(n="Eyes_Aim_CTRL", ch=False)[0]
        for attr in ["sx","sy","sz"]:
            mayac.setAttr("%s.%s"%(self.Aim_CTRL,attr), 4.0 if attr == "sy" else 8.0)
        mayac.makeIdentity(self.Aim_CTRL, apply=True, t=1, r=1, s=1)
        mayac.delete(mayac.parentConstraint(self.L_Eye_CTRL.Aim_CTRL, self.R_Eye_CTRL.Aim_CTRL, self.Aim_CTRL))
        DJB_ChangeDisplayColor(self.Aim_CTRL, color = "white") 
        mayac.parent(self.L_Eye_CTRL.Aim_CTRL, self.Aim_CTRL)
        mayac.parent(self.R_Eye_CTRL.Aim_CTRL, self.Aim_CTRL)
        mayac.makeIdentity(self.L_Eye_CTRL.Aim_CTRL, apply=True, t=1, r=1, s=1)
        mayac.makeIdentity(self.R_Eye_CTRL.Aim_CTRL, apply=True, t=1, r=1, s=1)
        self.CONST_GRP = DJB_createGroup(transform = self.Aim_CTRL, suffix = "_CONST_GRP", pivotFrom = "self")
        self.POS_GRP = DJB_createGroup(transform = self.CONST_GRP, suffix = "_POS_GRP", pivotFrom = "self")
        switchAttr = "FollowHead"
        mayac.addAttr(self.Aim_CTRL,  shortName=switchAttr, longName='FollowHead', h=False, k=True, defaultValue=1.0, minValue=0.0, maxValue=1.0 )
        CreateSwitch(self.CONST_GRP, Global_CTRL, Head_CTRL, switchAttr = "%s.%s"%(self.Aim_CTRL, switchAttr), type = "parentConstraint")
        
        
        
class Eye_CTRL(object):
    def __init__(self, eye_jnt, eye_CTRL):
        self.joint = eye_jnt
        self.CTRL = eye_CTRL
        self.Aim_CTRL = mayac.circle(n="%s_Aim_CTRL"%(self.CTRL.split("_")[0]), ch=False)[0]
        for attr in ["sx","sy","sz"]:
            mayac.setAttr("%s.%s"%(self.Aim_CTRL,attr), 2.0)
        mayac.delete(mayac.parentConstraint(self.joint, self.Aim_CTRL))
        mayac.setAttr("%s.tz"%self.Aim_CTRL, (mayac.getAttr("%s.tz"%self.Aim_CTRL)+ 40))
        mayac.makeIdentity(self.Aim_CTRL, apply=True, t=1, r=1, s=1)
        DJB_ChangeDisplayColor(self.Aim_CTRL, color = ("blue1" if "Left" in self.CTRL else "red1"))
        
        
        
    
class FacialControls(object):
    def __init__(self, meshes=None, characterNameSpace = ""):
        self.facePlusBlends = ["Blink_Left",
                                "Blink_Right",
                                "BrowsDown_Left",
                                "BrowsDown_Right",
                                "BrowsIn_Left",
                                "BrowsIn_Right",
                                "BrowsOuterLower_Left",
                                "BrowsOuterLower_Right",
                                "BrowsUp_Left",
                                "BrowsUp_Right",
                                "CheekPuff_Left",
                                "CheekPuff_Right",
                                "EyesWide_Left",
                                "EyesWide_Right",
                                "Frown_Left",
                                "Frown_Right",
                                "JawBackward",
                                "JawForeward",
                                "JawRotateY_Left",
                                "JawRotateY_Right",
                                "JawRotateZ_Left",
                                "JawRotateZ_Right",
                                "Jaw_Down",
                                "Jaw_Left",
                                "Jaw_Right",
                                "Jaw_Up",
                                "LowerLipDown_Left",
                                "LowerLipDown_Right",
                                "LowerLipIn",
                                "LowerLipOut",
                                "Midmouth_Left",
                                "Midmouth_Right",
                                "MouthDown",
                                "MouthNarrow_Left",
                                "MouthNarrow_Right",
                                "MouthOpen",
                                "MouthUp",
                                "MouthWhistle_NarrowAdjust_Left",
                                "MouthWhistle_NarrowAdjust_Right",
                                "NoseScrunch_Left",
                                "NoseScrunch_Right",
                                "Smile_Left",
                                "Smile_Right",
                                "Squint_Left",
                                "Squint_Right",
                                "TongueUp",
                                "UpperLipIn",
                                "UpperLipOut",
                                "UpperLipUp_Left",
                                "UpperLipUp_Right"]
        self.mesh = meshes
        self.characterNameSpace = characterNameSpace
        self.blendshapeNodes = self.verifyFacePlus()
        self.FacialControlLayer = None

    def verifyFacePlus(self):
        "Verifying Character is set up with FacePlus rig"
        blendshapeNodes = []
        for i in range(len(self.mesh)):
            oldSkin = mayac.listConnections(self.characterNameSpace + self.mesh[i], destination = True, type = "skinCluster")
            if oldSkin:
                oldSkin = oldSkin[0]
            else:  #special case if there are deformers on top of rig and skinCluster is no longer directly connected
                connections = mayac.listConnections((self.characterNameSpace + self.mesh[i]), destination = True)
                if not connections:
                    for connection in connections:
                        if "skinCluster" in connection:
                            oldSkin = connection[:-3]
            
            isBlendShape = mayac.listConnections(self.mesh[i], d=True, type='blendShape')
            if not isBlendShape:  
                #Keep track of blendshapes and zero out
                meshConnections = mayac.listConnections(self.mesh[i], type = "objectSet")
                if meshConnections:
                    meshConnections = set(meshConnections)
                    autoKeyframeState = mayac.autoKeyframe(q=True, state=True)
                    mayac.autoKeyframe(state=False)   
                    for con in meshConnections:
                        blendShapeCons = mayac.listConnections(con, type = "blendShape")
                        if blendShapeCons:
                            for blendShapeNode in blendShapeCons:
                                print "\tChecking %s"%(blendShapeNode)
                                availableShapes = mayac.aliasAttr(blendShapeNode, q=True)[::2]
                                for i in range(len(self.facePlusBlends)):
                                    if self.facePlusBlends[i] in availableShapes:
                                        print "valid"
                                        blendshapeNodes.append(blendShapeNode)
                                        break
        if not blendshapeNodes:
            print "No valid blendshape sets to apply rig to"
        return blendshapeNodes
        
        
    def create(self, global_CTRL, Head_CTRL, LeftEye, RightEye, blends = False):
        print "Setting up Facial Rig"
        if blends:
            #TEMP
            filePath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"FacialControls.ma")
            print filePath
            faceRig = FacePlusRig.FacePlusRig()
            self.hookupNode = faceRig.FacialHookupNode
            self.POSNode = faceRig.POS_GRP
            self.moverNode = faceRig.MoverCTRL.transformNode
            self.connectUI(global_CTRL, Head_CTRL, LeftEye.Bind_Joint, RightEye.Bind_Joint)
        self.FacialGRP = mayac.group(em=True, name = "Facial_CTRLS_GRP")
        self.FacialControl_Layer = mayac.createDisplayLayer(name="FacialControlLayer", number=2)
        mayac.editDisplayLayerMembers(self.FacialControl_Layer, self.FacialGRP, noRecurse=True)
        if blends:
            mayac.parent(self.POSNode, self.FacialGRP, noConnections=True)
        
        if LeftEye.Bind_Joint == None or RightEye.Bind_Joint == None: return None
        self.L_Eye_CTRL = Eye_CTRL(LeftEye.Bind_Joint, LeftEye.FK_CTRL)
        self.R_Eye_CTRL = Eye_CTRL(RightEye.Bind_Joint, RightEye.FK_CTRL)
        LeftEye.IK_CTRL = self.L_Eye_CTRL.Aim_CTRL
        RightEye.IK_CTRL = self.R_Eye_CTRL.Aim_CTRL
        self.Eyes_CTRL = Eyes_CTRL(self.L_Eye_CTRL, self.R_Eye_CTRL, Head_CTRL, global_CTRL)
        mayac.parent(self.Eyes_CTRL.POS_GRP, self.FacialGRP)
        LeftEye.IK_Constraint = mayac.aimConstraint(LeftEye.IK_CTRL, LeftEye.IK_Joint, n="LeftEye_IK_AimConstraint", maintainOffset=True, aim=[0,0,1])[0]
        RightEye.IK_Constraint = mayac.aimConstraint(RightEye.IK_CTRL, RightEye.IK_Joint, n="RightEye_IK_AimConstraint", maintainOffset=True, aim=[0,0,1])[0]
        LeftEye.FK_Constraint = mayac.orientConstraint(LeftEye.FK_CTRL, LeftEye.FK_Joint, n="LeftEye_FK_Constraint", maintainOffset=True)[0]
        RightEye.FK_Constraint = mayac.orientConstraint(RightEye.FK_CTRL, RightEye.FK_Joint, n="RightEye_FK_Constraint", maintainOffset=True)[0]
        LeftEye.IK_CTRL_COLOR = "blue1"
        RightEye.IK_CTRL_COLOR = "red1"
        
        
    def connectUI(self, global_CTRL, Head_CTRL, L_Eye_JNT, R_Eye_JNT):
        for blendshapeNode in self.blendshapeNodes:
            availableHookupAttrs = mayac.listAttr(self.hookupNode, s=True, r=True, w=True, c=True, ud=True)
            availableShapes = mayac.aliasAttr(blendshapeNode, q=True)[::2]
            for attr in availableHookupAttrs:
                match = []
                for shape in availableShapes:
                    if attr.lower() in shape.lower():
                        match.append(shape)
                if match:
                    mayac.connectAttr("%s.%s"%(self.hookupNode,attr),"%s.%s"%(blendshapeNode,match[0]))
                else:
                    print "NO MATCH FOR %s"%attr
        CreateSwitch(self.POSNode, global_CTRL, Head_CTRL, switchAttr = "%s.Follow_Head"%self.moverNode, type = "parentConstraint")