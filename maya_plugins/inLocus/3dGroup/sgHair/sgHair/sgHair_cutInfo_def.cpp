#include "sgHair_cutInfo.h"


MStatus sgHair_cutInfo::getOutput()
{
	MStatus status;

	MMatrix mtxMult = m_mtxInputCurve * m_mtxInputMesh.inverse();

	MMeshIntersector intersector;
	intersector.create( m_oMeshBase );

	MFnNurbsCurve fnBaseCurve = m_oCurveBase;
	int spans = fnBaseCurve.numSpans();
	int degree = fnBaseCurve.degree();
	double minParam = fnBaseCurve.findParamFromLength( 0 );
	double maxParam = fnBaseCurve.findParamFromLength( fnBaseCurve.length() );
	double eachParam = (maxParam-minParam) / (spans *10);
	double closeParam = 0.0;
	MPointOnMesh pointOnMesh;

	MPoint pointInCurve;
	MPoint pointInMesh;
	MVector normalInMesh;

	double minDist = 10000000.0;
	double targetParam = 0.0;
	MPoint closePoint;

	for( int i=0; i<(spans*10)+1; i++ )
	{
		fnBaseCurve.getPointAtParam( eachParam * i + minParam, pointInCurve );
		pointInCurve*= mtxMult;
		intersector.getClosestPoint( pointInCurve, pointOnMesh );
		pointInMesh = pointOnMesh.getPoint();
		normalInMesh = pointOnMesh.getNormal();

		if( ( pointInCurve - pointInMesh ) * normalInMesh > 0 )
		{
			targetParam = eachParam * i + minParam;
			closePoint = pointInMesh;
			break;
		}
	}

	float currentParam = targetParam;

	if( targetParam > 0.001 )
	{
		double currentParamMinus;
		double currentParamPlus;
		MPoint pointInCurvePlus;
		MPoint pointInCurveMinus;
		MPoint pointInMeshPlus;
		MPoint pointInMeshMinus;
		MPointOnMesh pointOnMeshPlus;
		MPointOnMesh pointOnMeshMinus;

		bool lastIsPlus = false;

		for( int i=0; i< 10; i++ )
		{
			currentParamPlus = currentParam + eachParam;
			currentParamMinus = currentParam - eachParam;
			fnBaseCurve.getPointAtParam( currentParamPlus, pointInCurvePlus );
			fnBaseCurve.getPointAtParam( currentParamMinus, pointInCurveMinus );
			pointInCurvePlus*= mtxMult;
			pointInCurveMinus*= mtxMult;
			intersector.getClosestPoint( pointInCurvePlus, pointOnMeshPlus );
			intersector.getClosestPoint( pointInCurveMinus, pointOnMeshMinus );
			pointInMeshPlus  = pointOnMeshPlus.getPoint();
			pointInMeshMinus = pointOnMeshMinus.getPoint();

			if( pointInMeshPlus.distanceTo( pointInCurvePlus ) < pointInMeshMinus.distanceTo( pointInCurveMinus ) )
			{
				currentParam = currentParamPlus;
				lastIsPlus = true;
			}
			else
			{
				currentParam = currentParamMinus;
				lastIsPlus = false;
			}

			if( currentParam < minParam )
			{
				currentParam = minParam;
				break;
			}
			if( currentParam > maxParam )
			{
				currentParam = maxParam;
				break;
			}
			eachParam *= 0.5;
		}

		if( lastIsPlus )
		{
			closePoint = pointOnMeshPlus.getPoint();
		}
		else
		{
			closePoint = pointOnMeshMinus.getPoint();
		}
	}

	float currentU = 0.0;
	float currentV = 0.0;

	MFnMesh fnMeshBase( m_oMeshBase );
	float2 uv = { currentU, currentV };
	
	MStringArray setNames;
	fnMeshBase.getUVSetNames( setNames );
	fnMeshBase.getUVAtPoint( closePoint, uv, MSpace::kTransform );

	m_outU = uv[0];
	m_outV = uv[1];
	m_outParam = currentParam;
	m_pointClose = closePoint * m_mtxInputMesh * m_mtxInputCurve.inverse();

	return MS::kSuccess;
}