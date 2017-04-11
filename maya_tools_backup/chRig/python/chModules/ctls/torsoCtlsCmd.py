import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaMPx as mpx
import chModules.rigbase as rigbase
import armandlegCtls
import chModules.system.switch as switch
import math

import ctlsAll


class Fly_CTL( ctlsAll.CtlsAll ):
    
    def goToRoot(self, target, *args ):
        
        ns = self.getNamespace( target )
        
        rootCtl = ns+'Root_CTL'
        flyCtl  = ns+'Fly_CTL'
        
        rootWm = cmds.getAttr( rootCtl+'.wm' )
        
        cmds.xform( flyCtl, ws=1, matrix= rootWm )
        
        
        
    def setFlyControlPoint(self, target, *args ):
        
        ns = self.getNamespace(target)
        rootCtl = ns+'Root_CTL'
        flyCtl = ns+'Fly_CTL'

        flyCtlMtxList = cmds.getAttr( flyCtl+'.wm' )
        rootCtlMtxList = cmds.getAttr( rootCtl+'.wm' )
        
        flyCtlMtx = om.MMatrix()
        rootCtlMtx = om.MMatrix()
        
        om.MScriptUtil.createMatrixFromList( flyCtlMtxList, flyCtlMtx )
        om.MScriptUtil.createMatrixFromList( rootCtlMtxList, rootCtlMtx )

        localMtx = rootCtlMtx * flyCtlMtx.inverse()

        mpxTrans = mpx.MPxTransformationMatrix( localMtx )
        trans = mpxTrans.translation()
        rotate = mpxTrans.eulerRotation().asVector()
        
        cmds.setAttr( flyCtl+'.pivTx', trans.x )
        cmds.setAttr( flyCtl+'.pivTy', trans.y )
        cmds.setAttr( flyCtl+'.pivTz', trans.z )
        cmds.setAttr( flyCtl+'.pivRx', math.degrees( rotate.x ) )
        cmds.setAttr( flyCtl+'.pivRy', math.degrees( rotate.y ) )
        cmds.setAttr( flyCtl+'.pivRz', math.degrees( rotate.z ) )
        
        cmds.setAttr( flyCtl+'.blend', 1 )
        

class Root_CTL( ctlsAll.CtlsAll ):
        
    def goToFlyControlPoint(self, target, *args ):
        
        ns = self.getNamespace( target )
        
        rootCtl = ns+'Root_CTL'
        flyCtl  = ns+'Fly_CTL'
        flyControlPoint  = ns+'Fly_CTL_ControlPoint'
        
        flyControlWm = cmds.getAttr( flyControlPoint+'.wm' )
        
        cmds.xform( rootCtl, ws=1, matrix= flyControlWm )
        
        cmds.setAttr( flyCtl+'.blend', 0 )