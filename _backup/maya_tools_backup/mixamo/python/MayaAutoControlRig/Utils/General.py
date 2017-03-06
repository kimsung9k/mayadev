'''
Utils.General
Handles:
    General Functions
'''
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

def DJB_LockNHide(node, tx = True, ty = True, tz = True, rx = True, ry = True, rz = True, s = True, v = True, other = None):
    if tx:
        mayac.setAttr("%s.tx" % (node), lock = True, keyable = False, channelBox  = False)
    if ty:
        mayac.setAttr("%s.ty" % (node), lock = True, keyable = False, channelBox  = False)
    if tz:
        mayac.setAttr("%s.tz" % (node), lock = True, keyable = False, channelBox  = False)
    if rx:
        mayac.setAttr("%s.rx" % (node), lock = True, keyable = False, channelBox  = False)
    if ry:
        mayac.setAttr("%s.ry" % (node), lock = True, keyable = False, channelBox  = False)
    if rz:
        mayac.setAttr("%s.rz" % (node), lock = True, keyable = False, channelBox  = False)
    if s:
        mayac.setAttr("%s.sx" % (node), lock = True, keyable = False, channelBox  = False)
        mayac.setAttr("%s.sy" % (node), lock = True, keyable = False, channelBox  = False)
        mayac.setAttr("%s.sz" % (node), lock = True, keyable = False, channelBox  = False)
    if v:
        mayac.setAttr("%s.v" % (node), lock = True, keyable = False, channelBox  = False)
    if other:
        for att in other:
            if mayac.objExists("%s.%s" % (node, att)):
                mayac.setAttr("%s.%s" % (node, att), lock = True, keyable = False, channelBox  = False)
        
        
def DJB_Unlock(node, tx = True, ty = True, tz = True, rx = True, ry = True, rz = True, s = True, v = True):
    if tx:
        mayac.setAttr("%s.tx" % (node), lock = False, keyable = True)
    if ty:
        mayac.setAttr("%s.ty" % (node), lock = False, keyable = True)
    if tz:
        mayac.setAttr("%s.tz" % (node), lock = False, keyable = True)
    if rx:
        mayac.setAttr("%s.rx" % (node), lock = False, keyable = True)
    if ry:
        mayac.setAttr("%s.ry" % (node), lock = False, keyable = True)
    if rz:
        mayac.setAttr("%s.rz" % (node), lock = False, keyable = True)
    if s:
        mayac.setAttr("%s.sx" % (node), lock = False, keyable = True)
        mayac.setAttr("%s.sy" % (node), lock = False, keyable = True)
        mayac.setAttr("%s.sz" % (node), lock = False, keyable = True)
    if v:
        mayac.setAttr("%s.v" % (node), lock = False, keyable = True)
 
 
def DJB_Unlock_Connect_Lock(att1, att2):
    mayac.setAttr(att2, lock = False, keyable = True)
    mayac.connectAttr(att1, att2)
    mayac.setAttr(att2, lock = True, keyable = False) 
    
def DJB_ConnectAll(xform1, xform2):
    mayac.connectAttr("%s.tx"%(xform1), "%s.tx"%(xform2))
    mayac.connectAttr("%s.ty"%(xform1), "%s.ty"%(xform2))
    mayac.connectAttr("%s.tz"%(xform1), "%s.tz"%(xform2))
    mayac.connectAttr("%s.rx"%(xform1), "%s.rx"%(xform2))
    mayac.connectAttr("%s.ry"%(xform1), "%s.ry"%(xform2))
    mayac.connectAttr("%s.rz"%(xform1), "%s.rz"%(xform2))

def DJB_parentShape(master, slaveGRP):
    mayac.parent(slaveGRP, master)
    mayac.makeIdentity(slaveGRP, apply = True, t=1, r=1, s=1, n=0) 
    shapes = mayac.listRelatives(slaveGRP, shapes = True)
    for shape in shapes:
        mayac.parent(shape, master, relative = True, shape = True)
    mayac.delete(slaveGRP)

def DJB_createGroup(transform = None, suffix = None, fullName = None, pivotFrom = "self"):
    Grp = 0
    if suffix:
        Grp = mayac.group(empty = True, name = (transform + suffix))
    elif fullName:
        Grp = mayac.group(empty = True, name = fullName)
    else:
        Grp = mayac.group(empty = True, name = (transform + "_GRP"))
    if pivotFrom == "self":
        mayac.delete(mayac.parentConstraint(transform, Grp))
    elif pivotFrom:
        mayac.delete(mayac.parentConstraint(pivotFrom, Grp))
    if transform:
        mayac.parent(transform, Grp)
    return Grp

def DJB_movePivotToObject(moveMe, toHere, posOnly = False):
    POS = mayac.xform(toHere, query=True, absolute=True, worldSpace=True ,rp=True)
    mayac.move(POS[0], POS[1], POS[2], (moveMe + ".rotatePivot"), (moveMe + ".scalePivot"), absolute=True, worldSpace=True)
    if not posOnly:
        mayac.parent(moveMe, toHere)
        DJB_cleanGEO(moveMe)
        mayac.parent(moveMe, world=True)
         

def DJB_findBeforeSeparator(object, separatedWith):
    if object == separatedWith:
        return ""
    latestSeparator = object.rfind(separatedWith)
    if ":" in separatedWith or '_' in separatedWith:
        return object[0:latestSeparator+1]
    return object[0:latestSeparator]
    
def DJB_findAfterSeperator(object, separatedWith):
    latestSeparator = object.rfind(separatedWith)
    if ":" in separatedWith:
        return object[latestSeparator+1:len(object)]
    return object[latestSeparator:len(object)]
    
    
    
def DJB_addNameSpace(namespace, string):
    if string == None:
        return None
    elif namespace == None:
        return string
    else:
        return namespace + string
    
def DJB_cleanGEO(mesh):
    mayac.setAttr("%s.tx" % (mesh), lock = False, keyable = True)
    mayac.setAttr("%s.ty" % (mesh), lock = False, keyable = True)
    mayac.setAttr("%s.tz" % (mesh), lock = False, keyable = True)
    mayac.setAttr("%s.rx" % (mesh), lock = False, keyable = True)
    mayac.setAttr("%s.ry" % (mesh), lock = False, keyable = True)
    mayac.setAttr("%s.rz" % (mesh), lock = False, keyable = True)
    mayac.setAttr("%s.sx" % (mesh), lock = False, keyable = True)
    mayac.setAttr("%s.sy" % (mesh), lock = False, keyable = True)
    mayac.setAttr("%s.sz" % (mesh), lock = False, keyable = True)
    mayac.setAttr("%s.visibility" % (mesh), lock = False, keyable = True)
    mayac.makeIdentity(mesh, apply = True, t=1, r=1, s=1, n=0)
    mayac.delete(mesh, constructionHistory = True)
    return mesh    


def DJB_ZeroOut(transform):
    if transform:
        if not mayac.getAttr("%s.tx" % (transform),lock=True):
            mel.eval('CBdeleteConnection "%s.tx";'%(transform))
            mayac.setAttr("%s.tx" % (transform), 0)
        if not mayac.getAttr("%s.ty" % (transform),lock=True):
            mel.eval('CBdeleteConnection "%s.ty";'%(transform))
            mayac.setAttr("%s.ty" % (transform), 0)
        if not mayac.getAttr("%s.tz" % (transform),lock=True):
            mel.eval('CBdeleteConnection "%s.tz";'%(transform))
            mayac.setAttr("%s.tz" % (transform), 0)
        if not mayac.getAttr("%s.rx" % (transform),lock=True):
            mel.eval('CBdeleteConnection "%s.rx";'%(transform))
            mayac.setAttr("%s.rx" % (transform), 0)
        if not mayac.getAttr("%s.ry" % (transform),lock=True):
            mel.eval('CBdeleteConnection "%s.ry";'%(transform))
            mayac.setAttr("%s.ry" % (transform), 0)
        if not mayac.getAttr("%s.rz" % (transform),lock=True):
            mel.eval('CBdeleteConnection "%s.rz";'%(transform))
            mayac.setAttr("%s.rz" % (transform), 0)


def DJB_ZeroOutAtt(att, value = 0):
    if mayac.objExists("%s" % (att)):
        mel.eval('CBdeleteConnection %s;'%(att))
        mayac.setAttr("%s" % (att), value)


def DJB_ChangeDisplayColor(object, color = None):
    colorNum = 0
    if color == "red1":
        colorNum = 12
    elif color == "red2":
        colorNum = 10
    elif color == "red3":
        colorNum = 24
    elif color == "blue1":
        colorNum = 15
    elif color == "blue2":
        colorNum = 29
    elif color == "blue3":
        colorNum = 28
    elif color == "yellow":
        colorNum = 17
    elif color == "white":
        colorNum = 16
    else:    #default is black
        colorNum = 1
    if object:
        for attr in ["drawOverride", "overrideColor"]:
            connection =  mayac.listConnections( "%s.%s" % (object, attr), s=True, plugs=True)
            if connection:
                mayac.disconnectAttr(connection[0], "%s.%s" % (object, attr))
        mayac.setAttr('%s.overrideEnabled' % (object), 1)
        mayac.setAttr('%s.overrideColor' % (object), colorNum)


def DJB_CheckAngle(object1, object2, object3, axis = "z", multiplier = 1): #axis can be "x", "y", or "z"
    obj1POS = mayac.xform(object1, query = True, worldSpace = True, absolute = True, translation = True)
    obj3POS = mayac.xform(object3, query = True, worldSpace = True, absolute = True, translation = True)
    rotOrig = mayac.getAttr("%s.rotate%s" % (object2, axis.upper()))
    distOrig = math.sqrt((obj3POS[0]-obj1POS[0])*(obj3POS[0]-obj1POS[0]) + (obj3POS[1]-obj1POS[1])*(obj3POS[1]-obj1POS[1]) + (obj3POS[2]-obj1POS[2])*(obj3POS[2]-obj1POS[2]))
    mayac.setAttr("%s.rotate%s" % (object2, axis.upper()), rotOrig + .5*multiplier)
    obj1POS = mayac.xform(object1, query = True, worldSpace = True, absolute = True, translation = True)
    obj3POS = mayac.xform(object3, query = True, worldSpace = True, absolute = True, translation = True)
    distBack = math.sqrt((obj3POS[0]-obj1POS[0])*(obj3POS[0]-obj1POS[0]) + (obj3POS[1]-obj1POS[1])*(obj3POS[1]-obj1POS[1]) + (obj3POS[2]-obj1POS[2])*(obj3POS[2]-obj1POS[2]))
    mayac.setAttr("%s.rotate%s" % (object2, axis.upper()), rotOrig)
    if distOrig < distBack:
        return True
    else:
        return False


def pyToAttr(objAttr, data):
    obj, attr = objAttr.split('.')
    if not mayac.objExists(objAttr):
        mayac.addAttr(obj, longName=attr, dataType='string')
    if mayac.getAttr(objAttr, type=True) != 'string':
        raise Exception("Object '%s' already has an attribute called '%s', but it isn't type 'string'"%(obj,attr))

    stringData = cPickle.dumps(data)
    mayac.setAttr(objAttr, stringData, type='string')


def attrToPy(objAttr):
    if mayac.objExists(objAttr):
        stringAttrData = str(mayac.getAttr(objAttr))
        loadedData = cPickle.loads(stringAttrData)
        return loadedData
    else:
        return None
        
        
        
def makeUnique(object, keyword):
    if "|" in object: #and geo[geo.rfind("|")+1:] == parent[parent.rfind("|")+1]:
        object = mayac.rename(object, object[object.rfind("|")+1:] + keyword)
        object = makeUnique(object, keyword)
    return object