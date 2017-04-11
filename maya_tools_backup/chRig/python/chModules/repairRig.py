import maya.cmds as cmds
import rigbase

class repair:
    def __init__(self):
        self.imInitCtls = cmds.ls( 'im_*_InitCTL', type='transform' )
        self.imCtls = cmds.ls( 'im_*_CTL', type='transform' )
        
        self.initCtls = []
        self.ctls = []
        
        for initCtl in self.imInitCtls:
            self.initCtls.append( initCtl[3:] )
            
        for ctl in self.imCtls:
            self.ctls.append( ctl[3:] )
            
        for i in cmds.ls( 'im_*' ):
            cmds.lockNode( i, lock=0 )
            
        self.setInitAttr()
        self.fixShape()
            
    def setInitAttr(self):
        for i in range( len(self.initCtls) ):
            imInitCtl = self.imInitCtls[i]
            initCtl = self.initCtls[i]
            rigbase.setTransformAttrToOther( imInitCtl, initCtl )
            
    def fixShape(self):
        for i in range( len( self.ctls ) ):
            imCtl = self.imCtls[i]
            ctl = self.ctls[i]
            try:rigbase.setShapeToOther( imCtl, ctl )
            except:pass