import maya.cmds as cmds


def addPositionBasedController( controller, relative=True ):
    
    import sgBFunction_connection
    import sgBFunction_attribute
    import sgCFnc_connection
    
    controllerName = controller.split( '|' )[-1]
    
    controllerP = cmds.listRelatives( controller, p=1, f=1 )[0]
    replaceObj = cmds.createNode( 'transform', n=controllerName + '_replace' )
    
    replaceObj = cmds.parent( replaceObj, controllerP )[0]
    
    cmds.xform( replaceObj, ws=1, matrix= cmds.getAttr( controller+'.wm' ) )
    sgBFunction_connection.getSourceConnection( controller, replaceObj )
    
    outputCons, inputCons = sgCFnc_connection.getSourceConnection( controller )
    
    for i in range( len( outputCons ) ):
        cmds.disconnectAttr( outputCons[i], inputCons[i] )
    
    locC  = cmds.createNode( 'transform', n='locC' )
    locCR = cmds.createNode( 'transform', n='locCR' )
    locCS = cmds.createNode( 'transform', n='locCS' )
    loc = cmds.spaceLocator()[0]
    locP = cmds.group( loc )
    pivCtl = cmds.createNode( 'transform' );cmds.setAttr( pivCtl + '.dh', 1 )
    locBase = cmds.group( locP, pivCtl )
    
    locC, locCR, locCS = cmds.parent( locC, locCR, locCS, loc )
    
    cmds.connectAttr( pivCtl + '.t',  locP + '.t' )
    cmds.connectAttr( pivCtl + '.r',  locP + '.r' )
    cmds.connectAttr( pivCtl + '.s',  locP + '.s' )
    cmds.connectAttr( pivCtl + '.sh', locP + '.sh' )
    
    mmdcLocCR = cmds.createNode( 'multMatrixDecompose' )
    cmds.connectAttr( locBase + '.wm', mmdcLocCR + '.i[0]' )
    cmds.connectAttr( pivCtl + '.wim', mmdcLocCR + '.i[1]' )
    cmds.connectAttr( mmdcLocCR + '.ot', locCR + '.t' )
    cmds.connectAttr( mmdcLocCR + '.or', locCR + '.r' )
    cmds.connectAttr( mmdcLocCR + '.os', locCR + '.s' )
    cmds.connectAttr( mmdcLocCR + '.osh', locCR + '.sh' )
    
    mmdcLocCS = cmds.createNode( 'multMatrixDecompose' )
    cmds.connectAttr( replaceObj + '.wm',  mmdcLocCS + '.i[0]' )
    cmds.connectAttr( loc  + '.wim', mmdcLocCS + '.i[1]' )
    cmds.connectAttr( mmdcLocCS + '.ot', locCS + '.t' )
    cmds.connectAttr( mmdcLocCS + '.or', locCS + '.r' )
    cmds.connectAttr( mmdcLocCS + '.os', locCS + '.s' )
    cmds.connectAttr( mmdcLocCS + '.osh', locCS + '.sh' )
    
    blendMtx = cmds.createNode( 'blendTwoMatrixDecompose' )
    blendCS  = cmds.createNode( 'blendColors' )
    blendCSH = cmds.createNode( 'blendColors' )
    mmdcOutput = cmds.createNode( 'multMatrixDecompose' )
    
    cmds.connectAttr(  locCR + '.s',  blendCS  + '.color1' )
    cmds.connectAttr(  locCS + '.s',  blendCS  + '.color2' )
    cmds.connectAttr(  locCR + '.sh', blendCSH + '.color1' )
    cmds.connectAttr(  locCS + '.sh', blendCSH + '.color2' )
    
    cmds.connectAttr( locCS + '.m', blendMtx + '.inMatrix1' )
    cmds.connectAttr( locCR + '.m', blendMtx + '.inMatrix2' )
    cmds.connectAttr( blendMtx + '.ot',  locC + '.t' )
    cmds.connectAttr( blendMtx + '.or',  locC + '.r' )
    cmds.connectAttr( blendCS + '.output',  locC + '.s' )
    cmds.connectAttr( blendCSH + '.output', locC + '.sh' )
    
    cmds.connectAttr( locC + '.wm', mmdcOutput + '.i[0]' )
    cmds.connectAttr( controller+'.pim',       mmdcOutput + '.i[1]' )
    cmds.connectAttr( mmdcOutput + '.ot',  controller+'.t' )
    cmds.connectAttr( mmdcOutput + '.or',  controller+'.r' )
    cmds.connectAttr( mmdcOutput + '.os',  controller+'.s' )
    cmds.connectAttr( mmdcOutput + '.osh', controller+'.sh' )
    
    sgBFunction_attribute.addAttr( loc, ln='blend', min=0, max=1, dv=1, k=1 )
    cmds.connectAttr( loc + '.blend', blendMtx + '.attributeBlender' )
    cmds.connectAttr( loc + '.blend', blendCS + '.blender' )
    cmds.connectAttr( loc + '.blend', blendCSH + '.blender' )

    if relative: sgBFunction_connection.constraintAll( replaceObj, locBase )
    else: cmds.xform( locBase, ws=1, matrix= cmds.getAttr( replaceObj + '.wm' ) )


