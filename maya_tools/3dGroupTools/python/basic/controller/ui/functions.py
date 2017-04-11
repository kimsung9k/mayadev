import maya.OpenMaya as om
import maya.cmds as cmds


def pointListToPointArr( pointList ):
    
    pointArr = om.MPointArray()
    pointArr.setLength( len( pointList ) )
    
    for i in range( pointArr.length() ):
        pointArr[i].x = pointList[i][0]
        pointArr[i].y = pointList[i][1]
        pointArr[i].z = pointList[i][2]
    return pointArr
    
def intListToIntArr( intList ):
    
    intArr = om.MIntArray()
    intArr.setLength( len( intList ) )
    
    for i in range( intArr.length() ):
        intArr[i] = intList[i]
    return intArr
    
    
def getMObject( target ):
    selList = om.MSelectionList()
    selList.add( target )
    oNode = om.MObject()
    selList.getDependNode( 0, oNode )
    return oNode



def addCostomShader( targetShape, color=[1,1,1], opacity=[0.5,0.5,0.5] ):
    
    surfShader = cmds.shadingNode( 'surfaceShader', asShader=1 )
    shadingEngin = cmds.sets( renderable=1, noSurfaceShader=1, empty=1 )
    cmds.connectAttr( surfShader+'.outColor', shadingEngin+'.surfaceShader' )
    
    cmds.connectAttr( targetShape+'.instObjGroups[0]', shadingEngin+'.dagSetMembers[0]' )
    cmds.setAttr( surfShader+'.outColor', *color )
    cmds.setAttr( surfShader+'.outTransparency', *opacity )
    
    return surfShader



def getPolyCreateInfo( meshName ):
    
    selList = om.MSelectionList()
    selList.add( meshName )
    path = om.MDagPath()
    selList.getDagPath( 0,path )
    
    fnMesh = om.MFnMesh( path )
    
    numVtx  = fnMesh.numVertices()
    numPoly = fnMesh.numPolygons()
    mPointArr = om.MPointArray()
    mCountArr = om.MIntArray()
    mConnectArr = om.MIntArray()
    
    fnMesh.getPoints( mPointArr )
    
    mCountArr.setLength( numPoly )
    
    for i in range( numPoly ):
        mCountArr[i] = fnMesh.polygonVertexCount( i )
        
        numStr = cmds.polyInfo( meshName+'.f[%d]' % i, fv=1 )[0].split( ':' )[1].strip()
        nums = numStr.split( '    ' )
        for j in range( len( nums ) ):
            mConnectArr.append( int(nums[j].strip()) )
        
    return numVtx, numPoly, mPointArr, mCountArr, mConnectArr



def printPointArrList( pointArr ):
    pointArrLength = pointArr.length()
    for i in range( 0, pointArrLength, 3 ):
        for j in range( 3 ):
            if pointArrLength <= i+j: break
            pos = pointArr[i+j]
            
            posX = '%6.5f' % pos.x
            posY = '%6.5f' % pos.y
            posZ = '%6.5f' % pos.z
            
            if len( posX ) > 7:
                posX = posX[:-1]
            if len( posY ) > 7:
                posY = posY[:-1]
            if len( posZ ) > 7:
                posZ = posZ[:-1]
            
            print '[%s,%s,%s],' %( posX,posY,posZ ),
        print
        
def printIntArrList( intArr ):
    intArrLength = intArr.length()
    for i in range( 0, intArrLength, 9 ):
        for j in range( 9 ):
            if intArrLength <= i+j: break
            print '%4d,' % intArr[i+j],
        print
        
        
def printCVPoints( crv ):
    sels = cmds.ls( crv+'.cv[*]', fl=1 )
    
    selLen = len( sels )
    for i in range( 0, len( sels), 3 ):
        for j in range( 3 ):
            if selLen <= i+j: break
            pos = cmds.xform( sels[i+j], q=1, t=1 )
            
            posX = '%6.5f' % pos[0]
            posY = '%6.5f' % pos[1]
            posZ = '%6.5f' % pos[2]
            
            if len( posX ) > 7:
                posX = posX[:-1]
            if len( posY ) > 7:
                posY = posY[:-1]
            if len( posZ ) > 7:
                posZ = posZ[:-1]
            
            print '[%s,%s,%s],' %( posX,posY,posZ ),
        print
        


def printMeshInfo( mesh ):
    
    numVtx, numPolygon, mPointArr, mCountArr, mConnectArr = getPolyCreateInfo( mesh )

    print numVtx
    print numPolygon
    printPointArrList( mPointArr )
    printIntArrList( mCountArr )
    print
    printIntArrList( mConnectArr )