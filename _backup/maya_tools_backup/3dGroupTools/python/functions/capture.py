import maya.cmds as cmds
import maya.OpenMaya as om



def createUICam():
    
    cameraName = 'Cam_forCapture'
    
    if not cmds.objExists( cameraName ):
        sels = cmds.ls( sl=1 )
        cam =  cmds.camera( centerOfInterest = 5,
                            focalLength = 35,
                            lensSqueezeRatio = 1,
                            cameraScale = 1,
                            horizontalFilmAperture = 1.41732,
                            horizontalFilmOffset = 0,
                            verticalFilmAperture = 0.94488,
                            verticalFilmOffset = 0, filmFit = 'Fill',
                            overscan = 1, motionBlur = 0, shutterAngle=144,
                            nearClipPlane = 0.1, farClipPlane = 10000,
                            orthographic = 0, orthographicWidth=30, panZoomEnabled=0,
                            horizontalPan = 0, verticalPan = 0, zoom = 1 )[0]

        cam = cmds.rename( cam, cameraName )
        cmds.setAttr( cam+'.v', 0 )
        cameraName = cam
    
    return cameraName



def setCameraToSelObject():
    
    sels = cmds.ls( sl=1 )
    if not sels: return None
    
    cameraName = createUICam()
    print cameraName
    
    boundingBoxDist = 1.2

    topTransform = []
    for sel in sels:
        if cmds.nodeType( sel ) in ['joint', 'transform']:
            topTransform.append( sel )

    BBMIN = [ 100000, 100000, 100000]
    BBMAX = [-100000,-100000,-100000]

    for tr in topTransform:
        bbmin = cmds.getAttr( tr+'.boundingBoxMin' )[0]
        bbmax = cmds.getAttr( tr+'.boundingBoxMax' )[0]
        
        for i in range( 3 ):
            if bbmin[i] < BBMIN[i]:
                BBMIN[i] = bbmin[i]
            if bbmax[i] > BBMAX[i]:
                BBMAX[i] = bbmax[i]

    bbLength = (( BBMIN[0] - BBMAX[0] )**2 + ( BBMIN[1] - BBMAX[1] )**2 + ( BBMIN[2] - BBMAX[2] )**2)**0.5
    bbCenter = ( (BBMIN[0]+BBMAX[0])/2.0, (BBMIN[1]+BBMAX[1])/2.0, (BBMIN[2]+BBMAX[2])/2.0 )

    panel = cmds.getPanel( wf=1 )

    activeCam = 'persp'
    if "modelPanel" == cmds.getPanel( to=panel ):
        activeCam = cmds.modelEditor( panel, q=1, camera=1 )
    activeCamPose = cmds.getAttr( activeCam+'.wm' )[-4:-1]
    activeCamVector = [activeCamPose[0]-bbCenter[0], activeCamPose[1]-bbCenter[1], activeCamPose[2]-bbCenter[2]]
    activeCamDist = ((activeCamVector[0]**2+activeCamVector[1]**2+activeCamVector[2]**2)**0.5)

    bbLength *= boundingBoxDist
    camPose = [activeCamVector[0]/activeCamDist*bbLength+bbCenter[0],
               activeCamVector[1]/activeCamDist*bbLength+bbCenter[1],
               activeCamVector[2]/activeCamDist*bbLength+bbCenter[2]]

    cmds.move( camPose[0], camPose[1], camPose[2], cameraName, ws=1 )

    camVector = om.MVector( *activeCamVector )
    upVector  = om.MVector( 0,1,0 )
    biVector  = upVector ^ camVector
    upVector  = camVector ^ biVector

    mtxList = [ biVector.x, biVector.y, biVector.z, 0,
                upVector.x, upVector.y, upVector.z, 0,
                camVector.x, camVector.y, camVector.z, 0,
                0, 0, 0, 1 ]

    mtx = om.MMatrix()
    om.MScriptUtil.createMatrixFromList( mtxList, mtx )

    trMtx = om.MTransformationMatrix( mtx )
    eulerRot = trMtx.eulerRotation()
    rot = eulerRot.asVector()

    radToDeg = 180/3.14159

    cmds.rotate( rot.x*radToDeg, rot.y*radToDeg, rot.z*radToDeg, cameraName, ws=1 )
    cmds.setAttr( cameraName+'.centerOfInterest', ( om.MVector( *camPose )-om.MVector( *bbCenter ) ).length() )