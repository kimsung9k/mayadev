#include "angleDriver.h"

#define PI 3.14159265359

MTypeId    angleDriver::id( 0xc8d604 );

MObject    angleDriver::aBaseMatrix;
MObject    angleDriver::aUpVectorMatrix;
MObject    angleDriver::aAngleMatrix;
MObject    angleDriver::aAxis;

MObject    angleDriver::aOutDriver;
MObject    angleDriver::aOutMatrix;


angleDriver::angleDriver()
{
	baseMatrixRequire = true;
	aimAxisRequire = true;
}

angleDriver::~angleDriver()
{
}

void angleDriver::getAngleMatrix( MMatrix& angleMatrix, int aimIndex )
{
	bool minusAim = false;
	bool minusFirst = false;
	bool minusSecond = false;

	int upIndex = ( aimIndex+1 ) % 3;

	int byIndex = 3-aimIndex-upIndex;

	MVector upTargetVector( upVectorMatrix( upIndex, 0 ), upVectorMatrix( upIndex, 1 ), upVectorMatrix( upIndex, 2 ) );

	MVector aimVector( angleMatrix( aimIndex, 0 ), angleMatrix( aimIndex, 1 ), angleMatrix( aimIndex, 2 ) );
	aimVector.normalize();

	if( aimVector[ upIndex ] < 0 )
		minusFirst = true;
	if( aimVector[ byIndex ] < 0 )
		minusSecond = true;

	MVector upVector( 0.0, 0.0, 0.0 );
	MVector byNormal( 0.0, 0.0, 0.0 );

	upVector[ aimIndex ] = -aimVector[ upIndex ];
	upVector[ upIndex ]  =  aimVector[ aimIndex ];
	byNormal[ aimIndex ] = -aimVector[ byIndex ];
	byNormal[ byIndex ]  =  aimVector[ aimIndex ];

	if( minusAim )
	{
		aimVector *= -1;
		upVector *= -1;
	}

	MVector crossUpVector = byNormal^aimVector;
	MVector crossByNormal = aimVector^upVector;

	double upValue = fabs( aimVector[ upIndex ] );
	double byValue = fabs( aimVector[ byIndex ] );

	MVector baseMVector( 0,0,0 );
	baseMVector[ aimIndex ] = 1.0;

	firstValue = 1.0 - baseMVector*aimVector;
	secondValue = firstValue;

	if( upValue == 0 && byValue == 0 )
	{
		upValue = 1.0;
		byValue = 0.0;
	}
	else
	{
		double allValue = upValue + byValue;
		upValue /= allValue;
		byValue /= allValue;
	}

	firstValue *= upValue;
	secondValue *= byValue;

	if( minusFirst )
		firstValue *= -1;
	if( minusSecond )
		secondValue *= -1;
	
	upVector = upVector*upValue + crossUpVector*byValue;
	byNormal = aimVector^upVector;
	upVector = byNormal^aimVector;

	upVector.normalize();
	byNormal.normalize();
	upTargetVector.normalize();

	thirdValue = upTargetVector.angle( upVector ) / PI * 2;

	if( upTargetVector * byNormal < 0 )
		thirdValue *= -1;

	//cout << "thirdValue : " << thirdValue << endl;

	buildMatrix( aimIndex, 0 ) = aimVector.x;
	buildMatrix( aimIndex, 1 ) = aimVector.y;
	buildMatrix( aimIndex, 2 ) = aimVector.z;
	buildMatrix( upIndex , 0 ) = upVector.x;
	buildMatrix( upIndex , 1 ) = upVector.y;
	buildMatrix( upIndex , 2 ) = upVector.z;
	buildMatrix( byIndex , 0 ) = byNormal.x;
	buildMatrix( byIndex , 1 ) = byNormal.y;
	buildMatrix( byIndex , 2 ) = byNormal.z;
}


MStatus  angleDriver::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;
	
	if( baseMatrixRequire )
	{
		MDataHandle hBaseMatrix = data.inputValue( aBaseMatrix );
		baseMatrix    = hBaseMatrix.asMatrix();
		baseInvMatrix = baseMatrix.inverse();
		baseMatrixRequire = false;
	}
	if( aimAxisRequire )
	{
		MDataHandle hAimAxis = data.inputValue( aAxis );
		aimAxisNum = hAimAxis.asInt();
		aimAxisRequire = false;
	}
	MDataHandle hUpVectorMatrix = data.inputValue( aUpVectorMatrix );
	MDataHandle hAngleMatrix = data.inputValue( aAngleMatrix );

	upVectorMatrix = hUpVectorMatrix.asMatrix()*baseInvMatrix;
	getAngleMatrix( hAngleMatrix.asMatrix() * baseInvMatrix, aimAxisNum );
	buildMatrix *= baseMatrix;

	MDataHandle hOutMatrix = data.outputValue( aOutMatrix );
	hOutMatrix.set( buildMatrix );

	MDataHandle hOutDriver = data.outputValue( aOutDriver );
	hOutDriver.set( MVector( firstValue, secondValue, thirdValue ) );

	data.setClean( plug );

	return MS::kSuccess;
}

void* angleDriver::creator()
{
	return new angleDriver();
}


MStatus angleDriver::initialize()
{
	MStatus  status;

	MFnMatrixAttribute  mAttr;
	MFnNumericAttribute nAttr;
	MFnEnumAttribute    eAttr;

	aOutDriver = nAttr.create( "outDriver", "outDriver", MFnNumericData::k3Double, 0.0 );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOutDriver ) );

	aOutMatrix = mAttr.create( "outMatrix", "outMatrix" );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOutMatrix ) );

	aBaseMatrix = mAttr.create( "baseMatrix", "baseMatrix" );
	mAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aBaseMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aBaseMatrix, aOutDriver ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aBaseMatrix, aOutMatrix ) );


	aUpVectorMatrix = mAttr.create( "upVectorMatrix", "upVectorMatrix" );
	mAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aUpVectorMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aUpVectorMatrix, aOutDriver ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aUpVectorMatrix, aOutMatrix ) );


	aAngleMatrix = mAttr.create( "angleMatrix", "angleMatrix" );
	mAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aAngleMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aAngleMatrix, aOutDriver ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aAngleMatrix, aOutMatrix ) );

	aAxis = eAttr.create( "axis", "axis" );
	eAttr.addField( "+ X", 0 );
	eAttr.addField( "+ Y", 1 );
	eAttr.addField( "+ Z", 2 );
	eAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aAxis ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aAxis, aOutDriver ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aAxis, aOutMatrix ) );

	return MS::kSuccess;
}

MStatus  angleDriver::setDependentsDirty( const MPlug& plug, MPlugArray& plugArray )
{
	if( plug.attribute() == aBaseMatrix )
		baseMatrixRequire = true;
	else if( plug.attribute() == aAxis )
		aimAxisRequire = true;

	return MS::kSuccess;
}