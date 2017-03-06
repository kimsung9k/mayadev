#include "editMatrixByCurve.h"

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MMatrix.h>
#include <maya/MPoint.h>
#include <maya/MFnNurbsCurve.h>

#include <maya/MGlobal.h>

using namespace std;

MTypeId     editMatrixByCurve::id( 0xc8d211 );

MObject editMatrixByCurve::aSourceMatrix;
MObject editMatrixByCurve::aUpMatrix;
MObject editMatrixByCurve::aSourceCurve;
MObject editMatrixByCurve::aDestCurve;
MObject editMatrixByCurve::aOutSourceMatrix;
MObject editMatrixByCurve::aOutDestMatrix;
MObject editMatrixByCurve::aOutOffsetMatrix;

editMatrixByCurve::editMatrixByCurve() {}
editMatrixByCurve::~editMatrixByCurve() {}

void* editMatrixByCurve::creator()
{
	return new editMatrixByCurve();
}


double getCloestParam( MPoint &inPoint, MFnNurbsCurve& fnCurve )
{
	int spans = fnCurve.numSpans();
	double maxParam = fnCurve.findParamFromLength( fnCurve.length() );
	
	double paramRate = maxParam/spans;
	double currentParam = 0.0;

	MPoint currentPoint;
	fnCurve.getPointAtParam( currentParam, currentPoint );
	double dist = 1000;

	double cuDist;

	double startParam = currentParam;

	for( int i=0; i< spans; i++ )
	{
		currentParam += paramRate;

		fnCurve.getPointAtParam( paramRate, currentPoint );
		cuDist = inPoint.distanceTo( currentPoint );

		if( cuDist < dist )
		{
			startParam = currentParam;
			dist = cuDist;
		}
	}
	int searchDetail = 15;

	MPoint increasePoint;
	double increaseDist;

	while( searchDetail > 0 && cuDist > 0.001 )
	{
		paramRate *= 0.5;
		fnCurve.getPointAtParam( startParam+0.0001, increasePoint );

		increaseDist = inPoint.distanceTo( increasePoint );

		if( cuDist > increaseDist )
		{
			startParam += paramRate;
		}
		else
		{
			startParam -= paramRate;
		}

		fnCurve.getPointAtParam( startParam, currentPoint );
		cuDist = inPoint.distanceTo( currentPoint );
		searchDetail--;
	}
	return currentParam;
}

MMatrix getEditMatrix( MMatrix& upMatrix, MVector aimVector, MPoint point )
{
	MMatrix upInverse = upMatrix.inverse();
	aimVector *= upInverse;
	point *= upInverse;

	MVector upVector( 0, 1, 0 );
	MVector byNormal = aimVector^upVector;
	upVector = byNormal^aimVector;

	aimVector.normalize();
	upVector.normalize();
	byNormal.normalize();

	double buildMatrix[4][4] = { aimVector.x, aimVector.y, aimVector.z, 0,
		                         upVector.x,  upVector.y,  upVector.z, 0,
								 byNormal.x, byNormal.y, byNormal.z, 0,
								 point.x, point.y, point.z, 1.0 };
	MMatrix localMatrix( buildMatrix );

	return localMatrix*upMatrix;
}

MStatus editMatrixByCurve::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	MDataHandle hOutSourceMatrix      = data.outputValue( aOutSourceMatrix );
	MDataHandle hOutDestMatrix        = data.outputValue( aOutDestMatrix );
	MDataHandle hOutOffsetMatrix      = data.outputValue( aOutOffsetMatrix );

	MDataHandle hSourceMatrix     = data.inputValue( aSourceMatrix );
	MDataHandle hUpMatrix         = data.inputValue( aUpMatrix );
	MDataHandle hSourceCurve      = data.inputValue( aSourceCurve, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hDestCurve        = data.inputValue( aDestCurve, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MMatrix  sourceMatrix = hSourceMatrix.asMatrix();
	MMatrix  upMatrix     = hUpMatrix.asMatrix();
	MFnNurbsCurve sourceCurve = hSourceCurve.asNurbsCurve();
	MFnNurbsCurve destCurve   = hDestCurve.asNurbsCurve();

	MPoint sourcePoint( sourceMatrix( 3,0 ), sourceMatrix( 3,1 ), sourceMatrix(3,2 ) );

	double closeParam;
	MPoint sourceClosePoint;
	MPoint destClosePoint;

	sourceCurve.closestPoint( sourcePoint, true, &closeParam );

	sourceCurve.getPointAtParam( closeParam, sourceClosePoint );
	destCurve.getPointAtParam( closeParam, destClosePoint );
	MVector sourceAimVector = sourceCurve.tangent( closeParam );
	MVector destAimVector   = destCurve.tangent( closeParam );

	MMatrix targetMatrix = getEditMatrix( upMatrix, sourceAimVector, sourceClosePoint );
	MMatrix destMatrix   = getEditMatrix( upMatrix, destAimVector, destClosePoint );
	MMatrix offsetMatrix = destMatrix*targetMatrix.inverse();

	hOutSourceMatrix.set( targetMatrix );
	hOutDestMatrix.set( destMatrix );
	hOutOffsetMatrix.set( offsetMatrix );

	data.setClean( plug );

	return status;
}

MStatus editMatrixByCurve::attributeAffectsArray( MObject& affectAttr, MObject** affectedAttrs )
{
	MStatus status;

	for( int i=0; i<3; i++ )
	{
		CHECK_MSTATUS( attributeAffects( affectAttr, *affectedAttrs[i] ) );
	}
	return MS::kSuccess;
}

MStatus editMatrixByCurve::initialize()
{
	MStatus status;

	MFnMatrixAttribute mAttr;
	MFnTypedAttribute tAttr;
	MFnNumericAttribute nAttr;

	MObject* affectedAttrs[3];
	affectedAttrs[0] = &aOutSourceMatrix;
	affectedAttrs[1] = &aOutDestMatrix;
	affectedAttrs[2] = &aOutOffsetMatrix;

	aOutSourceMatrix = mAttr.create( "outSourceMatrix", "outSourceMatrix" );
	CHECK_MSTATUS( addAttribute( aOutSourceMatrix ) );
	aOutDestMatrix = mAttr.create( "outDestMatrix", "outDestMatrix" );
	CHECK_MSTATUS( addAttribute( aOutDestMatrix ) );
	aOutOffsetMatrix = mAttr.create( "outOffsetMatrix", "outOffsetMatrix" );
	CHECK_MSTATUS( addAttribute( aOutOffsetMatrix ) );

	aSourceMatrix = mAttr.create( "sourceMatrix", "sourceMatrix" );
	CHECK_MSTATUS( addAttribute( aSourceMatrix ) );
	attributeAffectsArray( aSourceMatrix, affectedAttrs );

	aUpMatrix = mAttr.create( "upMatrix", "upMatrix" );
	CHECK_MSTATUS( addAttribute( aUpMatrix ) );
	attributeAffectsArray( aUpMatrix, affectedAttrs );

	aSourceCurve = tAttr.create( "sourceCurve", "sourceCurve", MFnData::kNurbsCurve );
	CHECK_MSTATUS( addAttribute( aSourceCurve ) );
	attributeAffectsArray( aSourceCurve, affectedAttrs );

	aDestCurve = tAttr.create( "destCurve", "destCurve", MFnData::kNurbsCurve );
	CHECK_MSTATUS( addAttribute( aDestCurve ) );
	attributeAffectsArray( aDestCurve, affectedAttrs  );

	//aLockLength = nAttr.create( "lockLength", "lockLength" );

	return MS::kSuccess;
}