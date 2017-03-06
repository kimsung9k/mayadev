import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaMPx as mpx
import os, math

from chModules import basecode
from chModules import rigbase
from chModules.set import mocapset
import ctlsAll

import allCtls
import armandlegCtls
import headCtls
import torsoCtls

import chModules.system.mirror as mirror

ctlModules = [ allCtls, armandlegCtls,  headCtls, torsoCtls ]

ctlH = allCtls.CtlsHierarchy()

def getProperClassInMenuModule( targetName, menuModules, targetClass=None ):
    for menuModule in menuModules:
        moduleClassList = dir( menuModule )
        
        targetName = basecode.removeNumber_str( targetName ).replace( '_L_', '_' ).replace( '_R_', '_' )
        matchLen = 0
        targetClassString = ''
        for cls in moduleClassList:
            if targetName == cls:
                targetClassString = cls
                break
            if targetName.find( cls ) != -1:
                cuLen = len( cls )
                if matchLen < cuLen:
                    targetClassString = cls
                    matchLen = cuLen
                    
        if targetClassString:
            exec( 'targetClass = %s.%s' % ( menuModule.__name__.split('.')[-1], targetClassString ) )
            break

    return targetClass



class CTL( ctlsAll.CtlsAll ):
    
    def goToObject(self, first, second, *args ):
        
        if cmds.nodeType( first ) == 'joint':
            
            jo = cmds.getAttr( first+'.jo' )[0]
            mpxTransform = mpx.MPxTransformationMatrix()
            rotVector = om.MVector( math.radians( jo[0] ), math.radians( jo[1] ), math.radians( jo[2] ) ) 
            mpxTransform.rotateTo( om.MEulerRotation( rotVector ) )
            joMtx = mpxTransform.asMatrix()
            
            fMtx = om.MMatrix()
            fPMtx = om.MMatrix()
            fMtxList = cmds.getAttr( first+'.wm' )
            fPMtxList = cmds.getAttr( first+'.pm' )
            sMtx = om.MMatrix()
            sMtxList = cmds.getAttr( second+'.wm' )
            
            om.MScriptUtil.createMatrixFromList( fMtxList, fMtx )
            om.MScriptUtil.createMatrixFromList( fPMtxList, fPMtx )
            om.MScriptUtil.createMatrixFromList( sMtxList, sMtx )
            
            sMtxPose = [ sMtx(3,0), sMtx(3,1), sMtx(3,2) ]
            
            rMtx = sMtx*(joMtx*fPMtx).inverse()
            rTransform = mpx.MPxTransformationMatrix( rMtx )
            rVector = rTransform.eulerRotation().asVector()
            
            rot = [ math.degrees( rVector.x ), math.degrees( rVector.y ), math.degrees( rVector.z ) ]

            cmds.setAttr( first+'.r', *rot )
            cmds.move( sMtxPose[0], sMtxPose[1], sMtxPose[2], first, ws=1 )

        else:
            rigbase.goToSamePosition( first, second )
        
    
    
    def setDefaultTransform( self, targets, *args ):
        for target in targets:
            targetClass = getProperClassInMenuModule( target, ctlModules, allCtls.AllCtls )
            if 'transformAttrs' in dir( targetClass ):
                if targetClass.transformAttrs == 'All':
                    targetAttrs = cmds.listAttr( target, k=1 )
                else:
                    targetAttrs = targetClass.transformAttrs
                for attr in targetAttrs:
                    rigbase.trySetAttr( target+'.'+attr, 0 )
            rigbase.transformDefault( target )
            
    def getHierarchy(self, target ):
        ns = self.getNamespace(target)
        
        hierarchyObjs = []
        for name in ctlH.getHierarchy( target.replace( ns,'' ) ):
            if cmds.objExists( ns+name ):
                hierarchyObjs.append( ns+name )
        
        return hierarchyObjs
        
    def setDefaultTransformH(self, target, *args ):
        targets = self.getHierarchy( target )
        self.setDefaultTransform(targets)
        
    def selectH(self, target, *args ):
        targets = self.getHierarchy( target )
        cmds.select( targets )
        
    def _mirror_setMirror(self, target, typ='mirror' ):
        if not target: return None
        namespace = self.getNamespace(target)
        targetClass = getProperClassInMenuModule( target.replace( namespace, '' ), ctlModules, allCtls.AllCtls )
        if 'mirrorType' in dir( targetClass ):
            if targetClass.mirrorType == 'object':
                if mirror.getOtherSide(target):
                    mirror.objectMirror( target, mirror.getOtherSide(target), typ )
            elif targetClass.mirrorType == 'center':
                mirror.centerMirror( target, namespace+targetClass.mirrorP, 0, typ )
            elif targetClass.mirrorType == 'position':
                mirror.positionMirror( target, mirror.getOtherSide(target), typ )
            elif targetClass.mirrorType == 'axis':
                if target.find( '_L_' ): 
                    targetP = targetClass.mirrorP.replace( '__', '_L_' )
                elif target.find( '_R_' ): 
                    targetP = targetClass.mirrorP.replace( '__', '_R_' )
                mirror.axisMirror( target,  mirror.getOtherSide(target), namespace+targetP, targetClass.mirrorBaseVector, typ )
            elif targetClass.mirrorType == 'objP':
                if target.find( '_L_' ): 
                    targetP = targetClass.mirrorP.replace( '__', '_L_' )
                    otherP = targetP.replace( '_L_', '_R_' )
                elif target.find( '_R_' ): 
                    targetP = targetClass.mirrorP.replace( '__', '_R_' )
                    otherP = targetP.replace( '_R_', '_L_' )
                mirror.objPMirror( target, mirror.getOtherSide(target), namespace+targetP, namespace+otherP, typ )
        
        otherTarget = None
        if target.find( '_L_' ) != -1:
            otherTarget = target.replace( '_L_', '_R_' )
        elif target.find( '_R_' ) != -1:
            otherTarget = target.replace( '_R_', '_L_' )
        
        if not otherTarget: return None
        
        if typ=='mirror':    
            for attr in targetClass.transformAttrs:
                value = cmds.getAttr( target+'.'+attr )
                cmds.setAttr( otherTarget+'.'+attr, value )

        elif typ=='flip':
            for attr in targetClass.transformAttrs:
                value = cmds.getAttr( target+'.'+attr )
                otherValue = cmds.getAttr( otherTarget+'.'+attr )
                cmds.setAttr( target+'.'+attr, otherValue )
                cmds.setAttr( otherTarget+'.'+attr, value )
        
    def _mirror_getFollowTargets(self, namespace ):
        self.__armL = namespace+'Arm_L_Switch_CTL'
        self.__armR = namespace+'Arm_R_Switch_CTL'
        self.__legL = namespace+'Leg_L_Switch_CTL'
        self.__legR = namespace+'Leg_R_Switch_CTL'
        self.__collarL = namespace+'Collar_L_CTL'
        self.__collarR = namespace+'Collar_R_CTL'
        self.__head = namespace+'Head_CTL'
        self.__followTargets = [ self.__armL, self.__armR, self.__legL, self.__legR, self.__collarL, self.__collarR, self.__head ]
        
    def _mirror_keepFollowValues(self):
        self.__followValues = []
        for i in range( len( self.__followTargets ) ):
            self.__followValues.append( [] )
        
        for target in self.__followTargets:
            index = self.__followTargets.index(target)
            
            udAttrs = cmds.listAttr( target, ud=1 )
            
            for attr in udAttrs:
                if attr.find( 'Follow' ) != -1:
                    followValue = cmds.getAttr( target+'.'+attr )
                    self.__followValues[index].append( followValue )
                    
    def _mirror_setFollowDefault(self):
        for target in self.__followTargets:
            if target.find( 'Collar' ) != -1:
                otherTarget = target.replace( 'Collar_L', 'Arm_L_PoleV' ).replace( 'Collar_R', 'Arm_R_PoleV' )
                mtxList = cmds.getAttr( otherTarget+'.wm' )
            elif target.find( 'Leg' ) != -1:
                poleVTarget = target.replace( 'Switch_CTL', 'PoleV_CTL' )
                poleVMtxList = cmds.getAttr( poleVTarget+'.wm' )
                mtxList = cmds.getAttr( target.replace( 'Switch', 'IK' ) +'.wm' )
            else:
                mtxList = cmds.getAttr( target.replace( 'Switch', 'IK' ) +'.wm' )
            
            udAttrs = cmds.listAttr( target, ud=1 )
            for attr in udAttrs:
                if attr.find( 'Follow' ) != -1:
                    case1 = target.find( 'Arm' ) != -1 and attr == 'collarFollow'
                    case2 = target.find( 'Leg' ) != -1 and attr == 'hipFollow'
                    case3 = attr == 'neckFollow'
                    if case1 or case2 or case3:
                        cmds.setAttr( target+'.'+attr, 10 )
                    else:
                        cmds.setAttr( target+'.'+attr, 0 )
                        
            if target.find( 'Switch' ) != -1: target = target.replace( 'Switch', 'IK' )
            elif target.find( 'Collar' ) != -1:
                target = target.replace( 'Collar_L', 'Arm_L_PoleV' ).replace( 'Collar_R', 'Arm_R_PoleV' )
            cmds.xform( target, ws=1, matrix = mtxList )
            if cmds.nodeType( target ) == 'joint':
                rigbase.setRotate_keepJointOrient(mtxList, target)
            
            if target.find( 'Leg' ) != -1:
                cmds.xform( poleVTarget, ws=1, matrix = poleVMtxList )
    
    def _mirror_setFollowValues(self):
        for target in self.__followTargets:
            if target.find( 'Collar' ) != -1:
                otherTarget = target.replace( 'Collar_L', 'Arm_L_PoleV' ).replace( 'Collar_R', 'Arm_R_PoleV' )
                mtxList = cmds.getAttr( otherTarget+'.wm' )
            elif target.find( 'Leg' ) != -1:
                poleVTarget = target.replace( 'Switch_CTL', 'PoleV_CTL' )
                poleVMtxList = cmds.getAttr( poleVTarget+'.wm' )
                mtxList = cmds.getAttr( target.replace( 'Switch', 'IK' )+'.wm' )
            else:
                mtxList = cmds.getAttr( target.replace( 'Switch', 'IK' )+'.wm' )
            
            index = self.__followTargets.index( target )
            udAttrs = cmds.listAttr( target, ud=1 )
            
            for attr in udAttrs:
                if attr.find( 'Follow' ) != -1:
                    cmds.setAttr( target+'.'+attr, self.__followValues[index].pop(0) )
                    
            if target.find( 'Switch' ) != -1: target = target.replace( 'Switch', 'IK' )
            elif target.find( 'Collar' ) != -1:
                target = target.replace( 'Collar_L', 'Arm_L_PoleV' ).replace( 'Collar_R', 'Arm_R_PoleV' )
            
            cmds.xform( target, ws=1, matrix = mtxList )
            if cmds.nodeType( target ) == 'joint':
                rigbase.setRotate_keepJointOrient( mtxList, target )
                
            if target.find( 'Leg' ) != -1:
                cmds.xform( poleVTarget, ws=1, matrix = poleVMtxList )
            
    def mirror(self, targets, *args ):
        for target in targets:
            self._mirror_setMirror( target )
            
    def mirrorH(self, target, side, *args ):
        namespace = self.getNamespace( target )
        #self._mirror_getFollowTargets( namespace )
        #self._mirror_keepFollowValues()
        #self._mirror_setFollowDefault()
        
        targets = self.getHierarchy( target )
        for target in targets:
            if target.find( '_%s_' % side ) != -1: continue
            self._mirror_setMirror( target )
        #self._mirror_setFollowValues()
            
    def flip(self, targets, *args ):
        for target in targets:
            self._mirror_setMirror( target, 'flip' )
            
    def flipH(self, mainTarget, *args ):
        namespace = self.getNamespace( mainTarget )
        self._mirror_getFollowTargets( namespace )
        self._mirror_keepFollowValues()
        self._mirror_setFollowDefault()
        targets = self.getHierarchy( mainTarget )
        
        if mainTarget.find( '_L_' ) != -1:
            side = 'R'
        else:
            side = 'L'
        for target in targets:
            if target.find( '_%s_' % side ) != -1: continue
            self._mirror_setMirror( target, 'flip' )
        self._mirror_setFollowValues()
        
    def mirrorShape(self, target, *args ):
        sels = cmds.ls( sl=1 )
        for sel in sels:
            try:
                otherTarget = mirror.getOtherSide( sel )
                rigbase.mirrorShape( sel, otherTarget )
            except: pass


class prefixWindow:
    
    def __init__(self):
        
        self._winName = "addCharacterPrefix"
        self._title   = "Add Character Name Prefix UI"
        
        self._worldCtl = cmds.ls( sl=1 )[-1]
    
        self.core()
    
    def core(self):
        
        if cmds.window( self._winName, ex=1 ):
            cmds.deleteUI( self._winName )
        cmds.window( self._winName, title=self._title )
        
        cmds.columnLayout()
        cmds.rowColumnLayout( nc=2, cw=[(1,100),(2,200)] )
        cmds.text( l='Prefix Name  : ' )
        self._field = cmds.textField()
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=2, cw=[(1,150),(2,150)])
        cmds.button( l='Rename', c= self.rename )
        cmds.button( l='Close', c= self.delWindow )
        cmds.setParent( '..' )
        
        cmds.window( self._winName, e=1, wh=[304,50] )
        cmds.showWindow( self._winName )
        
    
    def delWindow(self, *args ):
        cmds.deleteUI( self._winName )
        
    
    def rename(self, *args ):
        
        fieldName = cmds.textField( self._field, q=1, tx=1 )
        
        ns = self._worldCtl.replace( 'World_CTL', '' )
        
        allItems = cmds.ls()
        
        worldCtlChecked = False
        
        if not ns:
            
            if not fieldName: return None
            
            for item in allItems:
                if not worldCtlChecked:
                    if self._worldCtl == item:
                        self._worldCtl = cmds.rename( item, fieldName+item )
                        worldCtlChecked = True
                        continue
                try:
                    cmds.rename( item, fieldName+item )
                except: pass
        else:
            for item in allItems:
                if not worldCtlChecked:
                    if self._worldCtl == item:
                        self._worldCtl = cmds.rename( item, item.replace( ns, fieldName ) )
                        worldCtlChecked = True
                        continue
                try:
                    cmds.rename( item, item.replace( ns, fieldName ) )
                except: pass
            


class World_CTL( CTL ):
    def __init__( self ):
        
        self.moc_getParent_dict = { 'Root_MOCPiv' : 'Root_MOC',
                          'Root_MOC' : 'All_Moc',
                          'Chest_MOC' : 'Root_MOCPiv',
                          'Neck_MOC' : 'Chest_MOC',
                          'NeckMiddle_MOC' : 'Neck_MOC',
                          'Head_MOC' :'Neck_MOC',
                          'Collar_SIDE_MOC' : 'Chest_MOC',
                          'Shoulder_SIDE_MOC' : 'Collar_SIDE_MOC',
                          'Elbow_SIDE_MOC' : 'Shoulder_SIDE_MOC',
                          'Wrist_SIDE_MOC' : 'Elbow_SIDE_MOC',
                          'Hip_SIDE_MOC' : 'Root_MOC',
                          'Knee_SIDE_MOC' : 'Hip_SIDE_MOC',
                          'Ankle_SIDE_MOC' : 'Knee_SIDE_MOC' }
        

        self.ctl_getParent_dict = { 'TorsoRotate_CTL' : 'Root_CTL',
                              'Root_CTL' : 'Move_CTL',
                              'Chest_CTL' : 'TorsoRotate_CTL',
                              'ChestMove_CTL' : 'Chest_CTL',
                              'Neck_CTL' : 'ChestMove_CTL',
                              'NeckMiddle_CTL' : 'Neck_CTL',
                              'Head_CTL' : 'Neck_CTL',
                              'Collar_SIDE_CTL' : 'ChestMove_CTL',
                              'Shoulder_SIDE_CTL' : 'Collar_SIDE_CTL',
                              'Arm_SIDE_FK0_CTL' : 'Collar_SIDE_CTL',
                              'Arm_SIDE_FK1_CTL' : 'Arm_SIDE_FK0_CTL',
                              'Arm_SIDE_FK2_CTL' : 'Arm_SIDE_FK1_CTL',
                              'Arm_SIDE_IK_CTL' : 'Collar_SIDE_CTL',
                              'Leg_SIDE_FK0_CTL' : 'Root_CTL',
                              'Leg_SIDE_FK1_CTL' : 'Leg_SIDE_FK0_CTL',
                              'Leg_SIDE_FK2_CTL' : 'Leg_SIDE_FK1_CTL',
                              'Leg_SIDE_IK_CTL' : 'Root_CTL' }
        
        self.moc_getCtls_dict = {'All_Moc' : ['World_CTL'],
                                 'Root_MOCPiv' : ['TorsoRotate_CTL'],
                          'Root_MOC' : [ 'Root_CTL' ],
                          'Chest_MOC' : [ 'Chest_CTL','ChestMove_CTL' ],
                          'Neck_MOC' : [ 'Neck_CTL' ],
                          'NeckMiddle_MOC' : [ 'NeckMiddle_CTL' ],
                          'Head_MOC' : ['Head_CTL'],
                          'Collar_SIDE_MOC' : [ 'Collar_SIDE_CTL' ],
                          'Shoulder_SIDE_MOC' : [ 'Shoulder_SIDE_CTL', 'Arm_SIDE_FK0_CTL' ], 
                          'Elbow_SIDE_MOC' : [ 'Arm_SIDE_FK1_CTL' ],
                          'Wrist_SIDE_MOC' : [ 'Arm_SIDE_FK2_CTL' ],
                          'Hip_SIDE_MOC' : [ 'Leg_SIDE_FK0_CTL' ],
                          'Knee_SIDE_MOC' : [ 'Leg_SIDE_FK1_CTL' ],
                          'Ankle_SIDE_MOC' : [ 'Leg_SIDE_FK2_CTL' ] }
        
        self.moc_getCtls_items = self.moc_getCtls_dict.items()
        
        
        self.moc_getIkCtl_dict = { 'Wrist_SIDE_MOC' : [ 'Collar_SIDE_MOC', 'Arm_SIDE_IK_CTL' ],
                                   'Ankle_SIDE_MOC'    : [ 'Root_MOC', 'Leg_SIDE_IK_CTL' ] }
        
        self.moc_getIkCtl_items = self.moc_getIkCtl_dict.items()
        
        
        poleVCtl_getMoc_dict = { 'Arm_L_PoleV_CTL' : ['Shoulder_L_MOC', -1 ], 
                            'Leg_L_PoleV_CTL' : ['Hip_L_MOC', 1 ],
                            'Arm_R_PoleV_CTL' : ['Shoulder_R_MOC', -1 ], 
                            'Leg_R_PoleV_CTL' : ['Hip_R_MOC', 1 ] }
        
        self.poleVCtl_getMoc_items = poleVCtl_getMoc_dict.items()
        
        
    
    
    def isNameSpaced(self, target ):
        
        if target == 'World_CTL':
            return True
        else:
            return False
    
    
    def AddNameSpace(self, target, *args ):
        
        prefixWindow()
        
    
    def mocExists(self, target ):
        
        namespace = target.replace( 'World_CTL' , '' )
        
        mocs = ['*_MOC','*:*_MOC','*:*:*_MOC']
        if cmds.ls( mocs, type='joint'):
            return True
        
        return False


    def isAllMoc(self, target ):
        if target.find( 'All_Moc' ) != -1:
            return True
        else:
            return False


    def isConnected(self, target ):
        namespace = self.getNamespace(target)
        
        rootInit = namespace+'Root_Init'
        
        if cmds.listConnections( rootInit+'.r', s=1, d=0 ):
            return True
        else:
            return False
        

    def isMocConnected_old(self, target ):
        namespace = self.getNamespace(target)
        rootInit = namespace + 'Root_Init'
        cons = cmds.listConnections( rootInit+'.r', s=1, d=0, type='multMatrixDecompose' )
        if cons:
            moc = cmds.listConnections( cons[0], s=1, d=0)[0]
            if moc.find( 'Root_MOC' )!=-1:
                return True
        return False

    
    def isMocConnected(self, target ):
        namespace = self.getNamespace( target )
        rootCtl = namespace + 'Root_CTL'
        cons = cmds.listConnections( rootCtl, s=1, d=0, type='multMatrixDecompose' )
        if cons:
            allMocCons = cmds.listConnections( cons[0]+'.i[1]', s=1, d=0 )
            if allMocCons:
                if allMocCons[0].find( 'All_Moc' ) != -1:
                    return True
        return False
    

    def createMocapJoint(self, target, withSkin=False, *args ):
        mocapset.MocSet(target, withSkin )
        

    def connectMocapJoint_old(self, allMoc, worldCtl, *args ):
        mocNamespace = allMoc.replace( 'All_Moc', '' )
        initNamespace = worldCtl.replace( 'World_CTL', '' )
        
        interpoleMocs = [ 'Shoulder_L_MOC','Shoulder_R_MOC', 'Hip_L_MOC', 'Hip_R_MOC' ]
        
        def setPoleVOffset( target, directionValue ):
            offsetGrp = cmds.createNode( 'transform', n=midMoc.replace( 'MOC', 'MocOffsetGrp' ) )
            offset = cmds.createNode( 'transform', n=midMoc.replace( 'MOC', 'MocOffset' ) )
            blMtx = cmds.createNode( 'blendTwoMatrixDecompose', n=midMoc.replace( 'MOC', 'MocOffsetGrpBlend' ) )
            cmds.parent( offset, offsetGrp )
            cmds.parent( offsetGrp, midMoc )
            cmds.connectAttr( target+'.im', blMtx+'.inMatrix1' )
            cmds.connectAttr( blMtx+'.orx', offsetGrp+'.rx' )
            cmds.connectAttr( blMtx+'.ory', offsetGrp+'.ry' )
            cmds.connectAttr( blMtx+'.orz', offsetGrp+'.rz' )
            cmds.setAttr( offsetGrp+'.t', 0,0,0 )
            cmds.setAttr( offset+'.t', 0,0,directionValue )
            return offset
            
        for moc in interpoleMocs:
            topMoc = mocNamespace + moc
            topP = cmds.listRelatives( topMoc, p=1 )[0]
            midMoc = cmds.listRelatives( topMoc, c=1 )[0]
            endMoc = cmds.listRelatives( midMoc, c=1 )[0]
            
            cmds.select( topP )
            for moc in [ topMoc, midMoc, endMoc ]:
                mocAf = cmds.joint( n= moc.replace( 'MOC', 'MocAfter' ) )
                cmds.connectAttr( moc+'.t', mocAf+'.t' )
                cmds.connectAttr( moc+'.jo', mocAf+'.jo' )
                cmds.setAttr( mocAf+'.pay', cmds.getAttr( moc+'.pay' ) )
                cmds.select( mocAf )
            
            handle = cmds.ikHandle( sj=topMoc.replace( 'MOC', 'MocAfter' ), ee=endMoc.replace( 'MOC', 'MocAfter' ), sol='ikRPsolver', n=midMoc.replace( '_MOC', '_MocItpHandle' ) )[0]
            
            directionValue = (cmds.getAttr( midMoc+'.tx' )+cmds.getAttr( endMoc+'.tx' ))/2
            angleValue = 90
            if midMoc.find( 'Elbow' ) != -1:
                angleValue = -90
                directionValue *= -1
            offset = setPoleVOffset( midMoc, directionValue )
            cmds.setAttr( midMoc.replace( 'MOC', 'MocAfter' )+'.pay', angleValue )
                
            cmds.poleVectorConstraint( offset, handle )
            cmds.pointConstraint( endMoc, handle )
            cmds.orientConstraint( endMoc, endMoc.replace( 'MOC', 'MocAfter' ) ) 
            
            cmds.parent( handle, topP )
            cmds.setAttr( handle+'.v', 0 )
            
            cmds.setAttr( topMoc.replace( 'MOC', 'MocAfter' )+'.v', 0 )
            
        mocs = cmds.ls( mocNamespace+'*_MOC' )
        
        for moc in mocs:
            init = moc.replace( mocNamespace, initNamespace ).replace( '_MOC', '_Init' )
            dcmp = cmds.createNode( 'multMatrixDecompose', n=moc.replace( '_MOC', '_MocDmcp' ) )
            if cmds.objExists( moc.replace( 'MOC', 'MocAfter' ) ):
                moc = moc.replace( 'MOC', 'MocAfter' )
            cmds.connectAttr( moc+'.m', dcmp+'.i[0]' )
            mocP = cmds.listRelatives( moc, p=1 )[0]
            if mocP.find( 'MOCSep' ) != -1:
                cmds.connectAttr( mocP+'.m', dcmp+'.i[1]' )
                mocPP = cmds.listRelatives( mocP, p=1 )
                if mocPP: mocPP = mocPP[0]
                if mocPP.find( 'MOCPiv' ) != -1:
                    cmds.connectAttr( mocPP+'.m', dcmp+'.i[2]')
            cmds.connectAttr( dcmp+'.ot', init+'.t' )
            cmds.connectAttr( dcmp+'.or', init+'.r' )

        rigbase.repairConstraint()




    def connectMocapJoint(self, allMoc, worldCtl, *args ):

        print "self : ", self

        def chestConnect( chestCtl, mocNs ):
            import copy
            ns = chestCtl.replace( 'Chest_CTL', '' )
        
            torsoRot = ns + 'TorsoRotate_CTL'
            splineNodes = cmds.ls( ns + 'Spline*_SplinePoint' )
            conedJnts   = cmds.ls( ns + 'Spline*_SplineHJnt' )
            splineRoot  = ns + 'Root_GRP'
        
            condObj = cmds.createNode( 'transform' )
            condMmdc = cmds.createNode( 'multMatrixDecompose' )
            cmds.connectAttr( torsoRot + '.wm', condMmdc + '.i[0]' )
            cmds.connectAttr( condObj + '.pim', condMmdc + '.i[1]' )
            cmds.connectAttr( condMmdc + '.ot', condObj +'.t' )
            cmds.connectAttr( condMmdc + '.or', condObj +'.r' )
            cmds.connectAttr( condMmdc + '.os', condObj +'.s' )
            cmds.connectAttr( condMmdc + '.osh', condObj +'.sh' )
            
            jnts = []
            cmds.select( condObj )
            for i in range( len( splineNodes ) ):
                jnt = cmds.joint()
                jnts.append( jnt )
            jntChild = cmds.joint( rad=3 )
            jntChildP = cmds.listRelatives( jntChild, p=1, f=1 )[0]
        
            sJnts = []
            cmds.select( condObj )
            for i in range( len( splineNodes ) ):
                jnt = cmds.joint( rad=2 )
                sJnts.append( jnt )
            sJntChild = jnt
        
            worldCtl = ns + 'World_CTL'
            allMoc = mocNs + 'All_Moc'
            chestMoc = mocNs + 'Chest_MOC'
            
            mmdc = cmds.createNode( 'multMatrixDecompose' )
            cmds.connectAttr( chestMoc + '.wm', mmdc + '.i[0]' )
            cmds.connectAttr( allMoc + '.wim', mmdc + '.i[1]' )
            cmds.connectAttr( worldCtl + '.wm', mmdc + '.i[2]' )
            cmds.connectAttr( jntChildP + '.wim', mmdc + '.i[3]' )
            
            rootMoc = mocNs + 'Root_MOC'
            mmdcForTr = cmds.createNode( 'multMatrixDecompose' )
            cmds.connectAttr( chestMoc + '.wm', mmdcForTr + '.i[0]' )
            cmds.connectAttr( rootMoc + '.wim', mmdcForTr + '.i[1]' )
            cmds.connectAttr( splineRoot + '.wm',  mmdcForTr + '.i[2]' )
            cmds.connectAttr( sJntChild + '.wim',  mmdcForTr + '.i[3]' )
            
            
            sm = cmds.createNode( 'smartOrient' )
            multNode = cmds.createNode( 'multiplyDivide' )
            cmds.connectAttr( jntChild+'.matrix', sm + '.inputMatrix' )
            cmds.setAttr( sm + '.aimAxis', 1 )
            cmds.connectAttr( sm + '.outAngle', multNode + '.input1' )
            cmds.setAttr( multNode + '.input2', .3333, .3333, .3333 )
            
            root = copy.copy( torsoRot )
            for i in range( len( splineNodes ) ):
                mmdcSpline = cmds.createNode( 'multMatrixDecompose' )
                cmds.connectAttr( splineNodes[i] + '.wm', mmdcSpline + '.i[0]' )
                cmds.connectAttr( root + '.wim', mmdcSpline + '.i[1]' )
                cmds.connectAttr( mmdcSpline + '.ot', jnts[i] + '.t' )
                cmds.connectAttr( mmdcSpline + '.or', jnts[i] + '.jo' )
                cmds.connectAttr( mmdcSpline + '.ot', sJnts[i] + '.t' )
                cmds.connectAttr( mmdcSpline + '.or', sJnts[i] + '.jo' )
                srcCon = cmds.listConnections( conedJnts[i] + '.r', p=1 )
                if srcCon:
                    cmds.connectAttr( multNode+'.output', sJnts[i] + '.r' )
                root = copy.copy( splineNodes[i] )
            
            cmds.connectAttr( mmdc + '.or', jntChild + '.r' )
            cmds.connectAttr( mmdc + '.or', chestCtl + '.r' )
            cmds.connectAttr( mmdcForTr + '.ot', chestCtl + '.t' )
            
            cmds.parent( condObj, allMoc )
            cmds.setAttr( condObj + '.v', 0 )


        def connect( cuMoc, cuCtl, p_cuMoc, p_cuCtl ):
            
            cuCtlP = cmds.listRelatives( cuCtl, p=1 )[0]
                    
            mmDcmp = cmds.createNode( 'multMatrixDecompose', n=cuCtl+'_mmDcmp' )
    
            cmds.connectAttr( cuMoc+'.wm', mmDcmp+'.i[0]' )
            cmds.connectAttr( p_cuMoc+'.wim', mmDcmp+'.i[1]' )
            cmds.connectAttr( p_cuCtl+'.wm', mmDcmp+'.i[2]' )
            cmds.connectAttr( cuCtlP+'.wim', mmDcmp+'.i[3]' )
            
            if cuCtl.find( 'Chest_CTL' ) != -1:
                chestConnect( cuCtl, allMoc.replace( 'All_Moc', '' ) )
            elif cuCtl.find( 'ChestMove_CTL' ) != -1:
                pass
            else:
                rigbase.tryConnect( mmDcmp+'.otx', cuCtl+'.tx' )
                rigbase.tryConnect( mmDcmp+'.oty', cuCtl+'.ty' )
                rigbase.tryConnect( mmDcmp+'.otz', cuCtl+'.tz' )
            
                if cmds.nodeType( cuCtl ) == 'joint':
                    joMmDcmp = cmds.createNode( 'multMatrixDecompose', n=cuCtl+'.joMmDcmp' )
                    
                    cmds.connectAttr( cuMoc+'.wm', joMmDcmp+'.i[0]' )
                    cmds.connectAttr( allMoc+'.wim', joMmDcmp+'.i[1]' )
                    cmds.connectAttr( worldCtl+'.wm', joMmDcmp+'.i[2]' )
                    cmds.connectAttr( cuCtlP+'.wim', joMmDcmp+'.i[3]' )
                        
                    compose = cmds.createNode( 'composeMatrix', n=cuCtl+'_compose' )
                    inv     = cmds.createNode( 'inverseMatrix', n=cuCtl+'_invMtx')
                    joCon   = cmds.listConnections( cuCtl+'.jo', s=1, d=0, p=1, c=1 )[1]
                    
                    cmds.connectAttr( joCon, compose+'.ir' )
                    cmds.connectAttr( compose+'.outputMatrix', inv+'.inputMatrix' )
                    cmds.connectAttr( inv+'.outputMatrix', joMmDcmp+'.i[4]' )
                    
                    rigbase.tryConnect( joMmDcmp+'.orx', cuCtl+'.rx' )
                    rigbase.tryConnect( joMmDcmp+'.ory', cuCtl+'.ry' )
                    rigbase.tryConnect( joMmDcmp+'.orz', cuCtl+'.rz' )
                else:
                    rigbase.tryConnect( mmDcmp+'.orx', cuCtl+'.rx' )
                    rigbase.tryConnect( mmDcmp+'.ory', cuCtl+'.ry' )
                    rigbase.tryConnect( mmDcmp+'.orz', cuCtl+'.rz' )



        mocNamespace = allMoc.replace( 'All_Moc', '' )
        ctlNamespace = worldCtl.replace( 'World_CTL', '' )
        
        for item in self.moc_getCtls_items:
            
            if item[0] == 'All_Moc': continue
            
            moc = mocNamespace + item[0]
            p_moc = mocNamespace + self.moc_getParent_dict[ item[0] ]
            
            for target in item[1]:
                p_target = self.ctl_getParent_dict[ target ]
                
                target = ctlNamespace + target
                p_target = ctlNamespace + p_target
                
                if moc.find( '_SIDE_' ) != -1:
                    for side in ['L', 'R']:
                        cuMoc = moc.replace( 'SIDE', side )
                        p_cuMoc = p_moc.replace( 'SIDE', side )
                        cuCtl = target.replace( 'SIDE', side )
                        p_cuCtl = p_target.replace( 'SIDE', side )
                        connect( cuMoc, cuCtl, p_cuMoc, p_cuCtl )
                else:
                    cuMoc = moc
                    cuCtl = target
                    connect( cuMoc, cuCtl, p_moc, p_target )
        
        for item in self.moc_getIkCtl_items:
            
            moc = mocNamespace + item[0]
            p_moc, target = item[1]
            p_moc = mocNamespace + p_moc
            
            p_target = self.ctl_getParent_dict[ target ]
            
            target = ctlNamespace + target
            p_target = ctlNamespace + p_target
            
            for side in ['L', 'R']:
                cuMoc = moc.replace( 'SIDE', side )
                p_cuMoc = p_moc.replace( 'SIDE', side )
                cuCtl = target.replace( 'SIDE', side )
                p_cuCtl = p_target.replace( 'SIDE', side )
                connect( cuMoc, cuCtl, p_cuMoc, p_cuCtl )
            
        
        
        for item in self.poleVCtl_getMoc_items:
            
            cuCtl = ctlNamespace + item[0]
            cuCtlP = cmds.listRelatives( cuCtl, p=1 )[0]
            
            upper, direction = item[1]
            upper = mocNamespace + upper
            middle = cmds.listRelatives( upper, c=1 )[0]
            lower = cmds.listRelatives( middle, c=1 )[0]
            
            mixDcmp   = cmds.createNode( 'blendTwoMatrixDecompose', n=cuCtl+'_mixMtx' )
            upperDcmp = cmds.createNode( 'multMatrixDecompose', n= cuCtl+'_Upper_dcmp' )
            middleDcmp = cmds.createNode( 'multMatrixDecompose', n= cuCtl+'_middle_dcmp' )
            lowerDcmp = cmds.createNode( 'multMatrixDecompose', n= cuCtl+'_Lower_dcmp' )
            aimVNode =  cmds.createNode( 'plusMinusAverage', n= cuCtl+'_aimV' )
            cmds.setAttr( aimVNode+'.op', 2 )
            
            cmds.connectAttr( upper+'.wm', mixDcmp+'.inMatrix1' )
            cmds.connectAttr( lower+'.wm', mixDcmp+'.inMatrix2' )
            cmds.connectAttr( upper+'.wm', upperDcmp+'.i[0]' )
            cmds.connectAttr( allMoc+'.wim', upperDcmp+'.i[1]' )
            cmds.connectAttr( middle+'.wm', middleDcmp+'.i[0]' )
            cmds.connectAttr( allMoc+'.wim', middleDcmp+'.i[1]' )
            cmds.connectAttr( lower+'.wm', lowerDcmp+'.i[0]' )
            cmds.connectAttr( allMoc+'.wim', lowerDcmp+'.i[1]' )
            
            cmds.connectAttr( lowerDcmp+'.ot', aimVNode+'.input3D[0]' )
            cmds.connectAttr( upperDcmp+'.ot', aimVNode+'.input3D[1]' )
            
            upVNode = cmds.createNode( 'matrixToThreeByThree', n=cuCtl+'_upV' )
            cmds.connectAttr( upper+'.wm', upVNode+'.inMatrix' )
            
            byNormalNode = cmds.createNode( 'vectorProduct', n= cuCtl+'_byNormal' )
            cmds.setAttr( byNormalNode+'.op', 2 )
            cmds.setAttr( byNormalNode+'.normalizeOutput', 1 )
            
            if direction == 1:
                cmds.connectAttr( aimVNode+'.output3D', byNormalNode+'.input1' )
                cmds.connectAttr( upVNode+'.out10', byNormalNode+'.input2X' )
                cmds.connectAttr( upVNode+'.out11', byNormalNode+'.input2Y' )
                cmds.connectAttr( upVNode+'.out12', byNormalNode+'.input2Z' )
            else:
                cmds.connectAttr( aimVNode+'.output3D', byNormalNode+'.input2' )
                cmds.connectAttr( upVNode+'.out10', byNormalNode+'.input1X' )
                cmds.connectAttr( upVNode+'.out11', byNormalNode+'.input1Y' )
                cmds.connectAttr( upVNode+'.out12', byNormalNode+'.input1Z' )
            
            multByNormal = cmds.createNode( 'multiplyDivide', n= cuCtl+'_multByNormal' )
            upperDist = cmds.createNode( 'distanceBetween', n=cuCtl+'_upperDist' )
            lowerDist = cmds.createNode( 'distanceBetween', n=cuCtl+'_lowerDist' )
            cmds.connectAttr( upper+'.wm', upperDist+'.inMatrix1' )
            cmds.connectAttr( middle+'.wm', upperDist+'.inMatrix2' )
            cmds.connectAttr( middle+'.wm', lowerDist+'.inMatrix1' )
            cmds.connectAttr( lower+'.wm', lowerDist+'.inMatrix2' )
            
            distAverage = cmds.createNode( 'plusMinusAverage', n=cuCtl+'_distAverage' )
            cmds.setAttr( distAverage+'.op', 3 )
            
            cmds.connectAttr( upperDist+'.distance', distAverage+'.input1D[0]' )
            cmds.connectAttr( lowerDist+'.distance', distAverage+'.input1D[1]' )
            
            cmds.connectAttr( byNormalNode+'.output', multByNormal+'.input1' )
            cmds.connectAttr( distAverage+'.output1D', multByNormal+'.input2X' )
            cmds.connectAttr( distAverage+'.output1D', multByNormal+'.input2Y' )
            cmds.connectAttr( distAverage+'.output1D', multByNormal+'.input2Z' )
            
            poleVWorld = cmds.createNode( 'plusMinusAverage', n= cuCtl+'_poleVWorld' )
            poleVWorldCompose = cmds.createNode( 'composeMatrix', n= cuCtl+'_poleVWorldCompose' )
            
            cmds.connectAttr( middleDcmp+'.ot', poleVWorld+'.input3D[0]' )
            cmds.connectAttr( multByNormal+'.output', poleVWorld+'.input3D[1]' )
            
            cmds.connectAttr( poleVWorld+'.output3D', poleVWorldCompose+'.it' )
            
            mmDcmp = cmds.createNode( 'multMatrixDecompose', n=cuCtl+'_mmDcmp' )
            
            cmds.connectAttr( poleVWorldCompose+'.outputMatrix', mmDcmp+'.i[0]' )
            cmds.connectAttr( worldCtl+'.wm', mmDcmp+'.i[1]' )
            cmds.connectAttr( cuCtlP+'.wim', mmDcmp+'.i[2]' )
            
            cmds.connectAttr( mmDcmp+'.otx', cuCtl+'.tx' )
            cmds.connectAttr( mmDcmp+'.oty', cuCtl+'.ty' )
            cmds.connectAttr( mmDcmp+'.otz', cuCtl+'.tz' )


            
    def disconnectMocapJoint_old(self, worldCtl, *args ):
        initNamespace = worldCtl.replace( 'World_CTL', '' )
        
        rootInit = initNamespace + 'Root_Init'
        dcmp = cmds.listConnections( rootInit+'.rx', type='multMatrixDecompose' )[0]
        
        rootMoc = cmds.listConnections( dcmp+'.i[0]', s=1, d=0 )[0]
        
        mocNamespace = rootMoc.replace( 'Root_MOC', '' )
        
        interpoleMocs = [ 'Shoulder_L_MocAfter','Shoulder_R_MocAfter', 'Hip_L_MocAfter', 'Hip_R_MocAfter' ]
        
        mocs = cmds.ls( mocNamespace+'*_MOC' )
        
        for moc in mocs:
            dcmp = moc.replace( '_MOC', '_MocDmcp' )
            cmds.delete( dcmp )
        
        for moc in interpoleMocs:
            topMoc = mocNamespace + moc
            topMocAf = topMoc.replace( '_MOC', '_MocAfter' )
            cmds.delete( topMocAf )
        
        cmds.delete( mocNamespace+'*MocOffsetGrp' )
        
        
    def disconnectMocapJoint(self, worldCtl, *args ):
        namespace = worldCtl.replace( "World_CTL", '' )
        
        allCtls = cmds.ls( namespace+'*_CTL', tr=1 )
        
        mmdcs = []
        for ctl in allCtls:
            mmdc = cmds.listConnections( ctl, s=1, d=0, type='multMatrixDecompose' )
            if cmds.nodeType( ctl ) == 'joint':
                mmdcCons = cmds.listConnections( ctl + '.jo', s=1, d=0 )
                if not mmdcCons: mmdcCons = []
                for mmdcCon in mmdcCons:
                    mmdc.remove( mmdcCon )
            if mmdc:
                mmdcs += mmdc
                
        if mmdcs:
            cmds.delete( mmdcs )
        
         
        

class All_Moc():
    def createCharacter(self, target, *args ):
        self.humanIkPos(target)
        self.setHumanIk(target)
        self.addHumanIkAttribute(target)
        
    def humanIkPos(self, target, *args ):
        namespace = target.replace( 'All_Moc', '' )
        
        shoulderLMtx = [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]
        shoulderRMtx = [1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 1.0]
        hipLMtx = [0.0, -1.0, -0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]
        hipRMtx = [0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 1.0]
        
        shoulderL_moc = namespace + 'Shoulder_L_MOC'
        shoulderR_moc = namespace + 'Shoulder_R_MOC'
        hipL_moc = namespace + 'Hip_L_MOC'
        hipR_moc = namespace + 'Hip_R_MOC'
        
        shoulderLPos = cmds.xform( shoulderL_moc, q=1, ws=1, t=1 )[:3]
        shoulderLMtx[12] = shoulderLPos[0]
        shoulderLMtx[13] = shoulderLPos[1]
        shoulderLMtx[14] = shoulderLPos[2]
        
        shoulderRPos = cmds.xform( shoulderR_moc, q=1, ws=1, t=1 )[:3]
        shoulderRMtx[12] = shoulderRPos[0]
        shoulderRMtx[13] = shoulderRPos[1]
        shoulderRMtx[14] = shoulderRPos[2]
        
        hipLPos = cmds.xform( hipL_moc, q=1, ws=1, t=1 )[:3]
        hipLMtx[12] = hipLPos[0]
        hipLMtx[13] = hipLPos[1]
        hipLMtx[14] = hipLPos[2]
        
        hipRPos = cmds.xform( hipR_moc, q=1, ws=1, t=1 )[:3]
        hipRMtx[12] = hipRPos[0]
        hipRMtx[13] = hipRPos[1]
        hipRMtx[14] = hipRPos[2]
        
        mocList = [shoulderL_moc, shoulderR_moc, hipL_moc, hipR_moc ]
        mtxList = [shoulderLMtx, shoulderRMtx, hipLMtx, hipRMtx ]
        
        for i in range( len( mocList ) ):
            direction = 0.5
            if mocList[i].find( 'Shoulder' ) != -1:
                direction = -0.5
            
            moc = mocList[i]
            mtx = mtxList[i]
            
            mocChild0 = cmds.listRelatives( moc, c=1 )[0]
            mocChild1 = cmds.listRelatives( mocChild0, c=1 )[0]
            
            cmds.setAttr( mocChild0+'.jo', 0,0,0 )
            cmds.setAttr( mocChild1+'.jo', 0,0,0 )
            cmds.setAttr( mocChild0+'.pa', 0,direction,0 )
            
            cmds.xform( moc, ws=1, matrix=mtx )
            rValue = cmds.getAttr( moc+'.r' )[0]
            cmds.setAttr( moc+'.jo', *rValue )
            
        mocs = cmds.ls( namespace+'*_MOC' )
        for moc in mocs:
            cmds.setAttr( moc+'.r', 0,0,0 )
            
    def setHumanIk(self, target, *args ):
        namespace = target.replace( 'All_Moc', '' )
        
        properState = cmds.createNode( 'HIKProperty2State', n = namespace+'HIKproperties' )
        characterNode =   cmds.createNode( 'HIKCharacterNode', n = namespace+'HIKCharacter' )
        
        cmds.connectAttr( properState+'.message', characterNode+'.propertyState' )
        
        def connectCharacter( target, characterNodeAttr ):
            if not cmds.attributeQuery( 'Character', node=namespace+target, ex=1 ):
                cmds.addAttr( namespace+target, ln='Character', at='message' )
            cmds.connectAttr( namespace+target+'.Character', characterNode+'.'+characterNodeAttr )
            
        connectCharacter( 'All_Moc', 'Reference' )
        connectCharacter( 'Ankle_R_MOC', 'RightFoot' )
        connectCharacter( 'Ankle_L_MOC', 'LeftFoot' )
        connectCharacter( 'Knee_R_MOC', 'RightLeg' )
        connectCharacter( 'Knee_L_MOC', 'LeftLeg' )
        connectCharacter( 'Hip_R_MOC', 'RightUpLeg' )
        connectCharacter( 'Hip_L_MOC', 'LeftUpLeg' )
        connectCharacter( 'Collar_R_MOC', 'RightShoulder' )
        connectCharacter( 'Collar_L_MOC', 'LeftShoulder' )
        connectCharacter( 'Chest_MOC', 'Spine4' )
        connectCharacter( 'Chest_MOCSep', 'Spine3' )
        connectCharacter( 'Waist_MOC', 'Spine2' )
        connectCharacter( 'Root_MOCSep', 'Spine1' )
        connectCharacter( 'Root_MOC', 'Hips' )
        connectCharacter( 'Root_MOCPiv', 'Spine' )
        connectCharacter( 'NeckMiddle_MOC', 'Neck1' )
        connectCharacter( 'Neck_MOC', 'Neck' )
        connectCharacter( 'Head_MOC', 'Head' )
        connectCharacter( 'Wrist_R_MOC', 'RightHand' )
        connectCharacter( 'Wrist_L_MOC', 'LeftHand' )
        connectCharacter( 'Elbow_R_MOC', 'RightForeArm' )
        connectCharacter( 'Elbow_L_MOC', 'LeftForeArm' )
        connectCharacter( 'Shoulder_R_MOC', 'RightArm' )
        connectCharacter( 'Shoulder_L_MOC', 'LeftArm' )
        
    def addHumanIkAttribute( self, target, *args ):
        namespace = target.replace( 'All_Moc', '' )
        
        allMoc = namespace+'All_Moc'
        properties = namespace +'HIKproperties'
        attrNameList = ['ikBlendT', 'ikBlendR', 'ikPull' ]
        
        def addControler( target, targetAttrList, **options ):
            hik = rigbase.Controler( n=target.replace( 'MOC', 'HIK' ) )
            hik.setShape( **options )
            hik.setParent( allMoc )
            
            rigbase.constraint( target, hik.transformGrp )
            
            attrEdit = rigbase.AttrEdit( hik.name )
            attrEdit.lockAndHideAttrs( 'tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v' )
            for targetAttr in targetAttrList:
                index = targetAttrList.index( targetAttr )
                if not targetAttr: continue
                attrEdit.addAttr( ln=attrNameList[ index ], min=0, max=1, k=1 )
                cmds.connectAttr( hik +'.'+ attrNameList[index], properties+'.'+targetAttr )
        
        wristL = namespace+'Wrist_L_MOC'
        wristR = namespace+'Wrist_R_MOC'
        elbowL = namespace+'Elbow_L_MOC'
        elbowR = namespace+'Elbow_R_MOC'
        ankleL = namespace+'Ankle_L_MOC'
        ankleR = namespace+'Ankle_R_MOC'
        kneeL  = namespace+'Knee_L_MOC'
        kneeR  = namespace+'Knee_R_MOC'
        Root   = namespace+'Root_MOC'
        Chest  = namespace+'Chest_MOC'
        Head   = namespace+'Head_MOC'
        
        bbMinP = om.MPoint( *cmds.getAttr( target+'.boundingBoxMin' )[0] )
        bbMaxP = om.MPoint( *cmds.getAttr( target+'.boundingBoxMax' )[0] )
        
        rad = bbMinP.distanceTo( bbMaxP )*0.03
        
        addControler( wristL, ['ReachActorLeftWrist','ReachActorLeftWristRotation','CtrlChestPullLeftHand'], normal=[1,0,0], radius=rad )
        addControler( wristR, ['ReachActorRightWrist','ReachActorRightWristRotation','CtrlChestPullRightHand'], normal=[1,0,0], radius=rad )
        addControler( elbowL, ['ReachActorLeftElbow','','CtrlPullLeftElbow'], normal=[1,0,0], radius=rad )
        addControler( elbowR, ['ReachActorRightElbow','','CtrlPullRightElbow'], normal=[1,0,0], radius=rad )
        addControler( ankleL, ['ReachActorLeftAnkle','ReachActorLeftAnkleRotationRotation','CtrlPullLeftFoot'], normal=[1,0,0], radius=rad )
        addControler( ankleR, ['ReachActorRightAnkle','ReachActorRightAnkleRotation','CtrlPullRightFoot'], normal=[1,0,0], radius=rad )
        addControler( kneeL, ['ReachActorLeftKnee','','CtrlPullLeftKnee'], normal=[1,0,0], radius=rad )
        addControler( kneeR, ['ReachActorRightKnee','','CtrlPullRightKnee'], normal=[1,0,0], radius=rad )
        addControler( Root, ['','ReachActorLowerChestRotation','CtrlResistHipsPosition'], normal=[0,1,0], radius=rad )
        addControler( Chest, ['ReachActorChest','ReachActorChestRotation','CtrlResistChestPosition'], normal=[0,1,0], radius=rad )
        addControler( Head, ['','ReachActorHeadRotation',''], normal=[0,1,0], radius=rad )
        
        
    def isHIKCharacter(self, target ):
        
        if not cmds.attributeQuery( 'Character', node=target, ex=1 ): return False
        
        cons = cmds.listConnections( target+'.Character', type='HIKCharacterNode' )
        
        if not cons: return False
        
        return True
    
    
    def removeHumanIkCharacter(self, target, *args ):
        
        if not cmds.attributeQuery( 'Character', node=target, ex=1 ): return None
        
        cons = cmds.listConnections( target+'.Character', type='HIKCharacterNode' )
        
        if not cons: return None
        
        targetChildren = cmds.listRelatives( target, c=1 )
        
        for child in targetChildren:
            if child[-7:] == 'HIK_GRP':
                cons.append( child )
        
        cmds.delete( cons )
        
        
        
    def isMatchSource( self, target ):
        retargeterNode = cmds.listConnections( target+'.worldMatrix', type='HIKRetargeterNode')[0]
        propertyNode = cmds.listConnections( retargeterNode, s=1, d=0, type='HIKProperty2State' )[0]
        
        if cmds.getAttr( propertyNode+'.ForceActorSpace' ):
            return True
        else:
            return False
        
        
    def setMatchSource(self, target, *args ):
        retargeterNode = cmds.listConnections( target+'.worldMatrix', type='HIKRetargeterNode')[0]
        propertyNode = cmds.listConnections( retargeterNode, s=1, d=0, type='HIKProperty2State' )[0]
        
        cmds.setAttr( propertyNode+'.ForceActorSpace', 1 )
        
    def setNotMatchSource(self, target, *args ):
        retargeterNode = cmds.listConnections( target+'.worldMatrix', type='HIKRetargeterNode')[0]
        propertyNode = cmds.listConnections( retargeterNode, s=1, d=0, type='HIKProperty2State' )[0]
        
        cmds.setAttr( propertyNode+'.ForceActorSpace', 0 )
        
        
    def exportHIk(self, target, *args ):
        
        filePath = cmds.fileDialog2( fm= 0 )[0]
        
        hIkNode = cmds.listConnections( target+'.Character' )[0]
        
        hIkSources = cmds.listConnections( hIkNode, s=1, d=0 )
        
        HIKCtlPs = []
        for source in hIkSources:
            if cmds.nodeType( source ) == 'HIKProperty2State':
                cons = cmds.listConnections( source, s=1, d=0, c=1, p=1 )                
                outputs = cons[1::2]
                inputs  = cons[::2]
                
                for i in range( len( outputs ) ):
                    cmds.disconnectAttr( outputs[i], inputs[i] )
                    node = outputs[i].split( '.' )[0]
                    nodeP = cmds.listRelatives( node, p=1 )[0]
                    HIKCtlPs.append( nodeP )
        cmds.parent( HIKCtlPs, w=1 )
                    
        targetNS = target.replace( "All_Moc", '' )

        mocs = cmds.ls( targetNS+'*_MOC', type='joint' )
        for moc in mocs:
            cmds.rename( moc, moc.replace( "_MOC", "_ExportMoc" ) )

        target = cmds.rename( target, target.replace( 'All_Moc', 'Export_AllMoc' ) )
        
        cmds.select( target, hIkNode )
           
        cmds.file( filePath, force=1, options="v=0;", typ="mayaBinary", pr=1, es=1 )
            
        if os.path.exists( filePath ):
            os.remove( filePath )
        os.rename( filePath+'.mb', filePath )
        
        target = cmds.rename( target, target.replace( 'Export_AllMoc', 'All_Moc' ) )
        mocs = cmds.ls( targetNS+'*_ExportMoc', type='joint' )
        for moc in mocs:
            cmds.rename( moc, moc.replace( "_ExportMoc","_MOC" ) )
            
        for i in range( len( outputs ) ):
            cmds.connectAttr( outputs[i], inputs[i] )
            
        cmds.parent( HIKCtlPs, target )
        
        cmds.select( target )