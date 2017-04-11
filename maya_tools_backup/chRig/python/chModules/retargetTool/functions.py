import maya.OpenMaya as om
import maya.cmds as cmds
import maya.mel as mel
import os


def getSourceOutputsInputs( target, **options ):
    
    options.update( { 's':1, "d":0, "c":1, "p":1 } )
    
    cons = cmds.listConnections( target, **options )
    
    if not cons:
        return [], []

    outputs = cons[1::2]
    inputs  = cons[::2]
    
    return outputs, inputs


def getSourceNode( plug, typeName ):

    cons = om.MPlugArray()
    plug.connectedTo( cons, True, False )
    
    if cons.length() == 0:
        return None
    
    node = cons[0].node()
    
    if om.MFnDependencyNode( node ).typeName() == typeName:
        return node
    
    return None



def checkFilePath( path ):
    
    if not path:
        return False
    folderStr = '/'.join( path.split( '/' )[:-1] )
    
    if not folderStr:
        return False
    
    return os.path.exists( folderStr )



def getMObject( curveName ):
    
    selList = om.MSelectionList()
    
    selList.add( curveName )
    
    mObj = om.MObject()
    selList.getDependNode( 0, mObj )

    return mObj



def getNodeNameFromMObject( mObj ):
    
    fnNode = om.MFnDependencyNode( mObj )
    
    return fnNode.name()



def tryConnect( sourceAttr, destAttr ):
    try:
        if not cmds.isConnected( sourceAttr, destAttr ):
            try:
                cmds.connectAttr( sourceAttr, destAttr, f=1 )
            except:
                cmds.warning( "Can't not Connect %s to %s." %( sourceAttr, destAttr ) )
    except:
        cmds.warning( "Can't not Connect %s to %s." %( sourceAttr, destAttr ) )
            
            

def getLastIndex( attr ):
    
    cuPlug = getPlugFromString( attr )
    
    elementNum =  cuPlug.numElements()
    
    if elementNum == 0:
        return -1
    else:
        return cuPlug[elementNum-1].logicalIndex()



def getPlugFromString( attr ):
    
    splitAttrs = attr.split('.')
    
    node = splitAttrs[0]
    attrs = splitAttrs[1:]
    
    fnNode = om.MFnDependencyNode( getMObject( node ) )
    
    attrNames = []
    indies    = []
    
    for attr in attrs:
        if attr.find( '[' ) == -1:
            attrNames.append( attr )
            indies.append( None )
        else:
            attrName, index = attr.split( '[' )
            index = int( index.replace( ']','' ) )
            
            attrNames.append( attrName )
            indies.append( index )
    
    lenAttrs = len( attrNames )
    
    firstPlug = fnNode.findPlug( attrNames[0] )
    
    if lenAttrs == 1:
        return firstPlug

    for i in range( 1, lenAttrs ):
        beforeIndex = i-1

        firstPlug = firstPlug[beforeIndex]

        for j in range( firstPlug.numChildren() ):
            childName = firstPlug.child( j ).name()
            if childName.split( '.' )[-1] == attrNames[i]:
                break
        
        firstPlug = firstPlug.child( j )
        
        if not indies[i]:
            return firstPlug



def setAttrApi( attr, value ):
    plug = getPlugFromString( attr )
    
    if type( value ) == type( True ):
        plug.setBool( value )
    elif type( value ) == type( 1 ):
        plug.setInt( value )
    elif type( value ) == type( 1.0 ):
        plug.setDouble( value )
    elif type( value ) == type( '' ):
        plug.setString( value )
    elif type( value ) == type( om.MTime() ):
        plug.setMTime( value )



def clearArrayElement( targetAttr ):
    
    targetAttrPlug = getPlugFromString( targetAttr )
    
    numElements = targetAttrPlug.numElements()
    
    delIndies = []
    for i in range( numElements ):
        logicalIndex = targetAttrPlug[i].logicalIndex()
        
        try:
            childNum = targetAttrPlug[i].numChildren()
        except:
            childNum = 0
        
        if not childNum:
            if not cmds.listConnections( targetAttr+'[%d]' % logicalIndex ):
                delIndies.append( logicalIndex )
        else:
            childConnectExists = False
            for j in range( childNum ):
                childPlug = targetAttrPlug[i].child( j )
                if childPlug.isArray():
                    if not clearArrayElement( childPlug.name() ):
                        childConnectExists = True
                else:
                    if cmds.listConnections( childPlug.name() ):
                        childConnectExists = True
            if not childConnectExists:
                delIndies.append( logicalIndex )
    
    for delIndex in delIndies:
        cmds.removeMultiInstance( "%s[%d]" %( targetAttr, delIndex ) )
    
    if getLastIndex( targetAttr ) == -1:
        return True
    else:
        return False



def transformDefault( node ):

    for attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'shx', 'shy', 'shz']:
        
        try:cmds.setAttr( node+'.'+attr, 0 )
        except:pass
        
        
    for attr in ['sx', 'sy', 'sz']:
        
        try:cmds.setAttr( node+'.'+attr, 1 )
        except:pass
 
        

def getOrientRetargetNode_for( targetName ):
    
    retargetNodeCons = cmds.listConnections( targetName, s=1, d=0, type='retargetOrientNode' )
    
    if retargetNodeCons:
        retargetNode = retargetNodeCons[0]
    else:
        retargetNode = cmds.createNode( 'retargetOrientNode', n=targetName+'_rtgOrient' )
    
    tryConnect( retargetNode+'.outputRotateX', targetName+'.rx' )
    tryConnect( retargetNode+'.outputRotateY', targetName+'.ry' )
    tryConnect( retargetNode+'.outputRotateZ', targetName+'.rz' )
    
    tryConnect( targetName+'.jo', retargetNode+'.orient' )
    
    return retargetNode



def getTransRetargetNode_for( targetName ):
    
    retargetNodeCons = cmds.listConnections( targetName, s=1, d=0, type='retargetTransNode' )
    
    if retargetNodeCons:
        retargetNode = retargetNodeCons[0]
    else:
        retargetNode = cmds.createNode( 'retargetTransNode', n=targetName+'_rtgTrans' )
    
    tryConnect( retargetNode+'.outputX', targetName+'.tx' )
    tryConnect( retargetNode+'.outputY', targetName+'.ty' )
    tryConnect( retargetNode+'.outputZ', targetName+'.tz' )
    
    return retargetNode


def getCombineNode_from( target, targetOri ):
    
    targetCons = cmds.listConnections( target, s=0, d=1, type='transRotateCombineMatrix' )
    targetOriCons = cmds.listConnections( targetOri, s=0, d=1, type='transRotateCombineMatrix' )
    
    if targetCons and targetOriCons:
        if targetCons[0] == targetOriCons[0]:
            return targetCons[0]
        
    combineNode = cmds.createNode( 'transRotateCombineMatrix' )
    
    cmds.connectAttr( target+'.wm', combineNode+'.inputTransMatrix' )
    cmds.connectAttr( targetOri+'.wm', combineNode+'.inputRotateMatrix' )
    
    return combineNode



def addHelpTx( target, textName ):
    attrName = '____'
    
    while(1):
        if not cmds.attributeQuery( attrName, node=target, ex=1 ):
            break
        else:
            attrName += '_'
            
    cmds.addAttr( target, ln=attrName, at='enum', en=textName )
    cmds.setAttr( target+'.'+attrName, e=1, cb=1 )
    
    
def getIndexedName( name, index=0 ):
    
    if cmds.objExists( name+str(index) ):
        return getIndexedName( name, index+1 )
    
    return name+str(index)


def getP( targetName ):
    
    return cmds.listRelatives( targetName, p=1 )[0]