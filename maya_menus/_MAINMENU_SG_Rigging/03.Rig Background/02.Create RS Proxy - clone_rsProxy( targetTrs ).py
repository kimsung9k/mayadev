import pymel.core
from sgMaya import sgCmds
from maya import cmds
import ntpath, os


def getPivotMatrixMesh( inputTarget ):

    target = pymel.core.ls( inputTarget )[0]
    duTarget = pymel.core.duplicate( target )[0]
    pivotMtx = sgCmds.getPivotWorldMatrix( target )
    
    duTargetGrp = pymel.core.createNode( 'transform' )
    pymel.core.xform( duTargetGrp, ws=1, matrix=target.wm.get() )
    duTarget.setParent( duTargetGrp )
    
    return duTargetGrp


def createRedshiftProxy( inputTarget ):
    
    target = pymel.core.ls( inputTarget )[0]
    sceneName = cmds.file( q=1, sceneName=1 )
    proxydir = os.path.dirname( sceneName ) + '/proxy'
    if not os.path.exists( proxydir ):
        os.makedirs( proxydir )
    proxyPath = proxydir + '/%s.rs' % target.name().replace( '|', '_' )
    origMtx = target.wm.get()
    pymel.core.select( target )
    pymel.core.xform( target, ws=1, matrix=[1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1] )
    cmds.file( proxyPath, force=1, options="exportConnectivity=0;enableCompression=0;", typ="Redshift Proxy", pr=1, es=1 )
    pymel.core.xform( target, ws=1, matrix=origMtx )
    
    newMesh = pymel.core.createNode( 'mesh' )
    rsProxyNode = pymel.core.createNode( 'RedshiftProxyMesh' )
    rsProxyNode.fileName.set( proxyPath )
    rsProxyNode.outMesh >> newMesh.inMesh
    newTransform = newMesh.getParent()
    pymel.core.xform( newTransform, ws=1, matrix= sgCmds.matrixToList( sgCmds.getPivotWorldMatrix( target ) ) )
    
    newTransform.rename( target.nodeName() + '_rsProxy' )
    rsProxyNode.rename( newTransform.nodeName() + 'Shape' )
    
    return newTransform



def createGpuCache( inputTarget ):
    
    target = pymel.core.ls( inputTarget )[0]
    sceneName = cmds.file( q=1, sceneName=1 )
    proxydir = os.path.dirname( sceneName ) + '/proxy'
    if not os.path.exists( proxydir ):
        os.makedirs( proxydir )
    abcPath = proxydir + '/%s.abc' % target.name().replace( '|', '_' )
    pivMtxMesh = getPivotMatrixMesh( target )
    pymel.core.xform( pivMtxMesh, ws=1, matrix=[1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1] )
    pymel.core.AbcExport( j="-frameRange 1 1 -dataFormat ogawa -root %s -file %s" % ( pivMtxMesh, abcPath ) )
    pymel.core.delete( pivMtxMesh )
    
    gpuCacheNode = pymel.core.createNode( 'gpuCache' )
    gpuCacheNode.cacheFileName.set( abcPath )
    gpuCacheTr = gpuCacheNode.getParent()
    pymel.core.xform( gpuCacheTr, ws=1, matrix= sgCmds.matrixToList( sgCmds.getPivotWorldMatrix( target ) ) )
    gpuCacheTr.rename( target.nodeName() + '_gpu' )
    gpuCacheNode.rename( gpuCacheTr.nodeName() + 'Shape' )
    
    return gpuCacheTr



sels = pymel.core.ls( sl=1 )
proxyTrs = []
for sel in sels:
    rsProxyTr = createRedshiftProxy( sel )
    rsProxyShape = rsProxyTr.getShape()
    gpuCacheTr = createGpuCache( sel )
    pymel.core.parent( gpuCacheTr.getShape(), rsProxyTr, add=1, shape=1 )
    pymel.core.delete( gpuCacheTr )
    rsProxyShape.lodVisibility.set( 0 )
    sel.v.set( 0 )
        
    selMtx = pymel.core.xform( sel, q=1, ws=1, matrix=1 )
    selRp  = pymel.core.xform( sel, q=1, os=1, rp=1 )
    selSp  = pymel.core.xform( sel, q=1, os=1, sp=1 )
    
    pymel.core.xform( rsProxyTr, ws=1, matrix=selMtx )
    pymel.core.xform( rsProxyTr, os=1, rp=selRp )
    pymel.core.xform( rsProxyTr, os=1, sp=selSp )
    
    sgCmds.getSourceConnection( rsProxyTr, sel )
    if sel.getParent():
        rsProxyTr.setParent( sgCmds.makeCloneObject( sel.getParent(), cloneAttrName = 'rsProxy', connectionOn=True  ) )

    rsProxyTr.t >> sel.t
    rsProxyTr.r >> sel.r
    rsProxyTr.s >> sel.s
    rsProxyTr.sh >> sel.sh
    proxyTrs.append( rsProxyTr )

pymel.core.select( proxyTrs )
