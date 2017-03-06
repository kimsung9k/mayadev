#include "blendCurve.h"


MStatus blendCurve::setCleanInputGeom( MItGeometry& iter )
{
	if( !m_isInputGeomDirty ) return MS::kSuccess;
	iter.allPositions( m_pointArr );
	m_isInputGeomDirty = false;
}



MStatus blendCurve::getInputsValues( MDataBlock& data )
{
	MArrayDataHandle hArrInputs = data.inputArrayValue( aInputs );

	for( int i=0; i<m_inputInfoArray.length; i++, hArrInputs.next() )
	{
		MDataHandle hInput = hArrInputs.inputValue();
		MFnNurbsCurve fnCurve = hInput.child( aInputCurve ).asNurbsCurve();
		inputInfo& eInputInfo = m_inputInfoArray[i];
		if( eInputInfo.isCurveDirty )
		{
			fnCurve.getCVs( eInputInfo.points );
		}
		if( eInputInfo.isValuesDirty )
		{
			eInputInfo.weight = hInput.child( aWeight ).asFloat();
			eInputInfo.blendPosition = hInput.child( aBlendPosition ).asFloat();
			eInputInfo.blendArea = hInput.child( aBlendArea ).asFloat();
		}
	}

	return MS::kSuccess;
}


MStatus blendCurve::setClean( MItGeometry& iter )
{


	return MS::kSuccess;
}