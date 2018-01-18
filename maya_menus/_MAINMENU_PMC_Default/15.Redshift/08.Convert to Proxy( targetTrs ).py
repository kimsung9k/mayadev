from maya import cmds, mel
import pymel.core
import ntpath
from sgMaya import sgCmds, sgModel

plugins = ['AbcExport', 'AbcImport', 'gpuCache']

for plugin in plugins:
    if not cmds.pluginInfo( plugin, q=1, l=1 ):
        cmds.loadPlugin( plugin )

import maya.cmds as cmds
from sgMaya import sgCmds

def setMatrixPreventChildren( target, moveTarget ):
    targetChildren = cmds.listRelatives( target, c=1, type='transform', f=1 )
    if not targetChildren: targetChildren = []
    poses = []
    for targetChild in targetChildren:
        pose = cmds.xform( targetChild, q=1, ws=1, matrix=1 )
        poses.append( pose )
    
    cmds.xform( target, ws=1, matrix= cmds.getAttr( moveTarget + '.wm' ) )
    
    for i in range( len( targetChildren ) ):
        cmds.xform( targetChildren[i], ws=1, matrix= poses[i] )

sels = pymel.core.ls( sl=1 )
for sel in sels:
    selPivotMtx = sgCmds.getPivotWorldMatrix( sel )
    tr = pymel.core.createNode( 'transform' )
    pymel.core.xform( tr, ws=1, matrix= sgCmds.matrixToList( selPivotMtx ) )
    if sgCmds.getShape( sel.name() ):
        cmds.select( sel.name() )
        cmds.DeleteHistory( sel.name() )
        sgCmds.setGeometryMatrixToTarget( sel.name(), tr )
    setMatrixPreventChildren( sel.name(), tr )
    pymel.core.delete( tr )
    sgCmds.setPivotZero( sel.name() )

scenePath = cmds.file( q=1, sceneName=1 )
origdirPath = ntpath.split( scenePath )[0] + '/orig'
proxydirPath = ntpath.split( scenePath )[0] + '/proxy'

rsProxyTrs = []
for sel in sels:
    children = sel.listRelatives( c=1, ad=1, type='mesh' )
    if not children: continue
    targetChildren = []
    for child in children:
        if not sgCmds.isVisible( child ):
            pymel.core.delete( child )
        else:
            targetChildren.append( child )
    if not targetChildren: continue
    
    subdivisionValues = [ targetChild.attr( 'displaySmoothMesh' ).get() for targetChild in targetChildren ]
    pymel.core.select( sel )
    mel.eval( 'displaySmoothness -divisionsU 0 -divisionsV 0 -pointsWire 4 -pointsShaded 1 -polygonObject 1;' )
    gpuCacheTr = sgCmds.createGpuCache( sel )
    pymel.core.refresh()
    pymel.core.select( sel )
    for i in range( len(targetChildren) ):
        targetChildren[i].attr( 'displaySmoothMesh' ).set( subdivisionValues[i] )
    rsProxyTr = sgCmds.createRedshiftProxy( sel )
    pymel.core.refresh()
    rsProxyShape = rsProxyTr.getShape()
    pymel.core.parent( gpuCacheTr.getShape(), rsProxyTr, add=1, shape=1 )
    pymel.core.delete( gpuCacheTr )
    rsProxyShape.lodVisibility.set( 0 )
    
    selName = sel.nodeName()
    sgCmds.getSourceConnection( rsProxyTr, sel )
    if sel.getParent():
        try:rsProxyTr.setParent( sel.getParent() )
        except:pass
    rsProxyTr.addAttr( "origObjectPath", dt='string' )
    origExportPath = origdirPath + "/" + sel.name().replace( '|', '_' ).replace( ':', '_' ) + '.mb'
    sgCmds.addAttr( sel, ln="origName", dt='string' )
    sel.attr( 'origName' ).set( sel.name() )
    sel.setParent( w=1 )
    pymel.core.select( sel )
    cmds.file( origExportPath, f=1, options="v=0", typ="mayaBinary", pr=1, es=1 )
    rsProxyTr.attr( "origObjectPath" ).set( origExportPath )
    selName = sel.nodeName()
    pymel.core.delete( sel )
    rsProxyTr.rename( selName )
    
    for child in rsProxyTr.listRelatives( c=1, ad=1 ):
        if child.nodeType() == 'mesh':
            child.rename( rsProxyTr.nodeName() + 'Shape' )
        elif child.nodeType() == 'gpuCache':
            child.rename( rsProxyTr.nodeName() + '_gpuShape' )
    
    rsProxyTrs.append( rsProxyTr )

pymel.core.select( rsProxyTrs )