import maya.cmds as cmds
import maya.OpenMaya as om
import copy
import basic.baseFunctions as baseFunctions


class NameNumbering:
    
    def __init__(self, nameStr, targets, *args ):
        
        copyTargets = copy.copy( targets )
        
        targets.sort()
        targetLength = len( targets )
        
        mapIndices = []
        for i in range( targetLength ):
            for j in range( targetLength ):
                if targets[i] == copyTargets[j]:
                    mapIndices.append( j )
                    break
        
        if nameStr.find( '%' ) != -1:
            for i in range( targetLength ):
                invI = targetLength - i - 1
                cmds.rename( targets[invI], nameStr % mapIndices[invI] )
        else:
            for i in range( targetLength ):
                invI = targetLength - i - 1
                cmds.rename( targets[invI], nameStr + '%02d' % mapIndices[invI] )
                
                

class ReplaceName:
    
    def __init__(self, targetStr, replaceStr, targets, hierarchy=False, isNamespace=False, *args ):
        
        mObjects = []
        for target in targets:
            if hierarchy:
                children = cmds.listRelatives( target, c=1, ad=1, f=1 )
                children.append( target )
                for child in children:
                    if not cmds.nodeType( child ) in ['transform', 'joint']: continue
                    mObjects.append( baseFunctions.getMObject( child ) )
            else:
                mObjects.append( baseFunctions.getMObject(target) )
        
        for mObj in mObjects:
            try:
                fnNode = om.MFnDagNode( mObj )
                name = fnNode.name()
                fullPathName = fnNode.fullPathName()
                if isNamespace and name.find( targetStr ) != 0: continue
                replacedName = name.replace( targetStr, replaceStr )
                print fullPathName, replacedName
                cmds.rename( fullPathName, replacedName )
            except:
                fnNode = om.MFnDependencyNode( mObj )
                nodeName = fnNode.name()
                if isNamespace:
                    if nodeName.find( targetStr ) != 0: continue
                cmds.rename( nodeName, nodeName.replace( targetStr, replaceStr ) )
            