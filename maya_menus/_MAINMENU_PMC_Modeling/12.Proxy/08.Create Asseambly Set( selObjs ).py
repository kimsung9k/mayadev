import pymel.core
sels = pymel.core.ls( sl=1 )
folderPath = os.path.dirname( cmds.file( q=1, sceneName=1 ) )
fileName = cmds.file( q=1, sceneName=1 ).split( '/' )[-1].split( '.' )[0]

if not cmds.pluginInfo( 'sceneAssembly', q=1, l=1 ):
    cmds.loadPlugin( 'sceneAssembly' )

mel.eval( 'assemblyCreate assemblyDefinition' )
asmNode = pymel.core.ls( type='assemblyDefinition' )[-1]
asmNode.rename( 'ASM_' + fileName )
reps = pymel.core.assembly( asmNode, q=1, listRepresentations=1 )
if reps:
    for rep in reps:
        pymel.core.assembly( asmNode, e=1, deleteRepresentation=rep )

index = 0
for sel in sels:
    selShape = sel.getShape()
    repName = sel.split( '_' )[-1] 
    if selShape:
        if selShape.nodeType() == 'gpuCache':
            pymel.core.assembly( asmNode, edit=True, createRepresentation='Cache',
              input=selShape.cacheFileName.get() )
            asmNode.attr( 'representations' )[index].repLabel.set( repName )
            index+=1
            continue            
    pymel.core.select( sel )
    filePath = folderPath + '/ASMOBJ_' + sel.shortName() + '.mb'
    cmds.file( filePath, force=1, options="v=0;", typ="mayaBinary", pr=1, es=1 )    
    pymel.core.assembly( asmNode, edit=True, createRepresentation='Scene',
              input=filePath )
    asmNode.attr( 'representations' )[index].repLabel.set( repName )
    index+=1