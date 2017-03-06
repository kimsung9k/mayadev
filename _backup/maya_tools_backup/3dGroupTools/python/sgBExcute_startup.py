import sgBExcute_message
import sgBModel_editUi
import maya.cmds as cmds
import sgBFunction_fileAndPath
import sgBFunction_message
import sgBModel_data

def uiCloseSceneUpdate( *args ):
    
    existingWindows = cmds.lsUI( windows=1 )
    
    for ui in sgBModel_editUi.targetWindowsClose_whenSceneUpdate:
        if ui in existingWindows:
            cmds.deleteUI( ui )

try:
    sgBExcute_message.addAllSceneMessageCallbacks()
    sgBExcute_message.appendCallback_sceneMessage( 'kSceneUpdate', uiCloseSceneUpdate )
except:pass



def getOrderedObjectFromSelection( *args ):
    
    if not sgBModel_data.orderedObjects:
        targets = cmds.ls( sl=1, fl=1 )
        try:sgBModel_data.orderedObjects.append( targets[-1] )
        except:pass
    else:
        selTargets = cmds.ls( sl=1, fl=1 )
        
        removeTargets = []
        for target in sgBModel_data.orderedObjects:
            if not target in selTargets:
                try:removeTargets.append( target )
                except:pass
        for target in removeTargets:
            try:sgBModel_data.orderedObjects.remove( target )
            except:pass

        for target in selTargets:
            if target in sgBModel_data.orderedObjects: continue
            try:sgBModel_data.orderedObjects.append( target )
            except:pass



def getOrderedVerticeFromSelection( *args ):
    
    if not sgBModel_data.orderedVertices:
        vertices = cmds.ls( sl=1, fl=1 )
        for vtx in vertices:
            if vtx.find( '.vtx[' ) == -1: continue
            sgBModel_data.orderedVertices.append( vtx )
    else:
        vertices = cmds.ls( sl=1, fl=1 )
        for vtx in vertices:
            if vtx in sgBModel_data.orderedVertices: continue
            afterMeshName = vtx.split( '.' )[0]
            beforeMeshName = sgBModel_data.orderedVertices[-1].split( '.' )[0]
            if beforeMeshName == afterMeshName:
                sgBModel_data.orderedVertices.append( vtx )
            else:
                sgBModel_data.orderedVertices = [ vtx ]
        removeTargets = []
        for vtx in sgBModel_data.orderedVertices:
            if not vtx in vertices: removeTargets.append( vtx )
        
        for target in removeTargets:
            sgBModel_data.orderedVertices.remove( target )

sgBFunction_message.removeAllEventCallback()
sgBFunction_message.appendEventCallback( 'SelectionChanged', getOrderedObjectFromSelection )
sgBFunction_message.appendEventCallback( 'SelectionChanged', getOrderedVerticeFromSelection )