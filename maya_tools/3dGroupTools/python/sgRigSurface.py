import maya.cmds as cmds
import sgRigAttribute
import sgModelDg, sgModelDag



def createRoofPointers( surface, numPointer, aimDirection = 'v', roofLength = 10 ):

    surface      = sgModelDag.getTransform( surface )
    surfaceShape = sgModelDag.getShape( surface )
    
    dStr = aimDirection.upper()
    if dStr == 'V':
        upStr = 'U'
    else:
        upStr = 'V'
    
    sgRigAttribute.addAttr( surface, ln='roofValue', k=1 )
    
    minValue, maxValue = cmds.getAttr( surfaceShape+'.minMaxRange%s' % ( dStr ) )[0]
    
    eachInputOffset = float( roofLength ) / ( numPointer-1 )
    
    for i in range( numPointer ):
        surfaceInfo = cmds.createNode( 'pointOnSurfaceInfo' )
        pointer = cmds.createNode( 'transform', n= surface+'_pointer%d' % i )
        cmds.setAttr( pointer+'.dh', 1 )
        cmds.setAttr( pointer+'.dla', 1 )
        cmds.connectAttr( surfaceShape+'.local', surfaceInfo+'.inputSurface' )
        
        addNode = cmds.createNode( 'addDoubleLinear' )
        cmds.setAttr( addNode+'.input2', eachInputOffset * i )
        
        animCurve = sgModelDg.getRoofLinearCurve( 0, float( roofLength ), minValue, maxValue )
        
        cmds.connectAttr( surface+'.roofValue', addNode+'.input1' )
        cmds.connectAttr( addNode+'.output', animCurve+'.input' )
        cmds.connectAttr( animCurve+'.output', surfaceInfo+'.parameter%s' %( dStr ) )
        
        fbfMtx = cmds.createNode( 'fourByFourMatrix' )
        vProduct = cmds.createNode( 'vectorProduct' )
        mmdc = cmds.createNode( 'multMatrixDecompose' )
        
        cmds.setAttr( vProduct+'.op', 2 )
        
        cmds.connectAttr( surfaceInfo + '.tangent%sx' % ( dStr ), fbfMtx+'.i00'  )
        cmds.connectAttr( surfaceInfo + '.tangent%sy' % ( dStr ), fbfMtx+'.i01'  )
        cmds.connectAttr( surfaceInfo + '.tangent%sz' % ( dStr ), fbfMtx+'.i02'  )
        cmds.connectAttr( surfaceInfo + '.tangent%sx' % ( upStr ), fbfMtx+'.i10'  )
        cmds.connectAttr( surfaceInfo + '.tangent%sy' % ( upStr ), fbfMtx+'.i11'  )
        cmds.connectAttr( surfaceInfo + '.tangent%sz' % ( upStr ), fbfMtx+'.i12'  )
        cmds.connectAttr( surfaceInfo + '.positionX', fbfMtx+'.i30'  )
        cmds.connectAttr( surfaceInfo + '.positionY', fbfMtx+'.i31'  )
        cmds.connectAttr( surfaceInfo + '.positionZ', fbfMtx+'.i32'  )
        cmds.connectAttr( surfaceInfo+'.tangent%s' % ( dStr ), vProduct+'.input1' )
        cmds.connectAttr( surfaceInfo+'.tangent%s' % ( upStr ), vProduct+'.input2' )
        cmds.connectAttr( vProduct+'.outputX', fbfMtx+'.i20' )
        cmds.connectAttr( vProduct+'.outputY', fbfMtx+'.i21' )
        cmds.connectAttr( vProduct+'.outputZ', fbfMtx+'.i22' )
        
        cmds.connectAttr( fbfMtx+'.output', mmdc+'.i[0]' )
        cmds.connectAttr( pointer+'.pim', mmdc+'.i[1]' )
        
        cmds.connectAttr( mmdc+'.ot', pointer+'.t' )
        cmds.connectAttr( mmdc+'.or', pointer+'.r' )
        
        cmds.parent( pointer, surface )



def createRivetOnSurfacePoint( surfacePoint, firstDirection='u' ):
    
    import sgBFunction_attribute
    
    if firstDirection.lower() == 'u':
        fString = 'U'
        sString = 'V'
    else:
        fString = 'V'
        sString = 'U'
    
    surfaceName, uv = surfacePoint.split( '.uv' )
    
    surfaceName = sgModelDag.getShape( surfaceName )
    
    uvSplits = uv.split( '][' )
    
    uValue = float( uvSplits[0].replace( '[', '' ) )
    vValue = float( uvSplits[1].replace( ']', '' ) )
    
    pointOnSurf = cmds.createNode( 'pointOnSurfaceInfo' )
    vectorNode  = cmds.createNode( 'vectorProduct' )
    fbfNode     = cmds.createNode( 'fourByFourMatrix' )
    mmdcNode    = cmds.createNode( 'multMatrixDecompose' )
    rivetNode   = cmds.createNode( 'transform' )
    
    cmds.setAttr( pointOnSurf+'.u', uValue )
    cmds.setAttr( pointOnSurf+'.v', vValue )
    cmds.setAttr( vectorNode+'.operation', 2 )
    cmds.setAttr( rivetNode+'.dla',1 )
    cmds.setAttr( rivetNode+'.dh', 1 )
    
    cmds.connectAttr( surfaceName +'.worldSpace[0]', pointOnSurf+'.inputSurface' )
    cmds.connectAttr( pointOnSurf+'.tangent%s' % fString, vectorNode+'.input1' )
    cmds.connectAttr( pointOnSurf+'.tangent%s' % sString, vectorNode+'.input2' )
    
    cmds.connectAttr( pointOnSurf+'.tangent%sx' % fString, fbfNode+'.i00' )
    cmds.connectAttr( pointOnSurf+'.tangent%sy' % fString, fbfNode+'.i01' )
    cmds.connectAttr( pointOnSurf+'.tangent%sz' % fString, fbfNode+'.i02' )
    cmds.connectAttr( pointOnSurf+'.tangent%sx' % sString, fbfNode+'.i10' )
    cmds.connectAttr( pointOnSurf+'.tangent%sy' % sString, fbfNode+'.i11' )
    cmds.connectAttr( pointOnSurf+'.tangent%sz' % sString, fbfNode+'.i12' )
    cmds.connectAttr( vectorNode+'.outputX', fbfNode+'.i20' )
    cmds.connectAttr( vectorNode+'.outputY', fbfNode+'.i21' )
    cmds.connectAttr( vectorNode+'.outputZ', fbfNode+'.i22' )
    cmds.connectAttr( pointOnSurf+'.positionX', fbfNode+'.i30' )
    cmds.connectAttr( pointOnSurf+'.positionY', fbfNode+'.i31' )
    cmds.connectAttr( pointOnSurf+'.positionZ', fbfNode+'.i32' )
    
    cmds.connectAttr( fbfNode+'.output', mmdcNode+'.i[0]' )
    cmds.connectAttr( rivetNode+'.pim',  mmdcNode+'.i[1]' )
    cmds.connectAttr( mmdcNode+'.ot',  rivetNode+'.t' )
    cmds.connectAttr( mmdcNode+'.or',  rivetNode+'.r' )
    
    sgBFunction_attribute.addAttr( rivetNode, ln='paramU', min=0, dv=uValue, k=1 )
    sgBFunction_attribute.addAttr( rivetNode, ln='paramV', min=0, dv=vValue, k=1 )
    
    cmds.connectAttr( rivetNode+'.paramU', pointOnSurf+'.u' )
    cmds.connectAttr( rivetNode+'.paramV', pointOnSurf+'.v' )