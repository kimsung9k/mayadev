from sgMaya import sgCmds
import pymel.core
import maya.cmds as cmds


def exportProxyAndReplace( target, proxyName ):

    targetPos = pymel.core.xform( target, q=1, ws=1, matrix=1 )
    
    pymel.core.xform( target, ws=1, matrix= sgCmds.getDefaultMatrix() )
    pymel.core.select( target )
    proxyPath = 'Z:/SW_S2_Pipeline/03_Main-production/01_episode/ep237/bg/bg_237_Heilala_Festival/proxy/new/%s.rs' % proxyName
    cmds.file( proxyPath, force=1, options="exportConnectivity=1;", typ="Redshift Proxy", pr=1, es=1 )
    
    mesh = pymel.core.createNode( 'mesh' )
    meshObj = mesh.getParent()
    meshObj.setParent( target )
    proxyNode = pymel.core.createNode( 'RedshiftProxyMesh' )
    proxyNode.displayMode.set( 1 )
    proxyNode.displayPercent.set( 10 )
    proxyNode.outMesh >> mesh.inMesh
    
    proxyNode.fileName.set( proxyPath )
    
    pymel.core.xform( target, ws=1, matrix=targetPos )



def setGroupSameMeshs():
    
    sels = pymel.core.ls( sl=1 )
    
    children = pymel.core.listRelatives( sels[0], c=1, ad=1 )
    
    meshGroup = {}
    
    for child in children:
        proxyMesh = sgCmds.getNodeFromHistory( child, 'RedshiftProxyMesh' )
        if proxyMesh: continue
        numVertices = sgCmds.getNumVertices( child )
        if not numVertices: continue
        if meshGroup.has_key( numVertices ):
            meshGroup[numVertices].append( child )
        else:
            meshGroup.update({numVertices:[child]})
    
    for item in meshGroup.items():
        pymel.core.group( item[1:] )


def duplicateAndParentProxy():
    
    selection = pymel.core.ls( sl=1 )
    src = selection[0]
    sels = selection[1:]
    
    proxyMesh = sgCmds.getNodeFromHistory( src, 'RedshiftProxyMesh' )
    
    for sel in sels:
        if not proxyMesh: continue
        mesh = pymel.core.createNode( 'mesh' )
        meshObj = mesh.getParent()
        proxyMesh[0].outMesh >> mesh.inMesh
        meshObj.setParent( sel )
        
        pymel.core.xform( meshObj, os=1, matrix= sgCmds.getDefaultMatrix() )