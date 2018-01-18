import pymel.core
from sgMaya import sgCmds
from maya import cmds, OpenMaya, mel
import ntpath, os

plugins = ['AbcExport', 'AbcImport', 'gpuCache']

for plugin in plugins:
    if not cmds.pluginInfo( plugin, q=1, l=1 ):
        cmds.loadPlugin( plugin )

def duplicateRsProxyTr( rsProxyTr ):
    rsProxyTrShapes = rsProxyTr.listRelatives( s=1, type='mesh' )
    if not rsProxyTrShapes: return None
    proxyShape = rsProxyTrShapes[0]
    srcCon = proxyShape.inMesh.listConnections( s=1, d=0, p=1 )
    duProxy = pymel.core.duplicate( rsProxyTr )[0]
    duProxyShape = duProxy.listRelatives( s=1, type='mesh' )[0]
    srcCon[0] >> duProxyShape.inMesh
    return duProxy


selGrps = pymel.core.ls( sl=1 )
cmds.DeleteHistory( selGrps )
sels = pymel.core.listRelatives( selGrps, c=1, ad=1, type='transform' )

proxyTrs = []

bbstrdict = {}
for sel in sels:
    if not sel.getShape() or sel.getShape().nodeType() != 'mesh': continue
    bbstr = sgCmds.getBoundingBoxDistStr( sel )
    if bbstrdict.has_key( bbstr ):
        bbstrdict[ bbstr ] += [ sel ]
    else:
        bbstrdict[ bbstr ] = [ sel ]

print "len types : ", len( bbstrdict.keys() )
print "len objs  : ", len( sels )

scenePath = cmds.file( q=1, sceneName=1 )
origdirPath = ntpath.split( scenePath )[0] + '/orig'
proxydirPath = ntpath.split( scenePath )[0] + '/proxy'

for key in bbstrdict.keys():
    targets = bbstrdict[ key ]
    firstObject = targets[0]
    
    subdivisionValue = firstObject.attr( 'displaySmoothMesh' ).get()
    pymel.core.select( firstObject )
    mel.eval( 'displaySmoothness -divisionsU 0 -divisionsV 0 -pointsWire 4 -pointsShaded 1 -polygonObject 1;' )
    gpuCacheTr = sgCmds.createGpuCache( firstObject )
    pymel.core.refresh()
    firstObject.attr( 'displaySmoothMesh' ).set( subdivisionValue )
    rsProxyTr = sgCmds.createRedshiftProxy( firstObject )
    pymel.core.refresh()    
    pymel.core.parent( gpuCacheTr.getShape(), rsProxyTr, add=1, shape=1 )
    pymel.core.delete( gpuCacheTr )
    rsProxyTr.getShape().lodVisibility.set( 0 )
    firstObjName = firstObject.nodeName()
    
    rsProxyTr.rename( firstObjName + '_000' )
    rsProxyTr.addAttr( "origObjectPath", dt='string' )
    origExportPath = origdirPath + "/" + firstObject.name().replace( '|', '_' ).replace( ':', '_' ) + '.mb'
    rsProxyTr.attr( "origObjectPath" ).set( origExportPath )
    sgCmds.addAttr( firstObject, ln="origName", dt='string' )
    firstObject.attr( 'origName' ).set( firstObjName )
    firstObject.setParent( w=1 )
    pymel.core.select( firstObject )
    cmds.file( origExportPath, f=1, options="v=0", typ="mayaBinary", pr=1, es=1 )
    pymel.core.delete( firstObject )
    rsProxyTr.rename( firstObjName )
    
    if len( targets ) == 1: continue
    
    for otherObj in targets[1:]:
        duProxyTr = duplicateRsProxyTr( rsProxyTr )
        if not duProxyTr: continue
        try:duProxyTr.setParent( otherObj.getParent() )
        except:pass
        pymel.core.xform( duProxyTr, ws=1, matrix=otherObj.wm.get() )
        otherObjName = otherObj.nodeName()
        pymel.core.delete( otherObj )
        duProxyTr.rename( otherObjName )
