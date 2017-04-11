import maya.cmds as cmds
import sgBFunction_value


def curve_onJoint( topJoint, **options ):
    
    jntsH = cmds.listRelatives( topJoint, c=1, ad=1 )
    jntsH.append( topJoint )
    
    points = []
    for jnt in jntsH:
        point = cmds.xform( jnt, q=1, ws=1, t=1 )
        points.append( point )
    
    epCurve = sgBFunction_value.getValueFromDict( options, 'editPoint', 'ep' )
    degrees = sgBFunction_value.getValueFromDict( options, 'degrees', 'd' )
    
    if not degrees:
        if len( points ) == 2: degrees = 1
        elif len( points ) == 3: degrees = 2
        else: degrees = 3
    
    if epCurve:
        cmds.curve( ep=points, d=degrees )
    else:
        cmds.curve( p=points, d=degrees )