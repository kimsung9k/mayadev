import maya.cmds as cmds
import chModules.retargetTool.functions as fnc


def getTimeControl( targetWorldCtl, worldCtlList ):
    
    retargetNSs = []
    
    sourceNSs = []
    
    for worldCtl in worldCtlList:
        sourceNSs.append( worldCtl.replace( 'World_CTL', '' ) )
    
    targetNS = targetWorldCtl.replace( 'World_CTL', '' )
    
    targetCtls = cmds.ls( targetNS+'*_CTL', tr=1 )
    
    for ctl in targetCtls:
        
        if not sourceNSs: break
        
        retargetBlenderCons = cmds.listConnections( ctl, type='retargetBlender', s=1, d=0 )
        if retargetBlenderCons:
            retargetBlender = retargetBlenderCons[0]
            
            fnc.clearArrayElement( retargetBlender+'.input' )
            inputLen = fnc.getLastIndex( retargetBlender+'.input' )+1
            
            originName = ctl.replace( targetNS, '' )
            
            for i in range( inputLen ):
                RTTrans = cmds.listConnections( retargetBlender+'.input[%d].transMatrix' % i )
                if not RTTrans: continue
                
                RTTrans = RTTrans[0].split( '_RTTrans' )[0]
                
                RTNamespace = RTTrans.replace( originName, '' )
                
                if RTNamespace in sourceNSs:
                    timeControls = cmds.ls( RTNamespace.replace( 'DGTR_', '' )+'timeControl*' )
                    if not timeControls: "%s Motion File has no timeControl." % RTNamespace
                    cuTimeControl = None
                    for timeControl in timeControls:
                        if cmds.nodeType( timeControl ) == 'timeControl':
                            cuTimeControl = timeControl
                    retargetNSs.append( cuTimeControl )
                    sourceNSs.remove( RTNamespace )
                    
        udAttrBlenderCons = cmds.listConnections( ctl, type='udAttrBlender', s=1, d=0 )
                    
        if udAttrBlenderCons:
            retargetUdAttr = udAttrBlenderCons[0]
            
            fnc.clearArrayElement( retargetUdAttr+'.input' )
            inputLen = fnc.getLastIndex( retargetUdAttr+'.input' )+1
    
            originName = ctl.replace( targetNS, '' )
            
            for i in range( inputLen ):
                inputAnimNodes = cmds.listConnections( retargetUdAttr+'.input[%d].udAttr[0]' % i )
                if not inputAnimNodes: continue
                
                udNamespace = inputAnimNodes[0].split( originName )[0]+'DGTR_'

                if udNamespace in sourceNSs:
                    timeControls = cmds.ls( udNamespace.replace( 'DGTR_', '' )+'timeControl*' )
                    if not timeControls: "%S Motion File has no timeControl." % udNamespace
                    cuTimeControl = None
                    for timeControl in timeControls:
                        if cmds.nodeType( timeControl ) == 'timeControl':
                            cuTimeControl = timeControl
                    retargetNSs.append( cuTimeControl )
                    sourceNSs.remove( udNamespace )
        
    return retargetNSs