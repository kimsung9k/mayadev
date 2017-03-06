#include "volumeCurvesOnSurface.h"
#include "volumeCurvesOnSurface_def.h"


class CenterCurve
{
public:
	MPointArray centerPoints;
	MFnNurbsSurface*  pFnSurface;
	MObject           curveObj;
	int numCVsU;
	int numCVsV;
	int degreeU;
	MDoubleArray* pCenterCrvKnots;

	MPointArray outCenterPoints;
	MDoubleArray outParamArr;
public:
	CenterCurve( MFnNurbsSurface *pFnSurface, int numCVsU, int numCVsV, int degreeU, MDoubleArray* pCenterCrvKnots )
	{
		this->pFnSurface = pFnSurface;
		this->numCVsU    = numCVsU;
		this->numCVsV    = numCVsV;
		this->degreeU    = degreeU;
		this->pCenterCrvKnots = pCenterCrvKnots;
	}

	void getCenterCurvePoints( void )
	{
		centerPoints.setLength( numCVsU );

		MPoint surfPoint;
		for( int i=0; i< numCVsU; i++ )
		{
			MBoundingBox boundingBox;
			for( int j=0; j< numCVsV; j++ )
			{
				pFnSurface->getCV( i, j, surfPoint );
				boundingBox.expand( surfPoint );
			}
			centerPoints[i] = ( ( boundingBox.min() + boundingBox.max() )/2.0 );
		}
	}

	void getCenterCurve()
	{
		MFnNurbsCurve fnCreateCenterCurve;
		MFnNurbsCurveData fnCreateCurveData;
		curveObj = fnCreateCurveData.create();

		getCenterCurvePoints();

		fnCreateCenterCurve.create( centerPoints, *pCenterCrvKnots, degreeU, MFnNurbsCurve::kOpen, 0,0,curveObj );
	}

	void getCenterPointsAndParam( int numSample, double minRangeU, double maxRangeU )
	{
		getCenterCurve();

		outCenterPoints.setLength( numSample );
		outParamArr.setLength( numSample );

		MFnNurbsCurve fnCenterCurve( curveObj );

		double maxParam = fnCenterCurve.findParamFromLength( fnCenterCurve.length() );
		double crvParamRate = maxParam / ( numSample - 1 );
		double paramURate = ( maxRangeU-minRangeU ) / ( numSample - 1 );

		MPoint crvPoint;
		for( int j=0; j< numSample; j++ )
		{
			outParamArr[j] = paramURate*j+minRangeU;
			fnCenterCurve.getPointAtParam( crvParamRate*j, crvPoint );
			outCenterPoints[j] = crvPoint;
		}
	}
};