import maya.cmds as cmds
import dag
import name


def getPoleVectorController( radius= 1 ):
    
    circle1 = cmds.circle( ch=0, normal=[1,0,0], radius=radius )[0]
    circle2 = cmds.circle( ch=0, normal=[0,1,0], radius=radius )[0]
    circle3 = cmds.circle( ch=0, normal=[0,0,1], radius=radius )[0]
    
    circle1Shape = dag.getShape( circle1 )
    circle2Shape = dag.getShape( circle2 )
    circle3Shape = dag.getShape( circle3 )
    
    ctl = cmds.group( em=1 )
    
    cmds.parent( circle1Shape, ctl, add=1, shape=1 )
    cmds.parent( circle2Shape, ctl, add=2, shape=1 )
    cmds.parent( circle3Shape, ctl, add=3, shape=1 )
    
    cmds.delete( [circle1, circle2, circle3] )
    
    return ctl



def getCircleController( normal, radius, controllerName ):
    
    circle = cmds.circle( ch=1, normal=normal, radius = radius )[0]
    circle, pCircle = dag.makeParent( circle )[0]
    
    circle = cmds.rename( circle, controllerName )
    circle, pCircle = name.renameParent( circle )
    
    return circle, pCircle