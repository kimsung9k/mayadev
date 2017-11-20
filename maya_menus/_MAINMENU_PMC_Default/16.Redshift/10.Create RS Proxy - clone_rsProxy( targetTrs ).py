import pymel.core
from sgMaya import sgCmds
from maya import cmds, OpenMaya, mel
import ntpath, os



class TransformKeep:
    
    def __init__( self, inputTarget ):
        self.target = pymel.core.ls( inputTarget )[0]
        self.t = self.target.t.get()
        self.r = self.target.r.get()
        self.s = self.target.s.get()
        self.sh = self.target.sh.get()
        self.rotatePivot = self.target.rotatePivot.get()
        self.scalePivot = self.target.scalePivot.get()
        self.rotatePivotTranslate = self.target.rotatePivotTranslate.get()
        self.scalePivotTranslate = self.target.scalePivotTranslate.get()
        
        self.parent = self.target.getParent()


    def setToDefault(self):
        
        self.target.setParent( w=1 )

        self.cons = self.target.listConnections( s=1, d=0, p=1, c=1 )
        for origCon, dstCon in self.cons:
            dstCon // origCon

        self.target.t.set( 0,0,0 )
        self.target.r.set( 0,0,0 )
        self.target.s.set( 1,1,1 )
        self.target.sh.set( 0,0,0 )
        self.target.rotatePivot.set( 0,0,0 )
        self.target.scalePivot.set( 0,0,0 )
        self.target.rotatePivotTranslate.set( 0,0,0 )
        self.target.scalePivotTranslate.set( 0,0,0 )


    def setToOrig(self):
        
        if self.parent:self.target.setParent( self.parent )
        
        self.target.t.set( self.t )
        self.target.r.set( self.r )
        self.target.s.set( self.s )
        self.target.sh.set( self.sh )
        self.target.rotatePivot.set( self.rotatePivot )
        self.target.scalePivot.set( self.scalePivot )
        self.target.rotatePivotTranslate.set( self.rotatePivotTranslate )
        self.target.scalePivotTranslate.set( self.scalePivotTranslate )
        
        for origCon, dstCon in self.cons:
            dstCon >> origCon
    
    
    def setToOther( self, inputOther ):
        
        other = pymel.core.ls( inputOther )[0]
        origParent = other.getParent()
        if self.parent:
            other.setParent( self.parent )
        else:
            other.setParent( w=1 )
        other.t.set( self.t )
        other.r.set( self.r )
        other.s.set( self.s )
        other.sh.set( self.sh )
        other.rotatePivot.set( self.rotatePivot )
        other.scalePivot.set( self.scalePivot )
        other.rotatePivotTranslate.set( self.rotatePivotTranslate )
        other.scalePivotTranslate.set( self.scalePivotTranslate )
        if origParent:
            other.setParent( origParent )
        
        self.cons = self.target.listConnections( s=1, d=0, p=1, c=1 )
        for origCon, dstCon in self.cons:
            dstCon >> other.attr( origCon.longName() )



def isVisible( target ):
    allParents = target.getAllParents()
    allParents.append( target )
    for parent in allParents:
        if not parent.v.get(): return False
    return True


def createRedshiftProxy( inputTarget, targetName=None ):
    
    target = pymel.core.ls( inputTarget )[0]
    sceneName = cmds.file( q=1, sceneName=1 )
    proxydir = os.path.dirname( sceneName ) + '/proxy'
    if not os.path.exists( proxydir ):
        os.makedirs( proxydir )
    if not targetName:
        targetName = target.name().replace( '|', '_' )
    proxyPath = proxydir + '/%s.rs' % targetName
    origMtx = target.wm.get()
    pymel.core.select( target )
    transformKeep = TransformKeep( target )
    transformKeep.setToDefault()
    cmds.file( proxyPath, force=1, options="exportConnectivity=0;enableCompression=0;", typ="Redshift Proxy", pr=1, es=1 )
    pymel.core.rsProxy( fp=proxyPath, sl=1 )
    transformKeep.setToOrig()
    
    newMesh = pymel.core.createNode( 'mesh' )
    rsProxyNode = pymel.core.createNode( 'RedshiftProxyMesh' )
    rsProxyNode.fileName.set( proxyPath )
    rsProxyNode.outMesh >> newMesh.inMesh
    newTransform = newMesh.getParent()
    
    newTransform.rename( target.nodeName() + '_rsProxy' )
    rsProxyNode.rename( newTransform.nodeName() + 'Shape' )
    transformKeep.setToOther( newTransform )
    
    return newTransform



def createGpuCache( inputTarget, targetName=None ):
    
    target = pymel.core.ls( inputTarget )[0]
    sceneName = cmds.file( q=1, sceneName=1 )
    proxydir = os.path.dirname( sceneName ) + '/proxy'
    if not os.path.exists( proxydir ):
        os.makedirs( proxydir )
    if not targetName:
        targetName = target.name().replace( '|', '_' )
    abcFolder = proxydir
    transformKeep = TransformKeep( target )
    transformKeep.setToDefault()
    abcPath = cmds.gpuCache( target.name(), startTime=1, endTime=1, optimize=1, optimizationThreshold=1000, writeMaterials=0, dataFormat='ogawa',
                                 directory=abcFolder, fileName=targetName, saveMultipleFiles=False )[0]
    transformKeep.setToOrig()
    
    gpuCacheNode = pymel.core.createNode( 'gpuCache' )
    gpuCacheNode.cacheFileName.set( abcPath )
    gpuCacheTr = gpuCacheNode.getParent()
    gpuCacheTr.rename( target.nodeName() + '_gpu' )
    gpuCacheNode.rename( gpuCacheTr.nodeName() + 'Shape' )
    transformKeep.setToOther( gpuCacheTr )
    
    return gpuCacheTr


sels = pymel.core.ls( sl=1 )
proxyTrs = []
for sel in sels:
    
    children = sel.listRelatives( c=1, ad=1, type='transform' )
    for child in children:
        if not isVisible( child ):
            pymel.core.delete( child )
    
    gpuCacheTr = createGpuCache( sel )
    pymel.core.refresh()
    rsProxyTr = createRedshiftProxy( sel )
    pymel.core.refresh()
    rsProxyShape = rsProxyTr.getShape()
    pymel.core.parent( gpuCacheTr.getShape(), rsProxyTr, add=1, shape=1 )
    pymel.core.delete( gpuCacheTr )
    rsProxyShape.lodVisibility.set( 0 )
    sel.v.set( 0 )
    
    sgCmds.getSourceConnection( rsProxyTr, sel )
    if sel.getParent():
        rsProxyTr.setParent( sgCmds.makeCloneObject( sel.getParent(), cloneAttrName = 'rsProxy', connectionOn=True  ) )

    rsProxyTr.t >> sel.t
    rsProxyTr.r >> sel.r
    rsProxyTr.s >> sel.s
    rsProxyTr.sh >> sel.sh
    proxyTrs.append( rsProxyTr )

pymel.core.select( proxyTrs )
