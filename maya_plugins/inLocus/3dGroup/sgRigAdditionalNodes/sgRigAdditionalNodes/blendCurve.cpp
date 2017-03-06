#include "blendCurve.h"

MTypeId blendCurve::id( 0x2014072800 );

MObject blendCurve::aInputs;
	MObject blendCurve::aInputCurve;
	MObject blendCurve::aWeight;
	MObject blendCurve::aBlendPosition;
	MObject blendCurve::aBlendArea;


blendCurve::blendCurve()
{
	m_isInputGeomDirty = true;
	m_lengthDirty      = true;
}

blendCurve::~blendCurve(){}

void* blendCurve::creator()
{
	return new blendCurve();
}


MStatus blendCurve::deform( MDataBlock& data, MItGeometry& iter, const MMatrix& mat, unsigned int multiIndex )
{
	MStatus status;



	return MS::kSuccess;
}


MStatus blendCurve::initialize()
{
	MStatus status;

	MFnNumericAttribute  nAttr;
	MFnTypedAttribute    tAttr;
	MFnCompoundAttribute cAttr;

	aInputs = cAttr.create( "inputs", "inputs" );

	aInputCurve = tAttr.create( "inputCurve", "inputCurve", MFnData::kNurbsCurve );
	tAttr.setStorable( false );
	aWeight = nAttr.create( "weight", "weight", MFnNumericData::kFloat, 1.0 );
	nAttr.setMin( 0.0 );
	nAttr.setMax( 1.0 );
	nAttr.setKeyable( true );
	aBlendPosition = nAttr.create( "blendPosition", "blendPosition", MFnNumericData::kFloat, 1.0 );
	nAttr.setMin( 0.0 );
	nAttr.setMax( 1.0 );
	nAttr.setKeyable( true );
	aBlendArea     = nAttr.create( "blendArea", "blendArea", MFnNumericData::kFloat, 0.5 );
	nAttr.setMin( 0.0 );
	nAttr.setMax( 1.0 );
	nAttr.setKeyable( true );
	cAttr.addChild( aInputCurve );
	cAttr.addChild( aWeight );
	cAttr.addChild( aBlendPosition );
	cAttr.addChild( aBlendArea );
	cAttr.setArray( true );

	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputs ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputs, outputGeom ) );

	return MS::kSuccess;
}


MStatus blendCurve::setDependentsDirty( const MPlug& plug, MPlugArray& plugArr )
{
	MStatus status;
	if( plug == inputGeom )
	{
		m_isInputGeomDirty = true;
	}
	else if( plug == aInputCurve )
	{
		unsigned int logicalIndex = plug.parent().logicalIndex();
		if( !m_inputInfoArray.length < logicalIndex +1 )
		{
			m_inputInfoArray.setLength( logicalIndex+1 );
			m_lengthDirty = true;
		}
		m_inputInfoArray[ logicalIndex ].isCurveDirty = true;
	}
	else if( plug == aWeight )
	{
		unsigned int logicalIndex = plug.parent().logicalIndex();
		if( !m_inputInfoArray.length < logicalIndex +1 )
		{
			m_inputInfoArray.setLength( logicalIndex+1 );
			m_lengthDirty = true;
		}
		m_inputInfoArray[ logicalIndex ].isValuesDirty = true;
	}
	else if( plug == aBlendPosition )
	{
		unsigned int logicalIndex = plug.parent().logicalIndex();
		if( !m_inputInfoArray.length < logicalIndex +1 )
		{
			m_inputInfoArray.setLength( logicalIndex+1 );
			m_lengthDirty = true;
		}
		m_inputInfoArray[ logicalIndex ].isValuesDirty = true;
	}
	else if( plug == aBlendArea )
	{
		unsigned int logicalIndex = plug.parent().logicalIndex();
		if( !m_inputInfoArray.length < logicalIndex +1 )
		{
			m_inputInfoArray.setLength( logicalIndex+1 );
			m_lengthDirty = true;
		}
		m_inputInfoArray[ logicalIndex ].isValuesDirty = true;
	}
	return status;
}