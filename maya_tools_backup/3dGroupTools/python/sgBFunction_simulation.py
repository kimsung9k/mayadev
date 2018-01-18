import maya.cmds as cmds
import maya.mel as mel

def createPointConstrainedCam( targetObject ):
    
    cam = sgBFunction_scene.getCurrentCam()
    panel = cmds.getPanel( wf=1 )
    if not cam:
        cam = 'persp'
    duCam = cmds.duplicate( cam )[0]
    
    camGrp = cmds.group( em=1 )
    cmds.pointConstraint( targetObject, camGrp )
    
    cmds.parent( duCam, camGrp )
    
    if cmds.getPanel( to=panel ):
        print 'lookThroughModelPanel %s %s;' %( duCam, panel )
        mel.eval( 'lookThroughModelPanel %s %s;' %( duCam, panel ) )