#include "sgLockAngleMatrix.h"

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>

#include <maya/MGlobal.h>

#define  PI  3.14159265359


MTypeId     sgLockAngleMatrix::id( 0x2014091900 );

MObject     sgLockAngleMatrix::aBaseMatrix;        
MObject     sgLockAngleMatrix::aInputMatrix;     
MObject     sgLockAngleMatrix::aInputAngle;
MObject     sgLockAngleMatrix::aAngleAxis;
MObject     sgLockAngleMatrix::aOutputMatrix;     

sgLockAngleMatrix::sgLockAngleMatrix() {}
sgLockAngleMatrix::~sgLockAngleMatrix() {}

MStatus sgLockAngleMatrix::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	MDataHandle hBaseMatrix = data.inputValue( aBaseMatrix );
	m_baseMatrix = hBaseMatrix.asMatrix();

	MDataHandle hInputMatrix = data.inputValue( aInputMatrix );
	m_inputMatrix = hInputMatrix.asMatrix();

	MDataHandle hAngleAxis = data.inputValue( aAngleAxis );
	m_angleAxis = hAngleAxis.asUChar();

	MDataHandle hInputAngle = data.inputValue( aInputAngle );
	m_inputAngle = hInputAngle.asDouble();

	m_mtxResult = getsgLockAngleMatrix( m_inputMatrix*m_baseMatrix.inverse(), m_angleAxis, m_inputAngle );

	MDataHandle hOutputMatrix = data.outputValue( aOutputMatrix );
	hOutputMatrix.set( m_mtxResult * m_baseMatrix );

	data.setClean( plug );

	return MS::kSuccess;
}

void* sgLockAngleMatrix::creator()
{
	return new sgLockAngleMatrix();
}

MStatus sgLockAngleMatrix::initialize()	
{
	MStatus status;

	MFnMatrixAttribute mAttr;
	MFnNumericAttribute nAttr;
	MFnEnumAttribute   eAttr;

	aBaseMatrix = mAttr.create( "baseMatrix", "baseMatrix" );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aBaseMatrix ) );

	aInputMatrix = mAttr.create( "inputMatrix", "inputMatrix" );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputMatrix ) );

	aAngleAxis = eAttr.create( "angleAxis", "angleAxis" );
	eAttr.addField( " X", 0 );eAttr.addField( " Y", 1 );eAttr.addField( " Z", 2 );
	eAttr.addField( "-X", 3 );eAttr.addField( "-Y", 4 );eAttr.addField( "-Z", 5 );
	eAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aAngleAxis ) );

	aInputAngle = nAttr.create( "inputAngle", "inputAngle", MFnNumericData::kDouble, 45 );
	nAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputAngle ) );

	aOutputMatrix = mAttr.create( "outputMatrix", "outputMatrix" );
	mAttr.setStorable( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOutputMatrix ) );

	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aBaseMatrix, aOutputMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputMatrix, aOutputMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aAngleAxis, aOutputMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputAngle, aOutputMatrix ) );

	return MS::kSuccess;
}


MStatus  sgLockAngleMatrix::setDependentsDirty( const MPlug& plug, MPlugArray& plugArr )
{
	MStatus status;

	

	return MS::kSuccess;
}


MMatrix  sgLockAngleMatrix::getsgLockAngleMatrix( const MMatrix& inputMatrix, unsigned char axis, double angle )
{
	MStatus status;

	angle = angle/180 * PI;
	bool minusAxis = false;

	if( axis > 2 )
	{
		minusAxis = true;
		axis -= 3;
	}
	unsigned int upAxis = ( axis+1 ) % 3;
	unsigned int crossAxis = ( axis+2 ) % 3;

	MVector vDefault( 0,0,0 );
	vDefault[ axis ] = 1;
	MVector vAxis = inputMatrix[ axis ];
	vAxis.normalize();

	double dotValue = vAxis * vDefault;
	double cuAngle = acos( dotValue );

	if( angle > cuAngle ) angle = cuAngle;

	MVector vCross = vDefault ^ vAxis;
	MVector vUp    = vCross ^ vDefault;

	vUp.normalize();
	MVector vEdit = sin( angle ) * vUp + cos( angle ) * vDefault;

	if( minusAxis ) vEdit *= -1;

	MVector vUpEdit;
	vUpEdit[ axis ] = -vEdit[ upAxis ];
	vUpEdit[ upAxis ] = vEdit[ axis ];
	vUpEdit[ crossAxis ] = 0;

	MVector vCrossEdit = vEdit ^ vUpEdit;
	vUpEdit = vCrossEdit ^ vEdit;

	vEdit.normalize();
	vUpEdit.normalize();
	vCrossEdit.normalize();

	MMatrix returnMtx;

	returnMtx( axis, 0 ) = vEdit.x;
	returnMtx( axis, 1 ) = vEdit.y;
	returnMtx( axis, 2 ) = vEdit.z;
	returnMtx( upAxis, 0 ) = vUpEdit.x;
	returnMtx( upAxis, 1 ) = vUpEdit.y;
	returnMtx( upAxis, 2 ) = vUpEdit.z;
	returnMtx( crossAxis, 0 ) = vCrossEdit.x;
	returnMtx( crossAxis, 1 ) = vCrossEdit.y;
	returnMtx( crossAxis, 2 ) = vCrossEdit.z;

	return returnMtx;
}