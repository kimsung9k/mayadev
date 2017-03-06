import maya.cmds as cmds
import topInfo
import topInfoEdit
import functions as fnc


class EditNamespace:
    
    def __init__(self, sourceWorld, targetWorld ):
        
        topInfoEdit.EditNameSpaceInfo( sourceWorld, targetWorld )
        
        

class Each:
    
    def __init__(self, target ):
        
        try:
            topInfoEdit.EditCtlInfo( target )
        except:
            return None
        
        if not len( topInfo.parentList ) > 1: return None
        
        try:
            sourceFollow, targetFollow = self.getFollowNode( target )
        except: return None
        
        for i in range( len( topInfo.parentList )-1 ):
            
            inputNode = cmds.listConnections( sourceFollow+'.inputMatrix[%d]' % i )[0]

            if cmds.nodeType( inputNode ) == 'transRotateCombineMatrix':
                parentCtl = cmds.listConnections( inputNode+'.inputRotateMatrix' )[0]
            else:
                parentCtl = inputNode

            attrName = parentCtl.replace( topInfo.sourceNS, '' )+'_w'            
            
            if not cmds.attributeQuery( attrName, node= target, ex=1 ):
                cmds.addAttr( target, ln=attrName, min=0, max=10 )
                cmds.setAttr( target+'.'+attrName, e=1, k=1 )
            
            cmds.connectAttr( target+'.'+attrName, sourceFollow+'.inputWeight[%d]' % i, f=1 )
            cmds.connectAttr( target+'.'+attrName, targetFollow+'.inputWeight[%d]' % i, f=1 )
        
            
    def getFollowNode(self, target ):
        
        retargetNodes = []
        
        retargetBlender = cmds.listConnections( target, type='retargetBlender' )[0]
        
        cuIndex = fnc.getLastIndex( retargetBlender+'.input' )
        
        retargetTransNodeCons = cmds.listConnections( retargetBlender+'.input[%d].transMatrix' % cuIndex )
        retargetOrientNodeCons = cmds.listConnections( retargetBlender+'.input[%d].orientMatrix' % cuIndex )
        
        if retargetTransNodeCons:
            retargetNodes.append( retargetTransNodeCons[0] )
        if retargetOrientNodeCons:
            retargetNodes.append( retargetOrientNodeCons[0] )
        
        sourceFollow = cmds.listConnections( retargetNodes[-1]+'.sourceParentMatrix', type='followMatrix' )[0]
        targetFollow = cmds.listConnections( retargetNodes[-1]+'.targetParentMatrix', type='followMatrix' )[0]
        
        return sourceFollow, targetFollow
        
        
class All:
    
    def __init__(self):
        
        targetNS = topInfo.targetNS
        
        targetCtls = cmds.ls( targetNS+'*_CTL' )
        
        for targetCtl in targetCtls:
            
            Each( targetCtl )