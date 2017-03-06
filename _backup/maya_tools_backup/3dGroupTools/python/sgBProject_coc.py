import maya.cmds as cmds


def removeUiSeparateView( cam ):
    
    import sgBFunction_attribute
    import sgBFunction_dag
    
    uiPrefix = 'separatedViewCam_'
    
    uis = cmds.lsUI( wnd=1 )
    for ui in uis:
        if not len( ui ) > len( uiPrefix ): continue
        if ui[ : len( uiPrefix ) ] != uiPrefix: continue
        cmds.deleteUI( ui, wnd=1 )
    
    if not cmds.objExists( cam ): return None
    
    for cam in cmds.ls( type='camera' ):
        if not cmds.objExists( cam ): continue
        cam = sgBFunction_dag.getTransform( cam )
        sgBFunction_attribute.addAttr( cam, ln='filmTranslateCams', at='message' )
        sgBFunction_attribute.addAttr( cam, ln='aniamtionCam', at='message' )
        cons1 = cmds.listConnections( cam+'.filmTranslateCams', d=1, s=0 )
        cons2 = cmds.listConnections( cam+'.aniamtionCam', d=1, s=0 )

        if cons1: cmds.delete( cons1 )
        if cons2: cmds.delete( cons2 )



def createUiSeparactedViewGroup( cam, width, height, sgw, sgh, sw, sh, scale, createWindow=False ):

    import sgBModel_ui
    import sgBFunction_dag
    import sgBFunction_attribute
    
    uiPrefixMain = 'separatedViewCam_'
    removeUiSeparateView( cam )
    
    camShape = sgBFunction_dag.getShape( cam )
    if cmds.nodeType( camShape ) != 'camera': return None
    
    aspectRatio = float( height )/ width
    
    sepWidthValue = 1.0 / sgw
    gWidthValue  = -( 1.0 + sepWidthValue )
    gWidthValues = []
    for i in range( sgw ):
        gWidthValue += sepWidthValue * 2
        gWidthValues.append( gWidthValue )
    
    sepHeightValue = 1.0 / sgh
    gHeightValue = -( 1.0 + sepHeightValue )
    gHeightValues = []
    for i in range( sgh ):
        gHeightValue += sepHeightValue * 2
        gHeightValues.append( gHeightValue  )
    
    if createWindow:
        windowWidth  = width * scale
        windowHeight = height * scale
        
        inst = sgBModel_ui.ModelEditorWindow( uiPrefixMain + cam, windowWidth, windowHeight, camera=cam, hud=0, 
                                              cameras=0, dynamics=0, ikHandles=0, nurbsCurves=0, textures=False, grid=False,
                                              da='smoothShaded' )
        inst.create()
        cmds.window( inst.winName, e=1, title='WMain')
        top, left = cmds.window( inst.winName, q=1, tlc=1 )
        
        eachResolutionWidth = float( windowWidth ) / sw / sgw
        eachResolutionHeight = float( windowHeight ) / sh / sgh
    
    def createUiSeparatedView( cam, width, height, indexW, indexH, sgw, sgh, sw, sh, scale, camNum, createWindow=False ):

        uiPrefix = 'separatedViewCam_%d_' % camNum

        sepWidthValue = 1.0 / sgw / sw
        filmTransWidthValue = gWidthValues[ indexW ] - 1.0/sgw - sepWidthValue
        filmTransWidthValues = []
        for i in range( sw ):
            filmTransWidthValue += sepWidthValue * 2
            filmTransWidthValues.append( filmTransWidthValue )
        
        sepHeightValue = 1.0 / sgh / sh
        filmTransHeightValue = gHeightValues[ indexH ] - 1.0/sgh - sepHeightValue
        filmTransHeightValues = []
        for i in range( sh ):
            filmTransHeightValue += sepHeightValue * 2
            filmTransHeightValues.append( filmTransHeightValue * aspectRatio )
        
        targetCams = []
        tlcList    = []
        
        scaleValue = sw * sgw
        
        offsetWidth  = width / sgw * indexW
        offsetHeight = height / sgh * indexH
        
        animationCam = cmds.duplicate( cam, n= cam + '_animation_%d_%d' %( indexW, indexH ) )[0]
        aniCamShape  = sgBFunction_dag.getShape( animationCam )
        cmds.setAttr( aniCamShape+'.displayResolution', 0 )
        cmds.setAttr( aniCamShape+'.displayGateMask', 0 )
        cmds.setAttr( aniCamShape+'.postScale', scaleValue )
        cmds.setAttr( aniCamShape+'.filmFit', 1 )
        sgBFunction_attribute.addAttr( animationCam, ln='mainCam', at='message' )
        cmds.connectAttr( cam+'.aniamtionCam', animationCam+'.mainCam' )
        cmds.setAttr( aniCamShape+'.overscan', 1 )
        
        for i in range( len( filmTransHeightValues ) ):
            for j in range( len( filmTransWidthValues ) ):
                duCam = cmds.duplicate( cam, n= cam + '_translate_G_%d_%d_%02d_%02d' % ( indexW, indexH, i+1 , j+1 ) )[0]
                sgBFunction_attribute.addAttr( duCam, ln='mainCam', at='message' )
                cmds.connectAttr( cam+'.filmTranslateCams', duCam+'.mainCam' )
                duCamShape = sgBFunction_dag.getShape( duCam )
                cmds.setAttr( duCamShape+'.overscan', 1 )
                cmds.setAttr( duCamShape+'.displayResolution', 0 )
                cmds.setAttr( duCamShape+'.displayGateMask', 0 )
                cmds.setAttr( duCamShape+'.postScale', scaleValue )
                cmds.setAttr( duCamShape+'.filmFit', 1 )
                cmds.setAttr( duCamShape + '.filmTranslateH', filmTransWidthValues[j] )
                cmds.setAttr( duCamShape + '.filmTranslateV', -filmTransHeightValues[i] )
                cuFrame = i * len( filmTransWidthValues ) + j + 1
                #print "frame : %02d, %5.2f, %5.2f" %( cuFrame, filmTransWidthValues[j], -filmTransHeightValues[i] )
                cmds.setKeyframe( animationCam + '.filmTranslateH', t= cuFrame, v= filmTransWidthValues[j] )
                cmds.setKeyframe( animationCam + '.filmTranslateV', t= cuFrame, v=-filmTransHeightValues[i] )
                targetCams.append( duCam )
                tlcValue = [ int( ( (filmTransHeightValues[i]-filmTransHeightValues[0])*width/2 )*scale) + 23, 
                             int( ( (filmTransWidthValues[j]-filmTransWidthValues[0])*width/2 )*scale)+1 ]
                tlcList.append( tlcValue )
        
        
        if createWindow:
            for i in range( len( targetCams ) ):
                winName = uiPrefix + targetCams[i]
                tlc = tlcList[i]
                tlc[0] += top + offsetHeight *scale
                tlc[1] += left + offsetWidth *scale
                inst = sgBModel_ui.ModelEditorWindow( winName, eachResolutionWidth, eachResolutionHeight, tlc, False, camera=targetCams[i], hud=0, 
                                                  cameras=0, dynamics=0, ikHandles=0, nurbsCurves=0, textures=False, grid=False,
                                                  da='smoothShaded' )
                inst.create()
            
            tlc = tlcList[ 0 ]
            tlc[0] -= 23
            
            inst = sgBModel_ui.ModelEditorWindow( uiPrefix + animationCam, eachResolutionWidth, eachResolutionHeight, tlc, True, False, camera=animationCam, hud=0, 
                                                  cameras=0, dynamics=0, ikHandles=0, nurbsCurves=0, textures=False, grid=False,
                                                  da='smoothShaded' )
            inst.create()
            cmds.window( inst.winName, e=1, title='WCA_%d_%d' %( indexW, indexH ) ) 
        
        minFrame = 1
        maxFrame = len( filmTransHeightValues ) * len( filmTransWidthValues )
        cmds.playbackOptions( min=minFrame )
        cmds.playbackOptions( max=maxFrame )
        cmds.currentTime( minFrame )
    
    for i in range( len( gHeightValues ) ):
        for j in range( len( gWidthValues ) ):
            createUiSeparatedView( cam, width, height, j, i, sgw, sgh, sw, sh, scale, 0, createWindow )