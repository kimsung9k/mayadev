#include "sgWobbleCurve2.h"
#include "PerlinNoise.h"

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>

#include <maya/MGlobal.h>
MTypeId     sgWobbleCurve2::id( 0x2014083100 );


MObject    sgWobbleCurve2::aAimMatrix;
MObject    sgWobbleCurve2::aAimIndex;
MObject    sgWobbleCurve2::aInputCurveMatrix;
MObject    sgWobbleCurve2::aInputCurve;
MObject    sgWobbleCurve2::aWave1;
MObject    sgWobbleCurve2::aWave2;
MObject    sgWobbleCurve2::aOffset1;
MObject    sgWobbleCurve2::aWaveLength1;
MObject    sgWobbleCurve2::aTimeMult1;
MObject    sgWobbleCurve2::aOffset2;
MObject    sgWobbleCurve2::aWaveLength2;
MObject    sgWobbleCurve2::aTimeMult2;
MObject    sgWobbleCurve2::aPinEndRate;
MObject    sgWobbleCurve2::aFallOff1;
MObject    sgWobbleCurve2::aFallOff2;
MObject    sgWobbleCurve2::aEnvelope;
MObject    sgWobbleCurve2::aMatrixMult;
MObject    sgWobbleCurve2::aNoRelative;
MObject    sgWobbleCurve2::aTime;
MObject    sgWobbleCurve2::aOutputCurve;


sgWobbleCurve2::sgWobbleCurve2()
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
sgWobbleCurve2::~sgWobbleCurve2() {}


MStatus sgWobbleCurve2::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	MTime time = data.inputValue( aTime ).asTime();
	m_envelope = data.inputValue( aEnvelope ).asFloat();
	m_matrixMult = data.inputValue( aMatrixMult ).asBool();
	m_isNoRelative = data.inputValue( aNoRelative ).asBool();

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

void* sgWobbleCurve2::creator()
{
	return new sgWobbleCurve2();
}

MStatus sgWobbleCurve2::initialize()	
{
	setNoiseBase();

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
	
	aEnvelope = nAttr.create( "envelope", "envelope", MFnNumericData::kFloat, 1.0 );
	nAttr.setKeyable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aEnvelope ) );

	aWave1 = nAttr.create( "wave1", "wave1", MFnNumericData::kFloat, 30.0 );
	cAttr.addChild( aWave1 );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aWave1 ) );

	aOffset1 = nAttr.create( "offset1", "offset1", MFnNumericData::kFloat, 0.0 );
	aWaveLength1 = nAttr.create( "waveLength1", "waveLength1", MFnNumericData::kFloat, 0.25 );
	aTimeMult1   = nAttr.create( "timeMult1", "timeMult1", MFnNumericData::kFloat, 1.0 );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOffset1 ) );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aWaveLength1 ) );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aTimeMult1 ) );
	aFallOff1 = rAttr.createCurveRamp( "fallOff1", "fallOff1" );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aFallOff1 ) );

	aWave2 = nAttr.create( "wave2", "wave2", MFnNumericData::kFloat, 0.0 );
	cAttr.addChild( aWave1 );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aWave2 ) );

	aOffset2 = nAttr.create( "offset2", "offset2", MFnNumericData::kFloat, 0.0 );
	aWaveLength2 = nAttr.create( "waveLength2", "waveLength2", MFnNumericData::kFloat, 1.0 );
	aTimeMult2   = nAttr.create( "timeMult2", "timeMult2", MFnNumericData::kFloat, 1.0 );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOffset2 ) );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aWaveLength2 ) );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aTimeMult2 ) );
	aFallOff2 = rAttr.createCurveRamp( "fallOff2", "fallOff2" );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aFallOff2 ) );

	aPinEndRate = nAttr.create( "pinEndRate", "pinEndRate", MFnNumericData::kFloat, 0.0f );
	nAttr.setMin( 0.0f );
	nAttr.setMax( 1.0f );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aPinEndRate ) );

	aMatrixMult = nAttr.create( "matrixMult", "matrixMult", MFnNumericData::kBoolean, false );
	nAttr.setKeyable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aMatrixMult ) );

	aNoRelative = nAttr.create( "noRelative", "noRelative", MFnNumericData::kBoolean, false );
	nAttr.setKeyable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aNoRelative ) );

	aTime = uAttr.create( "time", "time", MFnUnitAttribute::kTime, 0.0 );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aTime ) );

	aOutputCurve = tAttr.create( "outputCurve", "outputCurve", MFnData::kNurbsCurve );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOutputCurve ) );

	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aNoRelative, aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aAimMatrix, aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aAimIndex, aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputCurveMatrix, aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputCurve, aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aWave1, aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aWave2, aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aOffset1,  aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aWaveLength1,  aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aTimeMult1,  aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aOffset2,  aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aWaveLength2,  aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aTimeMult2,  aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aTime,  aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aFallOff1,  aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aFallOff2,  aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aEnvelope,  aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aMatrixMult,  aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aMatrixMult,  aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aPinEndRate,  aOutputCurve ) );

	return MS::kSuccess;

}


MStatus sgWobbleCurve2::setDependentsDirty( const MPlug& plug, MPlugArray& plugArr )
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
	else if( plug == aWave1 || plug == aWave2 || plug == aOffset1 || plug == aWaveLength1
		|| plug == aOffset2 || plug == aWaveLength2 )
	{
		m_isWaveDirty = true;
	}
	else if( plug == aTime || plug == aTimeMult1 || plug == aTimeMult2 )
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