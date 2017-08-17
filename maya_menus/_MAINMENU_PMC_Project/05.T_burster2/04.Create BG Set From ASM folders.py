from maya import cmds
from sgMaya import sgCmds
import pymel.core

targetPath = 'D:/wms/pipeline/work/t_burster2/asset/rigging/BG_Proxy/Proxy_mod'

def getFile( basePath, endString ):
    for root, dirs, names in os.walk( basePath ):
        for name in names:
            fileEndString = '.'.join( name.split( '.' )[:-1] )[-len( endString ):]
            if fileEndString != endString: continue
            return root + '/' + name


def getObject( endString ):
    targetObjs = cmds.ls( '*_%s' % endString, l=1 )
    for targetObj in targetObjs:
        if len( targetObj.split( '|' ) ) != 2: continue
        return pymel.core.ls( targetObj )[0]

for root, dirs, names in os.walk( targetPath ):
    for assetName in dirs:
        cmds.file( f=1, new=1 )
        
        gpuFile = getFile( root + '/' + assetName, 'gpu' )
        reduceFile = getFile( root + '/' + assetName, 'reduced' )
        origFile = getFile( root + '/' + assetName, 'orig' )
        cmds.file( gpuFile, i=1, type="mayaBinary",  ignoreVersion=1, ra=1, mergeNamespacesOnClash=1, namespace=":", options="v=0;",  pr=1 )
        cmds.file( reduceFile, i=1, type="mayaBinary",  ignoreVersion=1, ra=1, mergeNamespacesOnClash=1, namespace=":", options="v=0;",  pr=1 )
        cmds.file( origFile, i=1, type="mayaBinary",  ignoreVersion=1, ra=1, mergeNamespacesOnClash=1, namespace=":", options="v=0;",  pr=1 )
        
        gpuObj = getObject( 'gpu' )
        reduceObj = getObject( 'reduced' )
        origObj = getObject( 'orig' )
        set = pymel.core.group( gpuObj, reduceObj, origObj, n='SET' )
        
        sgCmds.addOptionAttribute(set)
        set.addAttr( "type", at="enum", en="hidden:gpu:reduce:orig:", k=1, dv=1 )
        
        conditionGpu = pymel.core.createNode( 'condition' )
        conditionReduce = pymel.core.createNode( 'condition' )
        conditionOrig = pymel.core.createNode( 'condition' )
        
        set.attr( "type" ) >> conditionGpu.firstTerm
        set.attr( "type" ) >> conditionReduce.firstTerm
        set.attr( "type" ) >> conditionOrig.firstTerm
        
        conditionGpu.secondTerm.set( 1 )
        conditionReduce.secondTerm.set( 2 )
        conditionOrig.secondTerm.set( 3 )
        
        conditionGpu.ctr.set( 1 )
        conditionGpu.cfr.set( 0 )
        conditionReduce.ctr.set( 1 )
        conditionReduce.cfr.set( 0 )
        conditionOrig.ctr.set( 1 )
        conditionOrig.cfr.set( 0 )
        
        conditionGpu.outColorR >> gpuObj.v
        conditionReduce.outColorR >> reduceObj.v
        conditionOrig.outColorR >> origObj.v        
        
        cmds.file( rename= targetPath + '/' + assetName + '/' + assetName + '_.mb' )
        cmds.file( f=1, save =1, options="v=0;" )
    break