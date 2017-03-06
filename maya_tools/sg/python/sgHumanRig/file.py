import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import os
import shutil
import cPickle




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
    



def getProjectDir():
    return cmds.about(pd=True)




def exportModel( target, fileName, replace = False ):
    
    sceneName = cmds.file( q=1, sceneName=1 )
    targetPath = "/".join( sceneName.split( '/' )[:-1] ) + "/" + fileName +".mb"

    if replace:
        cmds.file( targetPath, f=1, options="v=0;", typ="mayaBinary", es=1 )
    else:
        cmds.file( targetPath, options="v=0;", typ="mayaBinary", es=1 )




def exportParts( targets, **options ):
    
    sceneName = cmds.file( q=1, sceneName=1 )
    splits = sceneName.split( '/' )
    folderPath = '/'.join( splits[:-1] ) + "/" + splits[-1].split( '.' )[0]
    
    makeFolder( folderPath )
    
    for target in targets:
        cmds.select( target )
        cmds.file( folderPath + "/" + target , **options )




def exportTransform():
    
    import json
    
    transformNode = cmds.ls( sl=1 )[0]
    
    filePath = getProjectDir() + '/sg_toolInfo/transformInfo.txt'
    makeFile( filePath )
    trPos = cmds.xform( transformNode, q=1, ws=1, matrix=1 )
    f = open( filePath, 'w' )
    json.dump( trPos, f )
    f.close()
    
    
def importTransform():
    
    import json
    
    filePath = getProjectDir() + '/sg_toolInfo/transformInfo.txt'
    if not os.path.exists( filePath ): return None
    f = open( filePath, 'r' )
    data = json.load( f )
    sels = cmds.ls( sl=1 )
    for sel in sels:
        cmds.xform( sel, ws=1, matrix= data )




def importAnimation( setGroup, importPath=None, *skipTargets ):

    import cPickle
    
    if importPath:
        fileName = importPath
    else:
        fileName = getProjectDir() + '/animation/bake.txt'
    
    
    


def reloadModules( pythonPath='' ):

    import os, imp, sys
    
    if not pythonPath:
        pythonPath = __file__.split( '\\' )[0]
    
    for root, folders, names in os.walk( pythonPath ):
        root = root.replace( '\\', '/' )
        for name in names:
            try:onlyName, extension = name.split( '.' )
            except:continue
            if extension.lower() != 'py': continue
            
            if name == '__init__.py':
                fileName = root
            else:
                fileName = root + '/' + name
                
            moduleName = fileName.replace( pythonPath, '' ).split( '.' )[0].replace( '/', '.' )[1:]
            moduleEx =False
            try:
                sys.modules[moduleName]
                moduleEx = True
            except:
                pass
            
            if moduleEx:
                reload( sys.modules[moduleName] )
    
    
    


    