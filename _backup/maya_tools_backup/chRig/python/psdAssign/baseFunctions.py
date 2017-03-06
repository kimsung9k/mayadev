import maya.OpenMaya as om
import maya.cmds as cmds


def cleanMesh( meshObj ):
    
    shapes = cmds.listRelatives( meshObj, s=1 )
    
    for shape in shapes:
        if cmds.getAttr( shape+'.io' ):
            cmds.delete( shape )



def getAttrRealName( attr ):
    
    def plugAttr( plug, attrName ):
        
        try:
            origAttrName, indexSep = attrName[0].split( '[' )
        except:
            origAttrName = attrName
            indexSep = None
        
        i=0
        
        while ( i < 100 ):
           
            childPlug = plug.child( i )
            
            if childPlug.name() == origAttrName:
                
                if not indexSep:
                    nextPlug = childPlug
                
                else:
                    index = int( indexSep[0] )
                    nextPlug = childPlug[ index ]
                    
                if not len( attrName ) > 1:
                    return nextPlug
                else:
                    return plugAttr( nextPlug, attrName[1:] )
            
            i+=1
        
    
    def findAttrPlug( fnNode, attrName ):

        try:
            origAttrName, indexSep = attrName[0].split( '[' )
        except:
            return fnNode.findPlug( attrName[0] )
            
        plug = fnNode.findPlug( origAttrName )
        
        index = int( indexSep[0] )
        nextPlug = plug[ index ]
        
        if not len( attrName ) > 1:
            return nextPlug
        else:
            return plugAttr( nextPlug, attrName[1:] )
            
            
    
    splitData = attr.split( '.' )
    
    node = splitData[0]
    attrName = splitData[1:]
    
    mObj = om.MObject()
    
    selList = om.MSelectionList()
    selList.add( node )
    selList.getDependNode( 0, mObj )
    
    fnNode = om.MFnDependencyNode( mObj )
    
    plug = findAttrPlug( fnNode, attrName )
    
    return plug.name()



def setAttrApi( attr, value ):
    
    def plugAttr( plug, attrName ):
        
        try:
            origAttrName, indexSep = attrName[0].split( '[' )
        except:
            origAttrName = attrName
            indexSep = None
        
        i=0
        
        while ( i < 100 ):
           
            childPlug = plug.child( i )
            
            if childPlug.name() == origAttrName:
                
                if not indexSep:
                    nextPlug = childPlug
                
                else:
                    index = int( indexSep[0] )
                    nextPlug = childPlug[ index ]
                    
                if not len( attrName ) > 1:
                    return nextPlug
                else:
                    return plugAttr( nextPlug, attrName[1:] )
            
            i+=1
        
    
    def findAttrPlug( fnNode, attrName ):

        try:
            origAttrName, indexSep = attrName[0].split( '[' )
        except:
            return fnNode.findPlug( attrName[0] )
            
        plug = fnNode.findPlug( origAttrName )
        
        index = int( indexSep[0] )
        nextPlug = plug[ index ]
        
        if not len( attrName ) > 1:
            return nextPlug
        else:
            return plugAttr( nextPlug, attrName[1:] )
        
            
    
    splitData = attr.split( '.' )
    
    node = splitData[0]
    attrName = splitData[1:]
    
    mObj = om.MObject()
    
    selList = om.MSelectionList()
    selList.add( node )
    selList.getDependNode( 0, mObj )
    
    fnNode = om.MFnDependencyNode( mObj )
    
    plug = findAttrPlug( fnNode, attrName )
    
    if type( value ) == type( True ):
        plug.setBool( value )
    elif type( value ) == type( 1 ):
        plug.setInt( value )
    elif type( value ) == type( 1.0 ):
        plug.setDouble( value )
    elif type( value ) == type( '' ):
        plug.setString( value )
    


def addHelpTx( target, textName ):
    attrName = '____'
    
    while(1):
        if not cmds.attributeQuery( attrName, node=target, ex=1 ):
            break
        else:
            attrName += '_'
            
    cmds.addAttr( target, ln=attrName, at='enum', en=textName )
    cmds.setAttr( target+'.'+attrName, e=1, cb=1 )
    


def getLastIndex( attr ):
    
    nodeName, attrName = attr.split( '.' )
    
    selList = om.MSelectionList()
    selList.add( nodeName )
    mObj = om.MObject()
    
    selList.getDependNode( 0, mObj )
    
    fnNode = om.MFnDependencyNode( mObj )
    wPlug = fnNode.findPlug( attrName )
    
    if not wPlug.numElements():
        return -1
    
    for i in range( wPlug.numElements() ):
        lastIndex = wPlug[i].logicalIndex()
        
    return lastIndex




def getAffectedIndies( attr ):
    
    lastIndex = getLastIndex( attr )
        
    affectedIndies = []
        
    for i in range( lastIndex+1 ):
            
        attrValue = cmds.getAttr( attr+'[%d]' % i )
        
        if attrValue:
            affectedIndies.append( i )
            
    return affectedIndies




def getUnConnectIndies( attr, keepIndies ):
    
    nodeName, attrName = attr.split( '.' )
    
    selList = om.MSelectionList()
    selList.add( nodeName )
    mObj = om.MObject()
    
    selList.getDependNode( 0, mObj )
    
    fnNode = om.MFnDependencyNode( mObj )
    wPlug = fnNode.findPlug( attrName )
    
    if not wPlug.numElements():
        return -1



def removeUnConnectedIndies( attr, keepIndies = [], childIndies =[] ):
    
    nodeName, attrName = attr.split( '.' )
    
    selList = om.MSelectionList()
    selList.add( nodeName )
    mObj = om.MObject()
    
    selList.getDependNode( 0, mObj )
    
    fnNode = om.MFnDependencyNode( mObj )
    wPlug = fnNode.findPlug( attrName )
    
    if not wPlug.numElements():
        return -1
    
    rangeList = range( wPlug.numElements() )
    rangeList.reverse()
    
    for i in rangeList:
        
        try:
            logicalIndex = wPlug[i].logicalIndex()
        except: break
        
        if logicalIndex in keepIndies:
            continue
        
        connections = om.MPlugArray()
        
        if childIndies:
            for index in childIndies:
                wPlug[i].child(index).connectedTo( connections, True, False )
                if connections.length() == 0:
                    cmds.removeMultiInstance( '%s[%d]' % (attr,logicalIndex) )
        else:
            wPlug[i].connectedTo( connections, True, False )
            if connections.length() == 0:
                cmds.removeMultiInstance( '%s[%d]' % (attr,logicalIndex) )
        


def getMObject( nodeStr ):
    
    selList = om.MSelectionList()
    
    mObj = om.MObject()
    selList.add( nodeStr )
    
    selList.getDependNode( 0, mObj )
    
    return mObj




def getSourseConnectPlug( plug ):
    
    connections = om.MPlugArray()
    
    plug.connectedTo( connections, True, False )
    
    if not connections.length():
        return None
    
    else:
        return connections[0]
    
    
   
    
def getBlendShapeGeoPlug( blendShapeNode, index ):
    
    if type( blendShapeNode ) != type( om.MObject() ):
        blendShapeNode = getMObject( blendShapeNode )
        
    fnBlendShapeNode = om.MFnDependencyNode( blendShapeNode )
    
    inputTargetPlug = fnBlendShapeNode.findPlug( 'inputTarget' ) 
    inputTargetGrpPlug = inputTargetPlug[0].child( 0 )
    
    inputTargetGrpIndexPlug = inputTargetGrpPlug.elementByLogicalIndex( index )
    
    inputTargetItemPlug = inputTargetGrpIndexPlug.child( 0 )
    geoPlug = inputTargetItemPlug[0].child(0)
    


def getPoints( mObj ):
    
    fnMesh = om.MFnMesh( mObj )
    
    pointArr = om.MPointArray()
    fnMesh.getPoints( pointArr )
    
    return pointArr



def setPoints( mObj, pointArr ):
    
    fnMesh = om.MFnMesh( mObj )
    
    fnMesh.setPoints( pointArr )
    
   
    
def getLastIndies( attr ):
    
    pass




def addArrayMessageAttr( targetName, attrName ):
    
    targetObj = om.MObject()
    
    selList = om.MSelectionList()
    selList.add( targetName )
    selList.getDependNode( 0, targetObj )
    
    msgAttr = om.MFnMessageAttribute()
    msgAttrObj = msgAttr.create( 'layerTarget', 'lt' )
    msgAttr.setArray( True )
    
    modify = om.MDGModifier()
    
    modify.addAttribute( targetObj, msgAttrObj )
    
    modify.doit()
    
    return modify



def createShader( shaderType = 'blinn', **options ):
    
    items = options.items()

    addOptions = {'asShader':True}
    
    for item in items:
        if item[0] in ['n', 'name']: addOptions.update( {item[0]: item[1]} ) 
    
    nodeName = cmds.shadingNode( shaderType, **addOptions )
    
    engin = cmds.sets( n= nodeName+'SG', renderable = True, noSurfaceShader=True, empty=True )
    
    cmds.connectAttr( nodeName+'.outColor', engin+'.surfaceShader' )
    
    return nodeName