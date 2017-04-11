import maya.cmds as cmds
import sgModelDag


def addAttr( target, **options ):
    
    items = options.items()
    
    attrName = ''
    channelBox = False
    keyable = False
    for key, value in items:
        if key in ['ln', 'longName']:
            attrName = value
        elif key in ['cb', 'channelBox']:
            channelBox = True
            options.pop( key )
        elif key in ['k', 'keyable']:
            keyable = True 
            options.pop( key )
    
    if cmds.attributeQuery( attrName, node=target, ex=1 ): return None
    
    cmds.addAttr( target, **options )
    
    if channelBox:
        cmds.setAttr( target+'.'+attrName, e=1, cb=1 )
    elif keyable:
        cmds.setAttr( target+'.'+attrName, e=1, k=1 )



def createSgWobbleAttribute( crv, wobbleCurve=None ):
    
    crv = sgModelDag.getTransform( crv )
    if not wobbleCurve:
        sgWobbleCurve = sgModelDag.getNodeFromHistory( crv , 'sgWobbleCurve2' )
        if not sgWobbleCurve: return None
        sgWobbleCurve = sgWobbleCurve[0]
    else:
        sgWobbleCurve = wobbleCurve
    
    addAttr( crv, ln='globalEnvelope', k=1, dv=1 )
    addAttr( crv, ln='globalWave1', k=1, dv=1 )
    addAttr( crv, ln='globalTimeMult1', k=1, dv=-.3 )
    addAttr( crv, ln='globalOffset1', k=1, dv=0.0 )
    addAttr( crv, ln='globalLength1', k=1, dv=0.0 )
    addAttr( crv, ln='globalWave2', k=1, dv=1 )
    addAttr( crv, ln='globalTimeMult2', k=1, dv=-.3 )
    addAttr( crv, ln='globalOffset2', k=1, dv=0.0 )
    addAttr( crv, ln='globalLength2', k=1, dv=0.0 )
    addAttr( crv, ln='envelope', k=1, dv=1 )
    addAttr( crv, ln='wave1', k=1, dv=30 )
    addAttr( crv, ln='timeMult1', k=1, dv=1 )
    addAttr( crv, ln='offset1', k=1, dv=0 )
    addAttr( crv, ln='waveLength1', k=1, dv=0.25 )
    addAttr( crv, ln='wave2', k=1, dv=30 )
    addAttr( crv, ln='timeMult2', k=1, dv=1 )
    addAttr( crv, ln='offset2', k=1, dv=0 )
    addAttr( crv, ln='waveLength2', k=1, dv=0.25 )
    
    envelopeMd = cmds.createNode( 'multDoubleLinear' )
    waveMd1     = cmds.createNode( 'multDoubleLinear' )
    timeMultMd1 = cmds.createNode( 'multDoubleLinear' )
    offsetAd1   = cmds.createNode( 'addDoubleLinear' )
    lengthAdd1  = cmds.createNode( 'addDoubleLinear' )
    waveMd2     = cmds.createNode( 'multDoubleLinear' )
    timeMultMd2 = cmds.createNode( 'multDoubleLinear' )
    offsetAd2   = cmds.createNode( 'addDoubleLinear' )
    lengthAdd2  = cmds.createNode( 'addDoubleLinear' )
    
    cmds.connectAttr( crv+'.globalEnvelope', envelopeMd+'.input1' )
    cmds.connectAttr( crv+'.envelope', envelopeMd+'.input2' )
    cmds.connectAttr( crv+'.globalWave1', waveMd1+'.input1' )
    cmds.connectAttr( crv+'.wave1', waveMd1+'.input2' )
    cmds.connectAttr( crv+'.globalTimeMult1', timeMultMd1+'.input1' )
    cmds.connectAttr( crv+'.timeMult1', timeMultMd1+'.input2' )
    cmds.connectAttr( crv+'.globalOffset1', offsetAd1+'.input1' )
    cmds.connectAttr( crv+'.offset1', offsetAd1+'.input2' )
    cmds.connectAttr( crv+'.globalLength1', lengthAdd1+'.input1' )
    cmds.connectAttr( crv+'.waveLength1', lengthAdd1+'.input2' )
    cmds.connectAttr( crv+'.globalWave2', waveMd2+'.input1' )
    cmds.connectAttr( crv+'.wave2', waveMd2+'.input2' )
    cmds.connectAttr( crv+'.globalTimeMult2', timeMultMd2+'.input1' )
    cmds.connectAttr( crv+'.timeMult2', timeMultMd2+'.input2' )
    cmds.connectAttr( crv+'.globalOffset2', offsetAd2+'.input1' )
    cmds.connectAttr( crv+'.offset2', offsetAd2+'.input2' )
    cmds.connectAttr( crv+'.globalLength2', lengthAdd2+'.input1' )
    cmds.connectAttr( crv+'.waveLength2', lengthAdd2+'.input2' )
    
    cmds.connectAttr( envelopeMd+'.output', sgWobbleCurve+'.envelope' )
    cmds.connectAttr( waveMd1+'.output', sgWobbleCurve+'.wave1' )
    cmds.connectAttr( timeMultMd1+'.output', sgWobbleCurve+'.timeMult1' )
    cmds.connectAttr( offsetAd1+'.output', sgWobbleCurve+'.offset1' )
    cmds.connectAttr( lengthAdd1+'.output', sgWobbleCurve+'.waveLength1' )
    cmds.connectAttr( waveMd2+'.output', sgWobbleCurve+'.wave2' )
    cmds.connectAttr( timeMultMd2+'.output', sgWobbleCurve+'.timeMult2' )
    cmds.connectAttr( offsetAd2+'.output', sgWobbleCurve+'.offset2' )
    cmds.connectAttr( lengthAdd2+'.output', sgWobbleCurve+'.waveLength2' )



def connectHairAttribute( ctl, hairSystem ):
    
    hairSystem = sgModelDag.getNodeFromHistory( hairSystem, 'hairSystem' )[0]
    
    try:addAttr( ctl, ln='________', en='Hair:', cb=1 )
    except:pass
    
    addAttr( ctl, ln='dynamicOn', min=0, max=1, at='long', cb=1 )
    addAttr( ctl, ln='startFrame', at='long', cb=1, dv=1 )
    if cmds.isConnected( ctl+'.startFrame', hairSystem+'.startFrame' ):
        return None
    addAttr( ctl, ln='attraction', min=0, max=1, dv=1, k=1 )
    addAttr( ctl, ln='attracDamp', min=0, max=1, dv=0.2, k=1 )
    addAttr( ctl, ln='stiffness', min=0, max=1, dv=0.15, k=1 )
    addAttr( ctl, ln='damp', min=0, max=1, dv=0.15, k=1 )
    addAttr( ctl, ln='mass', min=0.1, dv=1, k=1 )
    addAttr( ctl, ln='drag', min=0, dv=0.05, k=1 )
    
    condition = cmds.createNode( 'condition' )
    cmds.setAttr( condition+'.secondTerm', 0 )
    cmds.setAttr( condition+'.colorIfTrueR', 1 )
    cmds.setAttr( condition+'.colorIfFalseR', 3 )
    
    cmds.connectAttr( ctl+'.dynamicOn', condition+'.firstTerm' )
    cmds.connectAttr( ctl+'.startFrame', hairSystem+'.startFrame', f=1 )
    cmds.connectAttr( condition+'.outColorR', hairSystem+'.simulationMethod' )
    cmds.connectAttr( ctl+'.attraction', hairSystem+'.startCurveAttract' )
    cmds.connectAttr( ctl+'.damp', hairSystem+'.attractionDamp' )
    cmds.connectAttr( ctl+'.mass', hairSystem+'.mass' )
    cmds.connectAttr( ctl+'.drag', hairSystem+'.drag' )


def copyAttribute( firstAttr, second ):
    
    first, attr = firstAttr.split( '.' )
    
    keyAttrs = cmds.listAttr( first, k=1 )
    cbAttrs  = cmds.listAttr( first, cb=1 )
    
    if not cmds.attributeQuery( attr, node=second, ex=1 ):
        attrType = cmds.attributeQuery( attr, node=first, at=1 )
        
        if attrType == 'enum':
            enumList = cmds.attributeQuery( attr, node=first, le=1 )
            cmds.addAttr( second, ln=attr, at=attrType, en= ':'.join( enumList ) + ':' )
        else:
            minValue = None
            maxValue = None
            if cmds.attributeQuery( attr, node=first, mne=1 ):
                minValue = cmds.attributeQuery( attr, node=first, min=1 )[0]
            if cmds.attributeQuery( attr, node=first, mxe=1 ):
                maxValue = cmds.attributeQuery( attr, node=first, max=1 )[0]
            if minValue != None and maxValue == None:
                cmds.addAttr( second, ln=attr, at=attrType, min=minValue )
            elif minValue == None and maxValue != None :
                cmds.addAttr( second, ln=attr, at=attrType, max=maxValue )
            elif minValue != None and maxValue != None :
                cmds.addAttr( second, ln=attr, at=attrType, min=minValue, max=maxValue )
            else:
                cmds.addAttr( second, ln=attr, at=attrType )
        
        if attr in keyAttrs:
            cmds.setAttr( second+'.'+attr, e=1, k=1 )
        elif attr in cbAttrs:
            cmds.setAttr( second+'.'+attr, e=1, cb=1 )



def removeMultiInstances( node, attr ):
    
    attrs = cmds.ls( node+'.'+attr+'[*]' )
    
    for attr in attrs:
        if not cmds.listConnections( attr, s=1, d=0 ):
            cmds.removeMultiInstance( attr )




def setJointLabel( objJoint ):
    
    import copy
    otherTypeString = copy.copy( objJoint )
    if objJoint.find( '_L_' ) != -1:
        cmds.setAttr( objJoint+'.side', 1 )
        otherTypeString = objJoint.replace( '_L_', '_' )
    elif objJoint.find( '_R_' ) != -1:
        cmds.setAttr( objJoint+'.side', 2 )
        otherTypeString = objJoint.replace( '_R_', '_' )
    
    cmds.setAttr( objJoint+'.type', 18 )
    cmds.setAttr( objJoint+'.otherType', otherTypeString, type='string' )




def addUnderbarAttribute( target, attrName ):
    
    defaultAttr = '___'
    
    for i in range( 5 ):
        pass