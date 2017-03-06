import maya.cmds as cmds
import maya.OpenMaya as om


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




def simpleAttrCopy( srcObj, trgObj ):
    
    attrInfos = getUdAttrInfo( srcObj )
    setUdAttrInfo( attrInfos, trgObj )





def getUdAttrInfo( targetObj ):
    
    import sgBModel_data
    return sgBModel_data.ObjectUdAttrInfos( targetObj )





def setUdAttrInfo( objectUdAttrInfos, targetObj ):
    
    import sgBModel_data
    import copy
    
    for attrInfo in objectUdAttrInfos.attrInfos:
        
        attr    = attrInfo.attr
        atType  = attrInfo.atType
        options = attrInfo.options
        value   = attrInfo.value
        
        atOptions = copy.copy( options ); atOptions.update({"at":atType})
        dtOptions = copy.copy( options ); dtOptions.update({"dt":atType})
        
        try: addAttr( targetObj, **atOptions )
        except: addAttr( targetObj, **dtOptions )
        
        try:cmds.setAttr( targetObj+'.'+attr, value )
        except:cmds.setAttr( targetObj+'.'+attr, value, type=atType )



def removeMultiInstances( node, attr ):
    
    attrs = cmds.ls( node+'.'+attr+'[*]' )
    
    for attr in attrs:
        if not cmds.listConnections( attr, s=1, d=0 ):
            cmds.removeMultiInstance( attr )



def copyAttribute( firstAttr, second ):
    
    try:first, attr = firstAttr.split( '.' )
    except:
        cmds.warning( "Copy Error Attr : %s" % firstAttr )
        return None
    
    keyAttrs = cmds.listAttr( first, k=1 )
    cbAttrs  = cmds.listAttr( first, cb=1 )
    if not keyAttrs: keyAttrs = []
    if not cbAttrs:  cbAttrs = []
    
    if not cmds.attributeQuery( attr, node=second, ex=1 ):
        attrType= cmds.addAttr( first+'.'+attr, q=1, at=1 )
        isColor = cmds.addAttr( first+'.'+attr, q=1, uac=1 )
        
        if attrType == 'typed':
            dt= cmds.addAttr( first+'.'+attr, q=1, dt=1 )[0]
            addAttr( second, ln=attr, dt=dt )
            value = cmds.getAttr( first+'.'+attr )
            if value:
                cmds.setAttr( second+'.'+attr, value, type=dt )
        else:
            if attrType == 'enum':
                enumList = cmds.attributeQuery( attr, node=first, le=1 )
                cmds.addAttr( second, ln=attr, at=attrType, en= ':'.join( enumList ) + ':' )
            elif isColor:
                cmds.addAttr( second, ln=attr, at=attrType, uac=1, k=1 )
                cmds.addAttr( second, ln=attr+'R', at='float', p=attr, k=1 )
                cmds.addAttr( second, ln=attr+'G', at='float', p=attr, k=1 )
                cmds.addAttr( second, ln=attr+'B', at='float', p=attr, k=1 )
                attrValues = cmds.getAttr( second+'.'+attr )[0]
                cmds.setAttr( second+'.'+attr, *attrValues, type= attrType )
                print second, cmds.getAttr( second+'.'+attr )
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
    
    attrType= cmds.addAttr( first+'.'+attr, q=1, at=1 )
    if attrType == 'typed':
        dt= cmds.addAttr( first+'.'+attr, q=1, dt=1 )[0]
        addAttr( second, ln=attr, dt=dt )
        value = cmds.getAttr( first+'.'+attr )
        if value:
            cmds.setAttr( second+'.'+attr, value, type=dt )
    else:
        try:cmds.setAttr( second+'.'+attr, cmds.getAttr( firstAttr ) )
        except:
            cmds.warning( "Error Attr : %s" % attr )



def setAniColor( targets ):
    
    import sgBModel_data
    import sgBFunction_dag
    
    for target in targets:
        shape = sgBFunction_dag.getShape( target )
        cmds.setAttr( shape+'.overrideEnabled', True )
        cmds.setAttr( shape+'.overrideColor', sgBModel_data.setAniColorNum )
        
    sgBModel_data.setAniColorNum = ( sgBModel_data.setAniColorNum + 1 ) % 32
    
    if sgBModel_data.setAniColorNum in [ 16, 19 ]:
        sgBModel_data.setAniColorNum +=1


def setRandomColor( targets, each=True ):
    
    import sgBModel_data
    import sgBFunction_dag
    
    if each:
        for target in targets:
            shape = sgBFunction_dag.getShape( target )
            cmds.setAttr( shape+'.overrideEnabled', True )
            cmds.setAttr( shape+'.overrideColor', sgBModel_data.setAniColorNum )
            
            sgBModel_data.setAniColorNum = ( sgBModel_data.setAniColorNum + 1 ) % 32
            
            if sgBModel_data.setAniColorNum in [ 16, 19, 20, 1 ]:
                sgBModel_data.setAniColorNum +=1
    else:
        for target in targets:
            shape = sgBFunction_dag.getShape( target )
            cmds.setAttr( shape+'.overrideEnabled', True )
            cmds.setAttr( shape+'.overrideColor', sgBModel_data.setAniColorNum )



def copyFollicleAttribute( *args ):
    
    sels = cmds.ls( sl=1 )
    
    first = sels[0]
    others = sels[1:]
    
    import sgBModel_attribute
    import sgBFunction_dag
    
    first = sgBFunction_dag.getShape( first )
    if cmds.nodeType( first ) == 'nurbsCurve':
        first = sgBFunction_dag.getFollicleFromCurve( first )

    for i in range( len( others ) ):
        other = sgBFunction_dag.getShape( others[i] )
        if cmds.nodeType( other ) == 'nurbsCurve':
            other = sgBFunction_dag.getFollicleFromCurve( other )
        others[i] = other
    
    follicleRampAttrList = sgBModel_attribute.follicleRampAttrList

    follicleNormalAttrList = sgBModel_attribute.follicleNormalAttrList
    
    fnNode = om.MFnDependencyNode( sgBFunction_dag.getMObject( first ) )
    
    rampAttrNames = []
    rampValues    = []
    
    for rampAttr in follicleRampAttrList:
        plugAttr = fnNode.findPlug( rampAttr )
        
        for other in others:
            removeMultiInstances( other, rampAttr )
         
        for j in range( plugAttr.numElements() ):
            rampAttrNames.append( plugAttr[j].name().split( '.' )[-1] )
            rampValues.append( cmds.getAttr( plugAttr[j].name() )[0] )
    
    for other in others:
        for i in range( len( rampAttrNames ) ):
            cmds.setAttr( other+'.'+rampAttrNames[i], *rampValues[i] )
    
    for normalAttr in follicleNormalAttrList:
        attrValue = cmds.getAttr( first+'.'+normalAttr )
        for other in others:
            try:cmds.setAttr( other+'.'+normalAttr, attrValue )
            except:pass



def copySgWobbleAttribute( *args ):
    
    sels = cmds.ls( sl=1 )
    
    others = sels[:-1]
    first = sels[-1]
    
    import sgBModel_attribute
    import sgBFunction_dag
    import sgBFunction_hair
    
    first = sgBFunction_dag.getShape( first )
    
    if cmds.nodeType( first ) == 'nurbsCurve':
        first = sgBFunction_hair.getSgWobbleCurve( first )

    for i in range( len( others ) ):
        other = sgBFunction_dag.getShape( others[i] )
        if cmds.nodeType( other ) == 'nurbsCurve':
            other = sgBFunction_hair.getSgWobbleCurve( other )
        others[i] = other
    
    wobbleRampAttrList = sgBModel_attribute.wobbleRampAttrList

    wobbleNormalAttrList = sgBModel_attribute.wobbleNormalAttrList
    
    fnNode = om.MFnDependencyNode( sgBFunction_dag.getMObject( first ) )
    
    rampAttrNames = []
    rampValues    = []
    
    for rampAttr in wobbleRampAttrList:
        plugAttr = fnNode.findPlug( rampAttr )
        
        for other in others:
            removeMultiInstances( other, rampAttr )
         
        for j in range( plugAttr.numElements() ):
            rampAttrNames.append( plugAttr[j].name().split( '.' )[-1] )
            rampValues.append( cmds.getAttr( plugAttr[j].name() )[0] )
    
    for other in others:
        for i in range( len( rampAttrNames ) ):
            cmds.setAttr( other+'.'+rampAttrNames[i], *rampValues[i] )
    
    for normalAttr in wobbleNormalAttrList:
        attrValue = cmds.getAttr( first+'.'+normalAttr )
        for other in others:
            try:cmds.setAttr( other+'.'+normalAttr, attrValue )
            except:pass


def getChannelAttributeFromSelection():
    
    sma = cmds.channelBox( 'mainChannelBox', q=1, sma=1 )
    ssa = cmds.channelBox( 'mainChannelBox', q=1, ssa=1 )
    sha = cmds.channelBox( 'mainChannelBox', q=1, sha=1 )
    
    attrs = []
    if sma: attrs += sma
    if ssa: attrs += ssa
    if sha: attrs += sha
    
    return attrs



def copyShapeAttr( source, target, ud=False ):
    import sgBFunction_dag
    
    sourceShape = sgBFunction_dag.getShape( source )
    targetShape = sgBFunction_dag.getShape( target )
    
    udAttrs = cmds.listAttr( sourceShape, ud=1 )
    fpAttrs = cmds.listAttr( sourceShape, fp=1 )
    
    attrs = []
    if udAttrs:
        attrs += udAttrs
    if fpAttrs:
        attrs += fpAttrs
    
    for attr in attrs:
        if attr.find( '.' ) != -1: continue
        if not cmds.attributeQuery( attr, node = sourceShape, writable=1  ): continue
        copyAttribute( sourceShape+'.'+attr, targetShape )