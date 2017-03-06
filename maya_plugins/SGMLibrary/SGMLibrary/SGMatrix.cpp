#include "precompile.h"

#include "SGMatrix.h"
#include "SGPrintf.h"
#include <maya/MDagPath.h>
#include <maya/MTransformationMatrix.h>
#include <maya/MEulerRotation.h>
#include <maya/MQuaternion.h>
#include <maya/MPointArray.h>
#include <maya/MFnCamera.h>


const double radian = 3.14159265359f / 180.0f;


bool SGMatrix::isOrtho() {
	M3dView view = M3dView::active3dView();
	MDagPath dagPath;
	view.getCamera(dagPath);
	MFnCamera fnCam(dagPath);
	return fnCam.isOrtho();
}



void SGMatrix::viewToWorld( int x, int y, MPoint& nearClip, MPoint& farClip, const MMatrix& camMatrix) {
	M3dView view = M3dView::active3dView();
	view.viewToWorld(x, y, nearClip, farClip);
	MMatrix origCamMatrix = SGMatrix::getCamMatrix();
	MMatrix mirrorMatrix = origCamMatrix.inverse() * camMatrix;
	nearClip *= mirrorMatrix;
	farClip  *= mirrorMatrix;
}



MPoint SGMatrix::getCrossPoint(const MPoint& v1Src, const MPoint& v1Dst,
	const MPoint& v2Src, const MPoint& v2Dst) {

	/*
	MVector srcVector = v2Src - v1Src;
	MVector v1 = v1Dst - v1Src; v1.normalize();
	MVector v2 = v2Dst - v2Src; v2.normalize();

	MVector proj = v1*(v1 * srcVector);
	MVector vert = proj - srcVector;

	double cosValue = acos( vert.normal() * v2 );
	if (v1 * v2 < 0) cosValue *= -1;

	return v1*(tan(cosValue) * vert.length()) + proj + v1Src;*/
		
	MPoint A = v1Src;
	MPoint B = v1Dst;
	MPoint C = v2Src;
	MPoint D = v2Dst;

	double t1 = (( A.y - C.y ) * ( D.x - C.x ) - ( A.x - C.x ) * ( D.y - C.y ))/
		((B.x - A.x) * (D.y - C.y) - (B.y - A.y) * (D.x - C.x));
	return A + (B - A)*t1;
}



void SGMatrix::rotateMatrix(MMatrix& mtx, MVector rotXYZ) {
	MTransformationMatrix trMtx(mtx);
	trMtx.rotateTo(MEulerRotation(rotXYZ.x * radian, rotXYZ.y * radian, rotXYZ.z * radian));
	mtx = trMtx.asMatrix();
};



void SGMatrix::setMatrixPosition(MMatrix& matrix, MPoint pos) {
	matrix(3, 0) = pos.x;
	matrix(3, 1) = pos.y;
	matrix(3, 2) = pos.z;
}



MMatrix SGMatrix::getRotateMatrix( const MMatrix& mtx, MVector rotXYZ) {
	MMatrix matrix;
	MTransformationMatrix trMtx(mtx);
	trMtx.rotateTo(MEulerRotation(rotXYZ.x * radian, rotXYZ.y * radian, rotXYZ.z * radian));
	return trMtx.asMatrix();
}



MMatrix SGMatrix::getRotateMatrix(MVector base, MVector rot)
{
	MQuaternion quaternion = base.rotateTo(rot);
	return quaternion.asMatrix();
}



double SGMatrix::getLineDist(const MPoint& lineSrc, const MPoint& lineDst, const MPoint& point)
{
	MVector lineVector = lineDst - lineSrc;
	MVector pointVector = point - lineSrc;
	if (lineVector * pointVector < 0) return lineSrc.distanceTo(point);
	MVector projVector = lineVector * (lineVector * pointVector) / pow(lineVector.length(), 2);
	if (projVector.length() > lineVector.length()) return lineDst.distanceTo(point);
	return (pointVector - projVector).length();
}



MPoint SGMatrix::getTriangleCenter(const MPointArray& trianglePoints)
{
	if (trianglePoints.length() < 3) return MPoint(0,0,0);
	const MPoint& point1 = trianglePoints[0];
	const MPoint& point2 = trianglePoints[1];
	const MPoint& point3 = trianglePoints[2];
	MPoint center = (point1 + point2) / 2;
	MVector v = center - point3;
	return v * 2.0 / 3.0 + point3;
}



MPoint SGMatrix::getCamPos() {
	M3dView active3dView = M3dView().active3dView();
	MDagPath dagPathCam;
	active3dView.getCamera(dagPathCam);
	return MPoint((dagPathCam.inclusiveMatrix())[3]);
}


MVector SGMatrix::getCamVector(int indexAxis) {
	M3dView active3dView = M3dView().active3dView();
	MDagPath dagPathCam;
	active3dView.getCamera(dagPathCam);
	return MVector((dagPathCam.inclusiveMatrix())[indexAxis]);
}


MMatrix SGMatrix::getCamMatrix() {
	M3dView active3dView = M3dView().active3dView();
	MDagPath dagPathCam;
	active3dView.getCamera(dagPathCam);
	return dagPathCam.inclusiveMatrix();
}


double SGMatrix::getAngleWidthCam( const MPoint& pointSrc, const MVector& vector ) {
	MVector camVector;
	if (isOrtho()) {
		camVector = getCamVector();
	}
	else {
		camVector = getCamPos() - pointSrc;
	}
	return camVector.angle(vector)/3.14159 * 180;
}


double  SGMatrix::getManipSizeFromWorldPoint(const MPoint& worldPoint, const MMatrix& camMatrix){
	MVector camXVector = SGMatrix::getCamVector(0);
	MPoint viewCenter = SGMatrix::getViewPointFromWorld(worldPoint, camMatrix);
	MPoint viewX = SGMatrix::getViewPointFromWorld(worldPoint + camXVector, camMatrix);
	return viewCenter.distanceTo(viewX);
}


MMatrix SGMatrix::getCamInverseMatrix(M3dView view)
{
	MDagPath camDagPath;
	view.getCamera(camDagPath);
	MMatrix camMatrixInv = (camDagPath.inclusiveMatrix()).inverse();
	return camMatrixInv;
}


MMatrix SGMatrix::getProjectionMatrix(M3dView view)
{
	MMatrix MPerspective;
	view.projectionMatrix(MPerspective);
	return MPerspective;
}


MMatrix SGMatrix::getWorldToViewMatrix( const MMatrix& camMatrix )
{
	M3dView active3dView = M3dView().active3dView();
	MMatrix projection; active3dView.projectionMatrix(projection);
	MMatrix mtxResult = camMatrix.inverse() * projection;
	return mtxResult;
}



MMatrix SGMatrix::getViewToWorldMatrix(const MMatrix& camMatrix )
{
	return (getWorldToViewMatrix(camMatrix).inverse());
}



MPoint SGMatrix::getViewPointFromWorld(MPoint srcPoint, const MMatrix& camMatrix, MMatrix* pMatrix )
{
	bool getNewMatrix = false;
	if (pMatrix == NULL) {
		pMatrix = new MMatrix;
		*pMatrix = getWorldToViewMatrix(camMatrix);
		getNewMatrix = true;
	}

	MPoint dstPoint = srcPoint * (*pMatrix);
	M3dView active3dView = M3dView().active3dView();

	int width = active3dView.portWidth();
	int height = active3dView.portHeight();

	dstPoint.x /= dstPoint.w;
	dstPoint.y /= dstPoint.w;
	dstPoint.z = 0;
	dstPoint.w = 1;

	dstPoint.x = (dstPoint.x + 1) / 2 * width;
	dstPoint.y = (dstPoint.y + 1) / 2 * height;

	if (getNewMatrix) delete pMatrix;
	return dstPoint;
}



MPoint SGMatrix::getWorldPointFromView(MPoint viewPoint, const MMatrix& camMatrix, MMatrix* pMatrix )
{
	bool getNewMatrix = false;
	if (pMatrix == NULL) {
		pMatrix = new MMatrix;
		*pMatrix = getWorldToViewMatrix(camMatrix).inverse();
		getNewMatrix = true;
	}

	M3dView active3dView = M3dView().active3dView();
	int width = active3dView.portWidth();
	int height = active3dView.portHeight();
	viewPoint.x = viewPoint.x / width * 2 - 1;
	viewPoint.y = viewPoint.y / height * 2 - 1;
	viewPoint.z = 0;
	viewPoint.w = 1;
	viewPoint *= (*pMatrix);
	viewPoint.x /= viewPoint.w;
	viewPoint.y /= viewPoint.w;
	viewPoint.z /= viewPoint.w;
	viewPoint.w /= viewPoint.w;
	if (getNewMatrix) delete pMatrix;

	return viewPoint;
}


double SGMatrix::getPointAndVectorDist(const MPoint& vectorSrc, const MPoint& vectorDest, const MPoint& point, MPoint* pointProjected, float* param, bool lockStartAndEnd) {
	MVector edgeVector = vectorDest - vectorSrc;
	MVector pointVector = point - vectorSrc;

	if (edgeVector*pointVector < 0 && lockStartAndEnd) {
		if (pointProjected != NULL) *pointProjected = vectorSrc;
		if (param != NULL) *param = 0;
		return point.distanceTo(vectorSrc);
	}

	double edgeVectorPow = edgeVector.x*edgeVector.x + edgeVector.y*edgeVector.y + edgeVector.z*edgeVector.z;
	MVector projVector = edgeVector * ((edgeVector * pointVector) / edgeVectorPow);
	double projVectorPow = projVector.x*projVector.x + projVector.y*projVector.y + projVector.z*projVector.z;

	if (projVectorPow > edgeVectorPow && lockStartAndEnd) {
		if (pointProjected != NULL) *pointProjected = vectorDest;
		if (param != NULL) *param = 1;
		return point.distanceTo(vectorDest);
	}

	if (pointProjected != NULL) *pointProjected = projVector + vectorSrc;
	if (param != NULL) *param = (float)projVector.length() / (float)edgeVector.length();
	if (edgeVector*pointVector < 0) *param *= -1;
	MVector verticalVector = pointVector - projVector;

	return verticalVector.length();
}

MPoint SGMatrix::getLineIntersectPoint(MPoint lineSrc, MPoint lineDst, int mouseX, int mouseY, const MMatrix& camMatrix ) {
	M3dView view = M3dView::active3dView();
	double width  = (float)view.portWidth();
	double height = (float)view.portHeight();
	double aspect = (float)width / height;

	MPoint mouseView( mouseX, mouseY );
	MPoint lineSrcView = SGMatrix::getViewPointFromWorld(lineSrc, camMatrix );
	MPoint lineDstView = SGMatrix::getViewPointFromWorld(lineDst, camMatrix );

	MVector line = lineDstView - lineSrcView;
	MVector lineMouse = mouseView - lineSrcView;
	MVector vProj = line * ((line * lineMouse) / pow(line.length(), 2));

	double weight = vProj.length() / line.length();
	if (line * vProj < 0) weight *= -1;
	
	return (lineDst - lineSrc)*weight + lineSrc;
}


MPoint  SGMatrix::getPlaneIntersectPoint(MPoint planeSrc, MVector normal, int mouseX, int mouseY, const MMatrix& camMatrix)
{
	normal.normalize();

	MMatrix multMtx = getCamMatrix().inverse() * camMatrix;

	M3dView view = M3dView::active3dView();
	double width = (float)view.portWidth();
	double height = (float)view.portHeight();
	double aspect = width / height;

	MPoint  camNearPoint;
	MPoint  camFarPoint;
	view.viewToWorld(mouseX, mouseY, camNearPoint, camFarPoint);
	camNearPoint *= multMtx;
	camFarPoint *= multMtx;
	MVector mouseVector = camFarPoint - camNearPoint;
	mouseVector.normalize();

	MVector ncv = planeSrc - camNearPoint;
	MVector hVector = normal * (ncv * normal);
	MVector hVNormalize = hVector.normal();
	MVector proj = hVNormalize * (hVNormalize * mouseVector);
	double multLength = hVector.length()/proj.length();

	return multLength * mouseVector + camNearPoint;
}



bool SGMatrix::isPointInPolygon2d(const MPoint& targetPoint, const MPointArray& polyPoints, MBoundingBox* pbb )
{
	MPoint minPoint;
	MPoint maxPoint;

	if (pbb != NULL) {
		minPoint = pbb->min();
		maxPoint = pbb->max();
	}
	else {
		MBoundingBox bb;
		for (unsigned int i = 0; i < polyPoints.length(); i++)
			bb.expand(polyPoints[i]);

		minPoint = bb.min();
		maxPoint = bb.max();
	}

	if (targetPoint.x < minPoint.x || targetPoint.x > maxPoint.x ||
		targetPoint.y < minPoint.y || targetPoint.y > maxPoint.y)
		return false;

	MVector beforeV = polyPoints[1] - polyPoints[0];
	for (unsigned int i = 1; i < polyPoints.length(); i++) {
		MVector p1 = polyPoints[i - 1];
		MVector p2 = polyPoints[i];

		MVector currentV = p2 - p1;
		MVector compairV = targetPoint - p1;
		double crossValue = beforeV.x*currentV.y - beforeV.y*currentV.x;
		double crossValueTarget = currentV.x*compairV.y - currentV.y*compairV.x;
		if (crossValue > 0 && crossValueTarget < 0 ||
			crossValue < 0 && crossValueTarget > 0) return false;
		beforeV = currentV;
	}
	return true;
}