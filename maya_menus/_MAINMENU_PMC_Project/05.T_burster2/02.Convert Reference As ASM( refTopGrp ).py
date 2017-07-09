import pymel.core
sels = pymel.core.ls( sl=1 )

asmNodes = pymel.core.ls( type='assemblyDefinition' )
targetAsmNodes = []
for sel in sels:
    targetAsmNode = None
    path = pymel.core.referenceQuery( sel, filename=1 )
    rfn = pymel.core.referenceQuery( sel, rfn=1 )
    folderName = os.path.dirname( path )
    fileName = path.split( '/' )[-1].split( '.' )[0]
    targetPath = folderName + '/ASM_' + fileName + '.mb'
    cmds.file( targetPath, i=1, type="mayaBinary",  ignoreVersion=1, ra=1, mergeNamespacesOnClash=False, namespace=":", options="v=0;",  pr=1 )
    newAsmNodes = pymel.core.ls( type='assemblyDefinition' )
    for newAsmNode in newAsmNodes:
        if newAsmNode in asmNodes: continue
        targetAsmNodes.append( newAsmNode )
        asmNodes.append( newAsmNode )
        pymel.core.xform( newAsmNode, ws=1, matrix= sel.wm.get() )
        break
    cmds.file( removeReference=1, rfn=rfn )

pymel.core.select( targetAsmNodes )