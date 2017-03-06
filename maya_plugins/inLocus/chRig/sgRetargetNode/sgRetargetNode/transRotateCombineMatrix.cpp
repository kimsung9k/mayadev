#include "transRotateCombineMatrix.h"

#include <maya/MObject.h>
#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MMatrix.h>

#include <maya/MGlobal.h>


using namespace std;

MTypeId     transRotateCombineMatrix::id( 0xc8cc13 );

MObject     transRotateCombineMatrix::aInputTransMatrix;
MObject     transRotateCombineMatrix::aInputRotateMatrix;
MObject     transRotateCombineMatrix::aOutputMatrix;
MObject     transRotateCombineMatrix::aOutputInverseMatrix;

transRotateCombineMatrix::transRotateCombineMatrix() {}
transRotateCombineMatrix::~transRotateCombineMatrix() {}

void* transRotateCombineMatrix::creator()
{
	return new transRotateCombineMatrix();
}

MStatus transRotateCombineMatrix::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	MDataHandle hOutputMatrix = data.outputValue( aOutputMatrix, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hOutputInverseMatrix = data.outputValue( aOutputInverseMatrix, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hTransMatrix = data.inputValue( aInputTransMatrix, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hRotateMatrix = data.inputValue( aInputRotateMatrix, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MMatrix transMatrix = hTransMatrix.asMatrix();
	MMatrix rotateMatrix = hRotateMatrix.asMatrix();

	double buildMatrix[4][4] = { rotateMatrix( 0,0 ), rotateMatrix( 0,1 ), rotateMatrix( 0,2 ), 0,
		                         rotateMatrix( 1,0 ), rotateMatrix( 1,1 ), rotateMatrix( 1,2 ), 0,
								 rotateMatrix( 2,0 ), rotateMatrix( 2,1 ), rotateMatrix( 2,2 ), 0,
								 transMatrix( 3,0 ),  transMatrix( 3,1 ),  transMatrix( 3,2 ),  1 };

	MMatrix buildMtx = buildMatrix;
	
	if( plug == aOutputMatrix )
		hOutputMatrix.set( buildMtx );
	if( plug == aOutputInverseMatrix )
		hOutputInverseMatrix.set( buildMtx.inverse() );

	data.setClean( plug );

	return status;
}

MStatus transRotateCombineMatrix::initialize()
{
	MStatus status;

	MFnMatrixAttribute mAttr;

	aOutputMatrix = mAttr.create( "outputMatrix", "om" );
	mAttr.setStorable( false );
	status = addAttribute( aOutputMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aOutputInverseMatrix = mAttr.create( "outputInverseMatrix", "oim" );
	mAttr.setStorable( false );
	status = addAttribute( aOutputInverseMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aInputTransMatrix = mAttr.create( "inputTransMatrix", "itm" );
	mAttr.setStorable( true );
	status = addAttribute( aInputTransMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffects( aInputTransMatrix, aOutputMatrix );
	status = attributeAffects( aInputTransMatrix, aOutputInverseMatrix );

	aInputRotateMatrix = mAttr.create( "inputRotateMatrix", "irm" );
	mAttr.setStorable( true );
	status = addAttribute( aInputRotateMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffects( aInputRotateMatrix, aOutputMatrix );
	status = attributeAffects( aInputRotateMatrix, aOutputInverseMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	return MS::kSuccess;
}