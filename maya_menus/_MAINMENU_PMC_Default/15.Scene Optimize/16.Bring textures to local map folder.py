from sgMaya import sgCmds
import pymel.core
import ntpath, shutil

mapFolder = sgCmds.getLocalMapFolder()

nodeTypeAndAttrs = [('file','fileTextureName'),('RedshiftSprite','tex0')]

for nodeType, attrName in nodeTypeAndAttrs:
    paths = {}
    for targetNode in pymel.core.ls( type=nodeType ):
        key = targetNode.attr(attrName).get()
        if not os.path.exists( key ): continue
        if paths.has_key( key ):
            paths[ key ].append( targetNode )
        else:
            paths[ key ] = [targetNode]
    
    index = 0
    for key in paths.keys():
        fileName = ntpath.split( key )[-1]
        newPath = mapFolder + '/' + fileName
        if os.path.exists( newPath ) and os.stat(key) == os.stat(newPath): continue
        shutil.copy2( key, newPath )
        index += 1
        for targetNode in paths[ key ]:
            targetNode.attr( attrName ).set( newPath )