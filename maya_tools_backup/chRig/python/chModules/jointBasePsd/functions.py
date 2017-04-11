'''
Created on 2013. 8. 2.

@author: skkim
'''
import maya.cmds as cmds
import maya.OpenMaya as om



def getMObject( nodeName ):
    
    selList = om.MSelectionList()
    selList.add( nodeName )
    mObj = om.MObject()
    selList.getDependNode( 0, mObj )
    return mObj




def getNodeFromHist( target, nodeType ):
    
    hists = cmds.listHistory( target, pdo=1 )
    
    if not hists: return None
    
    for hist in hists:
        if cmds.nodeType( hist ) == nodeType:
            return hist
        


def clearNoneConnectedElements( targetPlug ):
    
    removeTargets = []
    for i in range( targetPlug.numElements() ):
        if not cmds.listConnections( targetPlug[i].name() ):
            removeTargets.append( targetPlug[i].name() )
    
    for target in removeTargets:
        cmds.removeMultiInstance( target )


        

def getPlugFromString( attr ):
    
    def plugAttr( plug, attrName ):
        
        try:
            origAttrName, indexSep = attrName[0].split( '[' )
        except:
            origAttrName = attrName
            indexSep = None
        
        i=0
        
        while ( i < plug.numChildren() ):
           
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
        nextPlug = plug.elementByLogicalIndex( index )
        
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
    
    return findAttrPlug( fnNode, attrName )




def getLastIndex( attr ):
    
    targetAttrPlug = getPlugFromString( attr )
    
    if not targetAttrPlug.numElements(): return -1;

    return targetAttrPlug[ targetAttrPlug.numElements()-1 ].logicalIndex()



def getOrigShape( shape ):
    
    nodeType = cmds.nodeType( shape )
    
    outputAttr = ''
    inputAttr = ''
    if nodeType in ['nurbsSurface','nurbsCurve']:
        outputAttr = 'local'
        inputAttr  = 'create'
    elif nodeType == 'mesh':
        outputAttr = 'outMesh'
        inputAttr  = 'inMesh'
    
    cons = cmds.listConnections( shape, s=1, d=0, c=1, p=1 )
    
    origShapeNode = None
    
    if cons:
        outputCons = cons[1::2]
        inputCons = cons[::2]
        
        outputNode = ''
        for i in range( len( inputCons ) ):
            if inputCons[i].split( '.' )[1] == inputAttr:
                outputNode = outputCons[i].split( '.' )[0]
        
        checkList = []
        if outputNode:
            def getOrigShapeNode( node ):
                if node in checkList: return None
                checkList.append( node )
                if not cmds.nodeType( node ): return None
                if cmds.nodeType( node ) == nodeType:
                    if cmds.getAttr( node+'.io' ):
                        return node

                cons = cmds.listConnections( node, s=1, d=0, p=1, c=1 )
                nodes = []
                if cons:
                    for con in cons[1::2]:
                        nodes.append( getOrigShapeNode( con.split( '.' )[0] ) )
                for node in nodes:
                    if node:
                        return node
                return None
            origShapeNode = getOrigShapeNode( outputNode )
    
    if origShapeNode:
        return origShapeNode
    else:
        cons = 1
        while( cons ):
            cons = cmds.listConnections( shape+'.'+inputAttr, p=1,c=1 )
            if cons:
                for con in cons[1::2]:
                    cmds.delete( con.split( '.' )[0] )
        
        origNode = cmds.createNode( nodeType, n='temp_origNodeShape' )
        origP    = cmds.listRelatives( origNode, p=1 )[0]
        cmds.connectAttr(    shape +  '.'+outputAttr, origNode+'.'+inputAttr )
        duOrigP  = cmds.duplicate( origP )[0]
        duOrig   = cmds.listRelatives( duOrigP, s=1 )[0]
        cmds.connectAttr(    duOrig+'.'+outputAttr, shape+   '.'+inputAttr )
        shapeP   = cmds.listRelatives( shape, p=1 )[0]
        cmds.parent( duOrig, shapeP, add=1, shape=1 )
        cmds.delete( origP, duOrigP )
        cmds.setAttr( duOrig+'.io', 1 )
        origShapeNode = cmds.rename( duOrig, shape+'Orig' )
        return origShapeNode