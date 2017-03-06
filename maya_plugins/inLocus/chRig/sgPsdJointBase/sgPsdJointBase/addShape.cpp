#include "addShape.h"
#include "node.h"

AddShape::AddShape()
{
}


AddShape::~AddShape()
{
}


MSyntax AddShape::newSyntax()
{
	MSyntax syntax;

	syntax.setObjectType( MSyntax::kSelectionList, 2, 2 );
	syntax.addFlag( "-i", "-index", MSyntax::kLong );
	syntax.useSelectionAsDefault( true );

	syntax.enableEdit( false );
	syntax.enableQuery( false );

	return syntax;
}


void* AddShape::creator()
{
	return new AddShape();
}


bool AddShape::isUndoable() const
{
	return true;
}


MStatus AddShape::doIt( const MArgList& args )
{
	MStatus status;

	MArgDatabase argData( syntax(), args, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = argData.getFlagArgument( "-i", 0, m_inputIndex );
	if( !status ) m_inputIndex = -1;

	MSelectionList selList;
	status = argData.getObjects( selList );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = selList.getDagPath( 0, m_pathTarget );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = selList.getDagPath( 1, m_pathBase );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = getShapeNode( m_pathTarget );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = getShapeNode( m_pathBase );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = getDeformer( m_oPsd, m_oSkin );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = getDeltas( m_pathTarget, m_pathBase );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = getMatrixInfo( m_oSkin );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = getWeightInfo( m_oSkin );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = multMatrixDelta();
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = getLastLogicalIndex( m_oPsd, m_logicalDeltaInfoAdd );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	return redoIt();
}


MStatus AddShape::redoIt()
{
	MStatus status;

	MFnDependencyNode fnPsd = m_oPsd;
	MPlug plugDeltaInfo = fnPsd.findPlug( "deltaInfo" );

	cout << "m_inputIndex : " << m_inputIndex << endl;
	if( m_inputIndex != -1 )
	{
		MPlug plugDeltaInfoEl = plugDeltaInfo.elementByLogicalIndex( m_inputIndex );
		
		int numDeltas =plugDeltaInfoEl.numElements();
		m_deltasBefore.setLength( numDeltas );
		m_logicalsBefore.setLength( numDeltas );

		for( int i=0; i<numDeltas ; i++ )
		{
			int   logical = plugDeltaInfoEl[i].logicalIndex();
			MPlug delta = plugDeltaInfoEl[i];
			MPlug deltaX = delta.child( 0 );
			MPlug deltaY = delta.child( 1 );
			MPlug deltaZ = delta.child( 2 );

			m_deltasBefore[i].x = deltaX.asDouble();
			m_deltasBefore[i].y = deltaY.asDouble();
			m_deltasBefore[i].z = deltaZ.asDouble();
			m_logicalsBefore[i] = logical;
		}

		char buffer[512];
		sprintf( buffer, "removeMultiInstance %s[%d];", plugDeltaInfo.name().asChar(), m_inputIndex );
		MGlobal::executeCommand( buffer );
		cout << buffer << endl;

		m_logicalDeltaInfoAdd = m_inputIndex;
	}

	MPlug plugDeltaInfoEl = plugDeltaInfo.elementByLogicalIndex( m_logicalDeltaInfoAdd );

	for( int i=0; i< m_deltas.length(); i++ )
	{
		int logical = m_logicalDeltas[i];
		const MPoint& point = m_deltas[i];

		MPlug plugDelta = plugDeltaInfoEl.child(2).elementByLogicalIndex( logical );
		MPlug plugDeltaX = plugDelta.child( 0 );
		MPlug plugDeltaY = plugDelta.child( 1 );
		MPlug plugDeltaZ = plugDelta.child( 2 );

		plugDeltaX.setDouble( point.x );
		plugDeltaY.setDouble( point.y );
		plugDeltaZ.setDouble( point.z );
	}

	return status;
}


MStatus AddShape::undoIt()
{
	MStatus status;

	MFnDependencyNode fnPsd = m_oPsd;
	MPlug plugDeltaInfo = fnPsd.findPlug( "deltaInfo" );

	char buffer[512];
	sprintf( buffer, "removeMultiInstance %s[%d];", plugDeltaInfo.name().asChar(), m_logicalDeltaInfoAdd );
	MGlobal::executeCommand( buffer );
	cout << buffer << endl;

	if( m_inputIndex != -1 )
	{
		MPlug plugDeltaInfoEl = plugDeltaInfo.elementByLogicalIndex( m_logicalDeltaInfoAdd );

		for( int i=0; i< m_deltasBefore.length(); i++ )
		{
			int logical = m_logicalsBefore[i];
			const MPoint& point = m_deltasBefore[i];

			MPlug plugDelta = plugDeltaInfoEl.child(2).elementByLogicalIndex( logical );
			MPlug plugDeltaX = plugDelta.child( 0 );
			MPlug plugDeltaY = plugDelta.child( 1 );
			MPlug plugDeltaZ = plugDelta.child( 2 );

			plugDeltaX.setDouble( point.x );
			plugDeltaY.setDouble( point.y );
			plugDeltaZ.setDouble( point.z );
		}
	}

	return status;
}


MStatus AddShape::getLastLogicalIndex( const MObject& oPsd, unsigned int& index )
{
	MStatus status;

	MFnDependencyNode fnPsd = oPsd;

	MPlug plugDeltaInfo = fnPsd.findPlug( "deltaInfo" );
	
	int lastNum = plugDeltaInfo.numElements() - 1;

	index = plugDeltaInfo[ lastNum ].logicalIndex() + 1;

	return MS::kSuccess;
}


MStatus AddShape::multMatrixDelta()
{
	MStatus status;

	MMatrix mtxMain;

	for( int i=0; i< m_deltas.length(); i++ )
	{
		MVector& delta = m_deltas[i];
		int     deltaLogical = m_logicalDeltas[i];

		WeightInfo& deltaInfo = m_weightArr[ deltaLogical ];

		mtxMain *= 0.0;
		for( int j=0; j< deltaInfo.fArrValues.length(); j++ )
		{
			int   logical = deltaInfo.indicesLogical[j];
			float value = deltaInfo.fArrValues[j];
			int  mtxIndex = m_mtxInfo.indicesLogicalMap[ logical ];

			const MMatrix& mtx = m_mtxInfo.mtxArr[ mtxIndex ];
			const MMatrix& mtxBpr = m_mtxInfo.mtxArrBindPre[ mtxIndex ];

			mtxMain += mtxBpr * mtx * value;
		}

		delta *= mtxMain.inverse();

	}

	return MS::kSuccess;
}



MStatus AddShape::getDeltas( MDagPath& pathTarget, MDagPath& pathBase )
{
	MStatus status;

	MFnMesh meshTarget = pathTarget;
	MFnMesh meshBase   = pathBase;

	MPointArray pointArrTarget;
	MPointArray pointArrBase;

	meshTarget.getPoints( pointArrTarget );
	meshBase.getPoints( pointArrBase );

	if( pointArrTarget.length() != pointArrBase.length() )
		return MS::kFailure;

	MVector delta;
	for( int i=0; i< pointArrTarget.length(); i++ )
	{
		MPoint& pointTarget = pointArrTarget[i];
		MPoint& pointBase = pointArrBase[i];

		delta = pointTarget - pointBase;

		if( delta.length() > 0.001 )
		{
			m_deltas.append( delta );
			m_logicalDeltas.append( i );
		}
	}

	return status;
}



MStatus AddShape::getMatrixInfo( const MObject& oSkin )
{
	MStatus status;

	MMatrix mtxBase = m_pathBase.inclusiveMatrix();

	MFnDependencyNode fnSkin = oSkin;
	MPlug plugMtx     = fnSkin.findPlug( "matrix" );
	MPlug plugBindPre = fnSkin.findPlug( "bindPreMatrix" );

	int lengthMtx = plugMtx.numElements();
	int lengthLogical = plugMtx[ lengthMtx -1 ].logicalIndex() + 1;

	m_mtxInfo.setLength( lengthMtx );
	m_mtxInfo.setLengthLogical( lengthLogical );

	for( int i=0; i< lengthMtx; i++ )
	{
		int indexLogical = plugMtx[i].logicalIndex();
		MFnMatrixData mtxData = plugMtx[i].asMObject();
		MFnMatrixData bprData = plugBindPre.elementByLogicalIndex( indexLogical ).asMObject();

		m_mtxInfo.mtxArr[i] = mtxData.matrix() * mtxBase.inverse();
		m_mtxInfo.mtxArrBindPre[i] = mtxBase * bprData.matrix();
		m_mtxInfo.indicesLogicalMap[indexLogical] = i;
	}

	return MS::kSuccess;
}



MStatus AddShape::getWeightInfo( const MObject& oSkin )
{
	MStatus status;

	MFnDependencyNode fnSkin = oSkin;
	MPlug plugWeightList = fnSkin.findPlug( "weightList" );
	
	int lengthWeightList = plugWeightList.numElements();
	m_weightArr.setLength( lengthWeightList );

	for( int i=0; i< lengthWeightList; i++ )
	{
		MPlug plugWeights = plugWeightList[i].child( 0 );
		int lengthWeights = plugWeights.numElements();
		m_weightArr[i].setLength( lengthWeights );

		for( int j=0; j< lengthWeights; j++ )
		{
			m_weightArr[i].indicesLogical[j] = plugWeights[j].logicalIndex();;
			m_weightArr[i].fArrValues[j] = plugWeights[j].asFloat();
		}
	}
	return MS::kSuccess;
}



MStatus AddShape::getShapeNode( MDagPath& path )
{
    MStatus status;

    if ( path.apiType() == MFn::kMesh )
    {
        return MS::kSuccess;
    }

    unsigned int numShapes;
    status = path.numberOfShapesDirectlyBelow( numShapes );
    CHECK_MSTATUS_AND_RETURN_IT( status );

    for ( unsigned int i = 0; i < numShapes; ++i )
    {
        status = path.extendToShapeDirectlyBelow( i );
        CHECK_MSTATUS_AND_RETURN_IT( status );

        if ( !path.hasFn( MFn::kMesh ) )
        {
            path.pop();
            continue;
        }

        MFnDagNode fnNode( path, &status );
        CHECK_MSTATUS_AND_RETURN_IT( status );
        if ( !fnNode.isIntermediateObject() )
        {
            return MS::kSuccess;
        }
        path.pop();
    }

    return MS::kFailure;
}



MStatus AddShape::getDeformer( MObject& oPsd, MObject& oSkin )
{
    MStatus status;
    MObject oBaseMesh = m_pathBase.node();
    MItDependencyGraph itGraph( oBaseMesh, MFn::kInvalid, MItDependencyGraph::kUpstream,
        MItDependencyGraph::kDepthFirst, MItDependencyGraph::kNodeLevel, &status );
    CHECK_MSTATUS_AND_RETURN_IT( status );

    while ( !itGraph.isDone() )
    {
        MObject oNode = itGraph.currentItem();
        MFnDependencyNode fnNode( oNode, &status );
        CHECK_MSTATUS_AND_RETURN_IT( status );
        if ( fnNode.typeId() == MainNode::id )
        {
            m_oPsd = oNode;
        }
		else if( fnNode.typeName() == "skinCluster" )
		{
			m_oSkin = oNode;
			return MS::kSuccess;
		}
        itGraph.next();
    }
    return MS::kFailure;
}