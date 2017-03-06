#include "buildSkinMesh.h"



buildSkinMesh::buildSkinMesh()
{
	m_index = 0;
}



buildSkinMesh::~buildSkinMesh()
{
}



bool buildSkinMesh::isUndoable() const
{
	return true;
}



void* buildSkinMesh::creator()
{
	return new buildSkinMesh();
}



MStatus  buildSkinMesh::displayError()
{
	MGlobal::displayError( "Select PSD Mesh" );
	return MS::kFailure;
}



MSyntax buildSkinMesh::newSyntax()
{
	MSyntax syntax;

	syntax.setObjectType( MSyntax::kSelectionList, 1 );
	syntax.useSelectionAsDefault( true );
	syntax.addFlag( "-i", "-index", MSyntax::kLong );

	syntax.enableEdit( false );
	syntax.enableQuery( false );

	return syntax;
}



MStatus buildSkinMesh::doIt( const MArgList& args )
{
	MStatus status;
	MArgDatabase argData( syntax(), args, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MSelectionList selList;
	argData.getObjects( selList ); 
	argData.getFlagArgument( "-i", 0, m_index );

	if( selList.length() == 0 )
		return displayError();

	MDagPath selectionPath;
	selList.getDagPath( 0, selectionPath );

	m_mtxWorld   = selectionPath.inclusiveMatrix();
	m_mtxInverse = selectionPath.inclusiveMatrixInverse();

	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = getNodes( selectionPath, m_fnSkinCluster, m_fnBlendAndFixedShape );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = getMatrixArrays();
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = getWeightInfos();
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = getDeltaInfos();
	CHECK_MSTATUS_AND_RETURN_IT( status );
	
	return redoIt();
}



MStatus buildSkinMesh::redoIt()
{
	MStatus status;

	m_view = M3dView::active3dView();

	m_trTargetParent.create();
	buildOriginalMesh( m_trTargetParent );

	m_meshTargetChild.setObject( m_trTargetParent.child(0) );

	m_trInverseParent.create();
	buildOriginalMesh( m_trInverseParent );

	m_meshInverseChild.setObject( m_trInverseParent.child( 0 ) );

	status = buildTarget();
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = buildInverse();
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = connect();
	CHECK_MSTATUS_AND_RETURN_IT( status );

	return MS::kSuccess;
}



MStatus buildSkinMesh::undoIt()
{
	MStatus status;

	status = m_mdagModifier.disconnect( m_plugOutput, m_plugInput );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = m_mdagModifier.deleteNode( m_trInverseParent.object() );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = m_mdagModifier.deleteNode( m_trTargetParent.object() );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = m_mdagModifier.doIt();
	CHECK_MSTATUS_AND_RETURN_IT( status );

	return MS::kSuccess;
}



MStatus buildSkinMesh::getNodes( MDagPath& path,
		               MFnDependencyNode& fnSkinCluster, 
					   MFnDependencyNode& fnBlendAndFixedShape )
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
		return displayError();
	}

	bool shapeExists;
	for( int i=0; i<shapeNum; ++i )
	{
		status = path.extendToShapeDirectlyBelow( i );
		CHECK_MSTATUS_AND_RETURN_IT( status );

		if( path.apiType() == MFn::kMesh )
		{
			MFnDagNode fnDagNode = path.node();
			if( !fnDagNode.isIntermediateObject() )
			{
				shapeExists = true;
				break;
			}
		}
	}

	
	if( !shapeExists ) 
	{
		return displayError();
	}
	
	MItDependencyGraph itGraph( path.node(), MFn::kInvalid, MItDependencyGraph::kUpstream,
		MItDependencyGraph::kDepthFirst, MItDependencyGraph::kNodeLevel, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	
	for( ; !itGraph.isDone(); itGraph.next() )
	{
		MFnDependencyNode fnCurrent = itGraph.currentItem();
		
		if( fnCurrent.typeName() == "skinCluster" && fnSkinCluster.typeName() != "skinCluster" )
			fnSkinCluster.setObject( fnCurrent.object() );
		else if( fnCurrent.typeName() == "blendAndFixedShape" && fnBlendAndFixedShape.typeName() != "blendAndFixedShape"  )
			fnBlendAndFixedShape.setObject( fnCurrent.object() );
	}

	if( fnSkinCluster.typeName() != "skinCluster" ||
		fnBlendAndFixedShape.typeName() != "blendAndFixedShape" )
	{
		return displayError();
	}

	return MS::kSuccess;
}



MStatus buildSkinMesh::buildOriginalMesh( MFnTransform& trParent )
{
	MStatus status;

	MPlug inputPlug = m_fnBlendAndFixedShape.findPlug( "input" );
	
	if( inputPlug.numElements() == 0 )
		return displayError();

	MPlug inputGeometryPlug = inputPlug[0].child( 0, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MPlugArray cons;
	inputGeometryPlug.connectedTo( cons, true, false );

	if( !cons.length() )
		return displayError();

	char buffer[512];
	sprintf( buffer, "createNode -parent %s mesh;", trParent.name().asChar() );
	status = MGlobal::executeCommand( buffer );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MFnDependencyNode fnChild = trParent.child( 0 );

	MPlug plugInMesh = fnChild.findPlug( "inMesh" );

	m_mdagModifier.connect( cons[0], plugInMesh );
	m_mdagModifier.doIt();
	m_view.refresh( true, false );
	m_mdagModifier.disconnect( cons[0], plugInMesh );
	m_mdagModifier.doIt();

	return MS::kSuccess;
}



MStatus buildSkinMesh::buildTarget()
{
	MStatus status;

	MPointArray pointArrTarget;
	m_meshTargetChild.getPoints( pointArrTarget );

	MMatrix mtxBase;
	for( int i=0; i<pointArrTarget.length(); i++ )
	{
		MIntArray&   intArrIndices  = m_vIntArrIndices[i];
		MFloatArray& floatArrValues = m_vFloatArrValues[i];

		mtxBase *= 0;
		for( int j=0; j<intArrIndices.length(); j++ )
		{
			MMatrix& mtxBuild = m_mtxArrBuild[ intArrIndices[j] ];
			mtxBase += ( mtxBuild * floatArrValues[j] );
		}

		if( m_intArrMapping[i] != -1 )
		{
			pointArrTarget[i] += m_pointArrDelta[ m_intArrMapping[i] ];
		}		
		pointArrTarget[i] *= m_mtxWorld * mtxBase * m_mtxInverse;
	}
	m_meshTargetChild.setPoints( pointArrTarget );

	return MS::kSuccess;
}


MStatus buildSkinMesh::connect()
{
	MStatus status;

	MPlug plugInMesh     = m_fnInverseNode.findPlug( "inMesh" );
	MPlug plugGeomMatrix = m_fnInverseNode.findPlug( "geomMatrix" );
	MPlug plugTargetSkin = m_fnInverseNode.findPlug( "targetSkinCluster" );
	MPlug plugMatrix     = m_fnInverseNode.findPlug( "matrix" );
	MPlug plugBindPre    = m_fnInverseNode.findPlug( "bindPreMatrix" );
	MPlug plugUpdate     = m_fnInverseNode.findPlug( "updateMatrix" );

	MPlug plugOutMesh = m_meshTargetChild.findPlug( "outMesh" );
	MPlug plugOutMatrix = m_meshTargetChild.findPlug( "matrix" );
	MPlug plugTargetSkinMessage = m_fnSkinCluster.findPlug( "message" );

	m_mdgModifier.connect( plugOutMesh, plugInMesh );
	m_mdgModifier.connect( plugOutMatrix, plugGeomMatrix );
	m_mdgModifier.connect( plugTargetSkinMessage, plugTargetSkin );
	status = m_mdgModifier.doIt();
	CHECK_MSTATUS_AND_RETURN_IT( status );

	int numMatrix = m_mtxArrMatrix.length();

	MFnMatrixData mtxData;
	for( int i=0; i<numMatrix; i++ )
	{
		MObject oMatrix = mtxData.create( m_mtxArrMatrix[i] );
		MObject oBindPre = mtxData.create( m_mtxArrBindPre[i] );
		plugMatrix.elementByLogicalIndex( i ).setMObject( oMatrix );
		plugBindPre.elementByLogicalIndex( i ).setMObject( oBindPre );
	}

	m_plugOutput  = m_meshInverseChild.findPlug( "outMesh" );
	MPlug plugBlendMeshInfosElement = m_fnBlendAndFixedShape.findPlug( "blendMeshInfos" ).elementByLogicalIndex( m_index );
	m_plugInput   = plugBlendMeshInfosElement.child( 0 );
	MPlug plugName    = plugBlendMeshInfosElement.child( 3 );

	MString stringTarget;
	MString stringInvTarget;

	m_mdagModifier.connect( m_plugOutput, m_plugInput );
	status = m_mdagModifier.doIt();
	CHECK_MSTATUS_AND_RETURN_IT( status );
	
	MPlug plugVis = m_trInverseParent.findPlug( "v" );
	plugVis.setBool( false );

	status = m_mdgModifier.doIt();
	CHECK_MSTATUS_AND_RETURN_IT( status );

	char buffer[512];
	sprintf( buffer, "rename %s %s", m_trTargetParent.fullPathName().asChar(), plugName.asString().asChar() );
	status = MGlobal::executeCommand( buffer, stringTarget, true );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	sprintf( buffer, "rename %s %s", m_trInverseParent.fullPathName().asChar(), (plugName.asString()+"_inv" ).asChar(), true );
	status = MGlobal::executeCommand( buffer, stringInvTarget );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MStringArray stringResult;
	stringResult.append( stringTarget );
	stringResult.append( stringInvTarget );

	setResult( stringResult );

	return MS::kSuccess;
}


MStatus buildSkinMesh::buildInverse()
{
	MStatus status;

	char buffer[512];
	sprintf( buffer, "deformer -type inverseSkinCluster %s;", m_meshInverseChild.name().asChar() );

	MStringArray stringArrResult;
	status = MGlobal::executeCommand( buffer, stringArrResult );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MSelectionList selectionInverseNode;
	selectionInverseNode.add( stringArrResult[0] );

	MObject oInverseNode;
	selectionInverseNode.getDependNode( 0, oInverseNode );

	m_fnInverseNode.setObject( oInverseNode );

	return MS::kSuccess;
}



MStatus buildSkinMesh::getMatrixArrays( )
{
	MStatus status;

	MPlug plugBlendMeshInfo= m_fnBlendAndFixedShape.findPlug( "blendMeshInfos", &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MPlug plugBlendMeshInfoElement = plugBlendMeshInfo.elementByLogicalIndex( m_index, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MPlug plugMatrix = plugBlendMeshInfoElement.child( 4, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MPlug plugBindPre = m_fnSkinCluster.findPlug( "bindPreMatrix", &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	int numMatrix  = plugMatrix.numElements();
	int numBindPre = plugBindPre.numElements();

	if( numMatrix > numBindPre )
	{
		numMatrix = numBindPre;
	}
	
	m_intArrBuildLogical.setLength( numMatrix );
	m_mtxArrBuild.setLength( numMatrix );
	m_mtxArrMatrix.setLength( numMatrix );
	m_mtxArrBindPre.setLength( numMatrix );

	MFnMatrixData mtxData;
	for( int i=0; i<numMatrix; i++ )
	{
		int logicalIndex = plugMatrix[i].logicalIndex();

		m_intArrBuildLogical[i] = logicalIndex;
		m_mtxArrBuild[i] = MMatrix();

		MPlug plugBindPreElement = plugBindPre.elementByLogicalIndex( logicalIndex, &status );
		CHECK_MSTATUS_AND_RETURN_IT( status );
		mtxData.setObject( plugBindPreElement.asMObject() );
		m_mtxArrBuild[i] *= mtxData.matrix();
		m_mtxArrBindPre[i] = mtxData.matrix();
		mtxData.setObject( plugMatrix[i].asMObject() );
		m_mtxArrBuild[i] *= mtxData.matrix();
		m_mtxArrMatrix[i] = mtxData.matrix();
	}

	return MS::kSuccess;
}



MStatus buildSkinMesh::getDeltaInfos()
{
	MStatus status;

	MPlug plugBlendMeshInfos = m_fnBlendAndFixedShape.findPlug( "blendMeshInfos", &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MPlug plugBlendMeshInfosElement = plugBlendMeshInfos.elementByLogicalIndex( m_index, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MPlug plugDeltas = plugBlendMeshInfosElement.child( 1 );
	
	int deltaCount = plugDeltas.numElements();

	m_intArrMapping.setLength( m_vFloatArrValues.size() );
	m_pointArrDelta.setLength( deltaCount );

	for( int i=0; i< m_intArrMapping.length(); i++ )
	{
		m_intArrMapping[i] = -1;
	}

	int logicalIndex = 0;
	for( int i=0; i<deltaCount; i++ )
	{
		logicalIndex = plugDeltas[i].logicalIndex( &status );
		CHECK_MSTATUS_AND_RETURN_IT( status );

		MPlug& deltaX = plugDeltas[i].child(0);
		MPlug& deltaY = plugDeltas[i].child(1);
		MPlug& deltaZ = plugDeltas[i].child(2);

		m_intArrMapping[logicalIndex] = i;
		m_pointArrDelta[i] = MPoint( deltaX.asDouble(), deltaY.asDouble(), deltaZ.asDouble() );
	}

	return MS::kSuccess;
}



MStatus buildSkinMesh::getWeightInfos()
{
	MStatus status;

	MPlug plugWeightList = m_fnSkinCluster.findPlug( "weightList", &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	int numWeightList = plugWeightList.numElements();

	m_vIntArrIndices.resize( numWeightList );
	m_vFloatArrValues.resize( numWeightList );

	int numWeights;

	for( int i=0; i<numWeightList; i++ )
	{
		m_vIntArrIndices[i] = MIntArray();
		m_vFloatArrValues[i] = MFloatArray();

		MPlug plugWeights = plugWeightList[i].child( 0 );
		numWeights = plugWeights.numElements();

		m_vIntArrIndices[i].setLength( numWeights );
		m_vFloatArrValues[i].setLength( numWeights );

		for( int j=0; j<numWeights; j++ )
		{
			int logicalIndex = plugWeights[j].logicalIndex();

			int physicalIndex =0;
			for( int k=0; k<m_intArrBuildLogical.length(); k++ )
			{
				if( m_intArrBuildLogical[k] == logicalIndex )
				{
					physicalIndex = k;
					break;
				}
			}
			m_vIntArrIndices[i][j] = physicalIndex;
			m_vFloatArrValues[i][j]  = plugWeights[j].asFloat();
		}
	}

	return MS::kSuccess;
}