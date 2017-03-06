#include "AddIndex.h"
#include "node.h"

AddIndex::AddIndex()
{
}


AddIndex::~AddIndex()
{
}


bool AddIndex::isUndoable() const
{
	return true;
}


void* AddIndex::creator()
{
	return new AddIndex();
}


MSyntax AddIndex::newSyntax()
{
	MSyntax syntax;

	syntax.setObjectType( MSyntax::kSelectionList, 1, 1 );
	syntax.useSelectionAsDefault( true );

	syntax.enableEdit( false );
	syntax.enableQuery( false );
	
	return syntax;
}


MStatus AddIndex::doIt( const MArgList& args )
{
	MStatus status;

	MArgDatabase	argData( syntax(), args, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MSelectionList	selList;
	status = argData.getObjects( selList );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = selList.getDependNode( 0, m_oDeformer );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	m_plugDeltaInfo = MFnDependencyNode( m_oDeformer ).findPlug( "deltaInfo" );

	int lastIndex = m_plugDeltaInfo.numElements()-1;

	if( lastIndex != -1 )
	{
		m_indexAdd = m_plugDeltaInfo[ lastIndex ].logicalIndex() + 1;
	}
	else
	{
		m_indexAdd = 0;
	}

	return MS::kSuccess;
}


MStatus AddIndex::redoIt()
{
	MStatus status;

	m_plugDeltaInfo.elementByLogicalIndex( m_indexAdd );

	return MS::kSuccess;
}


MStatus AddIndex::undoIt()
{
	MStatus status;

	char buffer[ 512];

	sprintf( buffer, "removeMultiInstance %s[%d]", m_plugDeltaInfo.name().asChar(), m_indexAdd );
	MGlobal::executeCommand( buffer );

	cout << "undo : " << buffer << endl;

	return MS::kSuccess;
}