import maya.cmds as cmds
import maya.OpenMaya as om
from model import *


class RemapConnect:
    
    def __init__(self):
        
        pass
    
    def reverseCheck(self, remapNode, reverseCheck ):
    
        if reverseCheck:
            revNode = self.getReverse()
            if not cmds.isConnected( revNode+'.output', remapNode+'.color' ):
                cmds.connectAttr( revNode+'.output', remapNode+'.color', f=1 )
            
            colorRCons = cmds.listConnections( remapNode+'.colorR', s=1, d=0, c=1, p=1 )
            if colorRCons: cmds.disconnectAttr( colorRCons[1], colorRCons[0] )
            colorGCons = cmds.listConnections( remapNode+'.colorG', s=1, d=0, c=1, p=1 )
            if colorGCons: cmds.disconnectAttr( colorGCons[1], colorGCons[0] )
            colorBCons = cmds.listConnections( remapNode+'.colorB', s=1, d=0, c=1, p=1 )
            if colorBCons: cmds.disconnectAttr( colorBCons[1], colorBCons[0] )
            
        else:
            sampler = self.getSamplerInfo()
            if not cmds.isConnected( sampler+'.facingRatio', remapNode+'.colorR' ):
                cmds.connectAttr( sampler+'.facingRatio', remapNode+'.colorR' )
            if not cmds.isConnected( sampler+'.facingRatio', remapNode+'.colorG' ):
                cmds.connectAttr( sampler+'.facingRatio', remapNode+'.colorG' )
            if not cmds.isConnected( sampler+'.facingRatio', remapNode+'.colorB' ):
                cmds.connectAttr( sampler+'.facingRatio', remapNode+'.colorB' )
            
            colorCons = cmds.listConnections( remapNode+'.color', s=1, d=0, c=1, p=1 )
            if colorCons:
                cmds.disconnectAttr( colorCons[1], colorCons[0] )
                
                
    def luminanceCheck(self, remapNode, checkLuminance ):
        
        if checkLuminance:
            remapOutCons = cmds.listConnections( remapNode+'.outColor', p=1, c=1 )
            
            if remapOutCons:
                outputs = remapOutCons[::2]
                inputs  = remapOutCons[1::2]
                
                for i in range( len( inputs ) ):
                    if cmds.nodeType( inputs[i].split( '.' )[0] ) == 'remapHsv':
                        continue
                    else:
                        remapHsv = cmds.shadingNode( 'remapHsv', asUtility=1 )
                        cmds.connectAttr( outputs[i], remapHsv+'.color' )
                        cmds.connectAttr( remapHsv+'.outColor', inputs[i], f=1 )
            else:
                remapHsv = cmds.shadingNode( 'remapHsv', asUtility=1 )
                cmds.connectAttr( remapNode+'.outColor', remapHsv+'.color' )
        else:
            remapOutCons = cmds.listConnections( remapNode+'.outColor', p=1, c=1 )
            
            if remapOutCons:
                outputs = remapOutCons[::2]
                inputs  = remapOutCons[1::2]
                
                for i in range( len( inputs ) ):
                    if cmds.nodeType( inputs[i].split( '.' )[0] ) == 'remapHsv':
                        hsv = inputs[i].split( '.' )[0]
                        cons = cmds.listConnections( hsv+'.outColor', p=1, c=1 )
                        if cons:
                            hsvOInputs  = cons[1::2]
                            
                            for j in range( len( hsvOInputs ) ):
                                cmds.connectAttr( remapNode+'.outColor', hsvOInputs[j], f=1 )
                        cons = cmds.listConnections( hsv+'.color', s=1, d=0, c=1, p=1 )
                        hsvIInput = cons[1]
                        cmds.disconnectAttr( hsvIInput, hsv+'.color' )
                        cmds.delete( hsv )
                        


    def gammaCheck(self, remapNode, checkGamma ):
        
        gammaNodeName = 'gammaCorrect'
        hsvNodes = cmds.listConnections( remapNode, s=0, d=1, type='remapHsv' )
        
        outputAttrs = []
        
        if hsvNodes:
            for hsvNode in hsvNodes:
                outputAttrs.append( hsvNode+'.outColor' )
        else:
            outputAttrs.append( remapNode+'.outColor' )
        
        if checkGamma:
            for outputAttr in outputAttrs:
                cons = cmds.listConnections( outputAttr, d=1, s=0, p=1, c=1 )
                if not cons:
                    gammaNode = cmds.shadingNode( gammaNodeName, asUtility=1 )
                    cmds.setAttr( gammaNode+'.gamma', 0.45, 0.45, 0.45 )
                    cmds.connectAttr( outputAttr, gammaNode+'.value' )
                    continue
                
                outputs = cons[::2]
                inputs  = cons[1::2]
                for i in range( len( outputs ) ):
                    inputAttr = inputs[i]
                    inputNode = inputAttr.split( '.' )[0]
                    if cmds.nodeType( inputNode ) == gammaNodeName:
                        continue
                    else:
                        gammaNode = cmds.shadingNode( gammaNodeName, asUtility=1 )
                        cmds.setAttr( gammaNode+'.gamma', 0.45, 0.45, 0.45 )
                        cmds.connectAttr( outputAttr, gammaNode+'.value' )
                        cmds.connectAttr( gammaNode+'.outValue', inputAttr, f=1 )
        else:
            for outputAttr in outputAttrs:
                cons = cmds.listConnections( outputAttr, d=1, s=0, p=1, c=1 )
                if not cons: continue
                
                outputs = cons[::2]
                inputs  = cons[1::2]
                for i in range( len( outputs ) ):
                    inputAttr = inputs[i]
                    inputNode = inputAttr.split( '.' )[0]
                    if cmds.nodeType( inputNode ) == gammaNodeName:
                        gammaCons = cmds.listConnections( inputNode+'.outValue', d=1, s=0, p=1, c=1 )
                        if not gammaCons: 
                            cmds.delete( inputNode )
                            continue
                        gammaInputs  = gammaCons[1::2]
                        for j in range( len( gammaInputs ) ):
                            cmds.connectAttr( outputAttr, gammaInputs[j], f=1 )
                        cmds.delete( inputNode )
                    else:
                        continue
                        

    
    def ucCreateSamplerInfo(self, checkReverse, checkLuminance, checkGamma, *args ):
        
        sels = cmds.ls( sl=1 )
        
        remapNodes = []
        if not sels: sels=[]
        
        for sel in sels:
            if cmds.nodeType( sel ) == 'remapColor':
                remapNodes.append( sel )
        
        if not remapNodes:
            remapNode = cmds.shadingNode( 'remapColor', asUtility=1 )
            remapNodes.append( remapNode )
        
        for remapNode in remapNodes:
            self.reverseCheck( remapNode, checkReverse )
            self.luminanceCheck( remapNode, checkLuminance )
            self.gammaCheck(remapNode, checkGamma)
            
        cmds.select( remapNodes )
        
        


    def getSamplerInfo(self):
        
        samplerInfoName = RemapConnectInfo._samplerInfoName
        samplerInfoAttr = RemapConnectInfo._samplerInfoAttr
        
        samplerInfos = cmds.ls( type='samplerInfo' )
        
        vrayRemapSamplerInfo = None
        
        if not samplerInfos : samplerInfos = []
        
        for samplerInfo in samplerInfos:
            if cmds.attributeQuery( samplerInfoAttr, node=samplerInfo, ex=1 ):
                return samplerInfo
        
        if not vrayRemapSamplerInfo:
            vrayRemapSamplerInfo = cmds.shadingNode( 'samplerInfo', n=samplerInfoName, asUtility=1 )
            cmds.addAttr( vrayRemapSamplerInfo, ln=samplerInfoAttr, at='message' )
            return vrayRemapSamplerInfo
    
    
    def getReverse(self):
        
        reverseName = RemapConnectInfo._reverseName
        reverseAttr = RemapConnectInfo._reverseAttr
        
        reverses = cmds.ls( type='reverse' )
        
        vrayRemapReverse = None
        
        if not reverses: reverses = []
        
        for reverse in reverses:
            if cmds.attributeQuery( reverseAttr, node=reverse, ex=1 ):
                vrayRemapReverse = reverse
                break
            
        if not vrayRemapReverse:
            vrayRemapReverse = cmds.shadingNode( 'reverse', n=reverseName, asUtility=1 )
            cmds.addAttr( vrayRemapReverse, ln=reverseAttr, at='message' )
        
        samplerInfos = cmds.listConnections( vrayRemapReverse, s=1, d=0, type='samplerInfo' )
        if not samplerInfos:
            samplerInfo = self.getSamplerInfo()
            if not cmds.isConnected( samplerInfo+'.facingRatio', vrayRemapReverse+'.inputX' ):
                cmds.connectAttr( samplerInfo+'.facingRatio', vrayRemapReverse+'.inputX', f=1 )
            if not cmds.isConnected( samplerInfo+'.facingRatio', vrayRemapReverse+'.inputY' ):
                cmds.connectAttr( samplerInfo+'.facingRatio', vrayRemapReverse+'.inputY', f=1 )
            if not cmds.isConnected( samplerInfo+'.facingRatio', vrayRemapReverse+'.inputZ' ):
                cmds.connectAttr( samplerInfo+'.facingRatio', vrayRemapReverse+'.inputZ', f=1 )
        
        return vrayRemapReverse
    

def getMObject( target ):
    
    selList = om.MSelectionList()
    selList.add( target )
    mObj = om.MObject()
    selList.getDependNode( 0, mObj )
    return mObj


def arrangePlugIndices( plug ):
    
    plugLength = plug.numElements()
    
    poseValueList=[]
    for i in range( plugLength ):
        posePlug = plug[i].child(0)
        valuePlug = plug[i].child(1)
        poseValueList.append( [posePlug.asFloat(), valuePlug.asFloat()] )
    poseValueList.sort()

    for i in range( plugLength ):
        pose, value = poseValueList[i]
        cmds.setAttr( plug[i].child(0).name(), pose )
        cmds.setAttr( plug[i].child(1).name(), value )

    
def remapColorSync( remapNode, fromList, toList ):
    
    fnNode = om.MFnDependencyNode( getMObject( remapNode ) )
    
    plugRed   = fnNode.findPlug( 'red' )
    plugGreen = fnNode.findPlug( 'green' )
    plugBlue  = fnNode.findPlug( 'blue' )
    
    arrangePlugIndices( plugRed )
    arrangePlugIndices( plugGreen )
    arrangePlugIndices( plugBlue )
    
    numRed = plugRed.numElements()
    numGreen = plugGreen.numElements()
    numBlue = plugBlue.numElements()
    
    fromPlugList = []
    fromPlugNums = []
    
    if 'red' in fromList:
        fromPlugList.append( plugRed )
        fromPlugNums.append( numRed )
    if 'green' in fromList:
        fromPlugList.append( plugGreen )
        fromPlugNums.append( numGreen )
    if 'blue' in fromList:
        fromPlugList.append( plugBlue )
        fromPlugNums.append( numBlue )
    
    largeNum = 0
    for i in range( len(fromPlugNums) ):
        if fromPlugNums[i] > largeNum:
            largeNum = fromPlugNums[i]
    
    resetIndices = []
    largeNumPlugs = []
    for i in range( len(fromPlugNums) ):
        if largeNum > fromPlugNums[i]:
            resetIndices.append( fromPlugList[i] )
        else:
            largeNumPlugs.append( fromPlugList[i] )
    
    avFloatValues = [ 0.0 for i in range( largeNum ) ]
    avPositions   = [ 0.0 for i in range( largeNum ) ]

    for i in range( largeNum ):
        sumFloatValue = 0.0
        sumPosition   = 0.0
        for plug in largeNumPlugs:
            plugPose  = plug[i].child( 0 )
            plugValue = plug[i].child( 1 )
            
            sumPosition   += plugPose.asFloat()
            sumFloatValue += plugValue.asFloat()
        
        avPositions[i]   = sumPosition / len( largeNumPlugs )
        avFloatValues[i] = sumFloatValue / len(largeNumPlugs)

    toPlugList = []
    if 'red' in toList:
        toPlugList.append( plugRed )
    if 'green' in toList:
        toPlugList.append( plugGreen )
    if 'blue' in toList:
        toPlugList.append( plugBlue )
    
    '''
        for plug in toPlugList:
            numPlug = plug.numElements()
            for i in range( numPlug-2 ):
                print plug[0].name()
                try:cmds.removeMultiInstance( plug[0].name() )
                except:pass
    '''
    
    for i in range( len( toList ) ):   
        toPlugName = toPlugList[i].name()
        toAttr = toList[i]
        for j in range( largeNum ):
            cmds.setAttr( toPlugName+'[%d].%s_Position' %( j, toAttr ), avPositions[j] )
            cmds.setAttr( toPlugName+'[%d].%s_FloatValue' %( j, toAttr ), avFloatValues[j] )
            cmds.setAttr( toPlugName+'[%d].%s_Interp' %( j, toAttr ), 3 )
            


def uiCmd_remapColorSync( fromList, toList, *args ):
    
    sels= cmds.ls( sl=1, type='remapColor' )
    if not sels: return None
    
    for sel in sels:
        remapColorSync( sel, fromList, toList )
    