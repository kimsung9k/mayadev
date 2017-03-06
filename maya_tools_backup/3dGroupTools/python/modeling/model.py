import maya.OpenMaya as om


class MeshInfo:
    
    fnFirstMesh = om.MFnMesh()
    fnSecondMesh = om.MFnMesh()
    
    firstUs = om.MFloatArray()
    firstVs=  om.MFloatArray()
    secondUs = om.MFloatArray()
    secondVs = om.MFloatArray()
    
    checkIds = om.MIntArray()

    cuCount = 0