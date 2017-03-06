import maya.cmds as cmds


def createBJT_from_RJT( rjts ):
    
    import sgBFunction_convert
    
    rjts = sgBFunction_convert.singleToList( rjts )
    
    for rjt in rjts:
        
        if cmds.objExists( rjt.replace( '_RJT', '_BJT' ) ):
            cmds.warning( "%s is aleady exists." % rjt.replace( '_RJT', '_BJT' ) )
            continue
        
        rjtP = cmds.listRelatives( rjt, p=1, f=1 )[0]
        targetP = cmds.listConnections( rjtP+'.t' )[0]
        cmds.select( targetP )
        target = cmds.joint()
        target = cmds.rename( target, rjt.replace( '_RJT', '_BJT' ) )
        cmds.connectAttr( rjt+'.t', target+'.t' )
        cmds.connectAttr( rjt+'.r', target+'.r' )




def exportCharacter( setGroup, exportPath=None ):
    
    import cPickle
    import sgBFunction_fileAndPath
    import sgBFunction_dag
    
    topTransforms = sgBFunction_dag.getTopTransformNodes()
    hidedObjs = []
    for topTransform in topTransforms:
        if cmds.getAttr( topTransform + '.v' ):
            try:
                cmds.setAttr( topTransform + '.v', 0 )
                hidedObjs.append( topTransform )
            except:pass
    cmds.showHidden( setGroup, a=1 )

    sceneName = cmds.file( q=1, sceneName=1 )
    sceneFolderName = '/'.join( sceneName.split( '/' )[:-1] )
    ns = setGroup.replace( 'SET', '' )
    
    if not exportPath:
        fileName = sceneFolderName + '/' + ns.replace( ':', '_' ) +'.txt'
        print fileName
    else:
        fileName = exportPath
    
    children = sgBFunction_dag.getChildrenCurveExists( setGroup )

    targetCtls = []
    for child in children:
        childName = child.split( '|' )[-1]
        
        if childName.lower().find( 'ctl' ) == -1: continue
        
        refConExists = False
        
        attrs = cmds.listAttr( child, k=1 )
        srcCons = []
        for attr in attrs:
            cons = cmds.listConnections( child + '.' + attr, s=1, d=0 )
            if not cons: cons = []
            parentAttrs = cmds.attributeQuery( attr, node=child, listParent=1 )
            if parentAttrs:
                consParent = cmds.listConnections( child + '.' + parentAttrs[0], s=1, d=0 )
                if consParent: cons += consParent
            if not cons: continue
            for con in cons:
                conNode = con.split( '.' )[0]
                if cmds.referenceQuery( conNode, inr=1 ): continue
                srcCons.append( con )

        for srcCon in srcCons:
            if cmds.referenceQuery( srcCon, inr=1 ):
                refConExists=True
                break
        
        if refConExists: continue

        attrs = cmds.listAttr( child, k=1 )
        targetCtls.append( [childName.replace( ns, '' ), attrs] )

    minFrame= int( cmds.playbackOptions( q=1, min=1 ) )
    maxFrame= int( cmds.playbackOptions( q=1, max=1 ) )
    
    framesCtlsValues = []
    for i in range( minFrame, maxFrame+1 ):
        cmds.currentTime( i )
        
        ctlsValues = []
        for targetCtl, attrs in targetCtls:
            
            targetCtl = ns + targetCtl
            ctlValues = []
            for attr in attrs:
                value = cmds.getAttr( targetCtl + '.' + attr )
                ctlValues.append( value )
            ctlsValues.append( ctlValues )
        framesCtlsValues.append( ctlsValues )
    
    for hideObj in hidedObjs:
        cmds.setAttr( hideObj + '.v', 1 )
    
    data = ( minFrame, maxFrame, targetCtls, framesCtlsValues )
    
    print "fileName : ", fileName
    f = open( fileName, 'w' )
    cPickle.dump( data, f )
    f.close()
    
    mayaDoc = sgBFunction_fileAndPath.getMayaDocPath()
    defaultBakePath = mayaDoc + '/defaultCharacterBakePath.txt'
    
    f = open( defaultBakePath, 'w' )
    f.write( fileName )
    f.close()




def importCharacter( setGroup, importPath=None, *skipTargets ):

    import cPickle
    import sgBFunction_fileAndPath
    
    ns = setGroup.replace( 'SET', '' )
    
    mayaDoc = sgBFunction_fileAndPath.getMayaDocPath()
    
    if not importPath:
        defaultBakePath = mayaDoc + '/defaultCharacterBakePath.txt'
        
        f = open( defaultBakePath, 'r' )
        path = f.read()
        f.close()
    else:
        path = importPath
    
    f = open( path, 'r' )
    data = cPickle.load( f )
    f.close()
    
    minFrame, maxFrame, targetCtls, framesCtlsValues = data

    for j in range( len( targetCtls ) ):
        targetCtl, attrs = targetCtls[j]
        
        if len( cmds.ls( targetCtl ) ) > 1:
            cmds.warning( 'More than one object matches name: %s' % targetCtl )
            continue
        
        isSkipTarget = False
        for skipTarget in skipTargets:
            if targetCtl.find( skipTarget ) != -1:
                print "skip target: ", targetCtl
                isSkipTarget = True;break
        if isSkipTarget: continue
        
        targetCtl = ns + targetCtl
        
        if not cmds.objExists( targetCtl ):
            print "%s is not exists" % targetCtl
            continue
        
        for k in range( len( attrs ) ):
            targetAttr = targetCtl + '.' + attrs[k]
            if not cmds.attributeQuery( attrs[k], node=targetCtl, ex=1 ): continue
            at = cmds.attributeQuery( attrs[k], node=targetCtl, at=1 )
            animCurveType='animCurveTU'
            if at == 'doubleLinear':
                animCurveType = 'animCurveTL'
            elif at == 'doubleAngle':
                animCurveType = 'animCurveTA'
            
            animCurve = cmds.createNode( animCurveType, n=targetAttr.replace( ':', '_' ).replace( '.', '_' ) )
            
            for i in range( minFrame, maxFrame+1 ):
                targetAttrValue = framesCtlsValues[i-minFrame][j][k]
                if type( targetAttrValue ) == type([]): continue
                cmds.setKeyframe( animCurve, t=i, v=targetAttrValue )
            
            try:
                cmds.connectAttr( animCurve + '.output', targetAttr, f=1 )
            except:
                cmds.delete( animCurve )
                print "failed connect %s" % targetAttr



def bakeFKfromIK( setNode ):
    
    def setKeyFKCtls( setNode ):
        ns = setNode.split( '|' )[-1].replace( 'SET', '' )
        
        cuObjs = cmds.ls( ns + '*_*_CU*' )
        
        targetCUS = []
        targetFKS = []
        for cuObj in cuObjs:
            if cuObj.find( 'GRP' ) != -1: continue
            if int( cuObj[-1] ) > 4: continue
            targetCUS.append( cuObj )
            
            fkCtl = cuObj.replace( 'CU', 'FK' ) + '_CTL'
            if fkCtl.find( 'FK4' ) != -1:
                fkCtl = fkCtl.replace( 'FK4', 'FK3' )
            targetFKS.append( fkCtl )
    
        for i in range( len( targetCUS ) ):
            
            cu = targetCUS[i]
            fk = targetFKS[i]
            
            cmds.xform( fk, ws=1, matrix= cmds.getAttr( cu + '.wm' ) )
            cmds.setKeyframe( fk )
    
    ikCtl = setNode.replace( 'SET', 'Move_CTL' )
    
    animCurves = cmds.listConnections( ikCtl, s=1, d=0, type='animCurveTL' )
    
    timeList = cmds.keyframe( animCurves[0], q=1, tc=1 )
    minTime = timeList[0]
    maxTime = timeList[-1]
    
    for i in range( int( minTime ), int( maxTime ) ):
        cmds.currentTime( i )
        setKeyFKCtls( setNode )



def constraintCtlToMoc( worldCtl, mocLoc ):
    
    nsCtl =  worldCtl.replace( 'World_CTL', '' )
    nsMoc  = mocLoc.replace( 'All_Moc', '' )
    
    locList = [ 'All_Moc',
                'Root_MOC', 'Root_MOCSep', 'Waist_MOC', 'Chest_MOCSep', 'Chest_MOC',
                'Collar_SIDE_MOC', 'Shoulder_SIDE_MOC', 'Elbow_SIDE_MOC', 'Wrist_SIDE_MOC',
                'Neck_MOC', 'NeckMiddle_MOC', 'Head_MOC',
                'Hip_SIDE_MOC', 'Knee_SIDE_MOC', 'Ankle_SIDE_MOC',
                'Thumb_INDEX_SIDE_MOC', 'Index_INDEX_SIDE_MOC', 'Middle_INDEX_SIDE_MOC', 'Ring_INDEX_SIDE_MOC', 'Pinky_INDEX_SIDE_MOC' ]
    
    ctlList = [ 'World_CTL',
                'Spline0_BJT', 'Spline1_BJT', 'Spline2_BJT', 'Spline3_BJT', 'Spline4_BJT',
                'Collar_SIDE_CTL', 'Arm_SIDE_CU0', 'Arm_SIDE_CU1', 'Arm_SIDE_CU2',
                'Neck_CTL', 'NeckMiddle_CTL', 'Head_CTL',
                'Leg_SIDE_CU0', 'Leg_SIDE_CU1', 'Leg_SIDE_CU2',
                'Thumb_INDEX_SIDE_BJT', 'Index_INDEX_SIDE_BJT', 'Middle_INDEX_SIDE_BJT', 'Ring_INDEX_SIDE_BJT', 'Pinky_INDEX_SIDE_BJT' ]
    
    for loc, ctl in zip( locList, ctlList ):
        if loc.find( '_SIDE_' ) != -1:
            locStr = nsMoc + loc.replace( '_SIDE_', '_*_' )
            ctlStr = nsCtl + ctl.replace( '_SIDE_', '_*_' )
                
            if locStr.find( '_INDEX_' ) != -1:
                locStr = locStr.replace( '_INDEX_', '*_' )
                ctlStr = ctlStr.replace( '_INDEX_', '*_' )
        else:
            locStr = nsMoc + loc
            ctlStr = nsCtl + ctl
        
        locList = cmds.ls( locStr )
        ctlList = cmds.ls( ctlStr )
        
        for locResult, ctlResult in zip( locList, ctlList ):
            if locResult.find( 'Ball_' ) != -1:
                cmds.select( ctlResult )
                childJnt = cmds.joint()
                cmds.setAttr( childJnt + '.ry', 90 )
                ctlResult = childJnt 
            cmds.parentConstraint( ctlResult, locResult )


def bakeMoc( mocLoc ):
    
    import sgBFunction_dag
    
    targetLocs = sgBFunction_dag.getChildrenJointExists( mocLoc )
    targetLocs.append( mocLoc )
    
    cmds.select( targetLocs )
    minFrame = cmds.playbackOptions( q=1, min=1 )
    maxFrame = cmds.playbackOptions( q=1, max=1 )
    cmds.bakeResults( sm=True, t=(minFrame, maxFrame), sb=1, dic=True, pok=True, sac=False, removeBakedAttributeFromLayer=False, bakeOnOverrideLayer=False, cp=False, s=True)