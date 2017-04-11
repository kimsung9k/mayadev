import maya.cmds as cmds
import maya.OpenMaya as om
import chModules.rigbase as rigbase
import chModules.system.basicfunc as basicfunc

import bjts

from ctlsAll import *

def getProperClassInMenuModule( targetName, menuModule, targetClass=None ):
    moduleClassList = dir( menuModule )
    
    targetName = basecode.removeNumber_str( targetName )
    
    matchLen = 0
    targetClassString = ''
    for cls in moduleClassList:
        if targetName.find( cls ) != -1:
            cuLen = len( cls )
            if matchLen < cuLen:
                targetClassString = cls
                matchLen = cuLen
    if targetClassString:
        exec( 'targetClass = %s.%s' % ( menuModule.__name__.split('.')[-1], targetClassString ) )
        
    return targetClass


class Basic( CtlsAll ):
    isUpperPoints = lambda x,y : y.find( 'Upper' ) != -1
    isSidePoints  = lambda x,y : y.find( '_L_' ) == -1 and y.find( '_R_' ) == -1

    def getMultRate(self, target ):
        splinePoint = target.replace( '_BJT', '_SplinePoint' )
        slineInfo = cmds.listConnections( splinePoint, type='splineCurveInfo' )[0]

        mObj = om.MObject()
        selList = om.MSelectionList()
        selList.add( slineInfo )
        selList.getDependNode( 0, mObj )
        
        mNode = om.MFnDependencyNode( mObj )
        prPlug = mNode.findPlug( 'parameter' )
        
        indexLength = prPlug.numElements()-1
        if self.isUpperPoints( target ) or self.isSidePoints( target ):
            indexLength += 1
        
        return 1.0/indexLength
    
    def getIndex(self, target ):
        numStr = ''
        for char in target:
            if char.isdigit():
                numStr += char
        return int( numStr )
    
    def getCrvInfos(self, target ):
        namespace = self.getNamespace( target )
        
        crvInfos = cmds.ls( type='splineCurveInfo' )
        return [ info for info in crvInfos if info.find( namespace ) == 0 ]
    
    def getSplinePoints(self, info ):
        tempSplinePoints = cmds.listConnections( info+'.output' )
        
        splinePoints = []
            
        while tempSplinePoints:
            tempSplinePoint = tempSplinePoints.pop(0)
                
            if not tempSplinePoint in splinePoints:
                splinePoints.append( tempSplinePoint )
                
        return splinePoints

class DefaultParam( Basic ):
    def defaultParam(self, targets, *args ):
        for target in targets:
            multRate = self.getMultRate( target )
            index    = self.getIndex( target )
            if cmds.attributeQuery( 'parameter', node = target, ex=1 ):
                cmds.setAttr( target+'.parameter', multRate*index )
    
    def defaultParamAll(self, target, *args  ):
        targetCrvInfos = self.getCrvInfos( target )
        
        for info in targetCrvInfos:
            splinePoints = self.getSplinePoints(info)
            
            indexLength = len(splinePoints)-1
            
            
            
            if self.isUpperPoints( splinePoints[0] ) or self.isSidePoints( splinePoints[0] ):
                indexLength += 1
            multRate = 1.0/indexLength
            for splinePoint in splinePoints:
                targetBjt = splinePoint.replace( 'SplinePoint', 'BJT' )
                index = self.getIndex( targetBjt )
                if cmds.attributeQuery( 'parameter', node=targetBjt, ex=1 ):
                    cmds.setAttr( targetBjt+'.parameter', multRate*index )

class MirrorParam( Basic ):
    def getOtherTarget(self, base):
        if base.find( '_L_' ):
            return base.replace( '_L_', '_R_' )
        elif base.find( '_R_' ):
            return base.replace( '_R_', '_L_' )
        else:
            return base
    
    def mirrorParamSet( self, bases, *args ):
        for base in bases:
            if not cmds.attributeQuery( 'parameter', node=base, ex=1 ):
                return None
            target = self.getOtherTarget( base )
            prValue = cmds.getAttr( base+'.parameter' )
            cmds.setAttr( target+'.parameter', prValue )
            
    def mirrorParamGet( self, bases, *args ):
        for base in bases:
            if not cmds.attributeQuery( 'parameter', node=base, ex=1 ):
                return None
            target = self.getOtherTarget( base )
            prValue = cmds.getAttr( target+'.parameter' )
            cmds.setAttr( base+'.parameter', prValue )
            
    def mirrorParamLToR(self, target, *args ):
        for info in self.getCrvInfos( target ):
            splinePoints = self.getSplinePoints(info)
            
            for splinePoint in splinePoints:
                bjt = splinePoint.replace( 'SplinePoint', 'BJT' )
                if bjt.find( '_L_' ) != -1:
                    self.mirrorParamSet( [bjt] )
                else:
                    self.mirrorParamGet( [bjt] )
        
    def mirrorParamRToL(self, target, *args ):
        for info in self.getCrvInfos( target ):
            splinePoints = self.getSplinePoints(info)
            
            for splinePoint in splinePoints:
                bjt = splinePoint.replace( 'SplinePoint', 'BJT' )
                if bjt.find( '_R_' ) != -1:
                    self.mirrorParamSet( [bjt] )
                else:
                    self.mirrorParamGet( [bjt] )
                    
class MiddleJoint( CtlsAll ):
    def addMiddleJoint(self, targets, *args ):
        for target in targets:
            targetInfo = getProperClassInMenuModule( target, bjts, bjts.BJT )()
            axis       = targetInfo.midAxis
            offsetValue = targetInfo.midOffset
            
            targetChild = cmds.listRelatives( target, c=1, type='joint' )[0]
            
            cmds.select( target )
            try: rad = cmds.getAttr( target+'.radius' )
            except: pass
            midJnt = cmds.joint( n= target.replace( '_BJT', '_MBJT' ), radius = rad*1.5 )
            blMtxDcmp = cmds.createNode( 'blendTwoMatrixDecompose', n=midJnt.replace( '_MBJT', '_Mbjt_blMtxDcmp' ) )
            distNode = cmds.createNode( 'distanceBetween', n=midJnt.replace( '_MBJT', '_Mbjt_dist' ) )
            multNode = cmds.createNode( 'multDoubleLinear', n=midJnt.replace( '_MBJT', '_Mbjt_ofsValue' ) )
            
            cmds.setAttr( multNode+'.input2', offsetValue )
            
            cmds.connectAttr( targetChild+'.t', distNode+'.point1' )
            cmds.connectAttr( distNode+'.distance', multNode+'.input1' )
            cmds.connectAttr( multNode+'.output', midJnt+'.t'+axis )
            cmds.connectAttr( target+'.im', blMtxDcmp+'.inMatrix1' )
            cmds.connectAttr( blMtxDcmp+'.or', midJnt+'.jo' )
            
class SelectBJTs( CtlsAll ):
    def selectBjts(self, target, *args ):
        namespace = self.getNamespace( target )
        cmds.select( namespace+'*_BJT', add=1 )
        cmds.select( target, d=1 )
        cmds.select( namespace+'Leg_*_Upper_BJT', d=1 )
        try: cmds.select( namespace+'*_MBJT', add=1 )
        except: pass

class BJT_Main( DefaultParam, MirrorParam, MiddleJoint, SelectBJTs ):
    pass

class connection( CtlsAll ):
    def isConnected( self, target ):
        namespace = self.getNamespace( target )
        rootBjtGrp = namespace+'Root_BJT_GRP'
        
        if cmds.listConnections( rootBjtGrp+'.r', s=1, d=0 ):
            return True
        else:
            return False
    
    def getInputsGrp( self, target ):
        namespace = self.getNamespace( target )
        
        bjtWorldGrp = namespace + 'BJT_World_GRP'
        bjtWorld    = namespace + 'BJT_World'
        rootBjtGrp  = namespace + 'Root_BJT_GRP'
        return bjtWorldGrp, bjtWorld, rootBjtGrp
    
    def getOutputsGrp( self, target ):
        namespace = self.getNamespace( target )
        
        worldCtlGrp = namespace + 'World_CTL_GRP'
        worldCtl    = namespace + 'World_CTL'
        rootGrp     = namespace + 'Root_GRP'
        return worldCtlGrp, worldCtl, rootGrp
    
    def getBjts(self, target ):
        namespace = self.getNamespace(target)
        returnBjts = cmds.ls( namespace+'*_BJT' )
        returnBjts += cmds.ls( namespace+'*_BJTN' )
        return returnBjts
    
    def disconnect( self, target,*args ):
        bjts = self.getBjts(target)
        bjts += list( self.getInputsGrp(target) )
        
        bjtWorldGrp, bjtWorld, rootBjtGrp = self.getInputsGrp(target)
        bjtNamespace = self.getNamespace( bjtWorld )
        
        try:
            worldCtl = cmds.listConnections( bjtWorld+'.v' )[0]
            attrName = bjtNamespace.replace( ':', '' )
            cmds.deleteAttr( worldCtl, attribute=attrName )
        except: pass
        
        
        for bjt in bjts:
            cons = cmds.listConnections( bjt, s=1, d=0, c=1, p=1, type='transform' )
            
            if not cons: continue
            
            outputs = cons[1::2]
            inputs  = cons[::2]
            
            mtx = basicfunc.getMMatrix( bjt )
            rValue = basicfunc.getRotateFromMatrix(mtx)
            for i in range( len( outputs ) ):
                if inputs[i].find( 'inverseScale' ) != -1: continue
                cmds.disconnectAttr( outputs[i], inputs[i] )
            try:
                cmds.setAttr( bjt+'.jo', *rValue )
                cmds.setAttr( bjt+'.r', 0,0,0 )
            except: pass
                
            if cmds.attributeQuery( 'parameter', node=bjt, ex=1 ):
                rjt = cmds.listConnections( bjt+'.parameter', d=1, s=0 )
                if rjt : 
                    rjt = rjt[0]
                    cmds.disconnectAttr( bjt+'.parameter', rjt+'.parameter' )
                
    def connect( self, sels, *args ):
        worldCtl = None
        bjtWorld = None
        for sel in sels:
            if sel.find( 'BJT_World' ) != -1:
                bjtWorld = sel
            elif sel.find( 'World_CTL' ) != -1:
                worldCtl = sel
                
        if not bjtWorld or not worldCtl:
            return None
            
        bjtWorldGrp, bjtWorld, rootBjtGrp = self.getInputsGrp( bjtWorld )
        worldCtlGrp, worldCtl, rootGrp = self.getOutputsGrp( worldCtl )
        
        bjtNamespace = self.getNamespace( bjtWorld )
        rjtNamespace = self.getNamespace( worldCtl )
        
        rigbase.connectSameAttr( worldCtlGrp, bjtWorldGrp ).doIt( 't', 'r','s' )
        rigbase.connectSameAttr( worldCtl, bjtWorld  ).doIt( 't', 'r','s' )
        #cmds.connectAttr( worldCtl+'.message', bjtWorld+'.World_CTL' )
        rigbase.connectSameAttr( rootGrp, rootBjtGrp ).doIt( 't', 'r' )
        
        bjts = self.getBjts( bjtWorld )
        
        
        try:
            attrEdit = rigbase.AttrEdit( worldCtl )
            attrEdit.addAttr( ln=bjtNamespace.replace( ':', '' ), at='long', cb=1, min=0, max=1 )
        except: pass
        try:
            bjtWorldShape = cmds.listRelatives( bjtWorld, s=1 )[0]
            cmds.connectAttr( worldCtl+'.'+bjtNamespace.replace( ':', '' ), bjtWorldShape+'.v' )
        except: pass
        
        for bjt in bjts:
            rjt = bjt.replace( '_BJT', '_RJT' )
            if not bjtNamespace:
                rjt = rjtNamespace + rjt
            else:
                rjt = rjt.replace( bjtNamespace, rjtNamespace )
            
            if not cmds.objExists( rjt ):continue
            
            cmds.connectAttr( rjt+'.t', bjt+'.t' )
            cmds.connectAttr( rjt+'.r', bjt+'.r' )
            cmds.connectAttr( rjt+'.s', bjt+'.s' )
            if rjt.find( 'Leg_L_Lower4' ) != -1 or rjt.find( 'Leg_R_Lower4' ) != -1:
                cmds.connectAttr( rjt+'.sh', bjt+'.sh' )
                
            try:
                cmds.connectAttr( rjt+'.jo', bjt+'.jo' )
            except: pass
            
            try:
                cmds.setAttr( bjt+'.jo', 0,0,0 )
            except: pass
            
            if cmds.attributeQuery( 'parameter', node=bjt, ex=1 ):
                cmds.connectAttr( bjt+'.parameter', rjt+'.parameter', f=1 )

class BJT_World_Main( connection ):
    pass