import maya.OpenMaya as openMaya


def getMDagPath( arg1 ):
    
    mDagPath = openMaya.MDagPath()
    
    if type( arg1 ) == str:
        mSelList = openMaya.MSelectionList()
        mSelList.add( str )
        mSelList.getDagPath( 0, mDagPath )
    elif type( arg1 ) == openMaya.MObject:
        mDagPath.getAPathTo( arg1, mDagPath )
    elif type( arg1 ) == openMaya.MDagPath:
        return arg1

    return mDagPath





def getMDagPathAndComponent():
    
    mSelList = openMaya.MSelectionList()
    openMaya.MGlobal.getActiveSelectionList( mSelList )
    
    returnTargets = []
    for i in range( mSelList.length() ):
        mDagPath = openMaya.MDagPath()
        mObject  = openMaya.MObject()
        
        mSelList.getDagPath( i, mDagPath, mObject )
        
        mIntArrU = openMaya.MIntArray()
        mIntArrV = openMaya.MIntArray()
        mIntArrW = openMaya.MIntArray()
        
        if not mObject.isNull():
            if mDagPath.apiType() == openMaya.MFn.kNurbsCurve:
                component = openMaya.MFnSingleIndexedComponent( mObject )
                component.getElements( mIntArrU )
            elif mDagPath.apiType() == openMaya.MFn.kNurbsSurface:
                component = openMaya.MFnDoubleIndexedComponent( mObject )
                component.getElements( mIntArrU, mIntArrV )
            elif mDagPath.apiType() == openMaya.MFn.kLattice:
                component = openMaya.MFnTripleIndexedComponent( mObject )
                component.getElements( mIntArrU, mIntArrV, mIntArrW )
            elif mObject.apiType() == openMaya.MFn.kMeshVertComponent:
                component = openMaya.MFnSingleIndexedComponent( mObject )
                component.getElements( mIntArrU )
            elif mObject.apiType() == openMaya.MFn.kMeshEdgeComponent:
                mfnMesh = openMaya.MFnMesh( mDagPath )
                component = openMaya.MFnSingleIndexedComponent( mObject )
                mIntArr = openMaya.MIntArray()
                component.getElements( mIntArr )
                mIntArrU.setLength( mIntArr.length() * 2 )
                util = openMaya.MScriptUtil()
                util.createFromList([0,0],2)
                ptrEdgeToVtxIndex = util.asInt2Ptr()
                for i in range( mIntArr.length() ):
                    mfnMesh.getEdgeVertices( mIntArr[i], ptrEdgeToVtxIndex )
                    index1 = util.getInt2ArrayItem( ptrEdgeToVtxIndex, 0, 0 )
                    index2 = util.getInt2ArrayItem( ptrEdgeToVtxIndex, 0, 1 )
                    mIntArrU[i*2  ] = index1
                    mIntArrU[i*2+1] = index2 
            elif mObject.apiType() == openMaya.MFn.kMeshPolygonComponent:
                mfnMesh = openMaya.MFnMesh( mDagPath )
                component = openMaya.MFnSingleIndexedComponent( mObject )
                mIntArr = openMaya.MIntArray()
                component.getElements( mIntArr )
                mIntArrEach = openMaya.MIntArray()
                for i in range( mIntArr.length() ):
                    mfnMesh.getPolygonVertices( mIntArr[i], mIntArrEach )
                    for i in range( mIntArrEach.length() ):
                        mIntArrU.append( mIntArrEach[i] )
        
        returnTargets.append( [mDagPath, mIntArrU, mIntArrV, mIntArrW] )
    
    return returnTargets




def getMBoundingBoxFromSelection( **options ):
    
    mBoundingBox = openMaya.MBoundingBox()
    
    for mDagPath, indicesU, indicesV, indicesW in getMDagPathAndComponent():
        
        mMatrixMult = mDagPath.inclusiveMatrix()
        mMatrixParent = mDagPath.exclusiveMatrix()
        mPointArr   = openMaya.MPointArray()
        
        if not indicesU.length():
            mBoundingBox.expand( openMaya.MFnDagNode( mDagPath ).boundingBox().min()*mMatrixParent )
            mBoundingBox.expand( openMaya.MFnDagNode( mDagPath ).boundingBox().max()*mMatrixParent )
        
        if mDagPath.apiType() == openMaya.MFn.kMesh:
            mfnMesh = openMaya.MFnMesh( mDagPath )
            mPointArrMesh = openMaya.MPointArray()
            mfnMesh.getPoints( mPointArrMesh )
            
            mPointArr.setLength( indicesU.length() )
            
            for i in range( indicesU.length() ):
                mPointArr.set( mPointArrMesh[ indicesU[i] ] * mMatrixMult, i )
        
        elif mDagPath.apiType() == openMaya.MFn.kNurbsCurve:
            mfnNurbsCurve = openMaya.MFnNurbsCurve( mDagPath )
            mPointArrCVs = openMaya.MPointArray()
            mfnNurbsCurve.getCVs( mPointArrCVs )
            
            mPointArr.setLength( indicesU.length() )
            
            for i in range( indicesU.length() ):
                mPointArr.set( mPointArrCVs[ indicesU[i] ] * mMatrixMult, i )
        
        elif mDagPath.apiType() == openMaya.MFn.kNurbsSurface:

            mfnNurbsSurface = openMaya.MFnNurbsSurface( mDagPath )
            mPointArrCVs = openMaya.MPointArray()
            mfnNurbsSurface.getCVs( mPointArrCVs )
            
            numV = mfnNurbsSurface.numCVsInV()
            
            mPointArr.setLength( indicesU.length() )
            
            for i in range( indicesU.length() ):
                mPointArr.set( mPointArrCVs[ indicesU[i]*numV + indicesV[i] ] * mMatrixMult, i )
        
        elif mDagPath.apiType() == openMaya.MFn.kLattice:
            
            import maya.cmds as cmds
            
            mfnDagNode = openMaya.MFnDagNode( mDagPath )
            
            strName = mfnDagNode.fullPathName()
            
            mPointArr.setLength(indicesU.length() )
            
            for i in range( indicesU.length() ):
                pt = strName+'.pt[%d][%d][%d]' % ( indicesU[i], indicesV[i], indicesW[i] )
                mPointArr.set( openMaya.MPoint( *cmds.xform( pt, q=1, os=1, t=1 ) ) * mMatrixMult, i )
        
        
        for i in range( mPointArr.length() ):
            mBoundingBox.expand( mPointArr[i] )
    
    return mBoundingBox