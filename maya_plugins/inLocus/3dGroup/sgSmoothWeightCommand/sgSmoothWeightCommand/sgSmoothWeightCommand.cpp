#include "sgSmoothWeightCommand.h"

#include <maya/MGlobal.h>
#include "SGPrintf.h"


MSyntax sgSmoothWeightCommand::newSyntax()
{
	MSyntax syntax;

	syntax.addFlag( "-i", "-index", MSyntax::kLong );
	syntax.addFlag( "-w", "-weight", MSyntax::kDouble );
	syntax.addFlag( "-h", "-isHardWeight", MSyntax::kBoolean );
	syntax.setObjectType( MSyntax::kSelectionList, 1 );
	syntax.useSelectionAsDefault( true );

	syntax.enableEdit( false );
	syntax.enableQuery( false );

	return syntax;
}


MStatus sgSmoothWeightCommand::doIt( const MArgList& argList )
{
	MStatus status;

	MArgDatabase argData( syntax(), argList, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	m_isHardWeight = false;

	status = argData.getFlagArgument( "-i", 0, m_index );
	if( !status ) return getInfomaiton( argData );
	status = argData.getFlagArgument( "-w", 0, m_weight );
	if( !status ) return getInfomaiton( argData );
	status = argData.getFlagArgument( "-h", 0, m_isHardWeight );

	if( !m_pathMesh.isValid() ) return MS::kFailure;

	status = getWeightValueAndIndices( m_plugWeightList.elementByLogicalIndex( m_index ), m_indicesBefore, m_valuesBefore );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	if( m_isHardWeight )
	{
		getHardWeight( m_plugWeightList, m_index, m_indicesBefore, m_valuesBefore, m_indicesAfter, m_valuesAfter );
	}
	else
	{
		getSmoothWeight( m_plugWeightList, m_index, m_indicesAfter, m_valuesAfter );
	}
	
	editAfterValueByWeight( m_indicesBefore, m_valuesBefore, m_indicesAfter, m_valuesAfter, m_weight );

	return redoIt();
}


MStatus sgSmoothWeightCommand::redoIt()
{
	MStatus status;
	setWeightValue( m_plugWeightList.elementByLogicalIndex( m_index ),
		m_indicesAfter, m_valuesAfter );

	return MS::kSuccess;
}


MStatus sgSmoothWeightCommand::undoIt()
{
	MStatus status;
	
	setWeightValue( m_plugWeightList.elementByLogicalIndex( m_index ),
		m_indicesBefore, m_valuesBefore );
	removeMultiInstance( m_indicesBefore, m_indicesAfter );
	return MS::kSuccess;
}


sgSmoothWeightCommand::sgSmoothWeightCommand(){}


sgSmoothWeightCommand::~sgSmoothWeightCommand(){}


void* sgSmoothWeightCommand::creator()
{
	return new sgSmoothWeightCommand();
}


bool sgSmoothWeightCommand::isUndoable() const
{
	return true;
}