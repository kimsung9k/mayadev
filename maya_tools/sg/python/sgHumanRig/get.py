import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
from sgModules import sgbase


def mesh( targets ):
    
    if not type( targets ) in [ type([]), type(()) ]:
        targets = [targets]
    
    meshs = []
    
    for target in targets:
        if cmds.nodeType( target ) == "transform":
            shapes = cmds.listRelatives( target, s=1, f=1 )
            for shape in shapes:
                if cmds.nodeType( shape ) == "mesh":
                    meshs.append( shape )
        elif cmds.nodeType( target ) == "mesh":
            mesh.append( target )
    
    return meshs



def ioMesh( targets ):
    
    if not type( targets ) in [ type([]), type(()) ]:
        targets = [targets]
    
    meshs = []
    
    for target in targets:
        if cmds.nodeType( target ) == "transform":
            shapes = cmds.listRelatives( target, s=1, f=1 )
            for shape in shapes:
                if not cmds.getAttr( shape + ".io" ) : continue
                if cmds.nodeType( shape ) == "mesh":
                    meshs.append( shape )
        elif cmds.nodeType( target ) == "mesh" and cmds.getAttr( shape + ".io" ):
            mesh.append( target )
    
    return meshs



def nonIoMesh( targets ):
    
    if not type( targets ) in [ type([]), type(()) ]:
        targets = [targets]
    
    meshs = []
    
    for target in targets:
        if cmds.nodeType( target ) == "transform":
            shapes = cmds.listRelatives( target, s=1, f=1 )
            if not shapes: continue
            for shape in shapes:
                if cmds.getAttr( shape + ".io" ) : continue
                if cmds.nodeType( shape ) == "mesh":
                    meshs.append( shape )
        elif cmds.nodeType( target ) == "mesh":
            meshs.append( target )
        
    return meshs


























def activeModelPanel():
    panel = cmds.getPanel( wf=1 )
    if panel in cmds.getPanel( type='modelPanel' ):
        return panel
    else:
        return None




def activeCam():
    panel = activeModelPanel()
    if not panel: return None
    return cmds.modelPanel( panel, q=1, cam=1 )
    




def isolateSelected():
    
    panel = activeModelPanel()
    if not panel: return None;
    selectedSet = cmds.isolateSelect( panel, q=1, viewObjects=1 )
    oSelSet = sgbase.getMObject( selectedSet )
    selList = OpenMaya.MSelectionList()
    fnSet = OpenMaya.MFnSet( oSelSet )
    fnSet.getMembers( selList, False )
    dagPath = OpenMaya.MDagPath()
    oComponent = OpenMaya.MObject();
    selList.getDagPath( 0, dagPath, oComponent )
    elements = OpenMaya.MIntArray()
    fnSingleComp = OpenMaya.MFnSingleIndexedComponent(oComponent)
    fnSingleComp.getElements( elements )
    dagNode = OpenMaya.MFnDagNode( dagPath )
    print dagNode.name(), elements.length()
    return dagPath, elements




def shapesOfComponentSelected():
    
    selList = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList(selList)
    
    nodeNames = []
    for i in range( selList.length() ):
        dagPath = OpenMaya.MDagPath()
        oComponent = OpenMaya.MObject();
        selList.getDagPath( i, dagPath, oComponent )
        if oComponent.isNull(): continue
        
        fnDagNode = OpenMaya.MFnDagNode( dagPath )
        nodeName = fnDagNode.partialPathName()
        nodeNames.append( nodeName )
    
    return nodeNames









def activeSelectionApi():
    
    selList = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList( selList )
    
    apiSelectionList = []
    
    for i in range( selList.length() ):
        oNode = OpenMaya.MObject()
        dagPath = OpenMaya.MDagPath()
        oComponent = OpenMaya.MObject()
        try: 
            selList.getDagPath( i, dagPath, oComponent )
            apiSelectionList.append( ( dagPath, oComponent ) )
        except: 
            selList.getDependNode( i, oNode )
            apiSelectionList.append( (oNode) )
    
    return apiSelectionList
        



def childrenAttr( attrName ):
    
    node, attr = attrName.split( '.' )
    childrenAttrs = cmds.attributeQuery( attr, node=node, lc=1 )
    if not childrenAttrs: return []
    
    return [ node + "." + childrenAttr for childrenAttr in childrenAttrs ]
















def nodeFromHistory( target, historyType, **options ):
    
    hists = cmds.listHistory( target, **options )
    
    if not hists: return []
    
    returnTargets = []
    for hist in hists:
        if cmds.nodeType( hist ) == historyType:
            returnTargets.append( hist )
    
    return returnTargets






    



def shapeTransformFromGroup( shapeGroup ):
    
    children = cmds.listRelatives( shapeGroup, c=1, ad=1, f=1 )
    if not children: children = []
    children.append( shapeGroup )
    
    shapeGroup = []
    for child in children:
        shapes = cmds.listRelatives( child, s=1, f=1 )
        if not shapes: continue
        shapeGroup.append( child )
    
    return shapeGroup
        
    
    