import maya.OpenMaya as om

def getDoublePtr():
    
    util = om.MScriptUtil()
    util.createFromDouble( 0.0 )
    ptrDouble = util.asDoublePtr()
    return (ptrDouble, util)