import topInfoEdit
import getItems
import topInfo
import maya.cmds as cmds
import functions as fnc


class EditNamespace:
    
    def __init__(self, sourceWorld, targetWorld ):
        
        topInfoEdit.EditNameSpaceInfo( sourceWorld, targetWorld )
        
        
class ConnectTimeControl:
    
    def __init__(self):
        
        timeControlNode = cmds.ls( topInfo.sourceNS[:-5]+'*', type='timeControl' )
        
        if not timeControlNode: return None
        
        timeControlNode = timeControlNode[0]
        
        if not cmds.isConnected( 'time1.outTime', timeControlNode+'.inTime' ):
            cmds.connectAttr( 'time1.outTime', timeControlNode+'.inTime' )
            
        self._timeControlNode = timeControlNode
        
        
        
class ConnectWeightControl:
    
    def __init__(self):
        self._timeControl = topInfo.sourceNS.replace( 'DGTR_', '' )+'timeControl'
        
        if not cmds.objExists( self._timeControl ): return None

        self.doIt()


    def doIt( self ):
        
        targetCtls = cmds.ls( topInfo.targetNS+'*_CTL', tr=1 )
        
        for ctl in targetCtls:
            originName = ctl.replace( topInfo.targetNS, '' )
            
            retargetBlenderCons = cmds.listConnections( ctl, type='retargetBlender', s=1, d=0 )

            if retargetBlenderCons:
                retargetBlender = retargetBlenderCons[0]
                
                fnc.clearArrayElement( retargetBlender+'.input' )
                inputLen = fnc.getLastIndex( retargetBlender+'.input' )+1
                
                for i in range( inputLen ):
                    RTTrans = cmds.listConnections( retargetBlender+'.input[%d].transMatrix' % i )
                    if not RTTrans: continue
                    
                    RTTrans = RTTrans[0].split( '_RTTrans' )[0]
                    
                    RTNamespace = RTTrans.replace( originName, '' )
                    
                    if RTNamespace != topInfo.sourceNS: continue
                    
                    if not cmds.isConnected( self._timeControl+'.outWeight', retargetBlender+'.input[%d].weight' % i ):
                        cmds.connectAttr( self._timeControl+'.outWeight', retargetBlender+'.input[%d].weight' % i, f=1 )
            
            udAttrBlenderCons = cmds.listConnections( ctl, type='udAttrBlender', s=1, d=0 )

            if udAttrBlenderCons:
                udAttrBlender = udAttrBlenderCons[0]
                
                fnc.clearArrayElement( udAttrBlender+'.input' )
                inputLen = fnc.getLastIndex( udAttrBlender+'.input' )+1
                
                for i in range( inputLen ):
                    outputNodes = cmds.listConnections( udAttrBlender+'.input[%d].udAttr' % i, s=1, d=0 )
                    
                    if not outputNodes: continue
                    
                    if outputNodes[0].find( topInfo.sourceNS.replace( 'DGTR_','') ) == 0:     
                        if not cmds.isConnected( self._timeControl+'.outWeight', udAttrBlender+'.input[%d].weight' % i ):
                            cmds.connectAttr( self._timeControl+'.outWeight', udAttrBlender+'.input[%d].weight' % i, f=1 )
            


class Each:
    
    def __init__(self, target ):
        
        try:
            topInfoEdit.EditCtlInfo( target )
        except: return None
        
        origin       = getItems.getOriginRate()
        source       = getItems.getSource()
        sourceOrig   = getItems.getSourceOrig()
        sourceFollow = getItems.getSourceFollow()
        targetOrig   = getItems.getTargetOrig()
        targetFollow = getItems.getTargetFollow()
        distRateNode = getItems.getDistNode()
        udAttrs      = getItems.getUdAttrs()
        
        
        transRetarget  = getItems.getTransRetargetNode()
        orientRetarget = getItems.getOrientRetargetNode()
        
        origin.trans >> transRetarget
        source.trans >> transRetarget
        sourceOrig   >> transRetarget
        sourceFollow >> transRetarget
        targetOrig   >> transRetarget
        targetFollow >> transRetarget
        distRateNode >> transRetarget
        
        origin.orient>> orientRetarget
        source.orient>> orientRetarget
        sourceOrig   >> orientRetarget
        sourceFollow >> orientRetarget
        targetOrig   >> orientRetarget
        targetFollow >> orientRetarget
        
        udAttrs      >> transRetarget
        


class All:
    
    def __init__(self):
        
        targetCtls = cmds.ls( topInfo.targetNS+'*_CTL', tr=1 )
        
        for i in range( len( targetCtls ) ):
            
            targetCtl = targetCtls[i]
            
            Each( targetCtl )