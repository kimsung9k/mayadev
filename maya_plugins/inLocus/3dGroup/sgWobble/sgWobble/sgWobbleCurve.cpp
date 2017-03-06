
#include "sgWobbleCurve.h"
#include "PerlinNoise.h"

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>

#include <maya/MGlobal.h>
MTypeId     sgWobbleCurve::id( 0x2014073000 );

// Example attributes
// 
MObject    sgWobbleCurve::aAimMatrix;
MObject    sgWobbleCurve::aAimIndex;
MObject    sgWobbleCurve::aInputCurveMatrix;
MObject    sgWobbleCurve::aInputCurve;
MObject    sgWobbleCurve::aWaves;
	MObject    sgWobbleCurve::aRate1;
	MObject    sgWobbleCurve::aRate2;
MObject    sgWobbleCurve::aWaveOptions;
	MObject    sgWobbleCurve::aOffset;
	MObject    sgWobbleCurve::aWaveLength;
	MObject    sgWobbleCurve::aTimeMult;
MObject    sgWobbleCurve::aPinEndRate;
MObject    sgWobbleCurve::aFallOff;
MObject    sgWobbleCurve::aEnvelope;
MObject    sgWobbleCurve::aMatrixMult;
MObject    sgWobbleCurve::aTime;
MObject    sgWobbleCurve::aApplyCurveLength;
MObject    sgWobbleCurve::aOutputCurve;
MObject    sgWobbleCurve::aOutMatrix;

sgWobbleCurve::sgWobbleCurve()
{
	m_numCVs = 0;
	m_degrees = 0;
	m_isCurveDirty = true;
	m_isCurveMatrixDirty = true;
	m_isAimMatrixDirty = true;
	m_isAimIndexDirty = true;
	m_isWaveDirty = true;
	m_isTimeDirty = true;
	m_isFalloffDirty = true;
	m_isEndRateDirty = true;
}
sgWobbleCurve::~sgWobbleCurve() {}

MStatus sgWobbleCurve::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	MTime time = data.inputValue( aTime ).asTime();
	m_envelope = data.inputValue( aEnvelope ).asFloat();
	m_matrixMult = data.inputValue( aMatrixMult ).asBool();
	if( m_isCurveDirty ) clearCurveDirty( data );
	if( m_isAimMatrixDirty ) clearAimMatrix( data );
	if( m_isAimIndexDirty ) clearAimIndex( data );
	if( m_isEndRateDirty ) clearEndRate( data );
	if( m_isWaveDirty || m_isTimeDirty || m_isFalloffDirty )
		clearWaves( data );
	if( m_isAimMatrixDirty || m_isAimIndexDirty || m_isWaveDirty || m_isTimeDirty || m_isFalloffDirty )
		getEachAngleMatrix();
	if( m_matrixMult )
	{
		clearCurveMatrix( data );
		getEachPointMatrix();
		editPointsByMatrixMult();
	}
	else
	{
		editPoints();
	}

	setResult( data );

	data.setClean( plug );

	m_isCurveDirty = false;
	m_isCurveMatrixDirty = false;
	m_isAimMatrixDirty = false;
	m_isAimIndexDirty = false;
	m_isWaveDirty = false;
	m_isTimeDirty = false;
	m_isFalloffDirty = false;
	m_isEndRateDirty = false;

	return MS::kSuccess;
}

void* sgWobbleCurve::creator()
{
	return new sgWobbleCurve();
}

MStatus sgWobbleCurve::initialize()	
{
	MStatus status;
	MFnEnumAttribute      eAttr;
	MFnNumericAttribute   nAttr;
	MFnMatrixAttribute    mAttr;
	MFnTypedAttribute     tAttr;
	MFnUnitAttribute      uAttr;
	MFnCompoundAttribute  cAttr;
	MRampAttribute        rAttr;

	aAimMatrix = mAttr.create( "aimMatrix", "aimMatrix" );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aAimMatrix ) );
	aAimIndex = eAttr.create( "aimIndex", "aimIndex" );
	eAttr.addField( "X", 0 ); eAttr.addField( "Y", 1 ); eAttr.addField( "Z", 2 );
	eAttr.addField( "-X", 3 ); eAttr.addField( "-Y", 4 ); eAttr.addField( "-Z", 5 );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aAimIndex ) );
	aInputCurveMatrix   = mAttr.create( "inputCurveMatrix", "inputCurveMatrix" );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputCurveMatrix ) );
	aInputCurve   = tAttr.create( "inputCurve", "inputCurve", MFnData::kNurbsCurve );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputCurve ) );
	
	aWaves = cAttr.create( "waves", "waves" );
		aRate1 = nAttr.create( "rate1", "rate1", MFnNumericData::kDouble, 0.0 );
		nAttr.setMin( -90 );nAttr.setMax( 90 );
		aRate2 = nAttr.create( "rate2", "rate2", MFnNumericData::kDouble, 0.0 );
		nAttr.setMin( -90 );nAttr.setMax( 90 );
	cAttr.addChild( aRate1 );
	cAttr.addChild( aRate2 );
	cAttr.setArray( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aWaves ) );

	aWaveOptions = cAttr.create( "waveOptions", "waveOptions" );
		aOffset = nAttr.create( "offset", "offset", MFnNumericData::kDouble, 0.0 );
		aWaveLength = nAttr.create( "waveLength", "waveLength", MFnNumericData::kDouble, 1.0 );
		aTimeMult   = nAttr.create( "timeMult", "timeMult", MFnNumericData::kDouble, 1.0 );
	cAttr.addChild( aOffset );
	cAttr.addChild( aWaveLength );
	cAttr.addChild( aTimeMult );
	cAttr.setArray( true );
	cAttr.setUsesArrayDataBuilder( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aWaveOptions ) );

	aApplyCurveLength = nAttr.create( "applyCurveLength", "applyCurveLength", MFnNumericData::kBoolean, true );
	nAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aApplyCurveLength ) );

	aFallOff = rAttr.createCurveRamp( "fallOff", "fallOff" );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aFallOff ) );

	aPinEndRate = nAttr.create( "pinEndRate", "pinEndRate", MFnNumericData::kFloat, 1.0f );
	nAttr.setMin( 0.0f );
	nAttr.setMax( 1.0f );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aPinEndRate ) );
	
	aEnvelope = nAttr.create( "envelope", "envelope", MFnNumericData::kFloat, 1.0 );
	nAttr.setKeyable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aEnvelope ) );

	aMatrixMult = nAttr.create( "matrixMult", "matrixMult", MFnNumericData::kBoolean, false );
	nAttr.setKeyable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aMatrixMult ) );

	aTime = uAttr.create( "time", "time", MFnUnitAttribute::kTime, 0.0 );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aTime ) );

	aOutputCurve = tAttr.create( "outputCurve", "outputCurve", MFnData::kNurbsCurve );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOutputCurve ) );

	aOutMatrix = mAttr.create( "outMatrix", "outMatrix" );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOutMatrix ) );

	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aAimMatrix, aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aAimIndex, aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputCurveMatrix, aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputCurve, aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aWaves, aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aWaveOptions, aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aTime,  aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aFallOff,  aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aEnvelope,  aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aMatrixMult,  aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aPinEndRate,  aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aAimMatrix,  aOutMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aApplyCurveLength, aOutputCurve ) );

	return MS::kSuccess;

}


MStatus sgWobbleCurve::setDependentsDirty( const MPlug& plug, MPlugArray& plugArr )
{
	MStatus status;

	if( plug == aInputCurve )
	{
		m_isCurveDirty = true;
	}
	else if( plug == aInputCurveMatrix )
	{
		m_isCurveMatrixDirty = true;
	}
	else if( plug == aAimMatrix )
	{
		m_isAimMatrixDirty = true;
	}
	else if( plug == aAimIndex )
	{
		m_isAimIndexDirty = true;
	}
	else if( plug == aRate1 || plug == aRate2 || plug == aOffset || plug == aWaveLength )
	{
		m_isWaveDirty = true;
	}
	else if( plug == aTime )
	{
		m_isTimeDirty = true;
	}
	else if( plug == aPinEndRate )
	{
		m_isEndRateDirty = true;
	}
	else 
	{
		m_isFalloffDirty = true;
	}

	return MS::kSuccess;
}