#include "sgCurveEditBrush_context.h"
#include <maya/MFnCamera.h>
#include <maya/MFloatMatrix.h>
#include "sgPrintf.h"
#include "sgCurveEditBrush_functions.h"


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

	/*
	MDagPath dagPathCam;
	M3dView view = M3dView::active3dView( &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	view.getCamera( dagPathCam );

	MPoint  camPos = dagPathCam.inclusiveMatrix()[3];
	MVector vCamUp  = dagPathCam.inclusiveMatrix()[1];
	vCamUp.normalize();

	radius *= .05f;

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

	for(unsigned int i=0; i< points.length(); i++ )
	{
		points[i] *= mtxCurve;
	}

	for(unsigned int i=1; i< points.length(); i++ )
	{
		MPoint cuPoint = points[i];
		MVector vPoint = cuPoint - camPos;

		MVector projV = ( vPoint * rayBefore )/( pow( rayBefore.length(), 2 ) )* rayBefore;
		MVector vertical = vPoint - projV;
		
		double radiusForPoint = vertical.length() / projV.length();

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

		for(unsigned int j=i+1; j< points.length(); j++ )
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
	for(unsigned int i=0; i< points.length(); i++ )
		points[i] *= invMtxCurve;
	

	fnCurve.setCVs( points );
	fnCurve.updateCurve();*/


	M3dView view = M3dView::active3dView(&status);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	MDagPath dagPathCam;
	view.getCamera(dagPathCam);
	MMatrix camMatrix = dagPathCam.inclusiveMatrix();

	MFnCamera fnCam(dagPathCam);

	MMatrix viewProjectionMatrix;
	view.projectionMatrix(viewProjectionMatrix);
	MPoint camPos( camMatrix[3] );
	MVector camVector = MVector(0,0,-1) * camMatrix;
	MMatrix worldToViewMatrix = dagPathCam.inclusiveMatrixInverse() * viewProjectionMatrix;

	MMatrix mtxCurve = dagPathCurve.inclusiveMatrix();
	MFnNurbsCurve fnCurve(dagPathCurve);

	fnCurve.getCVs(points);

	for (unsigned int i = 0; i< points.length(); i++)
	{
		points[i] *= mtxCurve;
	}

	MPoint  cuPointMouse(currentX, currentY);
	MVector beforePointMouse(beforeX, beforeY);

	MPoint  nearClipCu, farClipCu, nearClipBefore, farClipBefore;
	view.viewToWorld(currentX, currentY, nearClipCu, farClipCu);
	view.viewToWorld(beforeX, beforeY, nearClipBefore, farClipBefore);

	for (unsigned int i = 1; i < points.length(); i++)
	{
		MPoint beforeEditViewPoint = getWorldToViewPoint(points[i]);
		MPoint nearClipPivPoint, farClipPivPoint;
		view.viewToWorld(beforeEditViewPoint.x, beforeEditViewPoint.y, nearClipPivPoint, farClipPivPoint);

		float weight = 1.0 - beforeEditViewPoint.distanceTo(cuPointMouse) / radius;
		if (weight < 0) weight = 0;
		weight = pow(weight, 0.5);

		MVector targetVectorFromCam = points[i] - nearClipPivPoint;
		MPoint beforeEditedPoint = (farClipBefore - nearClipBefore).normal() * targetVectorFromCam.length() + nearClipBefore;
		MPoint editedPoint = (farClipCu - nearClipCu).normal() * targetVectorFromCam.length() + nearClipCu;
		MVector EditVector = editedPoint - beforeEditedPoint;
		MPoint pivPoint  = points[i-1];
		MPoint editPoint = points[i];

		MPoint keepLenghedEditedPoint = (editPoint - pivPoint + EditVector * weight ).normal() * (editPoint - pivPoint).length() + pivPoint;

		MPoint beforeBasePoint = points[i];
		MPoint afterBasePoint  = keepLenghedEditedPoint;
		points[i] = keepLenghedEditedPoint;

		if (weight < 0) continue;
		/**/
		for (unsigned int j = i+1; j < points.length(); j++)
		{
			MPoint keepLengthedFollowPoint = ( points[j] - afterBasePoint ).normal() * (points[j] - beforeBasePoint).length() + afterBasePoint;
			beforeBasePoint = points[j];
			afterBasePoint = keepLengthedFollowPoint;
			points[j] = keepLengthedFollowPoint;
		}/**/
		//sgPrintf("edited point[%d] : %f, %f, %f", i, editedPoint.x, editedPoint.y, editedPoint.z );
		//sgPrintf("weight[%d] : %f", i, weight );
	}
	//sgPrintf("");

	MMatrix invMtxCurve = mtxCurve.inverse();
	for (unsigned int i = 0; i< points.length(); i++)
		points[i] *= invMtxCurve;

	fnCurve.setCVs(points);
	fnCurve.updateCurve();

	return MS::kSuccess;
}