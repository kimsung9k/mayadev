#include  "addMirrorBlendMeshInfos.h"


int addMirrorBlendMeshInfos::m_iVerticesNum;
MMeshIntersector* addMirrorBlendMeshInfos::m_pMeshIntersector;


addMirrorBlendMeshInfos::addMirrorBlendMeshInfos()
{
	m_iSource = 0;
	m_iTargetAxisIndex = 0;

	m_iVerticesNum = -1;
	m_bReIntersect = false;

	MThreadPool::init();
}


addMirrorBlendMeshInfos::~addMirrorBlendMeshInfos()
{
	MThreadPool::release();
}



bool	addMirrorBlendMeshInfos::isUndoable() const
{
	return true;
}



void*	addMirrorBlendMeshInfos::creator()
{
	return new addMirrorBlendMeshInfos();
}



MSyntax	addMirrorBlendMeshInfos::newSyntax()
{
	MSyntax	syntax;

	syntax.setObjectType( MSyntax::kSelectionList, 1, 1 );
	syntax.useSelectionAsDefault( true );
	syntax.addFlag( "-i", "-index", MSyntax::kLong );
	syntax.addFlag( "-mi", "-mirrorIndex", MSyntax::kLong );
	syntax.addFlag( "-rei", "-reIntersect", MSyntax::kBoolean );

	syntax.enableEdit( false );
	syntax.enableQuery( false );

	return syntax;
}



MStatus	addMirrorBlendMeshInfos::doIt( const MArgList& args )
{
	MStatus status;

	MArgDatabase	argData( syntax(), args, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MSelectionList	selList;
	status = argData.getObjects( selList );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = argData.getFlagArgument( "-i", 0, m_iSource );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = argData.getFlagArgument( "-mi", 0, m_iTargetAxisIndex );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = argData.getFlagArgument( "-rei", 0, m_bReIntersect );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MDagPath pathShape;
	status = selList.getDagPath( 0, pathShape );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = getNodes( pathShape );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	
	MPlug plugBlendMeshInfo = m_fnBlendAndFixedShape.findPlug( "blendMeshInfos" );
	m_iTarget = plugBlendMeshInfo.numElements();

	m_pBlendMeshInfoData = new blendMeshInfoData;
	m_pMeshIntersectData = new meshIntersectData;

	getJointMatrixInfo();
	getMirrorJointIndices();

	getDeltaInfo();

	return redoIt();
}


MStatus  addMirrorBlendMeshInfos::createOriginalMesh( MObject& oParent, MObject& oMesh )
{
	MStatus status;

	MPlug plugInput = m_fnBlendAndFixedShape.findPlug( "input" );
	MPlug plugInputGeo = plugInput[0].child( 0 );

	MPlugArray cons;
	plugInputGeo.connectedTo( cons, true, false );

	if( !cons.length() )
	{
		return MS::kFailure;
	}

	oMesh = m_mdagModifier.createNode( "mesh", oParent, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = m_mdagModifier.doIt();
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MFnDependencyNode fnMesh = oMesh;
	MPlug plugInMesh = fnMesh.findPlug( "inMesh" );

	m_mdagModifier.connect( cons[0], plugInMesh );
	status = m_mdagModifier.doIt();
	CHECK_MSTATUS_AND_RETURN_IT( status );

	m_view = M3dView::active3dView();
	m_view.refresh( true, false );

	m_mdagModifier.disconnect( cons[0], plugInMesh );
	status = m_mdagModifier.doIt();
	CHECK_MSTATUS_AND_RETURN_IT( status );

	return MS::kSuccess;
}


MStatus	addMirrorBlendMeshInfos::redoIt()
{
	MStatus status;

	setJointMatrix();

	MObject oParent = m_mdagModifier.createNode( "transform" );
	m_mdagModifier.doIt();

	MObject oMesh;
	status = createOriginalMesh( oParent, oMesh );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	m_pMeshIntersectData->fnMesh.setObject( oMesh );

	setThread();
	MThreadPool::newParallelRegion( parallelCompute, ( void* )m_pThreadData );
	endThread();

	status = connectMeshToTarget( oMesh );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = m_mdagModifier.deleteNode( oParent );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	return MS::kSuccess;
}


void addMirrorBlendMeshInfos::endThread()
{
}


void addMirrorBlendMeshInfos::parallelCompute( void* data, MThreadRootTask *pRoot )
{
	addMirrorThreadData* m_pThreadData = ( addMirrorThreadData* )data;

	if( m_pThreadData )
	{
		for( int i=0; i< m_pThreadData->numThread; i++ )
		{
			MThreadPool::createTask( deformCompute, ( void* )&m_pThreadData[i], pRoot );
		}
		MThreadPool::executeAndJoin( pRoot );
	}
}


MThreadRetVal addMirrorBlendMeshInfos::deformCompute( void* pThread )
{

	addMirrorThreadData* m_pThreadData = ( addMirrorThreadData* )pThread;

	meshIntersectData* pInterectData = m_pThreadData->pMeshIntersectData;
	MMeshIntersector& intersector = *pInterectData->p_meshIntersector;
	MFnMesh& fnMesh   = pInterectData->fnMesh;

	MPointOnMesh pointOnMesh;
	MIntArray intArrVertices;
	int    indexClose;
	double  dbCloseDist;
	MPoint pointClose;

	for( int i=m_pThreadData->start; i< m_pThreadData->end; i++ )
	{	
		int logicalIndex = pInterectData->intArrDeltas[i];
		MPoint& pointArrDelta = pInterectData->pointArrDeltas[i];

		MPoint pointSource;
		fnMesh.getPoint( logicalIndex, pointSource );
		pointSource[0] *= -1;
		pointArrDelta[0] *= -1;

		intersector.getClosestPoint( pointSource, pointOnMesh );

		fnMesh.getPolygonVertices( pointOnMesh.faceIndex(), intArrVertices );
		
		dbCloseDist = 1000.0;
		for( int j=0; j<intArrVertices.length(); j++ )
		{
			fnMesh.getPoint( intArrVertices[j], pointClose );

			double dbDist = pointClose.distanceTo( pointSource );
			
			if( dbCloseDist > dbDist )
			{
				dbCloseDist = dbDist;
				indexClose = intArrVertices[j];
			}
		}
		MPoint pointTarget;
		fnMesh.getPoint( indexClose, pointTarget );

		fnMesh.setPoint( indexClose, pointArrDelta + pointTarget );
	}
	return (MThreadRetVal)0;
}



MStatus addMirrorBlendMeshInfos::connectMeshToTarget( MObject& oMesh )
{
	MStatus status;

	MPlug plugBlendMeshInfos = m_fnBlendAndFixedShape.findPlug( "blendMeshInfos" );
	MPlug plugTarget = plugBlendMeshInfos.elementByLogicalIndex( m_iTarget );

	MPlug plugInputMesh = plugTarget.child( 0 );

	MFnDependencyNode fnMesh = oMesh;
	MPlug plugOutMesh = fnMesh.findPlug( "outMesh" );

	status = m_mdagModifier.connect( plugOutMesh, plugInputMesh );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	m_mdagModifier.doIt();

	m_view = M3dView::active3dView();
	m_view.refresh( true, false );

	return MS::kSuccess;
}



MStatus addMirrorBlendMeshInfos::setJointMatrix()
{
	MStatus status;

	MPlug& plugTarget = m_pBlendMeshInfoData->plugTarget;
	MIntArray& intArrJoints = m_pBlendMeshInfoData->intArrJoints;
	MIntArray& intArrMirrorTarget = m_pBlendMeshInfoData->intArrMirrorTarget;
	MMatrixArray& mtxArrTargetJoints = m_pBlendMeshInfoData->mtxArrTargetJoints;
	MMatrixArray& mtxArrDefaultJoints = m_pBlendMeshInfoData->mtxArrDefaultJoints;

	MFnMatrixData mtxData;
	for( int i=0; i< intArrJoints.length(); i++ )
	{
		int logicalIndex = intArrJoints[i];
		MPlug& plugElement = plugTarget.elementByLogicalIndex( logicalIndex );
		
		int mirrorIndex = intArrMirrorTarget[i];

		MMatrix& mtxSource = mtxArrTargetJoints[ mirrorIndex ];
		MMatrix& mtxSourceDefault = mtxArrDefaultJoints[ mirrorIndex ];
		MMatrix& mtxTargetDefault = mtxArrDefaultJoints[ i ];

		MMatrix mtxSet;
		if( i != mirrorIndex )
		{
			mtxSet = setMatrixMirror( mtxSourceDefault, mtxTargetDefault, mtxSource );
		}
		else
		{
			mtxSet = mtxSource;
		}
		mtxData.create( mtxSet );
		plugElement.setMObject( mtxData.object() );
	}

	return MS::kSuccess;
}



MMatrix addMirrorBlendMeshInfos::setMatrixMirror( MMatrix& mtxSourceDefault, MMatrix& mtxTargetDefault, MMatrix& mtxSource )
{
	MMatrix mtxTargetDeaultCopy = mtxTargetDefault;
	
	for( int i=0; i<4; i++ )
	{
		mtxTargetDeaultCopy(i,m_iTargetAxisIndex%3) *= -1;
	}

	MMatrix mtxLocal = mtxTargetDeaultCopy*mtxSourceDefault.inverse();
	MMatrix mtxTarget = mtxLocal * mtxSource;

	for( int i=0; i<4; i++ )
	{
		mtxTarget(i,m_iTargetAxisIndex%3) *= -1;
	}

	return mtxTarget;
}



MStatus addMirrorBlendMeshInfos::getDeltaInfo()
{
	MStatus status;

	if( m_iVerticesNum != m_meshTarget.numVertices() || m_bReIntersect )
	{
		m_iVerticesNum = m_meshTarget.numVertices();

		m_pMeshIntersector = new MMeshIntersector;
		m_pMeshIntersector->create( m_meshTarget.object() );
	}

	MPlug plugBlendMeshInfo = m_fnBlendAndFixedShape.findPlug( "blendMeshInfos" );

	MPlug plugBlendMeshInfoElement = plugBlendMeshInfo[ m_iSource ].child( 1 );
	int numElements = plugBlendMeshInfoElement.numElements();
	m_pMeshIntersectData->intArrDeltas.setLength( numElements );
	m_pMeshIntersectData->pointArrDeltas.setLength( numElements );

	for( int i=0; i< numElements; i++ )
	{
		m_pMeshIntersectData->intArrDeltas[i] = plugBlendMeshInfoElement[i].logicalIndex();
		MPlug deltaX = plugBlendMeshInfoElement[i].child( 0 );
		MPlug deltaY = plugBlendMeshInfoElement[i].child( 1 );
		MPlug deltaZ = plugBlendMeshInfoElement[i].child( 2 );
		m_pMeshIntersectData->pointArrDeltas[i] = MPoint( deltaX.asDouble(), deltaY.asDouble(), deltaZ.asDouble() );
	}

	m_pMeshIntersectData->p_meshIntersector = m_pMeshIntersector;

	return MS::kSuccess;
}



MStatus addMirrorBlendMeshInfos::getJointMatrixInfo()
{
	MStatus status;

	MPlug plugBlendMeshInfos = m_fnBlendAndFixedShape.findPlug( "blendMeshInfos" );
	if( m_iSource >= plugBlendMeshInfos.numElements() )
	{
		return MS::kFailure;
	}
	MPlug plugSource = plugBlendMeshInfos[ m_iSource ];
	MPlug plugTarget = plugBlendMeshInfos.elementByLogicalIndex( m_iTarget );

	MPlug plugName = plugSource.child( 3 );
	MPlug plugDeltas = plugSource.child( 1 );
	MPlug plugKeepMatrix = plugSource.child( 4 );
	MPlug plugDefaultMatrix = m_fnSkinCluster.findPlug( "bindPreMatrix" );

	blendMeshInfoData& infoData = *m_pBlendMeshInfoData;

	infoData.name = plugName.asString();
	infoData.plugSource = plugSource.child( 4 );
	infoData.plugTarget = plugTarget.child( 4 );

	int matrixLength = plugKeepMatrix.numElements();
	infoData.intArrJoints.setLength( matrixLength );
	infoData.mtxArrDefaultJoints.setLength( matrixLength );
	infoData.mtxArrTargetJoints.setLength( matrixLength );

	MFnMatrixData mtxData;
	for( int i=0; i< matrixLength; i++ )
	{
		int logicalIndex = plugKeepMatrix[i].logicalIndex();
		infoData.intArrJoints[i] = logicalIndex;

		mtxData.setObject( plugKeepMatrix[i].asMObject() );
		infoData.mtxArrTargetJoints[i] = mtxData.matrix();
		mtxData.setObject( plugDefaultMatrix.elementByLogicalIndex( logicalIndex ).asMObject() );
		infoData.mtxArrDefaultJoints[i] = mtxData.matrix().inverse();
		//cout << infoData.mtxArrTargetJoints[i] << endl;
	}
	return MS::kSuccess;
}



MStatus addMirrorBlendMeshInfos::getMirrorJointIndices()
{
	MStatus status;

	blendMeshInfoData& infoData = *m_pBlendMeshInfoData;

	MMatrixArray& mtxArrDefaultJoints = infoData.mtxArrDefaultJoints;
	MIntArray&    intArrTarget       = infoData.intArrJoints;
	MIntArray&    intArrMirrorTarget = infoData.intArrMirrorTarget;

	MIntArray    intArrMirrorLogicalTarget;

	int matrixLength = mtxArrDefaultJoints.length();

	intArrMirrorLogicalTarget.setLength( matrixLength ); 
	intArrMirrorTarget.setLength( matrixLength );

	int    closeIndex;
	double closeDist;

	for( int i=0; i< matrixLength; i++ )
	{
		intArrMirrorLogicalTarget[i] = -1;
	}

	for( int i=0; i< matrixLength; i++ )
	{
		MPoint pointBaseMirrored = getMirrorPointFromMatrix( mtxArrDefaultJoints[i] );

		if( intArrMirrorLogicalTarget[i] != -1 )
		{
			continue;
		}

		closeIndex = i;
		closeDist = 10000.0;

		for( int j=i; j< matrixLength; j++ )
		{
			MPoint pointTarget = getPointFromMatrix( mtxArrDefaultJoints[j] );
			double dist = pointTarget.distanceTo( pointBaseMirrored );

			if( dist < closeDist )
			{
				closeDist = dist;
				closeIndex = j;
			}

			if( dist < 0.00001 )
				break;
		}

		intArrMirrorLogicalTarget[i] = intArrTarget[closeIndex];
		intArrMirrorLogicalTarget[closeIndex] = intArrTarget[i];

		intArrMirrorTarget[i] = closeIndex;
		intArrMirrorTarget[closeIndex] = i;
	}
	return MS::kSuccess;
}



MPoint addMirrorBlendMeshInfos::getPointFromMatrix( MMatrix& mtx )
{
	return MPoint( mtx(3,0), mtx(3,1), mtx(3,2) );
}



MPoint addMirrorBlendMeshInfos::getMirrorPointFromMatrix( MMatrix& mtx )
{
	MPoint mirrorPoint( mtx(3,0), mtx(3,1), mtx(3,2) );
	mirrorPoint[ m_iTargetAxisIndex%3 ] *= -1;
	return mirrorPoint;
}



MStatus addMirrorBlendMeshInfos::undoIt()
{
	MStatus status;

	MPlug plugElement = m_fnBlendAndFixedShape.findPlug( "blendMeshInfos" )[ m_iTarget ];
	char buffer[512];
	sprintf( buffer, "removeMultiInstance %s -b true;", plugElement.name().asChar() );
	MGlobal::executeCommand( buffer );

	return MS::kSuccess;
}



MStatus addMirrorBlendMeshInfos::getNodes( MDagPath& path )
{
	MStatus status;

	if( path.apiType() != MFn::kTransform )
	{
		status = path.pop( 0 );
		CHECK_MSTATUS_AND_RETURN_IT( status );
	}

	unsigned int shapeNum;
	path.numberOfShapesDirectlyBelow( shapeNum );
	
	if( !shapeNum ) 
	{
		return MS::kFailure;
	}

	bool shapeExists;
	for( int i=0; i<shapeNum; ++i )
	{
		status = path.extendToShapeDirectlyBelow( i );
		CHECK_MSTATUS_AND_RETURN_IT( status );

		if( path.apiType() == MFn::kMesh )
		{
			m_meshTarget.setObject( path.node() );
			if( !m_meshTarget.isIntermediateObject() )
			{
				shapeExists = true;
				break;
			}
		}
	}

	
	if( !shapeExists ) 
	{
		return MS::kFailure;
	}
	
	MItDependencyGraph itGraph( path.node(), MFn::kInvalid, MItDependencyGraph::kUpstream,
		MItDependencyGraph::kDepthFirst, MItDependencyGraph::kNodeLevel, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	
	bool skinExists = false;
	bool blendAndFixedExists = false;
	for( ; !itGraph.isDone(); itGraph.next() )
	{
		MFnDependencyNode fnCurrent = itGraph.currentItem();
		if( !skinExists && fnCurrent.typeName() == "skinCluster" )
		{
			m_fnSkinCluster.setObject( fnCurrent.object() );
			skinExists = true;
		}
		else if( !blendAndFixedExists && fnCurrent.typeName() == "blendAndFixedShape" )
		{
			m_fnBlendAndFixedShape.setObject( fnCurrent.object() );
			blendAndFixedExists = true;
		}
	}

	if( !skinExists && !blendAndFixedExists )
	{
		return MS::kFailure;
	}

	return MS::kSuccess;
}


void addMirrorBlendMeshInfos::setThread()
{
	int numThread = ADDMIRROR_NUMTHREAD;

	int numElements = m_pMeshIntersectData->intArrDeltas.length();
	int eachLength = numElements/numThread;
	int restLength = numElements - eachLength*numThread;

	m_pThreadData = new addMirrorThreadData[ numThread ];
	
	int start=0;
	for( int i=0; i< numThread; i++ )
	{
		if(  0 < restLength-- )
		{
			m_pThreadData[i].start = start;
			m_pThreadData[i].end   = start+eachLength+1;
		}
		else
		{
			m_pThreadData[i].start = start;
			m_pThreadData[i].end   = start+eachLength;
		}
		m_pThreadData[i].numThread = numThread;
		m_pThreadData[i].pMeshIntersectData = m_pMeshIntersectData;
		start = m_pThreadData[i].end;
	}
}