import maya.cmds as cmds
import maya.OpenMaya as om


def getShape( targetDagNode ):
    
    if cmds.nodeType( targetDagNode ) in ['joint', 'transform']:
        shapes = cmds.listRelatives( targetDagNode, s=1 )
        if not shapes: return None
        else:return shapes[0]
    else:
        if cmds.nodeType( targetDagNode ) in ['nurbsSurface', 'nurbsCurve', 'mesh' ]:
            return targetDagNode
        else:
            return None
        
        
def getDagPath( targetDagNode ):
    
    selList = om.MSelectionList()
    selList.add( targetDagNode )
    dagPath = om.MDagPath()
    selList.getDagPath( 0, dagPath )
    return dagPath