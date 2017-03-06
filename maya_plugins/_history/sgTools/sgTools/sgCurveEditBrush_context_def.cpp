#include "sgCurveEditBrush_context.h"

MStatus sgCurveEditBrush_context::getShapeNode( MDagPath& path )
{
    MStatus status;

    if ( path.apiType() == MFn::kNurbsCurve )
    {
        return MS::kSuccess;
    }

    unsigned int numShapes;
    status = path.numberOfShapesDirectlyBelow( numShapes );
    CHECK_MSTATUS_AND_RETURN_IT( status );

    for ( unsigned int i = 0; i < numShapes; ++i )
    {
        status = path.extendToShapeDirectlyBelow( i );
        CHECK_MSTATUS_AND_RETURN_IT( status );

        if ( !path.hasFn( MFn::kNurbsCurve ) )
        {
            path.pop();
            continue;
        }

        MFnDagNode fnNode( path, &status );
        CHECK_MSTATUS_AND_RETURN_IT( status );
        if ( !fnNode.isIntermediateObject() )
        {
            return MS::kSuccess;
        }
        path.pop();
    }

    return MS::kFailure;
}



MStatus sgCurveEditBrush_context::editCurve( MDagPath dagPathCurve,
		int beforeX, int beforeY, int currentX, int currentY, float radius, 
		const MDoubleArray& dArrLength, MPointArray &points )
{
	MStatus status;

	if( radius < 0 ) return MS::kSuccess;

	MDagPath dagPathCam;
	M3dView view = M3dView::active3dView( &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	view.getCamera( dagPathCam );

	MPoint  camPos = dagPathCam.inclusiveMatrix()[3];
	MVector vCamUp  = dagPathCam.inclusiveMatrix()[1];
	vCamUp.normalize();

	radius *= .05;

	MPoint nearClipBefore;
	MPoint farClipBefore;
	view.viewToWorld( beforeX, beforeY, nearClipBefore, farClipBefore );

	MVector rayBefore  = nearClipBefore - camPos;
	rayBefore.normalize();
	rayBefore *= 20;
	MPoint  posBefore = rayBefore + camPos;

	MPoint nearClipCurrent;
	MPoint farClipCurrent;
	view.viewToWorld( currentX, currentY, nearClipCurrent, farClipCurrent );

	MVector rayCurrent = nearClipCurrent - camPos;
	rayCurrent.normalize();
	rayCurrent *= 20;
	MPoint  posCurrent = rayCurrent + camPos;

	MVector vMove = posCurrent - posBefore;

	MMatrix mtxCurve = dagPathCurve.inclusiveMatrix();
	MFnNurbsCurve fnCurve( dagPathCurve );

	fnCurve.getCVs( points );

	for( int i=0; i< points.length(); i++ )
	{
		points[i] *= mtxCurve;
	}

	for( int i=1; i< points.length(); i++ )
	{
		MPoint cuPoint = points[i];
		MVector vPoint = cuPoint - camPos;

		MVector projV = ( vPoint * rayBefore )/( pow( rayBefore.length(), 2 ) )* rayBefore;
		MVector vertical = vPoint - projV;
		
		float radiusForPoint = vertical.length() / projV.length();

		if( radius < radiusForPoint )
			continue;
		MPoint parentPoint = points[i-1];

		MVector vCurveDirection = cuPoint - parentPoint;
		double vDirLength = vCurveDirection.length();

		MVector vEditDirection = vCurveDirection + vMove/rayBefore.length()*projV.length();

		double dotEdit = vCurveDirection.normal() * vEditDirection.normal();
		if( dotEdit < 0 ) continue;
		vEditDirection = vEditDirection * dotEdit + vCurveDirection*( 1-dotEdit );

		MVector vEditLength = vEditDirection / vEditDirection.length() * vCurveDirection.length();

		MVector vEdit = (vEditLength - vCurveDirection) * pow((double)(1-radiusForPoint/radius), 1 );
		points[i] += vEdit;

		for( int j=i+1; j< points.length(); j++ )
		{
			MPoint beforePoint = points[j];
			MPoint pPoint = points[j-1];
			MPoint beforePPoint = pPoint - vEdit;

			MVector vBefore = points[j] - beforePPoint;
			MVector vAfter  = points[j] - pPoint;
			MVector vCurrent = vAfter.normal() * dArrLength[j];
			
			points[j] = vCurrent + pPoint;

			vEdit = points[j] - beforePoint;
		}
	}

	MMatrix invMtxCurve = mtxCurve.inverse();
	for( int i=0; i< points.length(); i++ )
	{
		points[i] *= invMtxCurve;
	}

	fnCurve.setCVs( points );
	fnCurve.updateCurve();

	return MS::kSuccess;
}