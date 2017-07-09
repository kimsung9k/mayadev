import pymel.core
from sgMaya import sgCmds
from maya import cmds
sels = pymel.core.ls( sl=1 )

src = sels[0]
others = sels[1:]

sceneName = cmds.file( q=1, sceneName=1 )
fileName = sceneName.split( '/' )[-1].split( '.' )[0]
targetPath = '.'.join( sceneName.split( '.' )[:-1] ) + '.mi'

pymel.core.select( src )
cmds.file( targetPath, options='binary=1;compression=0;tabstop=8;perframe=0;padframe=0;perlayer=1;pathnames=3313323333;assembly=0;fragment=0;fragsurfmats=0;fragsurfmatsassign=0;fragincshdrs=0;fragchilddag=0;passcontrimaps=1;passusrdata=1;overrideAssemblyRootName=0;assemblyRootName=binary=1;compression=0;tabstop=8;perframe=0;padframe=0;perlayer=0;pathnames=3313333333;assembly=1;fragment=1;fragsurfmats=1;fragsurfmatsassign=1;fragincshdrs=1;fragchilddag=1;passcontrimaps=1;passusrdata=0;filter=00000011010000001101000;overrideAssemblyRootName=0;assemblyRootName=',
           typ='mentalRay', pr=1, es=1, force=1 )
mel.eval( 'Mayatomr -mi  -exportFilter 721600 -active -binary -fe  -fem  -fma  -fis  -fcd  -pcm  -as  -asn "%s" -xp "3313333333" -file "%s"' % (fileName,targetPath) )

for other in others:
    otherShape = other.getShape()
    if otherShape.nodeType() == 'mesh':
        otherShape.miUpdateProxyBoundingBoxMode.set(3)
        otherShape.miProxyFile.set( targetPath )