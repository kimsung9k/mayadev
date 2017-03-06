'''
DJB_Character.CharacterNode
Handles:
    Class for individual body parts
'''
from MayaAutoControlRig.Utils import *

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

class DJB_CharacterNode():
    def __init__(self, joint_name_, infoNode_ = None, optional_ = 0, hasIK_ = 0, parent = None, nameSpace_ = "", joint_namespace_ = "", actAsRoot_ = 0, alias_ = None, dynamic_ = None, twistJoint_ = False, translateOpen_ = False):
        self.characterNameSpace = nameSpace_
        self.joint_namespace = joint_namespace_
        self.infoNode = None
        if infoNode_:
            self.infoNode = self.characterNameSpace + infoNode_
        self.nodeName = joint_name_
        self.children = []
        self.AnimData_Joint = None
        self.Bind_Joint = None
        self.Export_Joint = None
        self.origPosX = None
        self.origPosY = None
        self.origPosZ = None
        self.origRotX = None
        self.origRotY = None
        self.origRotZ = None
        self.FK_Joint =  None
        self.IK_Joint = None
        self.IK_Dummy_Joint = None
        self.templateGeo = None
        self.FK_CTRL = None
        self.FK_CTRL_COLOR = None
        self.FK_CTRL_inRig_CONST_GRP = None
        self.FK_CTRL_animData_CONST_GRP = None
        self.FK_CTRL_animData_MultNode = None
        self.FK_CTRL_animData_MultNode_Trans = None
        self.FK_CTRL_POS_GRP = None
        self.IK_CTRL = None
        self.IK_CTRL_COLOR = None
        self.IK_CTRL_inRig_CONST_GRP = None
        self.IK_CTRL_animData_CONST_GRP = None
        self.IK_CTRL_animData_MultNode = None
        self.IK_CTRL_POS_GRP = None
        self.IK_CTRL_ReorientGRP = None
        
        self.IK_CTRL_parent_animData_CONST_GRP = None
        self.IK_CTRL_parent_animData_MultNode = None
        self.IK_CTRL_parent_POS_GRP = None
        
        self.IK_CTRL_grandparent_inRig_CONST_GRP = None
        self.IK_CTRL_grandparent_animData_CONST_GRP = None
        self.IK_CTRL_grandparent_animData_MultNode = None
        self.IK_CTRL_grandparent_POS_GRP = None
        
        self.Inherit_Rotation_GRP = None
        self.Inherit_Rotation_Constraint = None
        self.Inherit_Rotation_Reverse = None
        self.Constraint = None
        self.FK_Constraint = None
        self.IK_Constraint = None
        self.IK_Handle = None
        self.IK_EndEffector = None
        self.PV_Constraint = None
        self.Guide_Curve = None
        self.Guide_Curve_Cluster1 = None
        self.Guide_Curve_Cluster2 = None
        self.Options_CTRL = None
        self.Options_CTRL_COLOR = None
        
        self.IK_CTRL_parent_Global_POS_GRP = None
        self.IK_CTRL_grandparent_Global_POS_GRP = None
        self.grandparent_Global_Constraint = None
        self.grandparent_Global_Constraint_Reverse = None
        self.parent_Global_Constraint = None
        self.parent_Global_Constraint_Reverse = None
        
        self.follow_extremity_Constraint = None
        self.follow_extremity_Constraint_Reverse = None
        
        self.locator = None
        self.locatorConstraint = None
        self.locator1 = None
        self.locatorConstraint1 = None
        self.locator2 = None
        self.locatorConstraint2 = None
        self.locator3 = None
        self.locatorConstraint3 = None
        self.footRotateLOC = None
        self.Follow_Foot_GRP = None
        self.Follow_Knee_GRP = None
        self.Follow_Knee_Constraint = None
        self.Follow_Foot_Constraint = None
        self.IK_BakingLOC = None
        self.actAsRoot = actAsRoot_
        self.rotOrder = None
        self.alias = alias_
        self.twistJoint = twistJoint_
        
        self.dynamic = dynamic_
        self.Dyn_Joint = None
        self.DynMult_Joint = None
        self.Dyn_Mult = None
        self.Dyn_CTRL = None
        self.Dyn_CTRL_COLOR = None
        self.Dyn_Node = None
        self.translateOpen = translateOpen_
        self.parent = parent
        
        
        
        
        if not self.infoNode:
            if not self.Bind_Joint:
                self.Bind_Joint = self.validateExistance(str(self.joint_namespace) + joint_name_)
            if not self.Bind_Joint and self.alias:
                for alias in self.alias:
                    self.Bind_Joint = self.validateExistance(str(self.joint_namespace) + alias)
                    if self.Bind_Joint:
                        break
            if not self.Bind_Joint and not optional_:
                OpenMaya.MGlobal.displayError("ERROR: %s cannot be found and is necessary for the autorigger to complete process" % (str(self.joint_namespace) + joint_name_))
                sys.exit()
            
            if self.Bind_Joint:
                self.Bind_Joint = mayac.rename(self.Bind_Joint, 'Bind_' + joint_name_)
                mel.eval('CBdeleteConnection "%s.tx";'%(self.Bind_Joint))
                mel.eval('CBdeleteConnection "%s.ty";'%(self.Bind_Joint))
                mel.eval('CBdeleteConnection "%s.tz";'%(self.Bind_Joint))
                mel.eval('CBdeleteConnection "%s.rx";'%(self.Bind_Joint))
                mel.eval('CBdeleteConnection "%s.ry";'%(self.Bind_Joint))
                mel.eval('CBdeleteConnection "%s.rz";'%(self.Bind_Joint))
                self.rotOrder = mayac.getAttr("%s.rotateOrder" %(self.Bind_Joint))
            if not self.Bind_Joint:
                return None
            self.parent = parent
            if self.parent:
                self.parent.children.append(self)
       
        #recreate from an infoNode
        else:              
            self.parent = parent
            if self.parent:
                self.parent.children.append(self)
            try:
                self.Bind_Joint = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Bind_Joint" % (self.infoNode)))
            except:
                version = mel.eval("float $ver = `getApplicationVersionAsFloat`;")
                if version == 2010.0:
                    OpenMaya.MGlobal.displayError("The Auto-Control Setup requires namespaces in Maya 2010.")
                return None
            if not self.nodeName:
                self.nodeName = attrToPy("%s.nodeName" % (self.infoNode))
                if not self.nodeName:
                    self.nodeName = self.Bind_Joint[5:]
            self.AnimData_Joint = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.AnimData_Joint" % (self.infoNode)))
            self.rotOrder = attrToPy("%s.rotOrder" % (self.infoNode))
            self.origPosX = attrToPy("%s.origPosX" % (self.infoNode))
            self.origPosY = attrToPy("%s.origPosY" % (self.infoNode))
            self.origPosZ = attrToPy("%s.origPosZ" % (self.infoNode))
            self.origRotX = attrToPy("%s.origRotX" % (self.infoNode))
            self.origRotY = attrToPy("%s.origRotY" % (self.infoNode))
            self.origRotZ = attrToPy("%s.origRotZ" % (self.infoNode))
            self.FK_Joint =  DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.FK_Joint" % (self.infoNode)))
            self.IK_Joint = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.IK_Joint" % (self.infoNode)))
            self.IK_Dummy_Joint = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.IK_Dummy_Joint" % (self.infoNode)))
            self.Export_Joint = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Export_Joint" % (self.infoNode)))
            self.templateGeo = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.templateGeo" % (self.infoNode)))
            self.FK_CTRL = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.FK_CTRL" % (self.infoNode)))
            self.FK_CTRL_COLOR = attrToPy("%s.FK_CTRL_COLOR" % (self.infoNode))
            self.FK_CTRL_inRig_CONST_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.FK_CTRL_inRig_CONST_GRP" % (self.infoNode)))
            self.FK_CTRL_animData_CONST_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.FK_CTRL_animData_CONST_GRP" % (self.infoNode)))
            self.FK_CTRL_animData_MultNode = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.FK_CTRL_animData_MultNode" % (self.infoNode)))
            self.FK_CTRL_animData_MultNode_Trans = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.FK_CTRL_animData_MultNode_Trans" % (self.infoNode)))
            self.FK_CTRL_POS_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.FK_CTRL_POS_GRP" % (self.infoNode)))
            self.IK_CTRL = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.IK_CTRL" % (self.infoNode)))
            self.IK_CTRL_COLOR = attrToPy("%s.IK_CTRL_COLOR" % (self.infoNode))
            self.IK_CTRL_inRig_CONST_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.IK_CTRL_inRig_CONST_GRP" % (self.infoNode)))
            self.IK_CTRL_animData_CONST_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.IK_CTRL_animData_CONST_GRP" % (self.infoNode)))
            self.IK_CTRL_animData_MultNode = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.IK_CTRL_animData_MultNode" % (self.infoNode)))
            self.IK_CTRL_POS_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.IK_CTRL_POS_GRP" % (self.infoNode)))
            self.IK_CTRL_ReorientGRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.IK_CTRL_ReorientGRP" % (self.infoNode)))
            
            self.IK_CTRL_parent_animData_CONST_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.IK_CTRL_parent_animData_CONST_GRP" % (self.infoNode)))
            self.IK_CTRL_parent_animData_MultNode = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.IK_CTRL_parent_animData_MultNode" % (self.infoNode)))
            self.IK_CTRL_parent_POS_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.IK_CTRL_parent_POS_GRP" % (self.infoNode)))
            
            self.IK_CTRL_grandparent_inRig_CONST_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.IK_CTRL_parent_POS_GRP" % (self.infoNode)))
            self.IK_CTRL_grandparent_animData_CONST_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.IK_CTRL_grandparent_animData_CONST_GRP" % (self.infoNode)))
            self.IK_CTRL_grandparent_animData_MultNode = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.IK_CTRL_grandparent_animData_MultNode" % (self.infoNode)))
            self.IK_CTRL_grandparent_POS_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.IK_CTRL_grandparent_POS_GRP" % (self.infoNode)))
            
            self.Inherit_Rotation_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Inherit_Rotation_GRP" % (self.infoNode)))
            self.Inherit_Rotation_Constraint = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Inherit_Rotation_Constraint" % (self.infoNode)))
            self.Inherit_Rotation_Reverse = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Inherit_Rotation_Reverse" % (self.infoNode)))
            self.Constraint = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Constraint" % (self.infoNode)))
            self.FK_Constraint = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.FK_Constraint" % (self.infoNode)))
            self.IK_Constraint = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.IK_Constraint" % (self.infoNode)))
            self.IK_Handle = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.IK_Handle" % (self.infoNode)))
            self.IK_EndEffector = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.IK_EndEffector" % (self.infoNode)))
            self.PV_Constraint = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.PV_Constraint" % (self.infoNode)))
            self.Guide_Curve = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Guide_Curve" % (self.infoNode)))
            self.Guide_Curve_Cluster1 = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Guide_Curve_Cluster1" % (self.infoNode)))
            self.Guide_Curve_Cluster2 = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Guide_Curve_Cluster2" % (self.infoNode)))
            self.Options_CTRL = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Options_CTRL" % (self.infoNode)))
            self.Options_CTRL_COLOR = attrToPy("%s.Options_CTRL_COLOR" % (self.infoNode))
            
            self.IK_CTRL_parent_Global_POS_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.IK_CTRL_parent_Global_POS_GRP" % (self.infoNode)))
            self.IK_CTRL_grandparent_Global_POS_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.IK_CTRL_grandparent_Global_POS_GRP" % (self.infoNode)))
            self.grandparent_Global_Constraint = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.grandparent_Global_Constraint" % (self.infoNode)))
            self.grandparent_Global_Constraint_Reverse = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.grandparent_Global_Constraint_Reverse" % (self.infoNode)))
            self.parent_Global_Constraint = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.parent_Global_Constraint" % (self.infoNode)))
            self.parent_Global_Constraint_Reverse = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.parent_Global_Constraint_Reverse" % (self.infoNode)))
            
            self.follow_extremity_Constraint = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.follow_extremity_Constraint" % (self.infoNode)))
            self.follow_extremity_Constraint_Reverse = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.follow_extremity_Constraint_Reverse" % (self.infoNode)))
            
            self.locator = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.locator" % (self.infoNode)))
            self.locatorConstraint = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.locator" % (self.infoNode)))
            self.locator1 = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.locator1" % (self.infoNode)))
            self.locatorConstraint1 = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.locatorConstraint1" % (self.infoNode)))
            self.footRotateLOC = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.footRotateLOC" % (self.infoNode)))
            self.Follow_Foot_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Follow_Foot_GRP" % (self.infoNode)))
            self.Follow_Knee_GRP = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Follow_Knee_GRP" % (self.infoNode)))
            self.Follow_Knee_Constraint = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Follow_Knee_Constraint" % (self.infoNode)))
            self.Follow_Foot_Constraint = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Follow_Knee_Constraint" % (self.infoNode)))
            self.IK_BakingLOC = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.IK_BakingLOC" % (self.infoNode)))

            self.dynamic = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.dynamic" % (self.infoNode)))
            self.Dyn_Joint = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Dyn_Joint" % (self.infoNode)))
            self.Dyn_CTRL = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Dyn_CTRL" % (self.infoNode)))
            self.Dyn_CTRL_COLOR = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Dyn_CTRL_COLOR" % (self.infoNode)))
            self.Dyn_Node = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Dyn_Node" % (self.infoNode)))
            self.DynMult_Joint = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Dyn_Node" % (self.infoNode)))
            self.Dyn_Mult = DJB_addNameSpace(self.characterNameSpace, attrToPy("%s.Dyn_Mult" % (self.infoNode)))
            self.translateOpen = attrToPy("%s.translateOpen" % (self.infoNode))
            self.twistJoint = attrToPy("%s.twistJoint" % (self.infoNode))
            self.joint_namespace = attrToPy("%s.joint_namespace" % (self.infoNode))
        
        
    def writeInfoNode(self):
        self.infoNode = mayac.createNode("transform", name = "MIXAMO_CHARACTER_%s_infoNode" % (self.nodeName))
        
        pyToAttr("%s.nodeName" % (self.infoNode), self.nodeName)
        if self.parent:
            pyToAttr("%s.parent" % (self.infoNode), self.parent.nodeName)
        else:
            pyToAttr("%s.parent" % (self.infoNode), None)
        pyToAttr("%s.joint_namespace" % (self.infoNode), self.joint_namespace)
        pyToAttr("%s.Bind_Joint" % (self.infoNode), self.Bind_Joint)
        pyToAttr("%s.AnimData_Joint" % (self.infoNode), self.AnimData_Joint)
        pyToAttr("%s.rotOrder" % (self.infoNode), self.rotOrder)
        pyToAttr("%s.origPosX" % (self.infoNode), self.origPosX)
        pyToAttr("%s.origPosY" % (self.infoNode), self.origPosY)
        pyToAttr("%s.origPosZ" % (self.infoNode), self.origPosZ)
        pyToAttr("%s.origRotX" % (self.infoNode), self.origRotX)
        pyToAttr("%s.origRotY" % (self.infoNode), self.origRotY)
        pyToAttr("%s.origRotZ" % (self.infoNode), self.origRotZ)
        pyToAttr("%s.FK_Joint" % (self.infoNode), self.FK_Joint)
        pyToAttr("%s.IK_Joint" % (self.infoNode), self.IK_Joint)
        pyToAttr("%s.IK_Dummy_Joint" % (self.infoNode), self.IK_Dummy_Joint)
        pyToAttr("%s.Export_Joint" % (self.infoNode), self.Export_Joint)
        pyToAttr("%s.templateGeo" % (self.infoNode), self.templateGeo)
        pyToAttr("%s.FK_CTRL" % (self.infoNode), self.FK_CTRL)
        pyToAttr("%s.FK_CTRL_COLOR" % (self.infoNode), self.FK_CTRL_COLOR)
        pyToAttr("%s.FK_CTRL_inRig_CONST_GRP" % (self.infoNode), self.FK_CTRL_inRig_CONST_GRP)
        pyToAttr("%s.FK_CTRL_animData_CONST_GRP" % (self.infoNode), self.FK_CTRL_animData_CONST_GRP)
        pyToAttr("%s.FK_CTRL_animData_MultNode" % (self.infoNode), self.FK_CTRL_animData_MultNode)
        pyToAttr("%s.FK_CTRL_animData_MultNode_Trans" % (self.infoNode), self.FK_CTRL_animData_MultNode_Trans)
        pyToAttr("%s.FK_CTRL_POS_GRP" % (self.infoNode), self.FK_CTRL_POS_GRP)
        pyToAttr("%s.IK_CTRL" % (self.infoNode), self.IK_CTRL)
        pyToAttr("%s.IK_CTRL_COLOR" % (self.infoNode), self.IK_CTRL_COLOR)
        pyToAttr("%s.IK_CTRL_inRig_CONST_GRP" % (self.infoNode), self.IK_CTRL_inRig_CONST_GRP)
        pyToAttr("%s.IK_CTRL_animData_CONST_GRP" % (self.infoNode), self.IK_CTRL_animData_CONST_GRP)
        pyToAttr("%s.IK_CTRL_animData_MultNode" % (self.infoNode), self.IK_CTRL_animData_MultNode)
        pyToAttr("%s.IK_CTRL_POS_GRP" % (self.infoNode), self.IK_CTRL_POS_GRP)
        pyToAttr("%s.IK_CTRL_ReorientGRP" % (self.infoNode), self.IK_CTRL_ReorientGRP)
        pyToAttr("%s.IK_CTRL_parent_animData_CONST_GRP" % (self.infoNode), self.IK_CTRL_parent_animData_CONST_GRP)
        pyToAttr("%s.IK_CTRL_parent_animData_MultNode" % (self.infoNode), self.IK_CTRL_parent_animData_MultNode)
        pyToAttr("%s.IK_CTRL_parent_POS_GRP" % (self.infoNode), self.IK_CTRL_parent_POS_GRP)
        pyToAttr("%s.IK_CTRL_grandparent_inRig_CONST_GRP" % (self.infoNode), self.IK_CTRL_grandparent_inRig_CONST_GRP)
        pyToAttr("%s.IK_CTRL_grandparent_animData_CONST_GRP" % (self.infoNode), self.IK_CTRL_grandparent_animData_CONST_GRP)
        pyToAttr("%s.IK_CTRL_grandparent_animData_MultNode" % (self.infoNode), self.IK_CTRL_grandparent_animData_MultNode)
        pyToAttr("%s.IK_CTRL_grandparent_POS_GRP" % (self.infoNode), self.IK_CTRL_grandparent_POS_GRP)
        pyToAttr("%s.Inherit_Rotation_GRP" % (self.infoNode), self.Inherit_Rotation_GRP)
        pyToAttr("%s.Inherit_Rotation_Constraint" % (self.infoNode), self.Inherit_Rotation_Constraint)
        pyToAttr("%s.Inherit_Rotation_Reverse" % (self.infoNode), self.Inherit_Rotation_Reverse)
        pyToAttr("%s.Constraint" % (self.infoNode), self.Constraint)
        pyToAttr("%s.FK_Constraint" % (self.infoNode), self.FK_Constraint)
        pyToAttr("%s.IK_Constraint" % (self.infoNode), self.IK_Constraint)
        pyToAttr("%s.IK_Handle" % (self.infoNode), self.IK_Handle)
        pyToAttr("%s.IK_EndEffector" % (self.infoNode), self.IK_EndEffector)
        pyToAttr("%s.PV_Constraint" % (self.infoNode), self.PV_Constraint)
        pyToAttr("%s.Guide_Curve" % (self.infoNode), self.Guide_Curve)
        pyToAttr("%s.Guide_Curve_Cluster1" % (self.infoNode), self.Guide_Curve_Cluster1)
        pyToAttr("%s.Guide_Curve_Cluster2" % (self.infoNode), self.Guide_Curve_Cluster2)
        pyToAttr("%s.Options_CTRL" % (self.infoNode), self.Options_CTRL)
        pyToAttr("%s.Options_CTRL_COLOR" % (self.infoNode), self.Options_CTRL_COLOR)
        pyToAttr("%s.IK_CTRL_parent_Global_POS_GRP" % (self.infoNode), self.IK_CTRL_parent_Global_POS_GRP)
        pyToAttr("%s.IK_CTRL_grandparent_Global_POS_GRP" % (self.infoNode), self.IK_CTRL_grandparent_Global_POS_GRP)
        pyToAttr("%s.grandparent_Global_Constraint" % (self.infoNode), self.grandparent_Global_Constraint)
        pyToAttr("%s.grandparent_Global_Constraint_Reverse" % (self.infoNode), self.grandparent_Global_Constraint_Reverse)
        pyToAttr("%s.parent_Global_Constraint" % (self.infoNode), self.parent_Global_Constraint)
        pyToAttr("%s.parent_Global_Constraint_Reverse" % (self.infoNode), self.parent_Global_Constraint_Reverse)
        pyToAttr("%s.follow_extremity_Constraint" % (self.infoNode), self.follow_extremity_Constraint)
        pyToAttr("%s.follow_extremity_Constraint_Reverse" % (self.infoNode), self.follow_extremity_Constraint_Reverse)
        pyToAttr("%s.locator" % (self.infoNode), self.locator)
        pyToAttr("%s.locatorConstraint" % (self.infoNode), self.locatorConstraint)
        pyToAttr("%s.locator1" % (self.infoNode), self.locator1)
        pyToAttr("%s.locatorConstraint1" % (self.infoNode), self.locatorConstraint1)
        pyToAttr("%s.footRotateLOC" % (self.infoNode), self.footRotateLOC)
        pyToAttr("%s.Follow_Foot_GRP" % (self.infoNode), self.Follow_Foot_GRP)
        pyToAttr("%s.Follow_Knee_GRP" % (self.infoNode), self.Follow_Knee_GRP)
        pyToAttr("%s.Follow_Knee_Constraint" % (self.infoNode), self.Follow_Knee_Constraint)
        pyToAttr("%s.Follow_Foot_Constraint" % (self.infoNode), self.Follow_Foot_Constraint)
        pyToAttr("%s.IK_BakingLOC" % (self.infoNode), self.IK_BakingLOC)
        
        #Dynamics
        pyToAttr("%s.dynamic" % (self.infoNode), self.dynamic)
        pyToAttr("%s.Dyn_Joint" % (self.infoNode), self.Dyn_Joint)
        pyToAttr("%s.Dyn_CTRL" % (self.infoNode), self.Dyn_CTRL)
        pyToAttr("%s.Dyn_CTRL_COLOR" % (self.infoNode), self.Dyn_CTRL_COLOR)
        pyToAttr("%s.Dyn_Node" % (self.infoNode), self.Dyn_Node)
        pyToAttr("%s.DynMult_Joint" % (self.infoNode), self.DynMult_Joint)
        pyToAttr("%s.Dyn_Mult" % (self.infoNode), self.Dyn_Mult)
        pyToAttr("%s.translateOpen" % (self.infoNode), self.translateOpen)
        pyToAttr("%s.twistJoint" % (self.infoNode), self.twistJoint)
        
        return self.infoNode
        
     
     
    def fixAllLayerOverrides(self, layer):
        if self.FK_CTRL:
            self.fixLayerOverrides(self.FK_CTRL, self.FK_CTRL_COLOR, layer)
        if self.IK_CTRL:
            self.fixLayerOverrides(self.IK_CTRL, self.IK_CTRL_COLOR, layer)
        if self.Options_CTRL:
            self.fixLayerOverrides(self.Options_CTRL, self.Options_CTRL_COLOR, layer)
        if self.Dyn_CTRL:
            self.fixLayerOverrides(self.Dyn_CTRL, self.Dyn_CTRL_COLOR, layer)
        
           
    def fixLayerOverrides(self, control, color, layer, referenceAlways = False):
        connection =  mayac.listConnections( "%s.drawOverride" % (control), s=True, plugs=True)
        if connection:
            mayac.disconnectAttr(connection[0], "%s.drawOverride" % (control))
        mayac.connectAttr("%s.levelOfDetail" % (layer), "%s.overrideLevelOfDetail" % (control), force = True)
        mayac.connectAttr("%s.shading" % (layer), "%s.overrideShading" % (control), force = True)
        mayac.connectAttr("%s.texturing" % (layer), "%s.overrideTexturing" % (control), force = True)
        mayac.connectAttr("%s.playback" % (layer), "%s.overridePlayback" % (control), force = True)
        
        connection =  mayac.listConnections( "%s.overrideVisibility" % (control), s=True, plugs=True)
        if connection:
            mayac.disconnectAttr(connection, "%s.overrideVisibility" % (control))
        mayac.connectAttr("%s.visibility" % (layer), "%s.overrideVisibility" % (control), force = True)
        DJB_ChangeDisplayColor(control, color = color)
        if referenceAlways:
            mayac.setAttr("%s.overrideDisplayType" % (control), 2)
        else:
            mayac.connectAttr("%s.displayType" % (layer), "%s.overrideDisplayType" % (control), force = True)
        shapes = mayac.listRelatives(control, children = True, shapes = True)
        if shapes:
            for shape in shapes:
                self.fixLayerOverrides(shape, color, layer, referenceAlways)
    
        
    def validateExistance(self, object):
        if mayac.objExists(object):
            return object
        else:
            return None

    def duplicateJoint(self, type, parent_ = "UseSelf"):
        if self.Bind_Joint:
            if type == "AnimData":
                self.AnimData_Joint = mayac.duplicate(self.Bind_Joint, parentOnly = True, name = "AnimData_" + self.nodeName)[0]
            elif type == "FK":
                self.FK_Joint = mayac.duplicate(self.Bind_Joint, parentOnly = True, name = "FK_" + self.nodeName)[0]
            elif type == "IK":
                self.IK_Joint = mayac.duplicate(self.Bind_Joint, parentOnly = True, name = "IK_" + self.nodeName)[0]
            elif type == "IK_Dummy":
                self.IK_Dummy_Joint = mayac.duplicate(self.Bind_Joint, parentOnly = True, name = "IK_Dummy_" + self.nodeName)[0]
            elif type == "ExportSkeleton":
                if self.joint_namespace:
                    if not mayac.namespace(exists = self.joint_namespace):
                        mayac.namespace(add=self.joint_namespace[0:len(self.joint_namespace)-1])
                    self.Export_Joint = mayac.duplicate(self.Bind_Joint, parentOnly = True, inputConnections=False, name = self.joint_namespace + self.nodeName)[0]
                else:
                    temp = mayac.duplicate(self.Bind_Joint, parentOnly = True, name = self.nodeName)
                    self.Export_Joint = temp[0]
                try:
                    connections = mayac.listConnections("%s.drawOverride"%self.Export_Joint, s=True, plugs=True)
                    if connections:
                        mayac.disconnectAttr(connections[0], "%s.drawOverride"%self.Export_Joint)
                    connections = mayac.listConnections("%s.instObjGroups[0]"%self.Export_Joint, d=True, plugs=True)
                    if connections:
                        mayac.disconnectAttr("%s.instObjGroups[0]"%self.Export_Joint, connections[0])
                    
                    mayac.parent(self.Export_Joint, world = True)
                except:
                    pass
            elif type == "ZV":
                self.Dyn_Joint = mayac.duplicate(self.Bind_Joint, parentOnly = True, name = "DYN_" + self.nodeName)[0]
                self.DynMult_Joint = mayac.duplicate(self.Bind_Joint, parentOnly = True, name = "DynMult_" + self.nodeName)[0]
            if parent_ == "UseSelf" and self.parent:
                if type == "AnimData":
                    mayac.parent(self.AnimData_Joint, self.parent.AnimData_Joint)
                if type == "FK":
                    mayac.parent(self.FK_Joint, self.parent.FK_Joint)
                if type == "IK":
                    mayac.parent(self.IK_Joint, self.parent.IK_Joint)
                if type == "IK_Dummy":
                    mayac.parent(self.IK_Dummy_Joint, self.parent.IK_Dummy_Joint)
                if type == "ZV":
                    mayac.parent(self.Dyn_Joint, self.parent.Dyn_Joint)
                    mayac.parent(self.DynMult_Joint, self.parent.DynMult_Joint)
                if type == "ExportSkeleton":
                    mayac.parent(self.Export_Joint, self.parent.Export_Joint)
                    if self.joint_namespace and self.Export_Joint != (self.joint_namespace + self.nodeName):
                        #add namespace to scene if should have it but doesn't
                        if not mayac.namespace(exists = self.joint_namespace):
                            mayac.namespace(add=self.joint_namespace[0:len(self.joint_namespace)-1])
                        self.Export_Joint = mayac.rename(self.Export_Joint, (self.joint_namespace + self.nodeName))
                            
                    
                    
    def createGuideCurve(self, group_, optionsCTRL = None, attr = "FK_IK"):
        tempLoc = mayac.spaceLocator()[0]
        mayac.delete(mayac.parentConstraint(self.IK_CTRL, tempLoc))
        pos1 = mayac.xform(tempLoc, query = True, absolute = True, worldSpace = True, translation = True)
        mayac.delete(tempLoc)
        pos2 = mayac.xform(self.IK_Joint, query = True, absolute = True, worldSpace = True, translation = True)
        self.Guide_Curve = mayac.curve(degree = 1, name = "%s_GuideCurve" % (self.IK_CTRL),
                                      point = [(pos1[0], pos1[1], pos1[2]), (pos2[0], pos2[1], pos2[2])],
                                      knot = [0,1])
        mayac.xform(self.Guide_Curve, centerPivots = True)
        mayac.select("%s.cv[0]" % (self.Guide_Curve), replace = True) ;
        temp = mayac.cluster(name = "%s_Cluster1" % (self.Guide_Curve))
        self.Guide_Curve_Cluster1 = temp[1]
        mayac.select("%s.cv[1]" % (self.Guide_Curve), replace = True) ;
        temp = mayac.cluster(name = "%s_Cluster2" % (self.Guide_Curve))
        self.Guide_Curve_Cluster2 = temp[1]
        mayac.parent(self.Guide_Curve_Cluster1, self.IK_CTRL)
        mayac.parent(self.Guide_Curve_Cluster2, self.IK_Joint)
        mayac.parent(self.Guide_Curve, group_)
        mayac.setAttr("%s.visibility" % (self.Guide_Curve_Cluster1),0)
        mayac.setAttr("%s.visibility" % (self.Guide_Curve_Cluster2),0)
        mayac.setAttr("%s.overrideEnabled" % (self.Guide_Curve), 1)
        mayac.setAttr("%s.overrideDisplayType" % (self.Guide_Curve), 1)
        multDiv = mayac.createNode( 'multiplyDivide', n=self.Guide_Curve + "_Visibility_MultNode")
        mayac.addAttr(self.IK_CTRL, longName='GuideCurve', defaultValue=1.0, min = 0.0, max = 1.0, keyable = True)
        mayac.connectAttr("%s.GuideCurve" %(self.IK_CTRL), "%s.input2X" %(multDiv), force = True)
        if optionsCTRL:
            mayac.connectAttr("%s.%s" %(optionsCTRL, attr), "%s.input1X" %(multDiv), force = True)
        mayac.connectAttr("%s.outputX" %(multDiv), "%s.visibility" %(self.Guide_Curve), force = True)
        DJB_LockNHide(self.Guide_Curve)
        DJB_LockNHide(self.Guide_Curve_Cluster1)
        DJB_LockNHide(self.Guide_Curve_Cluster2)



    def createControl(self, type, rigType = "AutoRig", style = "circle", partialConstraint = 0, scale = (0.1,0.1,0.1), rotate = (0,0,0), offset = (0,0,0), estimateSize = True, color_ = None, name_ = None, flipFingers = False):
        control = 0 
        if style == "circle":
            if estimateSize:
                control = mayac.circle(constructionHistory = 0)
                control = control[0]
                mayac.rotate(0, 90, 90)
                if "Root" not in self.nodeName and "Spine" not in self.nodeName and "Hips" not in self.nodeName and rigType == "World":
                    mayac.rotate(rotate[0], rotate[1], rotate[2], control, absolute = True) #override for world-oriented rigs
                if rigType == "Dyn":
                    mayac.rotate(rotate[0], rotate[1], rotate[2], control, relative = True)
                mayac.scale(scale[0],scale[1],scale[2])
                mayac.move(offset[0], offset[1], offset[2], "%s.cv[0:7]" % (control), relative = True)
                mayac.makeIdentity(control, apply = True, t=1, r=1, s=1, n=0)
            else:
                print "exactSizeNotFunctionalYet"
                
        elif style == "sphere":
            if estimateSize:
                circles = []
                circles.append(mayac.circle(constructionHistory = 0)[0])
                circles.append(mayac.circle(constructionHistory = 0)[0])
                circles.append(mayac.circle(constructionHistory = 0)[0])
                circles.append(mayac.circle(constructionHistory = 0)[0])
                mayac.setAttr("%s.rx"%circles[1], 90)
                mayac.setAttr("%s.ry"%circles[2], 90)
                mayac.setAttr("%s.tz"%circles[3], 0.75)
                mayac.setAttr("%s.scale"%circles[3], 0.66, 0.66, 0.66)
                for c in circles:
                    DJB_cleanGEO(c)
                DJB_parentShape(circles[0], circles[1])
                DJB_parentShape(circles[0], circles[2])
                DJB_parentShape(circles[0], circles[3])
                control = circles[0]
                mayac.select(control, replace=True)
                mayac.scale(scale[0],scale[1],scale[2])
                mayac.makeIdentity(control, apply = True, t=1, r=1, s=1, n=0)
            else:
                print "exactSizeNotFunctionalYet"

        elif style == "box":
            if estimateSize:
                control = mayac.curve(degree = 1,
                                      point = [(0.5, 0.5, 0.5),
                                          (0.5, 0.5, -0.5),
                                          (-0.5, 0.5, -0.5),
                                          (-0.5, -0.5, -0.5),
                                          (0.5, -0.5, -0.5),
                                          (0.5, 0.5, -0.5),
                                          (-0.5, 0.5, -0.5),
                                          (-0.5, 0.5, 0.5),
                                          (0.5, 0.5, 0.5),
                                          (0.5, -0.5, 0.5),
                                          (0.5, -0.5, -0.5),
                                          (-0.5, -0.5, -0.5),
                                          (-0.5, -0.5, 0.5),
                                          (0.5, -0.5, 0.5),
                                          (-0.5, -0.5, 0.5),
                                          (-0.5, 0.5, 0.5)],
                                      knot = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])                                                                            
                mayac.move(0, -.2, 0, "%s.cv[0]" % (control), "%s.cv[7:8]" % (control), "%s.cv[15]" % (control), relative = True)
                mayac.scale(1.3, 1.3, 1.3, "%s.cv[3:4]" % (control), "%s.cv[9:12]" % (control), "%s.cv[13:14]" % (control))       
                mayac.scale(scale[0], scale[1], scale[2], control)
                mayac.rotate(rotate[0], rotate[1], rotate[2], control, relative = True)
                mayac.move(offset[0], offset[1], offset[2],  "%s.cv[0:15]" % (control), relative = True)
                mayac.makeIdentity(control, apply = True, t=1, r=1, s=1, n=0)
            else:
                print "exactSizeNotFunctionalYet"
                
        elif style == "box1":
            if estimateSize:
                control = mayac.curve(degree = 1,
                                      point = [(0.5, 0.5, 0.5),
                                          (0.5, 0.5, -0.5),
                                          (-0.5, 0.5, -0.5),
                                          (-0.5, -0.5, -0.5),
                                          (0.5, -0.5, -0.5),
                                          (0.5, 0.5, -0.5),
                                          (-0.5, 0.5, -0.5),
                                          (-0.5, 0.5, 0.5),
                                          (0.5, 0.5, 0.5),
                                          (0.5, -0.5, 0.5),
                                          (0.5, -0.5, -0.5),
                                          (-0.5, -0.5, -0.5),
                                          (-0.5, -0.5, 0.5),
                                          (0.5, -0.5, 0.5),
                                          (-0.5, -0.5, 0.5),
                                          (-0.5, 0.5, 0.5)],
                                      knot = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])                                                                                  
                mayac.scale(scale[0], scale[1], scale[2], control)
                mayac.rotate(rotate[0], rotate[1], rotate[2], control, relative = True)
                mayac.move(offset[0], offset[1], offset[2],  "%s.cv[0:15]" % (control), relative = True)
                mayac.makeIdentity(control, apply = True, t=1, r=1, s=1, n=0)
            else:
                print "exactSizeNotFunctionalYet"
                
                
        elif style == "footBox":
            if estimateSize:
                control = mayac.curve(degree = 1,
                                      point = [(0.5, 0.5, 0.5),
                                          (0.5, 0.5, -0.5),
                                          (-0.5, 0.5, -0.5),
                                          (-0.5, -0.5, -0.5),
                                          (0.5, -0.5, -0.5),
                                          (0.5, 0.5, -0.5),
                                          (-0.5, 0.5, -0.5),
                                          (-0.5, 0.5, 0.5),
                                          (0.5, 0.5, 0.5),
                                          (0.5, -0.5, 0.5),
                                          (0.5, -0.5, -0.5),
                                          (-0.5, -0.5, -0.5),
                                          (-0.5, -0.5, 0.5),
                                          (0.5, -0.5, 0.5),
                                          (-0.5, -0.5, 0.5),
                                          (-0.5, 0.5, 0.5)],
                                      knot = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])                                                                            
                mayac.move(0, -.4, .1, "%s.cv[1:2]" % (control), "%s.cv[5:6]" % (control), relative = True)
                mayac.move(0, .1, 0, "%s.cv[3:4]" % (control), "%s.cv[10:11]" % (control), relative = True)
                mayac.move(0, .3, 0, "%s.cv[0]" % (control), "%s.cv[7:8]" % (control), "%s.cv[15]" % (control), relative = True)
                mayac.scale(1.0, .75, 1.0, "%s.cv[1:6]" % (control), "%s.cv[10:11]" % (control))      
                mayac.scale(scale[0], scale[1], scale[2], control)
                mayac.rotate(rotate[0], rotate[1], rotate[2], control, relative = True)
                mayac.move(offset[0], offset[1], offset[2],  "%s.cv[0:15]" % (control), relative = True)
                mayac.makeIdentity(control, apply = True, t=1, r=1, s=1, n=0)
            else:
                print "exactSizeNotFunctionalYet"
                

                
        elif style == "circleWrapped":
            if estimateSize:
                control = mayac.circle(constructionHistory = 0)
                control = control[0]
                mayac.move(0, 0, 1.0, "%s.cv[3]" % (control), "%s.cv[7]" % (control), relative = True)
                mayac.move(0, 0, -1.0, "%s.cv[1]" % (control), "%s.cv[5]" % (control), relative = True)
                mayac.scale(scale[0],scale[1],scale[2])
                mayac.rotate(rotate[0], rotate[1], rotate[2], control, relative = True) #override for world-oriented rigs
                mayac.move(offset[0], offset[1], offset[2], "%s.cv[0:7]" % (control), relative = True)
                mayac.makeIdentity(control, apply = True, t=1, r=1, s=1, n=0)
            else:
                print "exactSizeNotFunctionalYet"
            
            
        elif style == "pin":
            if estimateSize:
                control = mayac.circle(constructionHistory = 0)
                control = control[0]
                mayac.scale(1.0, 0.0, 0.0, "%s.cv[1:5]" % (control))
                mayac.move(-2.891806, 0, 0, "%s.cv[3]" % (control), relative = True)
                mayac.move(4.0, 0, 0, "%s.cv[0:7]" % (control), relative = True)
                mayac.rotate(180, 0, 180, control)
                mayac.scale(scale[0], scale[1], scale[2], control)
                mayac.rotate(rotate[0], rotate[1], rotate[2], control, relative = True) #override for world-oriented rigs
                mayac.move(offset[0], offset[1], offset[2], "%s.cv[0:7]" % (control), relative = True)
                mayac.makeIdentity(control, apply = True, t=1, r=1, s=1, n=0)
            else:
                print "exactSizeNotFunctionalYet"
                
        elif style == "pin1" or style == "pin2":
            if estimateSize:
                control = mayac.circle(constructionHistory = 0)
                control = control[0]
                mayac.scale(1.0, 0.0, 0.0, "%s.cv[1:5]" % (control))
                mayac.move(-2.891806, 0, 0, "%s.cv[3]" % (control), relative = True)
                mayac.move(4.0, 0, 0, "%s.cv[0:7]" % (control), relative = True)
                mayac.scale(scale[0], scale[1], scale[2], control)
                if flipFingers:
                    mayac.rotate(rotate[0], 180, rotate[2], control, relative = True) #flip fingers
                else:
                    mayac.rotate(rotate[0], rotate[1], rotate[2], control, relative = True) #override for world-oriented rigs
                mayac.move(offset[0], offset[1], offset[2], "%s.cv[0:7]" % (control), relative = True)
                mayac.makeIdentity(control, apply = True, t=1, r=1, s=1, n=0)
            else:
                print "exactSizeNotFunctionalYet"       
        

        elif style == "options":
            if estimateSize:
                control = mayac.curve(degree = 1,
                                      point = [(-1.03923, 0.0, 0.6),
                                          (1.03923, 0.0, 0.6),
                                          (0.0, 0.0, -1.2),
                                          (-1.03923, 0.0, 0.6)],
                                      knot = [0,1,2,3])    
                mayac.scale(scale[0], scale[1], scale[2], control)
                mayac.rotate(rotate[0], rotate[1], rotate[2], control, relative = True)
                mayac.rotate(rotate[0], rotate[1], rotate[2], control, relative = True) #override for world-oriented rigs
                mayac.move(offset[0], offset[1], offset[2],  "%s.cv[0:15]" % (control), relative = True)
                mayac.makeIdentity(control, apply = True, t=1, r=1, s=1, n=0)
            else:
                print "exactSizeNotFunctionalYet"
            
            
        elif style == "hula":
            if estimateSize:
                control = mayac.circle(constructionHistory = 0)
                control = control[0]
                mayac.move(0, 0, -0.5, "%s.cv[0]" % (control), "%s.cv[2]" % (control), "%s.cv[4]" % (control), "%s.cv[6]" % (control), relative = True)
                mayac.move(0, 0, 0.3, "%s.cv[1]" % (control), "%s.cv[3]" % (control), "%s.cv[5]" % (control), "%s.cv[7]" % (control), relative = True)
                mayac.rotate(0, 90, 90, control)
                mayac.scale(scale[0], scale[1], scale[2], control)
                mayac.move(offset[0], offset[1], offset[2], "%s.cv[0:7]" % (control), relative = True)
                mayac.makeIdentity(control, apply = True, t=1, r=1, s=1, n=0)
            else:
                print "exactSizeNotFunctionalYet"
                
                
        elif style == "PoleVector":
            if estimateSize:
                control = mayac.curve(degree = 1,
                                      point = [(0.0, 2.0, 0.0),
                                          (1.0, 0.0, -1.0),
                                          (-1.0, 0.0, -1.0),
                                          (0.0, 2.0, 0.0),
                                          (-1.0, 0.0, 1.0),
                                          (1.0, 0.0, 1.0),
                                          (0.0, 2.0, 0.0),
                                          (1.0, 0.0, -1.0),
                                          (1.0, 0.0, 1.0),
                                          (-1.0, 0.0, 1.0),
                                          (-1.0, 0.0, -1.0)],
                                      knot = [0,1,2,3,4,5,6,7,8,9,10])
                mayac.rotate(90, 0, 0, control)
                mayac.rotate(rotate[0], rotate[1], rotate[2], control, relative = True)                                                                                          
                mayac.scale(scale[0], scale[1], scale[2], control)
                mayac.move(offset[0], offset[1], offset[2],  "%s.cv[0:9]" % (control), relative = True)
                mayac.makeIdentity(control, apply = True, t=1, r=1, s=1, n=0)
            else:
                print "exactSizeNotFunctionalYet"


        #set color
        DJB_ChangeDisplayColor(control, color = color_)
        #place control
        if not partialConstraint:
            mayac.delete(mayac.parentConstraint(self.Bind_Joint, control))
        elif partialConstraint == 2:
            mayac.delete(mayac.parentConstraint(self.Bind_Joint, control, sr=["x"]))
        elif partialConstraint == 1:
            mayac.delete(mayac.pointConstraint(self.Bind_Joint, control))
            mayac.makeIdentity(control, apply = True, t=1, r=1, s=1, n=0)
            mayac.xform(control, cp = True)
            mayac.scale(1,-1,1, control)
            mayac.makeIdentity(control, apply = True, t=1, r=1, s=1, n=0)
            cvPos = mayac.xform("%s.cv[0]" % (control), query = True, worldSpace = True, translation = True)
            pivPosY = mayac.getAttr("%s.rotatePivotY" % (control))
            mayac.setAttr("%s.translateY" % (control), cvPos[1] - pivPosY)
            DJB_movePivotToObject(control, self.Bind_Joint, posOnly = True)
            mayac.delete(mayac.aimConstraint(self.children[0].Bind_Joint, control, skip = ["x", "z"], weight = 1, aimVector = (0,0,1), worldUpType = "vector", upVector = (0,1,0)))

        if style == "pin1":
            mayac.delete(mayac.orientConstraint(self.Bind_Joint, control, offset = (0,-90,90)))
        if type == "FK":
            self.FK_CTRL = mayac.rename(control, DJB_findAfterSeperator(self.nodeName, ":") + "_FK_CTRL")
            self.FK_CTRL_COLOR = color_ 
        elif type == "IK":
            self.IK_CTRL = mayac.rename(control, DJB_findAfterSeperator(self.nodeName, ":") + "_IK_CTRL")
            self.IK_CTRL_COLOR = color_
        elif type == "options":
            if not name_:
                self.Options_CTRL = mayac.rename(control, DJB_findAfterSeperator(self.nodeName, ":") + "_Options")
            else:
                self.Options_CTRL = mayac.rename(control, name_)
            self.Options_CTRL_COLOR = color_
        elif type == "Dyn":
            if not name_:
                self.Dyn_CTRL = mayac.rename(control, DJB_findAfterSeperator(self.nodeName, ":") + "_Dyn_CTRL")
            else:
                self.Dyn_CTRL = mayac.rename(control, name_)
            self.Dyn_CTRL_COLOR = color_
        elif type == "normal":
            if "Hips" in self.nodeName:
                if self.actAsRoot:
                    self.FK_CTRL = mayac.rename(control, "Root_CTRL")
                else:
                    self.FK_CTRL = mayac.rename(control, "Pelvis_CTRL")
            else:
                self.FK_CTRL = mayac.rename(control, DJB_findAfterSeperator(self.nodeName, ":") + "_CTRL")
            self.FK_CTRL_COLOR = color_
     
     
     
        
    def zeroToOrig(self, transform):
        if transform:
            if not mayac.getAttr("%s.tx" % (transform),lock=True):
                mel.eval('CBdeleteConnection "%s.tx";'%(transform))
                mayac.setAttr("%s.tx" % (transform), self.origPosX)
            if not mayac.getAttr("%s.ty" % (transform),lock=True):
                mel.eval('CBdeleteConnection "%s.ty";'%(transform))
                mayac.setAttr("%s.ty" % (transform), self.origPosY)
            if not mayac.getAttr("%s.tz" % (transform),lock=True):
                mel.eval('CBdeleteConnection "%s.tz";'%(transform))
                mayac.setAttr("%s.tz" % (transform), self.origPosZ)
            if not mayac.getAttr("%s.rx" % (transform),lock=True):
                mel.eval('CBdeleteConnection "%s.rx";'%(transform))
                mayac.setAttr("%s.rx" % (transform), self.origRotX)
            if not mayac.getAttr("%s.ry" % (transform),lock=True):
                mel.eval('CBdeleteConnection "%s.ry";'%(transform))
                mayac.setAttr("%s.ry" % (transform), self.origRotY)
            if not mayac.getAttr("%s.rz" % (transform),lock=True):
                mel.eval('CBdeleteConnection "%s.rz";'%(transform))
                mayac.setAttr("%s.rz" % (transform), self.origRotZ)




    def finalizeCTRLs(self, parent = "UseSelf"):   
        #find type of chains
        switchName = ""
        if self.FK_Joint and self.IK_Joint:
            switchName = "FK_IK"
        elif self.FK_Joint and self.Dyn_Joint:
            switchName = "FK_Dyn"
        #record original positions, rotations
        self.origPosX = mayac.getAttr("%s.translateX" % (self.Bind_Joint))
        self.origPosY = mayac.getAttr("%s.translateY" % (self.Bind_Joint))
        self.origPosZ = mayac.getAttr("%s.translateZ" % (self.Bind_Joint))
        self.origRotX = mayac.getAttr("%s.rotateX" % (self.Bind_Joint))
        self.origRotY = mayac.getAttr("%s.rotateY" % (self.Bind_Joint))
        self.origRotZ = mayac.getAttr("%s.rotateZ" % (self.Bind_Joint))
        #hook up control
        if self.FK_CTRL:
            #place control
            temp = mayac.duplicate(self.Bind_Joint, parentOnly = True, name = "UnRotate" + self.nodeName)
            mayac.parent(self.FK_CTRL, temp[0])
            mayac.rotate(0,0,0, temp[0])
            mayac.parent(self.FK_CTRL, world = True)
            DJB_movePivotToObject(self.FK_CTRL, temp[0])
            mayac.delete(temp[0])
            #add attributes  
            mayac.addAttr(self.FK_CTRL, longName='AnimDataMult', defaultValue=1.0, keyable = True)
            self.FK_CTRL_inRig_CONST_GRP = DJB_createGroup(transform = self.FK_CTRL, fullName = self.FK_CTRL + "_In_Rig_CONST_GRP")
            self.FK_CTRL_animData_CONST_GRP = DJB_createGroup(transform = self.FK_CTRL_inRig_CONST_GRP, fullName = self.FK_CTRL + "_AnimData_CONST_GRP")
            self.FK_CTRL_animData_MultNode = mayac.createNode( 'multiplyDivide', n=self.FK_CTRL + "_AnimData_MultNode")
            self.FK_CTRL_POS_GRP = DJB_createGroup(transform = self.FK_CTRL_animData_CONST_GRP, fullName = self.FK_CTRL + "_POS_GRP")
            
            #set rotation orders
            mayac.setAttr("%s.rotateOrder" % (self.FK_CTRL), self.rotOrder)
            mayac.setAttr("%s.rotateOrder" % (self.FK_CTRL_inRig_CONST_GRP), self.rotOrder)
            mayac.setAttr("%s.rotateOrder" % (self.FK_CTRL_animData_CONST_GRP), self.rotOrder)
            mayac.setAttr("%s.rotateOrder" % (self.FK_CTRL_POS_GRP), self.rotOrder)
            
            #place in hierarchy
            if parent == "UseSelf" and self.parent:
                mayac.parent(self.FK_CTRL_POS_GRP, self.parent.FK_CTRL)
            elif parent != "UseSelf":
                mayac.parent(self.FK_CTRL_POS_GRP, parent)
                
            if "Head" in self.nodeName:
                mayac.addAttr(self.FK_CTRL, longName='InheritRotation', defaultValue=1.0, min = 0, max = 1.0, keyable = True)
                self.Inherit_Rotation_GRP = DJB_createGroup(transform = None, fullName = self.FK_CTRL + "_Inherit_Rotation_GRP", pivotFrom = self.FK_CTRL)
                mayac.parent(self.Inherit_Rotation_GRP, self.FK_CTRL_animData_CONST_GRP)
                mayac.setAttr("%s.inheritsTransform" % (self.Inherit_Rotation_GRP), 0)
                temp = mayac.orientConstraint(self.FK_CTRL_animData_CONST_GRP, self.FK_CTRL_inRig_CONST_GRP, maintainOffset = True)
                self.Inherit_Rotation_Constraint = temp[0]
                mayac.orientConstraint(self.Inherit_Rotation_GRP, self.FK_CTRL_inRig_CONST_GRP, maintainOffset = True)
                self.Inherit_Rotation_Constraint_Reverse = mayac.createNode( 'reverse', n="Head_Inherit_Rotation_Constraint_Reverse")
                mayac.connectAttr("%s.InheritRotation" %(self.FK_CTRL), "%s.inputX" %(self.Inherit_Rotation_Constraint_Reverse))
                mayac.connectAttr("%s.InheritRotation" %(self.FK_CTRL), "%s.%sW0" %(self.Inherit_Rotation_Constraint, self.FK_CTRL_animData_CONST_GRP))
                mayac.connectAttr("%s.outputX" %(self.Inherit_Rotation_Constraint_Reverse), "%s.%sW1" %(self.Inherit_Rotation_Constraint, self.Inherit_Rotation_GRP))
                mayac.setAttr("%s.interpType" %(self.Inherit_Rotation_Constraint), 2)
                
        
        
        
            #hook up CTRLs
            mayac.connectAttr("%s.rotateX" %(self.AnimData_Joint), "%s.input1X" %(self.FK_CTRL_animData_MultNode), force = True)
            mayac.connectAttr("%s.AnimDataMult" %(self.FK_CTRL), "%s.input2X" %(self.FK_CTRL_animData_MultNode), force = True)
            mayac.connectAttr("%s.rotateY" %(self.AnimData_Joint), "%s.input1Y" %(self.FK_CTRL_animData_MultNode), force = True)
            mayac.connectAttr("%s.AnimDataMult" %(self.FK_CTRL), "%s.input2Y" %(self.FK_CTRL_animData_MultNode), force = True)
            mayac.connectAttr("%s.rotateZ" %(self.AnimData_Joint), "%s.input1Z" %(self.FK_CTRL_animData_MultNode), force = True)
            mayac.connectAttr("%s.AnimDataMult" %(self.FK_CTRL), "%s.input2Z" %(self.FK_CTRL_animData_MultNode), force = True)
            
            mayac.connectAttr("%s.outputX" %(self.FK_CTRL_animData_MultNode), "%s.rotateX" %(self.FK_CTRL_animData_CONST_GRP), force = True)
            mayac.connectAttr("%s.outputY" %(self.FK_CTRL_animData_MultNode), "%s.rotateY" %(self.FK_CTRL_animData_CONST_GRP), force = True)
            mayac.connectAttr("%s.outputZ" %(self.FK_CTRL_animData_MultNode), "%s.rotateZ" %(self.FK_CTRL_animData_CONST_GRP), force = True)
            if not self.FK_Joint:
                if self.actAsRoot:
                    mayac.addAttr(self.FK_CTRL, longName='AnimDataMultTrans', defaultValue=1.0, keyable = True)
                    self.FK_CTRL_animData_MultNode_Trans = mayac.createNode( 'multiplyDivide', n=self.FK_CTRL + "_AnimData_MultNode_Trans")
                    temp = mayac.parentConstraint(self.FK_CTRL, self.Bind_Joint, mo = True, name = "%s_Constraint" %(self.nodeName))
                    self.Constraint = temp[0]
                    
                    mayac.connectAttr("%s.translateX" %(self.AnimData_Joint), "%s.input1X" %(self.FK_CTRL_animData_MultNode_Trans), force = True)
                    mayac.connectAttr("%s.AnimDataMultTrans" %(self.FK_CTRL), "%s.input2X" %(self.FK_CTRL_animData_MultNode_Trans), force = True)
                    mayac.connectAttr("%s.translateY" %(self.AnimData_Joint), "%s.input1Y" %(self.FK_CTRL_animData_MultNode_Trans), force = True)
                    mayac.connectAttr("%s.AnimDataMultTrans" %(self.FK_CTRL), "%s.input2Y" %(self.FK_CTRL_animData_MultNode_Trans), force = True)
                    mayac.connectAttr("%s.translateZ" %(self.AnimData_Joint), "%s.input1Z" %(self.FK_CTRL_animData_MultNode_Trans), force = True)
                    mayac.connectAttr("%s.AnimDataMultTrans" %(self.FK_CTRL), "%s.input2Z" %(self.FK_CTRL_animData_MultNode_Trans), force = True)
                    
                    mayac.connectAttr("%s.outputX" %(self.FK_CTRL_animData_MultNode_Trans), "%s.translateX" %(self.FK_CTRL_POS_GRP), force = True)
                    mayac.connectAttr("%s.outputY" %(self.FK_CTRL_animData_MultNode_Trans), "%s.translateY" %(self.FK_CTRL_POS_GRP), force = True)
                    mayac.connectAttr("%s.outputZ" %(self.FK_CTRL_animData_MultNode_Trans), "%s.translateZ" %(self.FK_CTRL_POS_GRP), force = True)
                    mayac.connectAttr("%s.outputX" %(self.FK_CTRL_animData_MultNode_Trans), "%s.translateX" %(self.IK_Dummy_Joint), force = True)
                    mayac.connectAttr("%s.outputY" %(self.FK_CTRL_animData_MultNode_Trans), "%s.translateY" %(self.IK_Dummy_Joint), force = True)
                    mayac.connectAttr("%s.outputZ" %(self.FK_CTRL_animData_MultNode_Trans), "%s.translateZ" %(self.IK_Dummy_Joint), force = True)
                elif self.translateOpen:
                    temp = mayac.parentConstraint(self.FK_CTRL, self.Bind_Joint, mo = True, name = "%s_Constraint" %(self.nodeName))
                    self.Constraint = temp[0]
                    mayac.setAttr("%s.offsetX" % (self.Constraint), 0)
                    mayac.setAttr("%s.offsetY" % (self.Constraint), 0)
                    mayac.setAttr("%s.offsetZ" % (self.Constraint), 0)
                else:
                    temp = mayac.orientConstraint(self.FK_CTRL, self.Bind_Joint, mo = True, name = "%s_Constraint" %(self.nodeName))
                    self.Constraint = temp[0]
                    mayac.setAttr("%s.offsetX" % (self.Constraint), 0)
                    mayac.setAttr("%s.offsetY" % (self.Constraint), 0)
                    mayac.setAttr("%s.offsetZ" % (self.Constraint), 0)
            elif self.translateOpen:
                temp= mayac.parentConstraint(self.FK_CTRL, self.FK_Joint, mo = True, name = "%s_FK_Constraint" %(self.nodeName))
                self.FK_Constraint = temp[0]
                temp = mayac.parentConstraint(self.FK_Joint, self.Bind_Joint, mo = True, name = "%s_%s_Constraint" %(self.nodeName, switchName))
                self.Constraint = temp[0]
            else:
                temp= mayac.orientConstraint(self.FK_CTRL, self.FK_Joint, mo = True, name = "%s_FK_Constraint" %(self.nodeName))
                self.FK_Constraint = temp[0]
                temp = mayac.orientConstraint(self.FK_Joint, self.Bind_Joint, mo = True, name = "%s_%s_Constraint" %(self.nodeName, switchName))
                self.Constraint = temp[0]
                mayac.setAttr("%s.offsetX" % (self.Constraint), 0)
                mayac.setAttr("%s.offsetY" % (self.Constraint), 0)
                mayac.setAttr("%s.offsetZ" % (self.Constraint), 0)
        
        if self.IK_Dummy_Joint:
            mayac.connectAttr("%s.rotateX" %(self.AnimData_Joint), "%s.rotateX" %(self.IK_Dummy_Joint), force = True)
            mayac.connectAttr("%s.rotateY" %(self.AnimData_Joint), "%s.rotateY" %(self.IK_Dummy_Joint), force = True)
            mayac.connectAttr("%s.rotateZ" %(self.AnimData_Joint), "%s.rotateZ" %(self.IK_Dummy_Joint), force = True)

        if self.IK_CTRL:
            #place control
            if "Foot" in self.nodeName:
                self.footRotateLOC = mayac.spaceLocator(n = self.IK_CTRL + "_footRotateLOC")
                self.footRotateLOC = self.footRotateLOC[0]
                DJB_movePivotToObject(self.footRotateLOC, self.IK_Joint)
                mayac.delete(mayac.orientConstraint(self.IK_CTRL, self.footRotateLOC))
                mayac.setAttr("%s.rotateOrder" % (self.footRotateLOC), self.rotOrder)

                
            if "Eye" not in self.nodeName:   
                temp = mayac.duplicate(self.Bind_Joint, parentOnly = True, name = "UnRotate" + self.nodeName)
                mayac.parent(self.IK_CTRL, temp[0])
                mayac.rotate(0,0,0, temp[0])
                mayac.parent(self.IK_CTRL, world = True)
                DJB_movePivotToObject(self.IK_CTRL, temp[0])
                mayac.delete(temp[0])
                #add attributes  
                mayac.addAttr(self.IK_CTRL, longName='AnimDataMult', defaultValue=1.0, keyable = True)
                mayac.addAttr(self.IK_CTRL, longName='FollowBody', defaultValue=1.0, minValue = 0, maxValue = 1.0, keyable = True)
                if "Foot" in self.nodeName:
                    self.IK_CTRL_ReorientGRP = DJB_createGroup(transform = self.IK_CTRL, fullName = self.IK_CTRL + "_Reorient_GRP")
                    self.IK_CTRL_inRig_CONST_GRP = DJB_createGroup(transform = self.IK_CTRL_ReorientGRP, fullName = self.IK_CTRL + "_In_Rig_CONST_GRP")
                    DJB_movePivotToObject(self.IK_CTRL, self.footRotateLOC)
                    DJB_movePivotToObject(self.IK_CTRL_ReorientGRP, self.footRotateLOC)
                    mayac.setAttr("%s.rotateOrder" % (self.IK_CTRL_ReorientGRP), self.rotOrder)
                    mayac.setAttr("%s.rotateOrder" % (self.IK_CTRL_inRig_CONST_GRP), self.rotOrder)
                    #mayac.delete(self.footRotateLOC)
                    mayac.parent(self.IK_CTRL_ReorientGRP, self.IK_CTRL_inRig_CONST_GRP)
                    mayac.parent(self.IK_CTRL, self.IK_CTRL_ReorientGRP)
                else:
                    self.IK_CTRL_inRig_CONST_GRP = DJB_createGroup(transform = self.IK_CTRL, fullName = self.IK_CTRL + "_In_Rig_CONST_GRP")
                self.IK_CTRL_animData_CONST_GRP = DJB_createGroup(transform = self.IK_CTRL_inRig_CONST_GRP, fullName = self.IK_CTRL + "_AnimData_CONST_GRP")
                self.IK_CTRL_animData_MultNode = mayac.createNode( 'multiplyDivide', n=self.IK_CTRL + "_AnimData_MultNode")
                self.IK_CTRL_POS_GRP = DJB_createGroup(transform = self.IK_CTRL_animData_CONST_GRP, fullName = self.IK_CTRL + "_POS_GRP")
                
                #set rotation orders
                mayac.setAttr("%s.rotateOrder" % (self.IK_CTRL), self.rotOrder)
                mayac.setAttr("%s.rotateOrder" % (self.IK_CTRL_inRig_CONST_GRP), self.rotOrder)
                mayac.setAttr("%s.rotateOrder" % (self.IK_CTRL_animData_CONST_GRP), self.rotOrder)
                mayac.setAttr("%s.rotateOrder" % (self.IK_CTRL_POS_GRP), self.rotOrder)
                
                #place in hierarchy
                #hook up CTRLs
                mayac.connectAttr("%s.rotateX" %(self.AnimData_Joint), "%s.input1X" %(self.IK_CTRL_animData_MultNode), force = True)
                mayac.connectAttr("%s.AnimDataMult" %(self.IK_CTRL), "%s.input2X" %(self.IK_CTRL_animData_MultNode), force = True)
                mayac.connectAttr("%s.rotateY" %(self.AnimData_Joint), "%s.input1Y" %(self.IK_CTRL_animData_MultNode), force = True)
                mayac.connectAttr("%s.AnimDataMult" %(self.IK_CTRL), "%s.input2Y" %(self.IK_CTRL_animData_MultNode), force = True)
                mayac.connectAttr("%s.rotateZ" %(self.AnimData_Joint), "%s.input1Z" %(self.IK_CTRL_animData_MultNode), force = True)
                mayac.connectAttr("%s.AnimDataMult" %(self.IK_CTRL), "%s.input2Z" %(self.IK_CTRL_animData_MultNode), force = True)
                
                mayac.connectAttr("%s.outputX" %(self.IK_CTRL_animData_MultNode), "%s.rotateX" %(self.IK_CTRL_animData_CONST_GRP), force = True)
                mayac.connectAttr("%s.outputY" %(self.IK_CTRL_animData_MultNode), "%s.rotateY" %(self.IK_CTRL_animData_CONST_GRP), force = True)
                mayac.connectAttr("%s.outputZ" %(self.IK_CTRL_animData_MultNode), "%s.rotateZ" %(self.IK_CTRL_animData_CONST_GRP), force = True)
                
                if "Hand" in self.nodeName or "ForeArm" in self.nodeName or "Foot" in self.nodeName or "Leg" in self.nodeName:
                    self.IK_CTRL_parent_animData_CONST_GRP = DJB_createGroup(transform = self.IK_CTRL_POS_GRP, fullName = self.IK_CTRL + "_parent_AnimData_CONST_GRP")
                    
                    #place parent GRP
                    temp = mayac.duplicate(self.parent.Bind_Joint, parentOnly = True, name = "UnRotate" + self.nodeName)
                    mayac.parent(self.IK_CTRL_parent_animData_CONST_GRP, temp[0])
                    mayac.rotate(0,0,0, temp[0])
                    mayac.parent(self.IK_CTRL_POS_GRP, world = True)
                    mayac.parent(self.IK_CTRL_parent_animData_CONST_GRP, world = True)
                    DJB_movePivotToObject(self.IK_CTRL_parent_animData_CONST_GRP, temp[0])
                    mayac.delete(temp[0])
                    mayac.parent(self.IK_CTRL_POS_GRP, self.IK_CTRL_parent_animData_CONST_GRP)
                    
                    self.IK_CTRL_parent_animData_MultNode = mayac.createNode( 'multiplyDivide', n=self.IK_CTRL + "_parent_AnimData_MultNode")
                    self.IK_CTRL_parent_Global_POS_GRP = DJB_createGroup(transform = self.IK_CTRL_parent_animData_CONST_GRP, fullName = self.IK_CTRL + "_parent_Global_POS_GRP")
                    self.IK_CTRL_parent_POS_GRP = DJB_createGroup(transform = self.IK_CTRL_parent_Global_POS_GRP, fullName = self.IK_CTRL + "_parent_POS_GRP")
    
                    #set rotation orders
                    mayac.setAttr("%s.rotateOrder" % (self.IK_CTRL_parent_animData_CONST_GRP), self.parent.rotOrder)
                    mayac.setAttr("%s.rotateOrder" % (self.IK_CTRL_parent_Global_POS_GRP), self.parent.rotOrder)
                    mayac.setAttr("%s.rotateOrder" % (self.IK_CTRL_parent_POS_GRP), self.parent.rotOrder)
    
                    mayac.connectAttr("%s.rotateX" %(self.parent.AnimData_Joint), "%s.input1X" %(self.IK_CTRL_parent_animData_MultNode), force = True)
                    mayac.connectAttr("%s.AnimDataMult" %(self.IK_CTRL), "%s.input2X" %(self.IK_CTRL_parent_animData_MultNode), force = True)
                    mayac.connectAttr("%s.rotateY" %(self.parent.AnimData_Joint), "%s.input1Y" %(self.IK_CTRL_parent_animData_MultNode), force = True)
                    mayac.connectAttr("%s.AnimDataMult" %(self.IK_CTRL), "%s.input2Y" %(self.IK_CTRL_parent_animData_MultNode), force = True)
                    mayac.connectAttr("%s.rotateZ" %(self.parent.AnimData_Joint), "%s.input1Z" %(self.IK_CTRL_parent_animData_MultNode), force = True)
                    mayac.connectAttr("%s.AnimDataMult" %(self.IK_CTRL), "%s.input2Z" %(self.IK_CTRL_parent_animData_MultNode), force = True)
                    
                    mayac.connectAttr("%s.outputX" %(self.IK_CTRL_parent_animData_MultNode), "%s.rotateX" %(self.IK_CTRL_parent_animData_CONST_GRP), force = True)
                    mayac.connectAttr("%s.outputY" %(self.IK_CTRL_parent_animData_MultNode), "%s.rotateY" %(self.IK_CTRL_parent_animData_CONST_GRP), force = True)
                    mayac.connectAttr("%s.outputZ" %(self.IK_CTRL_parent_animData_MultNode), "%s.rotateZ" %(self.IK_CTRL_parent_animData_CONST_GRP), force = True)
                    
                    mayac.addAttr(self.IK_CTRL, longName='ParentToGlobal', defaultValue=0.0, minValue = 0, maxValue = 1.0, keyable = True)
    
                    if "ForeArm" in self.nodeName:
                        mayac.addAttr(self.IK_CTRL, longName='FollowHand', defaultValue=0.0, minValue = 0, maxValue = 1.0, keyable = True)
                        #if "Left" in self.nodeName:
                            #mayac.aimConstraint(self.IK_Joint, self.IK_CTRL, upVector = (0,1,0), aimVector = (-1,0,0))
                        #elif "Right" in self.nodeName:
                            #mayac.aimConstraint(self.IK_Joint, self.IK_CTRL, upVector = (0,1,0), aimVector = (1,0,0))
                            
                        #IK elbow bakingLOCs
                        temp = mayac.spaceLocator(name = "%s_IK_BakingLOC" % (self.nodeName))
                        self.IK_BakingLOC = temp[0]
                        mayac.parent(self.IK_BakingLOC, self.Bind_Joint)
                        DJB_ZeroOut(self.IK_BakingLOC)
                        mayac.setAttr("%s.rotateOrder" % (self.IK_BakingLOC), self.rotOrder)
                        
                        
                    
                            
                    if "Leg" in self.nodeName:
                        mayac.addAttr(self.IK_CTRL, longName='FollowFoot', defaultValue=0.0, minValue = 0, maxValue = 1.0, keyable = True)
                        #mayac.aimConstraint(self.IK_Joint, self.IK_CTRL, upVector = (0,1,0), aimVector = (0,0,-1))
                        
                        #groups for follow foot Attr
                        self.Follow_Knee_GRP = DJB_createGroup(transform = None, fullName = self.IK_CTRL + "_Follow_Knee_GRP", pivotFrom = self.FK_CTRL)
                        self.Follow_Foot_GRP = DJB_createGroup(transform = self.Follow_Knee_GRP, fullName = self.IK_CTRL + "_Follow_Foot_GRP", pivotFrom = self.FK_CTRL)
                        #set rotation orders
                        mayac.setAttr("%s.rotateOrder" % (self.Follow_Knee_GRP), self.rotOrder)
                        mayac.setAttr("%s.rotateOrder" % (self.Follow_Foot_GRP), self.rotOrder)
    
                        mayac.parent(self.Follow_Foot_GRP, self.IK_CTRL_animData_CONST_GRP)
                        selfPOS = mayac.xform(self.Bind_Joint, query = True, absolute = True, worldSpace = True, translation = True)
                        parentPOS = mayac.xform(self.parent.Bind_Joint, query = True, absolute = True, worldSpace = True, translation = True)
                        tempDistance = math.sqrt((selfPOS[0]-parentPOS[0])*(selfPOS[0]-parentPOS[0]) + (selfPOS[1]-parentPOS[1])*(selfPOS[1]-parentPOS[1]) + (selfPOS[2]-parentPOS[2])*(selfPOS[2]-parentPOS[2]))
                        mayac.setAttr("%s.translateZ" % (self.Follow_Knee_GRP), tempDistance / 2)
                        temp = mayac.pointConstraint(self.IK_Joint, self.Follow_Knee_GRP, sk = ("x", "y"), mo = True)
                        self.Follow_Knee_Constraint = temp[0]
                        
                        #IK knee bakingLOCs
                        temp = mayac.spaceLocator(name = "%s_IK_BakingLOC" % (self.nodeName))
                        self.IK_BakingLOC = temp[0]
                        mayac.parent(self.IK_BakingLOC, self.Bind_Joint)
                        DJB_ZeroOut(self.IK_BakingLOC)
                        mayac.setAttr("%s.rotateOrder" % (self.IK_BakingLOC), self.rotOrder)
    
                        if "Left" in self.nodeName:
                            mayac.setAttr("%s.translateZ" % (self.IK_BakingLOC), tempDistance / 2)
                            #mayac.setAttr("%s.translateX" % (self.IK_BakingLOC), -2.017)
                        elif "Right" in self.nodeName:
                            mayac.setAttr("%s.translateZ" % (self.IK_BakingLOC), tempDistance / 2)
                        
    
                    if "Hand" in self.nodeName or "Foot" in self.nodeName:
                        self.IK_CTRL_grandparent_inRig_CONST_GRP = DJB_createGroup(transform = self.IK_CTRL_parent_POS_GRP, fullName = self.IK_CTRL + "_grandparent_inRig_CONST_GRP", pivotFrom = self.parent.parent.Bind_Joint)
                        
                        
                        #place parent GRP
                        temp = mayac.duplicate(self.parent.parent.Bind_Joint, parentOnly = True, name = "UnRotate" + self.nodeName)
                        mayac.parent(self.IK_CTRL_grandparent_inRig_CONST_GRP, temp[0])
                        mayac.rotate(0,0,0, temp[0])
                        mayac.parent(self.IK_CTRL_parent_POS_GRP, world = True)
                        mayac.parent(self.IK_CTRL_grandparent_inRig_CONST_GRP, world = True)
                        DJB_movePivotToObject(self.IK_CTRL_grandparent_inRig_CONST_GRP, temp[0])
                        mayac.delete(temp[0])
                        mayac.parent(self.IK_CTRL_parent_POS_GRP, self.IK_CTRL_grandparent_inRig_CONST_GRP)
                    
                        self.IK_CTRL_grandparent_animData_CONST_GRP = DJB_createGroup(transform = self.IK_CTRL_grandparent_inRig_CONST_GRP, fullName = self.IK_CTRL + "_grandparent_AnimData_CONST_GRP")
                        self.IK_CTRL_grandparent_animData_MultNode = mayac.createNode( 'multiplyDivide', n=self.IK_CTRL + "_grandparent_AnimData_MultNode")
                        self.IK_CTRL_grandparent_Global_POS_GRP = DJB_createGroup(transform = self.IK_CTRL_grandparent_animData_CONST_GRP, fullName = self.IK_CTRL + "_grandparent_Global_POS_GRP")
                        self.IK_CTRL_grandparent_POS_GRP = DJB_createGroup(transform = self.IK_CTRL_grandparent_Global_POS_GRP, fullName = self.IK_CTRL + "_grandparent_POS_GRP")
                        
                        #set rotation orders
                        mayac.setAttr("%s.rotateOrder" % (self.IK_CTRL_grandparent_inRig_CONST_GRP), self.parent.parent.rotOrder)
                        mayac.setAttr("%s.rotateOrder" % (self.IK_CTRL_grandparent_animData_CONST_GRP), self.parent.parent.rotOrder)
                        mayac.setAttr("%s.rotateOrder" % (self.IK_CTRL_grandparent_Global_POS_GRP), self.parent.parent.rotOrder)
                        mayac.setAttr("%s.rotateOrder" % (self.IK_CTRL_grandparent_POS_GRP), self.parent.parent.rotOrder)
                        
                        mayac.connectAttr("%s.rotateX" %(self.parent.parent.AnimData_Joint), "%s.input1X" %(self.IK_CTRL_grandparent_animData_MultNode), force = True)
                        mayac.connectAttr("%s.AnimDataMult" %(self.IK_CTRL), "%s.input2X" %(self.IK_CTRL_grandparent_animData_MultNode), force = True)
                        mayac.connectAttr("%s.rotateY" %(self.parent.parent.AnimData_Joint), "%s.input1Y" %(self.IK_CTRL_grandparent_animData_MultNode), force = True)
                        mayac.connectAttr("%s.AnimDataMult" %(self.IK_CTRL), "%s.input2Y" %(self.IK_CTRL_grandparent_animData_MultNode), force = True)
                        mayac.connectAttr("%s.rotateZ" %(self.parent.parent.AnimData_Joint), "%s.input1Z" %(self.IK_CTRL_grandparent_animData_MultNode), force = True)
                        mayac.connectAttr("%s.AnimDataMult" %(self.IK_CTRL), "%s.input2Z" %(self.IK_CTRL_grandparent_animData_MultNode), force = True)
                        
                        mayac.connectAttr("%s.outputX" %(self.IK_CTRL_grandparent_animData_MultNode), "%s.rotateX" %(self.IK_CTRL_grandparent_animData_CONST_GRP), force = True)
                        mayac.connectAttr("%s.outputY" %(self.IK_CTRL_grandparent_animData_MultNode), "%s.rotateY" %(self.IK_CTRL_grandparent_animData_CONST_GRP), force = True)
                        mayac.connectAttr("%s.outputZ" %(self.IK_CTRL_grandparent_animData_MultNode), "%s.rotateZ" %(self.IK_CTRL_grandparent_animData_CONST_GRP), force = True)
                        
                        temp = mayac.ikHandle( n="%s_IK_Handle" % (self.nodeName), sj= self.parent.parent.IK_Joint, ee= self.IK_Joint, solver = "ikRPsolver", weight = 1)
                        self.IK_Handle = temp[0]
                        mayac.setAttr("%s.visibility" % (self.IK_Handle), 0)
                        self.IK_EndEffector = temp[1]
                        temp = mayac.poleVectorConstraint( self.parent.IK_CTRL, self.IK_Handle )
                        self.PV_Constraint = temp[0]
                        if "Foot" in self.nodeName:
                            temp = mayac.orientConstraint(self.IK_CTRL_inRig_CONST_GRP, self.IK_Joint)
                            self.IK_Constraint = temp[0]
                        else:
                            temp = mayac.orientConstraint(self.IK_CTRL, self.IK_Joint)
                            self.IK_Constraint = temp[0]
                                         
                        
                        if "Hand" in self.nodeName:
                            mayac.parent(self.IK_Handle, self.IK_CTRL)
                            DJB_LockNHide(self.IK_Handle)
                            DJB_LockNHide(self.IK_EndEffector)
                        if "Foot" in self.nodeName:
                            mayac.addAttr(self.IK_CTRL, longName='FootControls', defaultValue=0.0, hidden = False, keyable = True)
                            mayac.setAttr("%s.FootControls" % (self.IK_CTRL), lock = True)
                            mayac.addAttr(self.IK_CTRL, longName='FootRoll', defaultValue=0.0, hidden = False, keyable = True)
                            mayac.addAttr(self.IK_CTRL, longName='ToeTap', defaultValue=0.0, hidden = False, keyable = True)
                            mayac.addAttr(self.IK_CTRL, longName='ToeSideToSide', defaultValue=0.0, hidden = False, keyable = True)
                            mayac.addAttr(self.IK_CTRL, longName='ToeRotate', defaultValue=0.0, hidden = False, keyable = True)
                            mayac.addAttr(self.IK_CTRL, longName='ToeRoll', defaultValue=0.0, hidden = False, keyable = True)
                            mayac.addAttr(self.IK_CTRL, longName='HipPivot', defaultValue=0.0, hidden = False, keyable = True)
                            mayac.addAttr(self.IK_CTRL, longName='BallPivot', defaultValue=0.0, hidden = False, keyable = True)
                            mayac.addAttr(self.IK_CTRL, longName='ToePivot', defaultValue=0.0, hidden = False, keyable = True)
                            mayac.addAttr(self.IK_CTRL, longName='HipSideToSide', defaultValue=0.0, hidden = False, keyable = True)
                            mayac.addAttr(self.IK_CTRL, longName='HipBackToFront', defaultValue=0.0, hidden = False, keyable = True)
                            
                            #Foot IK Baking LOCs
                            temp = mayac.spaceLocator(n = "%s_IK_BakingLOC" % (self.nodeName))
                            self.IK_BakingLOC = temp[0]
                            mayac.setAttr("%s.visibility"%(self.IK_BakingLOC), 0)
                            mayac.parent(self.IK_BakingLOC, self.Bind_Joint)
                            mayac.delete(mayac.parentConstraint(self.IK_CTRL, self.IK_BakingLOC))
                        
            
            mayac.orientConstraint(self.IK_Joint, self.Bind_Joint, mo = True)
        if not self.IK_CTRL and self.IK_Joint and not self.translateOpen:
            mayac.orientConstraint(self.IK_Joint, self.Bind_Joint, mo = True)
        elif not self.IK_CTRL and self.IK_Joint and self.translateOpen:
            mayac.parentConstraint(self.IK_Joint, self.Bind_Joint, mo = True)
        if self.Dyn_Joint:
            if not self.translateOpen:
                mayac.orientConstraint(self.DynMult_Joint, self.Bind_Joint, mo = True)
            else:
                mayac.parentConstraint(self.DynMult_Joint, self.Bind_Joint, mo = True)
                self.Dyn_Mult1 = mayac.createNode( 'multiplyDivide', n="%s_MultNodeTrans" %(self.nodeName))
                mayac.connectAttr("%s.translate"%(self.Dyn_Joint), "%s.input1"%(self.Dyn_Mult1))
                mayac.connectAttr("%s.output"%(self.Dyn_Mult1), "%s.translate"%(self.DynMult_Joint))
            self.Dyn_Mult = mayac.createNode( 'multiplyDivide', n="%s_MultNode" %(self.nodeName))
            mayac.connectAttr("%s.rotate"%(self.Dyn_Joint), "%s.input1"%(self.Dyn_Mult))
            mayac.connectAttr("%s.output"%(self.Dyn_Mult), "%s.rotate"%(self.DynMult_Joint))
        if self.Dyn_CTRL:
            mayac.addAttr(self.Dyn_CTRL, longName='weight', defaultValue=1.0, min = 0.0, max = 1.0, keyable = True)
            mayac.addAttr(self.Dyn_CTRL, longName='conserve', defaultValue=1.0, min = 0.0, max = 1.0, keyable = True)
            mayac.addAttr(self.Dyn_CTRL, longName='multiplier', defaultValue=1.0, min = 0.0, keyable = True)
            
        if self.Options_CTRL:
            #place control
            DJB_movePivotToObject(self.Options_CTRL, self.Bind_Joint)
            mayac.parentConstraint(self.Bind_Joint, self.Options_CTRL, mo = True, name = "%s_Constraint" %(self.Options_CTRL))
            #add attributes  
            mayac.addAttr(self.Options_CTRL, longName=switchName, defaultValue=0.0, min = 0.0, max = 1.0, keyable = True)
            mayac.setAttr("%s.rotateOrder" % (self.Options_CTRL), self.rotOrder)
            if "Hand" in self.nodeName:
                mayac.addAttr(self.Options_CTRL, longName='FingerControls', defaultValue=0.0, hidden = False, keyable = True)
                mayac.setAttr("%s.FingerControls" % (self.Options_CTRL), lock = True)
                mayac.addAttr(self.Options_CTRL, longName='ThumbCurl', defaultValue=0.0, min = -10.0, max = 10.0, hidden = False, keyable = True)
                mayac.addAttr(self.Options_CTRL, longName='IndexCurl', defaultValue=0.0, min = -10.0, max = 10.0, hidden = False, keyable = True)
                mayac.addAttr(self.Options_CTRL, longName='MiddleCurl', defaultValue=0.0, min = -10.0, max = 10.0, hidden = False, keyable = True)
                mayac.addAttr(self.Options_CTRL, longName='RingCurl', defaultValue=0.0, min = -10.0, max = 10.0, hidden = False, keyable = True)
                mayac.addAttr(self.Options_CTRL, longName='PinkyCurl', defaultValue=0.0, min = -10.0, max = 10.0, hidden = False, keyable = True)
                mayac.addAttr(self.Options_CTRL, longName='Sway', defaultValue=0.0, min = -10.0, max = 10.0, hidden = False, keyable = True)
                mayac.addAttr(self.Options_CTRL, longName='Spread', defaultValue=0.0, min = -10.0, max = 10.0, hidden = False, keyable = True)
                
            
            
        
    def lockUpCTRLs(self):    
        #lock and hide attributes
        if self.Dyn_CTRL:
            DJB_LockNHide(self.Dyn_CTRL)
        if self.FK_CTRL:
            if self.nodeName == "Root":
                DJB_LockNHide(self.FK_CTRL, tx = False, ty = False, tz = False, rx = False, ry = False, rz = False)
            elif self.nodeName == "Hips" and self.actAsRoot:
                DJB_LockNHide(self.FK_CTRL, tx = False, ty = False, tz = False, rx = False, ry = False, rz = False)
            elif self.translateOpen:
                DJB_LockNHide(self.FK_CTRL, tx = False, ty = False, tz = False, rx = False, ry = False, rz = False)
            else:
                DJB_LockNHide(self.FK_CTRL, rx = False, ry = False, rz = False)
            DJB_LockNHide(self.FK_CTRL_inRig_CONST_GRP)
            DJB_LockNHide(self.FK_CTRL_animData_CONST_GRP)
            DJB_LockNHide(self.FK_CTRL_POS_GRP)
            
        if self.IK_CTRL:
            #lock and hide channels
            DJB_LockNHide(self.IK_CTRL, tx = False, ty = False, tz = False, rx = False, ry = False, rz = False)
            if "Eye" not in self.nodeName:
                DJB_LockNHide(self.IK_CTRL_inRig_CONST_GRP)
                DJB_LockNHide(self.IK_CTRL_animData_CONST_GRP)
                DJB_LockNHide(self.IK_CTRL_POS_GRP)
            if self.IK_CTRL_grandparent_inRig_CONST_GRP:
                DJB_LockNHide(self.IK_CTRL_grandparent_inRig_CONST_GRP)
            if self.IK_CTRL_parent_POS_GRP:
                DJB_LockNHide(self.IK_CTRL_parent_POS_GRP)
                DJB_LockNHide(self.IK_CTRL_parent_Global_POS_GRP)
                DJB_LockNHide(self.IK_CTRL_parent_animData_CONST_GRP)
                if self.IK_CTRL_grandparent_POS_GRP:
                    DJB_LockNHide(self.IK_CTRL_grandparent_POS_GRP)
                    DJB_LockNHide(self.IK_CTRL_grandparent_Global_POS_GRP)
                    DJB_LockNHide(self.IK_CTRL_grandparent_animData_CONST_GRP)
            if self.IK_CTRL_ReorientGRP:
                DJB_LockNHide(self.IK_CTRL_ReorientGRP)
            if self.IK_Handle:
                DJB_LockNHide(self.IK_Handle)
            if "ForeArm" in self.nodeName or "LeftLeg" in self.nodeName or "RightLeg" in self.nodeName:
                DJB_LockNHide(self.IK_CTRL, tx = False, ty = False, tz = False, rx = True, ry = True, rz = True)
                mayac.setAttr("%s.visibility" % (self.IK_BakingLOC), 0)
            
        if self.Options_CTRL:
            DJB_LockNHide(self.Options_CTRL)