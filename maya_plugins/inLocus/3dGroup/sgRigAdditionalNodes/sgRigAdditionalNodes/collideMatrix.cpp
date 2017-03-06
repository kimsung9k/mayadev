#include "collideMatrix.h"

MTypeId     collideMatrix::id( 0x2014052800 );

MObject     collideMatrix::aEnvelop;
MObject		collideMatrix::aCollideList;
MObject		collideMatrix::aCollideMatrix;
MObject		collideMatrix::aCollideRate;
MObject		collideMatrix::aCollideBaseMatrix;

MObject     collideMatrix::aOutMatrix;


collideMatrix::collideMatrix(){}

collideMatrix::~collideMatrix(){}


void* collideMatrix::creator()
{
	return new collideMatrix();
}



MStatus collideMatrix::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	MArrayDataHandle hArrCollideList = data.inputArrayValue( aCollideList );

	MMatrixArray mtxArrCollide;
	MFloatArray  valuesCollide;

	for( int i=0; i< hArrCollideList.elementCount(); i++, hArrCollideList.next() )
	{
		MDataHandle hCollideList = hArrCollideList.inputValue();
		MDataHandle hCollideMatrix = hCollideList.child( aCollideMatrix );
		MDataHandle hCollideRate   = hCollideList.child( aCollideRate );

		mtxArrCollide.append( hCollideMatrix.asMatrix() );
		valuesCollide.append( hCollideRate.asFloat() );
	}

	getResult( mtxArrCollide, valuesCollide );

	return MS::kSuccess;
}



MStatus collideMatrix::initialize()
{
	MStatus status;

	MFnCompoundAttribute cAttr;
	MFnNumericAttribute  nAttr;
	MFnMatrixAttribute   mAttr;

	aOutMatrix = mAttr.create( "outMatrix", "outMatrix" );
	mAttr.setStorable( false );
	mAttr.setArray( true );
	mAttr.setUsesArrayDataBuilder( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOutMatrix ) );

	aEnvelop = nAttr.create( "envelop", "envelop", MFnNumericData::kFloat, 1.0 );
	nAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aEnvelop ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aEnvelop, aOutMatrix ) );

	aCollideMatrix = mAttr.create( "collideMatrix", "collideMatrix" );
	aCollideRate    = nAttr.create( "collideRate", "collideRate", MFnNumericData::kFloat, 1.0 );
	aCollideList   = cAttr.create( "collideList", "colliderList" );
	cAttr.addChild( aCollideMatrix );
	cAttr.addChild( aCollideRate );
	cAttr.setStorable( true );
	cAttr.setArray( true );
	cAttr.setUsesArrayDataBuilder( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aCollideList ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aCollideList, aOutMatrix ) );

	aCollideBaseMatrix = mAttr.create( "collideBaseMatrix", "collideBaseMatrix" );
	mAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aCollideBaseMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aCollideBaseMatrix, aOutMatrix ) );

	return MS::kSuccess;
}