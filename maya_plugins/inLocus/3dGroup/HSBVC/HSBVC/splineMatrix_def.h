#ifndef _splineMatrix_def_h
#define _splineMatrix_def_h

#include "splineMatrix.h"


MStatus splineMatrix::updateCurveInfo( MObject oInputCurve )
{
	MFnNurbsCurve fnCurve( oInputCurve );

	minParam = fnCurve.findParamFromLength( 0.0 );
	maxParam = fnCurve.findParamFromLength( fnCurve.length() );

	return MS::kSuccess;
}



MMatrix* splineMatrix::getMatrixArrayFromParamList( MMatrix upMatrix, double* paramList, MMatrix mtxCurve, MObject* p_oCurve, int paramListLength ) 
{
	MMatrix* retrunMatrixPtr = new MMatrix[ paramListLength ];

	MFnNurbsCurve fnCurve( *p_oCurve );

	double pivParam;
	double aimParam;
	MPoint pivPoint;
	MPoint aimPoint;
	MVector aimVector;
	MMatrix localMatrix = mtxCurve.inverse()*upMatrix;
	MMatrix localMatrixInv = upMatrix.inverse();

	for( int i=0; i< paramListLength; i++ )
	{
		pivParam = minParam + paramList[i]*( maxParam - minParam );
		aimParam = minParam + paramList[i+1]*( maxParam - minParam );

		if( angleByTangent )
		{
			fnCurve.getPointAtParam( pivParam, pivPoint );
			aimVector = fnCurve.tangent( pivParam );
		}
		else
		{
			fnCurve.getPointAtParam( pivParam, pivPoint );
			fnCurve.getPointAtParam( aimParam, aimPoint );
			aimVector = aimPoint - pivPoint;
		}

		aimVector *= localMatrixInv;
		pivPoint  *= localMatrixInv;

		aimVector.normalize();

		MVector upVector( -aimVector.y, aimVector.x, 0 );
		MVector otherVector( -aimVector.z, 0, aimVector.x );

		MVector editUpVector = otherVector^aimVector;

		double absY = abs( aimVector.y );

		upVector = upVector*absY + editUpVector*( 1-absY ); 

		otherVector = aimVector^upVector;
		upVector = otherVector^aimVector;

		otherVector.normalize();
		upVector.normalize();

		double buildMatrix[4][4] = { aimVector.x, aimVector.y, aimVector.z, 0,
									 upVector.x,  upVector.y,  upVector.z, 0,
									 otherVector.x, otherVector.y, otherVector.z, 0,
									 pivPoint.x, pivPoint.y, pivPoint.z, 1.0 };

		localMatrix = MMatrix( buildMatrix )*localMatrix;
		localMatrixInv = localMatrix.inverse();

		retrunMatrixPtr[i] = localMatrix;
	}
	return retrunMatrixPtr;
}



MStatus  splineMatrix::initialize()
{
	MStatus  status;

	MFnNumericAttribute  nAttr;
	MFnMatrixAttribute   mAttr;
	MFnTypedAttribute    tAttr;
	MFnCompoundAttribute cAttr;

	aOutputMatrix = mAttr.create( "outputMatrix", "outputMatrix" );
	mAttr.setArray( true );
	mAttr.setUsesArrayDataBuilder( true );
	CHECK_MSTATUS( addAttribute( aOutputMatrix ) );

	aInputCurve = tAttr.create( "inputCurve", "inputCurve", MFnData::kNurbsCurve );
	tAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aInputCurve ) );
	CHECK_MSTATUS( attributeAffects( aInputCurve, aOutputMatrix ) );

	aInputCurveMatrix = mAttr.create( "inputCurveMatrix", "inputCurveMatrix" );
	mAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aInputCurveMatrix ) );
	CHECK_MSTATUS( attributeAffects( aInputCurveMatrix, aOutputMatrix ) );

	aTopMatrix = mAttr.create( "topMatrix", "topMatrix" );
	mAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aTopMatrix ) );
	CHECK_MSTATUS( attributeAffects( aTopMatrix, aOutputMatrix ) );

	aParameter = nAttr.create( "parameter", "parameter", MFnNumericData::kDouble, 0.0 );
	nAttr.setMin( 0.0 );
	nAttr.setMax( 1.0 );
	nAttr.setArray( true );
	nAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aParameter ) );
	CHECK_MSTATUS( attributeAffects( aParameter, aOutputMatrix ) );

	aAngleByTangent = nAttr.create( "angleByTangent", "angleByTangent", MFnNumericData::kBoolean, true );
	nAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aAngleByTangent ) );
	CHECK_MSTATUS( attributeAffects( aAngleByTangent, aOutputMatrix ) );

	return MS::kSuccess;
}

#endif