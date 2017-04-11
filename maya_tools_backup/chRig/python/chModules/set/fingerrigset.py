import maya.cmds as cmds
import chModules.rigbase as rigbase

class CtlSet:
    def __init__(self):
        pass
            
    def create(self, inits, grp, colorIndex ):
        parentTarget = grp
        self.ctls = []
        for init in inits:
            ctl = rigbase.Controler( n=init.replace( 'Init', 'CTL' ) )
            rigbase.AttrEdit( ctl ).lockAndHideAttrs( 'sx', 'sy', 'sz', 'v' )
            rigbase.connectSameAttr( init, ctl.transformGrp ).doIt( 't', 'r' )
            ctl.setShape( typ='box', size=[.1,.1,.1] )
            ctl.setColor( colorIndex )
            ctl.setParent( parentTarget )
            parentTarget = ctl
            self.ctls.append( ctl )
            
class AimObjectSet:
    def __init__(self):
        pass
    
    def create(self, ctls ):
        inverse = False
        if ctls[0].name.find( '_R_' ) != -1:
            inverse = True
        
        self.aimObjs = []
        for i in range( len( ctls )-1 ):
            base = ctls[i].name
            aimTarget = ctls[i+1].name
            aimObj, childDcmp = rigbase.makeAimObject( aimTarget, base, inverseAim=inverse )
            self.aimObjs.append( aimObj )
            
class JointSet:
    def __init__(self):
        pass
    
    def create(self, inits, ctls, aimObjs, parentTarget ):
        cmds.select( parentTarget )
        
        jnts = []
        for init in inits:
            jnt = cmds.joint( n=init.replace( 'Init', 'RJT' ), radius=.5 )
            jnts.append( jnt )
            
        rigbase.connectSameAttr( inits[-1], jnt ).doIt( 't', 'r' )
        
        for i in range( len( aimObjs ) ):
            aimObj = aimObjs[i]
            jnt = jnts[i]
            rigbase.constraint( aimObj, jnt )
            
        rigbase.constraint( ctls[-1], jnts[-2] )
            
class RigAll:
    def __init__(self, rigInstance ):
        self.fingerLInits = rigInstance.fingerLInits
        self.fingerRInits = rigInstance.fingerRInits
        self.handLConst = rigInstance.handLConst
        self.handRConst = rigInstance.handRConst
        self.handLRjt = rigInstance.handLRjt
        self.handRRjt = rigInstance.handRRjt
        self.rootGrp = rigInstance.rootGrp
        self.switchLCtl = rigInstance.armLSwitchCtl
        self.switchRCtl = rigInstance.armRSwitchCtl
        
        self.ctlSet = CtlSet()
        self.aimObjSet = AimObjectSet()
        self.jointSet = JointSet()
        
    def allSet(self):
        colorLIndexList = [ 21, 20, 4, 15, 18 ]
        colorRIndexList = [ 21, 20, 4, 15, 18 ]
        
        def createScaleNode( switchCtl ):
            scaleNode = cmds.createNode( 'multiplyDivide', n=switchCtl+'_handScale' )
            cmds.setAttr( scaleNode+'.op', 3 )
            cmds.connectAttr( switchCtl+'.handScale', scaleNode+'.input2X' )
            cmds.connectAttr( switchCtl+'.handScale', scaleNode+'.input2Y' )
            cmds.connectAttr( switchCtl+'.handScale', scaleNode+'.input2Z' )
            cmds.setAttr( scaleNode+'.input1X', 2 )
            cmds.setAttr( scaleNode+'.input1Y', 2 )
            cmds.setAttr( scaleNode+'.input1Z', 2 )
            return scaleNode
        
        handLGrp = rigbase.Transform( n='Hand_L_CTL_GRP' )
        rigbase.constraint( self.handLConst, handLGrp )
        cmds.connectAttr( self.switchLCtl+'.fingerCtl', handLGrp+'.v' )
        
        handRGrp = rigbase.Transform( n='Hand_R_CTL_GRP' )
        rigbase.constraint( self.handRConst, handRGrp )
        cmds.connectAttr( self.switchRCtl+'.fingerCtl', handRGrp+'.v' )
        
        handLGrp.setParent( self.rootGrp )
        handRGrp.setParent( self.rootGrp )
        
        for inits in self.fingerLInits:
            self.ctlSet.create( inits[:-1], handLGrp, colorLIndexList.pop(0) )
            self.aimObjSet.create( self.ctlSet.ctls )
            self.jointSet.create( inits, self.ctlSet.ctls, self.aimObjSet.aimObjs, self.handLRjt )
            
        for inits in self.fingerRInits:
            self.ctlSet.create( inits[:-1], handRGrp, colorRIndexList.pop(0) )
            self.aimObjSet.create( self.ctlSet.ctls )
            self.jointSet.create( inits, self.ctlSet.ctls, self.aimObjSet.aimObjs, self.handRRjt )
        
        scaleNode = createScaleNode( self.switchLCtl )
        cmds.connectAttr( scaleNode+'.output', handLGrp+'.s' )
        cmds.connectAttr( scaleNode+'.output', self.handLRjt+'.s', f=1 )
        
        children = cmds.listRelatives( self.handLRjt, c=1, type='joint' )
        for child in children:
            cmds.setAttr( child+'.ssc', False )
            
        scaleNode = createScaleNode( self.switchRCtl )
        cmds.connectAttr( scaleNode+'.output', handRGrp+'.s' )
        cmds.connectAttr( scaleNode+'.output', self.handRRjt+'.s', f=1 )
            
        children = cmds.listRelatives( self.handRRjt, c=1, type='joint' )
        for child in children:
            cmds.setAttr( child+'.ssc', False )