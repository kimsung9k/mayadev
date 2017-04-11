import maya.cmds as cmds
import maya.OpenMaya as om
import maya.mel as mel
from chModules import rigbase
from chModules.ctls.ctlsAll import * 


class MocSet( CtlsAll ):
    def __init__(self, target, withSkin = False ):
        self.namespace = self.getNamespace(target)
        self.allInit = self.namespace + 'All_Init'
        
        #self.getPanelCondition()
        #self.setPanelWireframe()
        
        cmds.refresh()
        self.mocSet()
        self.splineDriverMocSet()
        if withSkin:
            self.copySkinedMesh()
        
        #self.setPanelOriginal()
        
        cmds.select( self.allMoc )
        
    def mocSet(self):
        allMoc = cmds.spaceLocator( n=self.allInit.replace( '_Init', '_Moc' ) )[0]
        rigbase.setColor( allMoc, 27 )
        
        rigbase.connectSameAttr( self.allInit, allMoc ).doIt( 't', 'r', 's' )
        
        self.allMoc = allMoc
        
        rootInit = cmds.listRelatives( self.allInit, c=1 )[0]
        
        rootMoc = rigbase.hierarchyCopyConnections( rootInit, typ='joint', replaceTarget='_Init', replace='_MOC', t=1, r=1, s=0 )
        cmds.parent( rootMoc, self.allMoc )
        
        cmds.delete( self.namespace+'Heel_*_MOC', self.namespace+'*PoleV_*_MOC', self.namespace+'EyeAimPiv_MOC', self.namespace+'Upper*_*_MOC_GRP', self.namespace+'Lower*_*_MOC_GRP' )
        
        allMocChildren = cmds.listRelatives( self.allMoc, c=1, ad=1, type='transform' )
        allMocChildren.append( self.allMoc )
        
        for moc in allMocChildren:
            cons = cmds.listConnections( moc, s=1, d=0, c=1, p=1 )
            
            outputs = cons[1::2]
            inputs  = cons[::2]
            
            for i in range( len( outputs ) ):
                cmds.disconnectAttr( outputs[i], inputs[i] )
        
        cmds.makeIdentity( self.allMoc, t=0, r=1, s=0, n=0, apply=1 )
        
        self.rootMoc = rootMoc
        self.allMoc = allMoc
        
    def splineDriverMocSet(self):
        chestMoc = self.namespace+'Chest_MOC'
        waistMoc = self.namespace+'Waist_MOC'
        rootMoc  = self.namespace+'Root_MOC'
        
        cmds.select( waistMoc )
        cmds.joint( e=1, oj='yzx', sao='zup' )
        chestMocSep = cmds.joint( n=chestMoc.replace( 'MOC', 'MOCSep' ) )
        cmds.setAttr( chestMocSep+'.ty', cmds.getAttr( chestMoc+'.ty')/2 )
        cmds.parent( chestMoc, chestMocSep )
        
        cmds.select( rootMoc )
        rootMocPiv = cmds.joint( n=rootMoc.replace( 'MOC', 'MOCPiv' ) )
        cmds.parent( waistMoc, rootMocPiv )
        cmds.select( rootMocPiv )
        cmds.joint( e=1, oj='yzx', sao='zup' )
        
        rootMocSep = cmds.joint( n=rootMoc.replace( 'MOC', 'MOCSep' ) )
        cmds.setAttr( rootMocSep+'.ty', cmds.getAttr( waistMoc+'.ty')/2 )
        cmds.parent( waistMoc, rootMocSep )
        
        rootMocPivChild = cmds.listRelatives( rootMocPiv, c=1, f=1 )[0]
        pos = cmds.getAttr( rootMocPivChild+'.wm' )
        cmds.setAttr( rootMocPiv+'.jo', 0,0,0 )
        cmds.xform( rootMocPivChild, ws=1, matrix= pos )


    def copySkinedMesh(self):
        
        rootRjt = self.namespace+'Spline0_RJT'
        rootBjtCheck = cmds.listConnections( rootRjt+'.r', s=0, d=1, type='joint' )
        
        if not rootBjtCheck:
            return None
        rootBjt = rootBjtCheck[0]
        bjts = cmds.listRelatives( rootBjt, c=1, ad=1 )
        bjts.append( rootBjt )
        meshs = rigbase.getSkinedMeshByJnt( bjts )
        duMeshs = []
        
        neadJnts= cmds.ls( self.namespace+'*_MOC*', type='joint' )
        
        for neadJnt in neadJnts:
            self.moveToParentPoseLittle( neadJnt )
        
        for mesh in meshs:
            meshSkinCl = rigbase.getHistory( mesh, 'skinCluster' )[0]
            
            cmds.setAttr( meshSkinCl+'.envelope', 0 )
            duMesh = cmds.duplicate( mesh )[0]
            duMeshs.append( duMesh )
            rigbase.cleanMesh( duMesh )
            
            bindObjs = []
            bindObjs += neadJnts
            bindObjs.append( duMesh )
            cmds.skinCluster( bindObjs, mi=3, tsb=1 )
            cmds.setAttr( meshSkinCl+'.envelope', 1 )
        
        cmds.undoInfo( swf=0 )
        if duMeshs:
            cmds.select( duMeshs )
            mel.eval( 'removeUnusedInfluences' )
            for i in range( len( meshs ) ):
                cmds.copySkinWeights( meshs[i], duMeshs[i], noMirror=1, sa='closestPoint', ia='closestBone', normalize=1 )
        cmds.undoInfo( swf=1 )
        try:
            cmds.parent( cmds.group( duMeshs, n='MocMesh_GRP'), w=1 )
            mel.eval( "sets -e -forceElement initialShadingGroup;" )
            cmds.select( duMeshs )
        except: pass
        
    
    def moveToParentPoseLittle( self, target ):
        targetP = cmds.listRelatives( target, p=1 )[0]
        
        targetPose = om.MVector( *cmds.xform( target, q=1, ws=1, t=1 )[:3] )
        targetPPose = om.MVector( *cmds.xform( targetP, q=1, ws=1, t=1 )[:3] )
        
        pVector = targetPPose - targetPose
        
        cuPose = targetPose + pVector*0.001
        
        cmds.move( cuPose.x, cuPose.y, cuPose.z, target, ws=1, rpr=1 )
        

    def getPanelCondition(self):      
        currentPanel = cmds.getPanel( underPointer=1 )
        
        if not currentPanel:
            currentPanel = cmds.getPanel( withFocus=1 )
        
        if currentPanel:
            panelType = cmds.getPanel( typeOf=currentPanel )
            if panelType == 'modelPanel':
                panelCondition = cmds.modelEditor( currentPanel, q=1, displayAppearance=1 )
        
        self._panelCondition = ''
        
        try: self._panelCondition = panelCondition
        except: pass

        
    def setPanelWireframe(self):
        currentPanel = cmds.getPanel( underPointer=1 )
        
        if not currentPanel:
            currentPanel = cmds.getPanel( withFocus=1 )
            
        if currentPanel:
            panelType = cmds.getPanel( typeOf=currentPanel )
            if panelType == 'modelPanel':
                cmds.modelEditor( currentPanel, e=1, displayAppearance="wireframe" )
                
                
    def setPanelOriginal(self):
        currentPanel = cmds.getPanel( underPointer=1 )
        
        if not currentPanel:
            currentPanel = cmds.getPanel( withFocus=1 )
            
        if currentPanel:
            panelType = cmds.getPanel( typeOf=currentPanel )
            if panelType == 'modelPanel':
                cmds.modelEditor( currentPanel, e=1, displayAppearance=self._panelCondition )