import maya.cmds as cmds
import maya.OpenMaya as om
import math


class SetJointOrient:
    
    def __init__(self, topObject, endObject, upObject, aimAxisIndex, upAxisIndex, upType = 'object', worldUpAxisIndex=2, *args ):
    
        self._topObject = cmds.ls( topObject, l=1 )[0]
        self._endObject = cmds.ls( endObject, l=1 )[0]
        self._upObject  = cmds.ls( upObject,  l=1 )[0]
        self._upType    = upType
        self._aimAxis     = aimAxisIndex
        self._upAxis      = upAxisIndex
        self._worldUpAxis = worldUpAxisIndex
        
        self.core()
        
        
    def core(self):
        
        parent = cmds.listRelatives( self._endObject, p=1, f=1 )
        parents = []
        while parent:
            parents.append( parent[0] )
            if parent[0] == self._topObject: break
            parent = cmds.listRelatives( parent[0], p=1, f=1 )
        if not parents: parents = [self._topObject]
        
        parents.reverse()
        
        for parent in parents[1:]:
            self.setPosition( parent )
        
        for parent in parents:
            self.setRotate( parent )



    def getAimVector(self, target, child='' ):
        
        if not child:
            targetChild = cmds.listRelatives( target, c=1, f=1 )[0]
        else:
            targetChild = child
        
        topPose = om.MVector( *cmds.getAttr( target + '.wm' )[-4:-1] )
        endPose = om.MVector( *cmds.getAttr( targetChild + '.wm' )[-4:-1] )
        
        return endPose - topPose



    def getUpVector(self, target, upObject ):
        
        if not upObject:
            return om.MVector( 0,1,0 )
        
        if self._upType == "object":
            topPose = om.MVector( *cmds.getAttr( target + '.wm' )[-4:-1] )
            upPose  = om.MVector( *cmds.getAttr( upObject  + '.wm' )[-4:-1] )
            return upPose - topPose
        else:
            worldUpAxis = self._worldUpAxis % 3
            upVector = om.MVector( *cmds.getAttr( upObject + '.wm' )[4*worldUpAxis:4*worldUpAxis+3] )
            if self._worldUpAxis >= 3:
                upVector *= -1
            return upVector
        
        
    
    def setPosition(self, target ):
        
        aimVector = self.getAimVector( self._topObject, self._endObject )
        upVector  = self.getUpVector( self._topObject, self._upObject )
        
        crossVector = aimVector.normal() ^ upVector.normal()
        upVector = crossVector ^ aimVector.normal()
        
        topPose    = om.MVector( *cmds.getAttr( self._topObject + '.wm' )[-4:-1] )
        targetPose = om.MVector( *cmds.getAttr( target + '.wm' )[-4:-1] )
        
        targetVector = targetPose - topPose
        
        projAim = aimVector * (aimVector*targetVector)/(aimVector.length()**2)
        projUp  = upVector * (upVector *targetVector)/(upVector.length()**2)
        
        cuPose = projAim + projUp + topPose
        cmds.move( cuPose.x, cuPose.y, cuPose.z, target, ws=1, pcp=1 )
        



    def setRotate(self, target ):
        
        aimVector = self.getAimVector( target )
        upVector = self.getUpVector( target, self._upObject )
        crossVector = om.MVector()
        
        aimIndex = self._aimAxis%3
        upIndex  = self._upAxis%3
        
        crossIndex = 3-(aimIndex + upIndex)
        
        if self._aimAxis >= 3: aimVector *= -1
        if self._upAxis  >= 3: upVector  *= -1
        
        if ( aimIndex + 1 )%3 == upIndex:
            crossVector = aimVector^upVector
        else:
            crossVector = upVector^aimVector
        upVector = crossVector^aimVector
        
        #mtxList = cmds.getAttr( self._topObject+'.wm' )
        mtxList = [ (not i%5) and 1 or 0 for i in range( 16 ) ]
        
        mtxList[ aimIndex * 4 + 0 ] = aimVector.x
        mtxList[ aimIndex * 4 + 1 ] = aimVector.y
        mtxList[ aimIndex * 4 + 2 ] = aimVector.z
        mtxList[ upIndex * 4 + 0 ] = upVector.x
        mtxList[ upIndex * 4 + 1 ] = upVector.y
        mtxList[ upIndex * 4 + 2 ] = upVector.z
        mtxList[ crossIndex * 4 + 0 ] = crossVector.x
        mtxList[ crossIndex * 4 + 1 ] = crossVector.y
        mtxList[ crossIndex * 4 + 2 ] = crossVector.z
        
        mtx = om.MMatrix()
        om.MScriptUtil.createMatrixFromList( mtxList, mtx )
        
        trMtx = om.MTransformationMatrix( mtx )
        eulerRot = trMtx.eulerRotation().asVector()
        
        rot = [ math.degrees( eulerRot.x ), math.degrees( eulerRot.y ), math.degrees( eulerRot.z ) ]
        cmds.rotate( rot[0], rot[1], rot[2], target, ws=1, pcp=1 )