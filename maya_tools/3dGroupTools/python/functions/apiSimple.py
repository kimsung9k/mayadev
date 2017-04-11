import maya.OpenMaya as om


def getMObject( target ):
    selList = om.MSelectionList()
    selList.add( target )
    mObj = om.MObject()
    selList.getDependNode( 0, mObj )
    return mObj


def getDagPath( target ):
    selList = om.MSelectionList()
    selList.add( target )
    dagPath = om.MDagPath()
    selList.getDagPath( 0, dagPath )
    return dagPath



def getMMatrixFromDagNode( dagNodeName ):
    
    dagPath = getDagPath( dagNodeName )
    return dagPath.inclusiveMatrix()