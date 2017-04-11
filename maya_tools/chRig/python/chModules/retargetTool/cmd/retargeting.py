import maya.cmds as cmds
import maya.mel as mel
import chModules.retargetTool.connect as mainConnect
import chModules.retargetTool.followConnect as followConnect
import chModules.retargetTool.topInfoEdit as topInfoEdit
import chModules.retargetTool.functions as fnc
import editTransform
import timeControl as timeCmd


timeLimitAble = False
minTime = 1
maxTime = 10


def setTimeLimitAble( limitAble, minValue, maxValue ):
    global timeLimitAble 
    global minTime
    global maxTime
    
    timeLimitAble = limitAble
    minTime = minValue
    maxTime = maxValue


def connect( sourceWorldCtl, targetWorldCtl ):
    
    sels = cmds.ls( sl=1, tr=1 )
    
    topInfoEdit.EditNameSpaceInfo( sourceWorldCtl, targetWorldCtl )
    
    if targetWorldCtl in sels:
        sels.remove( targetWorldCtl )

    if sels:
        for sel in sels:
            mainConnect.Each( sel )
            followConnect.Each( sel )
    else:
        mainConnect.All()
        followConnect.All()

    timeControlInst = mainConnect.ConnectTimeControl()

    mainConnect.ConnectWeightControl()

    try:
        timeControlNode =  timeControlInst._timeControlNode
    except: return None

    cmds.setAttr( timeControlNode+'.limitAble', timeLimitAble )
    cmds.setAttr( timeControlNode+'.minTime', minTime )
    cmds.setAttr( timeControlNode+'.maxTime', maxTime )
    

def disconnect( sourceWorldCtl, targetWorldCtl ):
    
    def deleteFollowWeightAttrs( tr ):
        udAttrs = cmds.listAttr( tr, k=1, ud=1 )
        
        if not udAttrs: return None
        
        for attr in udAttrs:
            if attr[-5:] == 'CTL_w':
                cmds.deleteAttr( tr+'.'+attr )
                
    def disconnectOutWeight( sourceNS, targetNS ):
        timeControl = timeCmd.getTimeControl( targetNS+'World_CTL', [sourceNS+'World_CTL'] )[0]
        
        if not timeControl: return None
        outWeights = cmds.listConnections( timeControl+'.outWeight', s=0, d=1, c=1, p=1 )
        
        if not outWeights: return None
        
        outputs = outWeights[::2]
        inputs  = outWeights[1::2]
        
        for i in range( len( outputs ) ):
            if inputs[i].find( targetNS ) == 0:
                cmds.disconnectAttr( outputs[i], inputs[i] )
                
    def deleteDistRate( sourceNS, targetNS ):
        distRates = cmds.ls( sourceNS+'*_distRate' )
        
        connectedAttrs = []
        for distRate in distRates:
            cons = cmds.listConnections( distRate+'.message', d=1, s=0, p=1, c=1 )
            
            if not cons: continue
            inputs  = cons[1::2]
            outputs = cons[::2]
            for i in range( len( inputs ) ):
                cmds.disconnectAttr( outputs[i], inputs[i] )
            
            connectedAttrs += inputs
        
        cmds.delete( distRate )
        
        for connectedAttr in connectedAttrs:
            mel.eval( "removeMultiInstance %s" % connectedAttr )
            
    localCtlInst = editTransform.localControler( sourceWorldCtl, targetWorldCtl )
    
    localCtls = localCtlInst.getLocalControler()
    
    for localCtl in localCtls:
        localCtlInst.deleteLocalControler( localCtl )
    
    sourceNS = sourceWorldCtl.replace( 'World_CTL', '' )
    targetNS = targetWorldCtl.replace( 'World_CTL', '' )
    
    disconnectOutWeight( sourceNS, targetNS )
    deleteDistRate( sourceNS, targetNS )
    
    retargetTrans = cmds.ls( sourceNS+'*', type='retargetTransNode' )
    retargetOrient = cmds.ls( sourceNS+'*', type='retargetOrientNode' )
    
    if retargetTrans:
        cmds.delete( retargetTrans )
    if retargetOrient:
        cmds.delete( retargetOrient )
        
    retargetBlenders = cmds.ls( targetNS+'*', type='retargetBlender' )
    udAttrBlenders   = cmds.ls( targetNS+'*', type='udAttrBlender' )
    
    if udAttrBlenders:
        for udAttrBlender in udAttrBlenders:
            cons = cmds.listConnections( udAttrBlender, s=1, d=0, c=1, p=1 )
            
            if not cons: 
                cmds.delete( udAttrBlender )
                continue
            
            outputs = cons[1::2]
            inputs = cons[::2]
            
            for i in range( len( outputs ) ):
                if outputs[i].find( sourceNS.replace( 'DGTR_','' ) ) == 0:
                    cmds.disconnectAttr( outputs[i], inputs[i] )
            
            fnc.clearArrayElement( udAttrBlender+'.input' )
            if fnc.getLastIndex( udAttrBlender+'.input' ) == -1:
                cmds.delete( udAttrBlender )
    
    if retargetBlenders:
        for retargetBlender in retargetBlenders:
            fnc.clearArrayElement( retargetBlender+'.input' )
            if not cmds.listConnections( retargetBlender, s=1, d=0, type='retargetTransNode' ):
                trCons = cmds.listConnections( retargetBlender, s=0, d=1 )
                if trCons:
                    deleteFollowWeightAttrs( trCons[0] )
                cmds.delete( retargetBlender )
                
    multNodes   = cmds.ls( sourceNS+'*', type='multiplyDivide' )
    multNodes  += cmds.ls( targetNS+'*', type='multiplyDivide' )
    
    if multNodes:
        cmds.delete( multNodes )
        


def getWorldCtlList():
    
    refs = cmds.ls( type='reference' )

    worldCtls = []
    for ref in refs:
        try :ctls = cmds.reference( rfn=ref, n=1 )
        except: continue
        for ctl in ctls:
            if ctl[-9:] == 'World_CTL':
                worldCtls.append( ctl )
                break
            elif ctl.find( 'DGTR' ) != -1 and ctl[-4:] == '_CTL':
                namespace = ctl.split( 'DGTR' )[0]
                worldCtls.append( namespace+'DGTR_World_CTL' )
                break
            
    return worldCtls


def getConnectedRetargetWorldCtl( targetWorldCtl ):
    
    worldCtlList = getWorldCtlList()
    if targetWorldCtl in worldCtlList:
        worldCtlList.remove( targetWorldCtl )
    
    retargetNSs = []
    
    sourceNSs = []
    
    for worldCtl in worldCtlList:
        sourceNSs.append( worldCtl.replace( 'World_CTL', '' ) )
    if not sourceNSs: return None
    
    targetNS = targetWorldCtl.replace( 'World_CTL', '' )
    
    targetCtls = cmds.ls( targetNS+'*_CTL', tr=1 )
    
    for ctl in targetCtls:
        
        retargetBlenderCons = cmds.listConnections( ctl, type='retargetBlender', s=1, d=0 )
        retargetUdAttrCons  = cmds.listConnections( ctl, type='udAttrBlender', s=1, d=0 )
        
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
                    retargetNSs.append( RTNamespace+'World_CTL' )
                    sourceNSs.remove( RTNamespace )
                    
        if retargetUdAttrCons:
            retargetUdAttr = retargetUdAttrCons[0]
            
            fnc.clearArrayElement( retargetUdAttr+'.input' )
            inputLen = fnc.getLastIndex( retargetUdAttr+'.input' )+1
    
            originName = ctl.replace( targetNS, '' )
            
            for i in range( inputLen ):
                inputAnimNodes = cmds.listConnections( retargetUdAttr+'.input[%d].udAttr[0]' % i )
                if not inputAnimNodes: continue
                
                udNamespace = inputAnimNodes[0].split( originName )[0]+'DGTR_'

                if udNamespace in sourceNSs:
                    retargetNSs.append( udNamespace+'World_CTL' )
                    sourceNSs.remove( udNamespace )
    
    return retargetNSs