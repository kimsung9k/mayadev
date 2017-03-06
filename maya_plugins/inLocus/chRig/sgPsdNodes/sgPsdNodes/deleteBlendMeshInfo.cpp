#include  "deleteBlendMeshInfo.h"

deleteBlendMeshInfo::deleteBlendMeshInfo()
{
}

deleteBlendMeshInfo::~deleteBlendMeshInfo()
{
}

bool	deleteBlendMeshInfo::isUndoable() const
{
	return true;
}


void*	deleteBlendMeshInfo::creator()
{
	return new deleteBlendMeshInfo();
}

MSyntax	deleteBlendMeshInfo::newSyntax()
{
	MSyntax	syntax;

	syntax.setObjectType( MSyntax::kSelectionList, 1, 1 );
	syntax.useSelectionAsDefault( false );
	syntax.addFlag( "-i", "-index", MSyntax::kLong );

	syntax.enableEdit( false );
	syntax.enableQuery( false );

	return syntax;
}

MStatus	deleteBlendMeshInfo::doIt( const MArgList& args )
{
	MStatus status;

	MArgDatabase	argData( syntax(), args, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MSelectionList	selList;
	status = argData.getObjects( selList );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	int index;
	status = argData.getFlagArgument( "-i", 0, index );

	status = selList.getDependNode( 0, m_oNode );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MFnDependencyNode fnNode = m_oNode;
	if( fnNode.typeName() !="blendAndFixedShape" )
	{
		return MS::kFailure;
	}
	
	MPlug plugBlendMeshInfo = fnNode.findPlug( "blendMeshInfos" );

	bool exists = false;
	for( int i=0; i< plugBlendMeshInfo.numElements(); ++i )
	{
		if( index == plugBlendMeshInfo[i].logicalIndex() )
		{
			exists = true;
			m_indexTarget = index;
			break;
		}
	}
	m_indexLast = plugBlendMeshInfo.numElements() -1;

	if( !exists )
		return MS::kInvalidParameter;

	return redoIt();
}


MStatus	deleteBlendMeshInfo::redoIt()
{
	MStatus status;

	getIndexInfo( m_infoTarget, m_oNode, m_indexTarget );
	getIndexInfo( m_infoLast,   m_oNode, m_indexLast );

	MFnDependencyNode fnNode = m_oNode;
	MPlug lastPlugElement = fnNode.findPlug( "blendMeshInfos" )[ m_indexLast ];
	MPlug targetPlugElement = fnNode.findPlug( "blendMeshInfos" )[ m_indexTarget ];

	char buffer[512];

	sprintf( buffer, "removeMultiInstance %s -b true;", targetPlugElement.name().asChar() );
	MGlobal::executeCommand( buffer );
	m_deleteModifier.deleteNode( m_infoTarget.oAnimCurve );
	m_deleteModifier.doIt();

	if( m_indexTarget != m_indexLast )
	{
		sprintf( buffer, "removeMultiInstance %s -b true;", lastPlugElement.name().asChar() );
		status = MGlobal::executeCommand( buffer );
		setIndexInfo( m_infoLast,  m_oNode,  m_indexTarget );
	}

	return MS::kSuccess;
}


MStatus deleteBlendMeshInfo::undoIt()
{
	MStatus status;

	MFnDependencyNode fnNode = m_oNode;

	status = m_deleteModifier.undoIt();
	setIndexInfo( m_infoLast,   m_oNode, m_indexLast );

	if( m_indexTarget != m_indexLast )
	{
		MPlug plugElement = fnNode.findPlug( "blendMeshInfos" )[ m_indexTarget ];
		char buffer[512];
		sprintf( buffer, "removeMultiInstance %s -b true;", plugElement.name().asChar() );
		MGlobal::executeCommand( buffer );
		setIndexInfo( m_infoTarget, m_oNode, m_indexTarget );
	}
	
	return MS::kSuccess;
}


MStatus	deleteBlendMeshInfo::getIndexInfo( blendMeshInfo& info, MObject oNode, int index )
{
	MStatus status;

	MFnDependencyNode fnNode = oNode;

	MPlug plugElement = fnNode.findPlug( "blendMeshInfos" )[ index ];

	MPlug plugInputMesh = plugElement.child( 0 );
	MPlugArray plugArrCons;

	plugInputMesh.connectedTo( plugArrCons, true, false );

	if( plugArrCons.length() )
	{
		info.existInputMesh = true;
		info.nameConnectedNode = MFnDependencyNode( plugArrCons[0].node() ).name();
		info.nameConnectedAttr = MFnAttribute( plugArrCons[0].attribute() ).name();
	}
	else
	{
		info.existInputMesh = false;
		MPlug plugDelta = plugElement.child( 1 );
		int numElementsDelta = plugDelta.numElements();

		info.indicesDelta.setLength( numElementsDelta );
		info.pointsDelta.setLength( numElementsDelta );

		for( int i=0; i<numElementsDelta;  ++i )
		{
			double deltaValueX = plugDelta[i].child(0).asDouble();
			double deltaValueY = plugDelta[i].child(1).asDouble();
			double deltaValueZ = plugDelta[i].child(2).asDouble();

			MPoint ptDelta( deltaValueX, deltaValueY, deltaValueZ );

			info.indicesDelta[i] = plugDelta[i].logicalIndex();
			info.pointsDelta[i] = ptDelta;
		}
	}

	MPlug plugTargetWeight = plugElement.child( 2 );
	int numElementsTargetWeight = plugTargetWeight.numElements();

	info.indicesTargetWeight.setLength( numElementsTargetWeight );
	info.floatArrTargetWeight.setLength( numElementsTargetWeight );

	for( int i=0; i<numElementsTargetWeight; i++ )
	{
		info.indicesTargetWeight[i] = plugTargetWeight[i].logicalIndex();
		info.floatArrTargetWeight[i] = plugTargetWeight[i].asFloat();
	}

	MPlug plugMeshName = plugElement.child( 3 );
	info.nameMesh = plugMeshName.asString();
	
	MPlug plugMatrices = plugElement.child( 4 );
	int numElementsMatrices = plugMatrices.numElements();

	info.indicesMatrix.setLength( numElementsMatrices );
	info.oArrMatrix.setLength( numElementsMatrices );

	for( int i=0; i<numElementsMatrices; i++ )
	{
		info.indicesMatrix[i] = plugMatrices[i].logicalIndex();
		info.oArrMatrix[i] = plugMatrices[i].asMObject();
	}

	MPlug plugAnimCurve = plugElement.child( 5 );
	MPlugArray cons;
	plugAnimCurve.connectedTo( cons, true, false );

	if( cons.length() )
	{
		info.oAnimCurve = cons[0].node();
	}

	return MS::kSuccess;
}


MStatus deleteBlendMeshInfo::setIndexInfo( blendMeshInfo& info, MObject oNode, int index )
{
	MStatus status;

	MDGModifier mdgModifier;

	MFnDependencyNode fnNode = oNode;

	MPlug plugElement = fnNode.findPlug( "blendMeshInfos" ).elementByLogicalIndex( index );
	
	if( info.existInputMesh )
	{
		MPlug plugInputMesh = plugElement.child( 0 );

		MSelectionList selList;
		selList.add( info.nameConnectedNode );

		MObject oNode;
		selList.getDependNode( 0, oNode );

		MFnDependencyNode fnNode( oNode );
		MPlug plugOutput = fnNode.findPlug( info.nameConnectedAttr );

		mdgModifier.connect( plugOutput, plugInputMesh );
		mdgModifier.doIt();
	}
	else
	{
		MPlug plugDelta = plugElement.child( 1 );

		int numElements = info.indicesDelta.length();

		for( int i=0; i < numElements; i++ )
		{
			MPlug plugLogicalElement = plugDelta.elementByLogicalIndex( info.indicesDelta[i] );
			MPlug plugDeltaX = plugLogicalElement.child( 0 );
			MPlug plugDeltaY = plugLogicalElement.child( 1 );
			MPlug plugDeltaZ = plugLogicalElement.child( 2 );

			plugDeltaX.setDouble( info.pointsDelta[i].x );
			plugDeltaY.setDouble( info.pointsDelta[i].y );
			plugDeltaZ.setDouble( info.pointsDelta[i].z );
		}
	}

	MPlug plugTargetWeight = plugElement.child( 2 );

	int numElements = info.indicesTargetWeight.length();

	for( int i=0; i< numElements; i++ )
	{
		MPlug plugLogicalElement = plugTargetWeight.elementByLogicalIndex( info.indicesTargetWeight[i] );
		plugLogicalElement.setFloat( info.floatArrTargetWeight[i] );
	}

	MPlug plugMeshName = plugElement.child( 3 );
	plugMeshName.setString( info.nameMesh );
	
	MPlug plugMatrices = plugElement.child( 4 );
	int numElementsMatrices = info.indicesMatrix.length();

	for( int i=0; i<numElementsMatrices; i++ )
	{
		MPlug plugLogicalElement = plugMatrices.elementByLogicalIndex( info.indicesMatrix[i] );
		plugLogicalElement.setMObject( info.oArrMatrix[i] );
	}

	MPlug plugAnimMessage = plugElement.child( 5 );
	MPlug plugAnimOutput = plugElement.child( 6 );

	if( !info.oAnimCurve.isNull() )
	{
		MFnDependencyNode fnAnimCurve = info.oAnimCurve;
		MPlug plugMessage = fnAnimCurve.findPlug( "message" );
		MPlug plugOutput  = fnAnimCurve.findPlug( "output" );

		m_mdgModifier.connect( plugMessage, plugAnimMessage );
		m_mdgModifier.connect( plugOutput, plugAnimOutput );

		m_mdgModifier.doIt();
	}

	return MS::kSuccess;
}