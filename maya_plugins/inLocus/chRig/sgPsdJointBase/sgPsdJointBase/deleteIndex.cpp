#include "deleteIndex.h"

DeleteIndex::DeleteIndex()
{
}


DeleteIndex::~DeleteIndex()
{
}


bool DeleteIndex::isUndoable() const
{
	return true;
}


void* DeleteIndex::creator()
{
	return new DeleteIndex();
}


MSyntax DeleteIndex::newSyntax()
{
	MSyntax syntax;

	syntax.setObjectType( MSyntax::kSelectionList, 1, 1 );
	syntax.useSelectionAsDefault( false );
	syntax.addFlag( "-i", "-index", MSyntax::kLong );

	syntax.enableEdit( false );
	syntax.enableQuery( false );
	
	return syntax;
}


MStatus DeleteIndex::doIt( const MArgList& args )
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
	if( fnNode.typeName() !="psdJointBase" )
	{
		return MS::kFailure;
	}

	m_plugTarget = fnNode.findPlug( "deltaInfo" );

	for( int i=0; i< m_plugTarget.numElements(); i++ )
	{
		MPlug plugDeltaInfo = m_plugTarget[i];

		if( plugDeltaInfo.logicalIndex() == index )
		{
			MPlug plugName = plugDeltaInfo.child( 0 );
			MPlug plugDelta = plugDeltaInfo.child( 2 );
			MPlug plugWeight = plugDeltaInfo.child( 3 );

			m_shapeName = plugName.asString();
			m_weight = plugWeight.asFloat();

			for( int j=0; j< plugDelta.numElements(); j++ )
			{
				MPlug plugDeltaX = plugDelta[j].child( 0 );
				MPlug plugDeltaY = plugDelta[j].child( 1 );
				MPlug plugDeltaZ = plugDelta[j].child( 2 );

				m_deltas.append( MPoint( plugDeltaX.asDouble(), plugDeltaY.asDouble(), plugDeltaZ.asDouble() ) );
				m_logicalIndices.append( plugDelta[j].logicalIndex() );
			}

			m_namePlug = plugDeltaInfo.name();
			m_indexTarget = plugDeltaInfo.logicalIndex();

			return redoIt();
		}
	}
	return MS::kFailure;
}


MStatus DeleteIndex::redoIt()
{
	MStatus status;

	char buffer[512];
	sprintf( buffer, "removeMultiInstance %s;", m_namePlug.asChar() );
	MGlobal::executeCommand( buffer );

	return MS::kSuccess;
}


MStatus DeleteIndex::undoIt()
{
	MStatus status;

	MPlug plugDeltaInfo = m_plugTarget.elementByLogicalIndex( m_indexTarget );
	MPlug plugName  = plugDeltaInfo.child( 0 );
	MPlug plugDelta = plugDeltaInfo.child( 2 );
	MPlug plugWeight = plugDeltaInfo.child( 3 );

	plugName.setString( m_shapeName );
	plugWeight.setFloat( m_weight );

	for( int i=0; i< m_logicalIndices.length(); i++ )
	{
		int logicalIndex = m_logicalIndices[i];
		MPoint& point = m_deltas[i];

		MPlug plugDeltaEl = plugDelta.elementByLogicalIndex( logicalIndex );
		MPlug plugDeltaX = plugDeltaEl.child( 0 );
		MPlug plugDeltaY = plugDeltaEl.child( 1 );
		MPlug plugDeltaZ = plugDeltaEl.child( 2 );

		plugDeltaX.setDouble( point.x );
		plugDeltaY.setDouble( point.y );
		plugDeltaZ.setDouble( point.z );
	}

	return MS::kSuccess;
}