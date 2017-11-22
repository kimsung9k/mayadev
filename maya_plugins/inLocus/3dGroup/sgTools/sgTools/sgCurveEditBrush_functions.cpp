#include "sgCurveEditBrush_functions.h"


MPoint getWorldToViewPoint(MPoint& worldPoint)
{
	M3dView activeView = M3dView::active3dView();
	MDagPath camDagPath;
	activeView.getCamera(camDagPath);

	MMatrix projectionMatrix;
	activeView.projectionMatrix(projectionMatrix);
	MMatrix camInvMatrix = camDagPath.inclusiveMatrixInverse();

	MPoint viewPoint = worldPoint * camInvMatrix * projectionMatrix;
	viewPoint.x = (viewPoint.x / viewPoint.w + 1.0) / 2.0 * activeView.portWidth();
	viewPoint.y = (viewPoint.y / viewPoint.w + 1.0) / 2.0 * activeView.portHeight();
	viewPoint.z = 0;
	viewPoint.w = 1;

	return viewPoint;
}


MPoint getViewToWorldPoint(MPoint& viewPoint)
{
	M3dView activeView = M3dView::active3dView();
	MDagPath camDagPath;
	activeView.getCamera(camDagPath);

	MMatrix projectionMatrix;
	activeView.projectionMatrix(projectionMatrix);
	MMatrix camInvMatrix = camDagPath.inclusiveMatrixInverse();

	viewPoint.x = viewPoint.x / activeView.portWidth() * 2 - 1.0;
	viewPoint.y = viewPoint.y / activeView.portHeight() * 2 - 1.0;
	viewPoint = viewPoint * (camInvMatrix * projectionMatrix).inverse();

	viewPoint.x /= viewPoint.w;
	viewPoint.y /= viewPoint.w;
	viewPoint.z /= viewPoint.w;
	viewPoint.w /= viewPoint.w;

	return viewPoint;
}