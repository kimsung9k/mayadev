import maya.cmds as cmds

nsList = cmds.namespaceInfo( lon=1 )

targetStr = 'bg_237_Heilala_Festival_gpu'
targetNs = ''
for ns in nsList:
    if ns.find( targetStr ) != -1:
        targetNs = ns
        break

modifiedTargetAndValues = []
targets = cmds.ls( targetNs + ':*_gpu', type='transform' )
for target in targets:
    values = cmds.getAttr( target + '.t' )[0]
    values += cmds.getAttr( target + '.r' )[0]
    sValues = cmds.getAttr( target + '.s' )[0]
    
    isModified = False
    for value in values:
        if value:
            isModified = True
            break
            
    for sValue in sValues:
        if sValue != 1:
            isModified = True
            break

    if isModified:
        cmds.warning( "%s is modified" % target )
    values += sValues

    modifiedTargetAndValues.append( [target, values] )
   
import json
dataPath = 'A:/@@DEV@@/maya_tools/sg/datas/modifiedGpuObjs.txt'

def makeFolder( pathName ):
    
    pathName = pathName.replace( '\\', '/' )
    splitPaths = pathName.split( '/' )
    
    cuPath = splitPaths[0]
    
    folderExist = True
    for i in range( 1, len( splitPaths ) ):
        checkPath = cuPath+'/'+splitPaths[i]
        if not os.path.exists( checkPath ):
            os.chdir( cuPath )
            os.mkdir( splitPaths[i] )
            folderExist = False
        cuPath = checkPath
        
    if folderExist: return None
        
    return pathName


def makeFile( filePath ):
    if os.path.exists( filePath ): return None
    filePath = filePath.replace( "\\", "/" )
    splits = filePath.split( '/' )
    folder = '/'.join( splits[:-1] )
    makeFolder( folder )
    f = open( filePath, "w" )
    f.close()


makeFile( dataPath )

f = open( dataPath, 'w' )
json.dump( modifiedTargetAndValues, f )
f.close()


