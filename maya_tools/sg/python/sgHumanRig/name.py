import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
from sgModules import sgbase




def getLocalName( dagNode ):
    
    dagNode = OpenMaya.MFnDagNode( sgbase.getDagPath( dagNode ) )
    return dagNode.name()




def getPartialPathName( dagNode ):
    
    dagNode = OpenMaya.MFnDagNode( sgbase.getDagPath( dagNode ) )
    return dagNode.partialPathName()




def getFullPathName( dagNode ):
    
    dagNode = OpenMaya.MFnDagNode( sgbase.getDagPath( dagNode ) )
    return dagNode.fullPathname()



def addName( target, origName, addName ):
    
    localName = getLocalName( origName )
    if localName[:-1] != '_' and addName[1:] != '_':
        addName = '_' + addName
        
    return cmds.rename( target, localName + addName )



def replaceNameToTarget( srcObject, target, src, dst ):
    
    return cmds.rename( target, getLocalName(srcObject).replace( src, dst ) )



def renameParent( target ):
    
    fnTarget = OpenMaya.MFnDagNode( sgbase.getDagPath( target ) )
    targetP = cmds.listRelatives( target, p=1, f=1)[0]
    targetP = cmds.rename( targetP, 'P' + getLocalName( target ) )
    return fnTarget.partialPathName(), targetP
    
    
    