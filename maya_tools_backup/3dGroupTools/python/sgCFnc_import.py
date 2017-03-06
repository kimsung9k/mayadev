import maya.cmds as cmds
import maya.OpenMaya as om


def import_transformsBake( fileName=None ):
    
    import sgBFunction_fileAndPath
    import sgFunctionDag
    import cPickle

    if not fileName:
        defaultExportTransformBakePath = sgBFunction_fileAndPath.getMayaDocPath() + '/defaultExportTransformsBake.txt'
        f = open( defaultExportTransformBakePath, 'r' )
        fileName = cPickle.load( f )
    
    f = open( fileName, 'r' )
    datas = cPickle.load( f )
    f.close()
    
    unit, minFrame, maxFrame = datas[:3]

    imTargets = datas[3:]

    cmds.currentUnit( time= unit )
    
    for imTarget, targetMtxs in imTargets:
        if not cmds.objExists( imTarget ):
            sgFunctionDag.makeTransform( imTarget )
    
    for imTarget, targetMtxs in imTargets:
        
        attrs = cmds.listAttr( imTarget, k=1 )
        animCurves = []
        for k in range( len( attrs ) ):
            targetAttr = imTarget + '.' + attrs[k]
            at = cmds.attributeQuery( attrs[k], node=imTarget, at=1 )
            animCurveType='animCurveTU'
            if at == 'doubleLinear':
                animCurveType = 'animCurveTL'
            elif at == 'doubleAngle':
                animCurveType = 'animCurveTA'
            animCurve = cmds.createNode( animCurveType, n=targetAttr.split( '|' )[-1].replace( '.', '_' ) )
            animCurves.append( animCurve )
        
        for time in range( int( minFrame ), int( maxFrame+1 ) ):
            i = time - int( minFrame )
            cmds.xform( imTarget, os=1, matrix= targetMtxs[i] )
            for k in range( len( attrs ) ):
                targetAttr = imTarget + '.' + attrs[k]
                targetAttrValue= cmds.getAttr( targetAttr )
                animCurve  = animCurves[k]
                cmds.setKeyframe( animCurves[k], t=i, v=targetAttrValue )
        
        for k in range( len( attrs ) ):
            targetAttr = imTarget + '.' + attrs[k]
            cmds.connectAttr( animCurves[k]+'.output', targetAttr )
    
    cmds.select( imTargets[-1][0] )