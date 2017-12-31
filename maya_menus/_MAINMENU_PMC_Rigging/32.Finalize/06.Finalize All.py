import pymel.core
from sgMaya import sgCmds

references = pymel.core.ls( type='reference' )
for refNode in references:
    try:cmds.file( importReference=1, referenceNode=refNode.name() )
    except:pass


import maya.cmds as cmds

def cleanMeshInScene( *args ):

    def cleanMesh( targetObj ):
    
        targetShapes = cmds.listRelatives( targetObj, s=1, f=1 )
        for targetShape in targetShapes:
            if not cmds.getAttr( targetShape+'.io' ): continue
            if cmds.listConnections( targetShape + '.outMesh', s=0, d=1 ): continue 
            if cmds.listConnections( targetShape + '.worldMesh', s=0, d=1 ): continue 
            cmds.delete( targetShape )
            cmds.warning( "%s is deleted" % targetShape )
    
    meshs = cmds.ls( type='mesh' )
    
    meshObjs = []
    for mesh in meshs:
        if cmds.getAttr( mesh+'.io' ): continue
        meshP = cmds.listRelatives( mesh, p=1, f=1 )[0]
        if meshP in meshObjs: continue
        meshObjs.append( meshP ) 
    
    for meshObj in meshObjs:
        cleanMesh( meshObj )

cleanMeshInScene()

sels = pymel.core.ls( type='unknown' )
pymel.core.delete( sels )

targets = pymel.core.ls( type='nodeGraphEditorInfo' )
pymel.core.delete( targets )

from maya import mel
mel.eval( 'hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");' )

import pymel.core
nsList = pymel.core.namespaceInfo( lon=1 )

for ns in nsList:
    nodes = pymel.core.ls( ns + ':*' )
    if not len( nodes ): continue
    for node in nodes:
        node.rename( node.replace( ns + ':', '' ) )
    pymel.core.namespace( rm=ns )

sels = pymel.core.ls( 'Ctl_*', type='transform' )

for sel in sels:
    if not sel.getShape(): continue
    sgCmds.lockParent( sel )
    sgCmds.renameShape( sel )
    if not sel.getParent().nodeName()[:3] == 'Ctl':
        sgCmds.renameParent( sel )

from maya import cmds
plugins = cmds.unknownPlugin( q=1, list=1 )
if not plugins: plugins = []
for plugin in plugins:
    cmds.unknownPlugin( plugin, remove=1 )