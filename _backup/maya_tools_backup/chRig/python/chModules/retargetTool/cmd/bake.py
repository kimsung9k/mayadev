import maya.cmds as cmds
import maya.OpenMayaAnim as anim
import editTransform
import retargeting


class Bake:
    
    def __init__(self):
        
        pass

        
    def lastBake( self, worldCtl, timeRange ):
        
        namespace = worldCtl.replace( 'World_CTL', '' )
        ctls = cmds.ls( namespace+'*_CTL' )
        
        localControlers = self.getConnectedLocalControlers( worldCtl )
        

        localCrvs = self.getEditMatrixCurve( localControlers )
        
        time = ( timeRange[0], timeRange[1] )
        sampleValue = timeRange[2]
        
        cmds.bakeResults( ctls, simulation=True, t=time, sampleBy=sampleValue, disableImplicitControl=True, preserveOutsideKeys=False, 
                  sparseAnimCurveBake=False, removeBakedAttributeFromLayer=False, bakeOnOverrideLayer=False, minimizeRotation=False, 
                  controlPoints=False, shape=False )
        
        self.deleteLocalControlers( localControlers )
        self.deleteFollowAttr( ctls )
        if localCrvs:
            cmds.delete( localCrvs )
    
    
    def exportBake( self, ctls, timeRange ):
        
        cmds.undoInfo( swf=0 )
        time = ( timeRange[0], timeRange[1] )
        sampleValue = timeRange[2]
        
        cmds.bakeResults( ctls, simulation=True, t=time, sampleBy=sampleValue, disableImplicitControl=True, preserveOutsideKeys=False, 
                  sparseAnimCurveBake=False, removeBakedAttributeFromLayer=False, bakeOnOverrideLayer=False, minimizeRotation=False, 
                  controlPoints=False, shape=False )
        
        timeControl = cmds.createNode( 'timeControl', n='timeControl' )
        
        dgtrAnimCurves = cmds.ls( 'DGTR_*', type='animCurve' )
    
        for anim in dgtrAnimCurves:
            cmds.connectAttr( timeControl+'.outTime', anim+'.input' )
            
        for ctl in ctls:
            animNodeRx = cmds.listConnections( ctl+'.rx', s=1, d=0, type='animCurve' )[0]
            animNodeRy = cmds.listConnections( ctl+'.ry', s=1, d=0, type='animCurve' )[0]
            animNodeRz = cmds.listConnections( ctl+'.rz', s=1, d=0, type='animCurve' )[0]
            
            animNodeIrx = cmds.listConnections( ctl+'.irx', s=1, d=0, type='animCurve' )[0]
            animNodeIry = cmds.listConnections( ctl+'.iry', s=1, d=0, type='animCurve' )[0]
            animNodeIrz = cmds.listConnections( ctl+'.irz', s=1, d=0, type='animCurve' )[0]
            
            self.eulerFilter( [animNodeRx, animNodeRy, animNodeRz] )
            self.eulerFilter( [animNodeIrx, animNodeIry, animNodeIrz] )
        cmds.undoInfo( swf=1 )


    def eulerFilter(self, inputRotAnims ):
        
        trNode = cmds.createNode( 'transform' )
        
        xCons = cmds.listConnections( inputRotAnims[0]+'.output', s=0, d=1, p=1, c=1 )
        yCons = cmds.listConnections( inputRotAnims[1]+'.output', s=0, d=1, p=1, c=1 )
        zCons = cmds.listConnections( inputRotAnims[2]+'.output', s=0, d=1, p=1, c=1 )
        
        cmds.disconnectAttr( xCons[0], xCons[1] )
        cmds.disconnectAttr( yCons[0], yCons[1] )
        cmds.disconnectAttr( zCons[0], zCons[1] )
        
        cmds.connectAttr( inputRotAnims[0]+'.output', trNode+'.rx' )
        cmds.connectAttr( inputRotAnims[1]+'.output', trNode+'.ry' )
        cmds.connectAttr( inputRotAnims[2]+'.output', trNode+'.rz' )
        
        cmds.filterCurve( inputRotAnims[0], inputRotAnims[1], inputRotAnims[2] )
        
        cmds.disconnectAttr( inputRotAnims[0]+'.output', trNode+'.rx' )
        cmds.disconnectAttr( inputRotAnims[1]+'.output', trNode+'.ry' )
        cmds.disconnectAttr( inputRotAnims[2]+'.output', trNode+'.rz' )
        
        cmds.connectAttr( xCons[0], xCons[1] )
        cmds.connectAttr( yCons[0], yCons[1] )
        cmds.connectAttr( zCons[0], zCons[1] )
        
        cmds.delete( trNode )
        
        
    def deleteFollowAttr(self, ctls ):
        
        for ctl in ctls:
            
            attrs = cmds.listAttr( ctl, k=1, ud=1 )
            
            if not attrs: continue
            
            for attr in attrs:
                if attr[-5:] == 'CTL_w':
                    cmds.deleteAttr( ctl, at = attr )
                    
                    
    def getConnectedLocalControlers(self, worldCtl ):
        
        sourceWorldCtls = retargeting.getConnectedRetargetWorldCtl( worldCtl )
        
        localCtls = []
        for sourceWorldCtl in sourceWorldCtls:
            self._inst = editTransform.localControler( sourceWorldCtl, worldCtl )
            
            localCtls += self._inst.getLocalControler()
        
        return localCtls
    
    
    def getEditMatrixCurve(self, localCtls ):
        
        trs = []
        for localCtl in localCtls:
            if cmds.nodeType( localCtl ) == 'editMatrixByCurve':
                trGeos = cmds.listConnections( localCtl, s=1, d=0, type='transformGeometry' )
                trs += cmds.listConnections( trGeos, type='transform', s=1, d=0 )
        return trs
                
       
    def deleteLocalControlers(self, localControlers ):
        
        for localCtl in localControlers:
            self._inst.deleteLocalControler( localCtl )