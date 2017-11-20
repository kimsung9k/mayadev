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



selGrps = pymel.core.ls( sl=1 )
proxys = []

for selGrp in selGrps:
    sels = pymel.core.listRelatives( selGrp, c=1, type='transform' )
    
    src  = sels[0]
    
    rsProxyTr = createRedshiftProxy( src )
    rsProxyShape = rsProxyTr.getShape()
    gpuCacheTr = createGpuCache( src )
    pymel.core.parent( gpuCacheTr.getShape(), rsProxyTr, add=1, shape=1 )
    pymel.core.delete( gpuCacheTr )
    rsProxyShape.lodVisibility.set( 0 )
    
    proxyNode = rsProxyShape.inMesh.listConnections( s=1, d=0 )[0]
    
    for sel in sels:
        if not sel.v.get():
            pymel.core.delete( sel )
            continue
        duProxyTr = pymel.core.duplicate( rsProxyTr )[0]
        duProxyMesh = duProxyTr.listRelatives( s=1, type='mesh' )[0]
        proxyNode.outMesh >> duProxyMesh.inMesh
        
        selMtx = pymel.core.xform( sel, q=1, ws=1, matrix=1 )
        selRp  = pymel.core.xform( sel, q=1, os=1, rp=1 )
        selSp  = pymel.core.xform( sel, q=1, os=1, sp=1 )
        
        pymel.core.xform( duProxyTr, ws=1, matrix=selMtx )
        pymel.core.xform( duProxyTr, os=1, rp=selRp )
        pymel.core.xform( duProxyTr, os=1, sp=selSp )
        
        if sel.getParent():
            duProxyTr.setParent( sgCmds.makeCloneObject( sel.getParent(), cloneAttrName='rsProxy', connectionOn=True ) )
        duProxyTr.t >> sel.t
        duProxyTr.r >> sel.r
        duProxyTr.s >> sel.s
        duProxyTr.sh >> sel.sh
        proxys.append( duProxyTr )
        
        allParents = duProxyTr.getAllParents()
        for parent in allParents:
            targets = parent.message.listConnections( s=0, d=1 )
            if not targets: continue
            if pymel.core.isConnected( parent.t, targets[0].t ):
                continue
            parent.t >> targets[0].t
            parent.r >> targets[0].r
            parent.s >> targets[0].s
            parent.sh >> targets[0].sh   
        proxys.append( duProxyTr ) 
    pymel.core.delete( rsProxyTr )
    selGrp.v.set( 0 )

pymel.core.select( proxys )