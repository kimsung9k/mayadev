import maya.cmds as cmds
import chModules.rigbase as rigbase

class RigAll:
    def __init__(self, rigInstance ):
        self.rigInstance = rigInstance
        
        rigbase.ctlAllScale = reduce( (lambda x,y: x+y), [ s/3 for s in cmds.getAttr( 'All_InitCTL.s' )[0] ] )
        
        self.initAll = cmds.createNode( 'transform', n='All_Init' )
        
        self.rootInit = rigbase.hierarchyCopyConnections( self.rigInstance.torsoInitJnts[0], replaceTarget = '_InitJnt', replace = '_Init' )
        
        cmds.parent( self.rootInit, self.initAll )
        
        rigbase.connectSameAttr( self.rigInstance.initJntsGrp, self.initAll ).doIt( 't', 'r' )
        
        self.rigInstance.rootInit = self.rootInit
        self.rigInstance.initAll = self.initAll
        
    def worldCtlSet(self):
        self.worldCtl, self.worldCtlGrp = rigbase.putControler( self.initAll, n='World_CTL', radius=5, normal=[0,1,0] )
        rigbase.connectSameAttr( self.initAll, self.worldCtlGrp ).doIt( 't', 'r' )
        self.rigInstance.worldCtl = self.worldCtl
        rigbase.controlerSetColor( self.worldCtl , 17 )
        
    def moveCtlSet(self):
        self.moveCtl, self.moveCtlGrp = rigbase.putControler( self.worldCtl, n='Move_CTL', typ='move', size= [2,2,2] )
        cmds.parent( self.moveCtlGrp, self.worldCtl )
        self.rigInstance.moveCtl = self.moveCtl
        rigbase.controlerSetColor( self.moveCtl , 20 )
        rigbase.AttrEdit( self.moveCtl ).lockAndHideAttrs( 'sx', 'sy', 'sz', 'v' )
        
    def allSet(self):
        self.worldCtlSet()
        self.moveCtlSet()