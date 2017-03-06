import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import convert
import math


def makeSymmetry( side ):
    
    def setRotationMirror( stdOther, std ):
        trMtx = OpenMaya.MTransformationMatrix()
        trMtx.rotateTo( OpenMaya.MEulerRotation( math.radians(180), 0, 0 ) )
        mirrorRotMtx = trMtx.asMatrix()
        
        mtx = convert.listToMatrix( cmds.getAttr( otherStd + '.wm' ) )
        mtx *= mirrorRotMtx
        mtxList = convert.matrixToList( mtx )
        pos = cmds.xform( otherStd, q=1, t=1, ws=1 )
        mtxList[12] = -pos[0]
        mtxList[13] = pos[1]
        mtxList[14] = pos[2]
        cmds.xform( std, ws=1, matrix=mtxList )
    
    def setPositionMirror( stdOther, std ):
        pos = cmds.xform( stdOther, q=1, t=1, ws=1 )
        cmds.xform( std, ws=1, t=[-pos[0], pos[1], pos[2]])
    
    

    otherSide = side.replace( '_R_', '_L_' )
    if otherSide == side:
        otherSide = side.replace( '_L_', '_R_' )
    
    sels = cmds.ls( sl=1 )
    target = sels[-1]    
    ns = target.split( 'Std_' )[0]
    stdList = cmds.ls( ns + 'Std_*', type='transform' )
    
    for std in stdList:
        if std.find( side ) != -1: continue
        if std.find( otherSide ) != -1: continue
        cmds.setAttr( std + '.tx', 0 )
    
    
    for std in stdList:
        if std.find( side ) == -1: continue
        otherStd = std.replace( side, otherSide )
        
        if not cmds.objExists( std ) or not cmds.objExists( otherStd ): continue
        
        if std.find( '_Wrist_' ) != -1:
            setRotationMirror( otherStd, std )


    for std in stdList:
        if std.find( side ) == -1: continue
        otherStd = std.replace( side, otherSide )
        
        if not cmds.objExists( std ) or not cmds.objExists( otherStd ): continue
        
        if std.find( '_Thumb_' ) != -1 or std.find( '_Index_' ) != -1 or std.find( '_Middle_' ) != -1 or std.find( '_Ring_' ) != -1 or std.find( '_Pinky_' ) != -1:
            setRotationMirror( otherStd, std )
    
    for std in stdList:
        if std.find( side ) == -1: continue
        otherStd = std.replace( side, otherSide )
        
        if not cmds.objExists( std ) or not cmds.objExists( otherStd ): continue
        
        setPositionMirror( otherStd, std )
    
    

def makeSymmetryToR( evt=0 ):
    makeSymmetry( '_R_' )


def makeSymmetryToL( evt=0 ):
    makeSymmetry( '_L_' )