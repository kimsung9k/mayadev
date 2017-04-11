import maya.cmds as cmds
import volumeHairTool.functions as fnc
import random
import maya.mel as mel


class CreateVolumeHair:

    def __init__(self, surface, mesh  ):
        
        self._surfObj = surface
        self._surfShape = fnc.getShapeFromObject( surface )
        self._meshShape = fnc.getShapeFromObject( mesh )
        
        self.inCurveNode = self.getInCurveNode()
        self.outCurveNode = self.getOutCurveNode()
        
        
    def setGroup( self, curve ):
        
        surfObjGrp = cmds.listRelatives( self._surfObj, p=1 )[0]
        
        if not cmds.attributeQuery( 'volumeCurveGrps', node=surfObjGrp, ex=1 ):
            cmds.addAttr( surfObjGrp, ln='volumeCurveGrps', at='message' )
        
        cons = cmds.listConnections( surfObjGrp+'.volumeCurveGrps', s=1, d=0 )
        if not cons:
            volumeCurveGrps = cmds.createNode( 'transform', n=surfObjGrp+'_volumeCurveGrps' )
            cmds.connectAttr( volumeCurveGrps+'.message', surfObjGrp+'.volumeCurveGrps' )
        else:
            volumeCurveGrps = cons[0]

        if not cmds.attributeQuery( 'volumeCurveGrp', node=self._surfObj, ex=1 ):
            cmds.addAttr( self._surfObj, ln='volumeCurveGrp', at='message' )
        cons = cmds.listConnections( self._surfObj+'.volumeCurveGrp', s=1, d=0 )
        if not cons:
            volumeCurveGrp = cmds.createNode( 'transform', n=self._surfObj+'_volumeCurveGrp' )
            cmds.connectAttr( volumeCurveGrp+'.message', self._surfObj+'.volumeCurveGrp' )
        else:
            volumeCurveGrp = cons[0]
        
        volumeCurveGrpParents = cmds.listRelatives( volumeCurveGrp, p=1 )
        if volumeCurveGrpParents:
            if not volumeCurveGrps in volumeCurveGrpParents:
                cmds.parent( volumeCurveGrp, volumeCurveGrps )
        else:
            cmds.parent( volumeCurveGrp, volumeCurveGrps )
        
        volumeCurveParent = cmds.listRelatives( curve, p=1 )
        if volumeCurveParent:
            if not volumeCurveGrp in volumeCurveParent:
                cmds.parent( curve, volumeCurveGrp )
        else:
            cmds.parent( curve, volumeCurveGrp )
            


    def getSurfaceInfo(self, paramSep ):
        
        minValue, maxValue = cmds.getAttr( self._surfShape+'.minMaxRangeV' )[0]
        self._paramRate = ( maxValue-minValue )/paramSep
        self._numSpans = cmds.getAttr( self._surfShape+'.spansU' )
        


    def getInCurveNode(self):
        
        cons = cmds.listConnections( self._surfShape, s=0, d=1, type='volumeCurvesOnSurface' )
        
        if cons:
            for con in cons:
                if cmds.attributeQuery( 'isInCurveNode', node=con, ex=1 ):
                    return con

        node = cmds.createNode( 'volumeCurvesOnSurface' )
        cmds.addAttr( node, ln='isInCurveNode', at='bool' )
        
        cmds.connectAttr( self._surfShape+'.local', node+'.inputSurface' )
        cmds.connectAttr( self._surfShape+'.wm', node+'.inputMatrix' )
        
        cmds.connectAttr( self._meshShape+'.outMesh', node+'.inputMesh' )
        cmds.connectAttr( self._meshShape+'.wm', node+'.meshMatrix' )
        
        return node
    


    def getOutCurveNode(self):
        
        cons = cmds.listConnections( self._surfShape, s=0, d=1, type='volumeCurvesOnSurface' )
        
        if cons:
            for con in cons:
                if cmds.attributeQuery( 'isOutCurveNode', node=con, ex=1 ):
                    return con

        node = cmds.createNode( 'volumeCurvesOnSurface' )
        cmds.addAttr( node, ln='isOutCurveNode', at='bool' )
        
        cmds.connectAttr( self._surfShape+'.local', node+'.inputSurface' )
        cmds.connectAttr( self._surfShape+'.wm', node+'.inputMatrix' )
        
        cmds.connectAttr( self._meshShape+'.outMesh', node+'.inputMesh' )
        cmds.connectAttr( self._meshShape+'.wm', node+'.meshMatrix' )
        
        return node
    


    def reduceOutputCurve(self, outputCurves ):
        
        for crvObj in outputCurves:
            print crvObj


    
    def createInCurve(self, numCurve, paramRand, offsetRand, centerOffset = 0.4 ):
        
        node = self.inCurveNode
        
        minValue, maxValue = cmds.getAttr( self._surfShape+'.minMaxRangeV' )[0]
        
        if numCurve in [1,2,3]:
            paramRate = ( maxValue-minValue )/numCurve
        else:
            paramRate = ( maxValue-minValue )/(numCurve-1)
        
        offsetRand *=0.5
        
        outputCurves = cmds.listConnections( node+'.outputCurve' )
        
        if outputCurves:
            lenOutputCurves = len( outputCurves )
            
            if lenOutputCurves > numCurve:
                cmds.delete( outputCurves[numCurve-lenOutputCurves:] )
        
        if not numCurve:
            return None
        
        for i in range( numCurve ):
            addOffsetParam = random.uniform( -paramRate/2*paramRand, paramRate/2*paramRand )
            addOffsetCenter = random.uniform( -offsetRand, offsetRand )
            
            outputCurveCon = cmds.listConnections( node+'.outputCurve[%d]' % i )
            
            if not outputCurveCon:
                crvNode = cmds.createNode( 'nurbsCurve' )
                crvObj = cmds.listRelatives( crvNode, p=1 )[0]
                cmds.connectAttr( node+'.outputCurve[%d]' % i, crvNode+'.create' )
                cmds.addAttr( crvObj, ln='paramRate', dv= paramRate*i + addOffsetParam + paramRate*0.5 )
                cmds.setAttr( crvObj+'.paramRate', e=1, k=1 )
                cmds.addAttr( crvObj, ln='centerRate', dv= centerOffset+addOffsetCenter )
                cmds.setAttr( crvObj+'.centerRate', e=1, k=1 )
                cmds.connectAttr( crvObj+'.paramRate', node+'.curveInfo[%d].paramRate' % i )
                cmds.connectAttr( crvObj+'.centerRate', node+'.curveInfo[%d].centerRate' % i )
            else:
                crvObj = outputCurveCon[0]
                cmds.setAttr( crvObj+'.paramRate', paramRate*i + addOffsetParam + paramRate*0.5  )
                cmds.setAttr( crvObj+'.centerRate', centerOffset+addOffsetCenter  )
            crvObj = cmds.rename( crvObj, self._surfObj+'_curve_%d' % i )
            
            if i == numCurve -1:
                if not numCurve in [2,3]:
                    cmds.setAttr( crvObj+'.centerRate', 0 )
            
            self.setGroup( crvObj )
        
        outputLen = fnc.getLastIndex( node+'.outputCurve' )+1
        
        for i in range( outputLen ):
            outputCons = cmds.listConnections( node+'.outputCurve[%d]' % i )
            if not outputCons:
                cmds.removeMultiInstance( '%s[%d]' %( node+'.outputCurve', i ) )
                cmds.removeMultiInstance( '%s[%d]' %( node+'.curveInfo', i ) )


            
    def createOutCurve(self, numCurve, paramRand, offsetRand, centerOffset = 0.9 ):
        
        node = self.outCurveNode
        
        minValue, maxValue = cmds.getAttr( self._surfShape+'.minMaxRangeV' )[0]
        
        if not numCurve:
            paramRate = ( maxValue-minValue )/1
        else:
            paramRate = ( maxValue-minValue )/ numCurve
        
        offsetRand *=0.5
        
        outputCurves = cmds.listConnections( node+'.outputCurve' )
        
        if outputCurves:
            lenOutputCurves = len( outputCurves )
            
            if lenOutputCurves > numCurve:
                cmds.delete( outputCurves[numCurve-lenOutputCurves:] )
        
        if not numCurve:
            return None
        
        for i in range( numCurve ):
            addOffsetParam = random.uniform( -paramRate/2*paramRand, paramRate/2*paramRand )
            addOffsetCenter = random.uniform( -offsetRand, offsetRand )
            
            outputCurveCon = cmds.listConnections( node+'.outputCurve[%d]' % i )
            
            if not outputCurveCon:
                crvNode = cmds.createNode( 'nurbsCurve' )
                crvObj = cmds.listRelatives( crvNode, p=1 )[0]
                cmds.connectAttr( node+'.outputCurve[%d]' % i, crvNode+'.create' )
                cmds.addAttr( crvObj, ln='paramRate', dv= paramRate*i + addOffsetParam )
                cmds.setAttr( crvObj+'.paramRate', e=1, k=1 )
                cmds.addAttr( crvObj, ln='centerRate', dv= centerOffset+addOffsetCenter )
                cmds.setAttr( crvObj+'.centerRate', e=1, k=1 )
                cmds.connectAttr( crvObj+'.paramRate', node+'.curveInfo[%d].paramRate' % i )
                cmds.connectAttr( crvObj+'.centerRate', node+'.curveInfo[%d].centerRate' % i )
            else:
                crvObj = outputCurveCon[0]
                cmds.setAttr( crvObj+'.paramRate', paramRate*i + addOffsetParam  )
                cmds.setAttr( crvObj+'.centerRate', centerOffset+addOffsetCenter  )
            crvObj = cmds.rename( crvObj, self._surfObj+'_curve_%d' % i )
            self.setGroup( crvObj )
        
        outputLen = fnc.getLastIndex( node+'.outputCurve' )+1
        
        for i in range( outputLen ):
            outputCons = cmds.listConnections( node+'.outputCurve[%d]' % i )
            if not outputCons:
                cmds.removeMultiInstance( '%s[%d]' %( node+'.outputCurve', i ) )
                cmds.removeMultiInstance( '%s[%d]' %( node+'.curveInfo', i ) )