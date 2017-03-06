#pragma once

#include "SGBase.h"
#include <maya/MPoint.h>
#include <maya/MVector.h>
#include <maya/MFnMesh.h>
#include <maya/MMatrix.h>
#include <maya/M3dView.h>
#include <maya/MPointArray.h>
#include <maya/MBoundingBox.h>



class SGMatrix
{
public:
	
	static MMatrix getCamMatrix();
	static bool    isOrtho();
	static void    viewToWorld( int x, int y, MPoint& nearClip, MPoint& farClip, const MMatrix& camMatrix );
	static MPoint  getCrossPoint(const MPoint& v1Src, const MPoint& v1Dst, const MPoint& v2Src, const MPoint& v2Dst);
	static void    rotateMatrix( MMatrix& mtx, MVector rotXYZ );
	static void    setMatrixPosition(MMatrix& matrix, MPoint pos);
	static MMatrix getRotateMatrix(const MMatrix& mtx, MVector rotXYZ);
	static MMatrix getRotateMatrix(MVector base, MVector rot);
	static double  getLineDist(const MPoint& lineSrc, const MPoint& lineDest, const MPoint& point);
	static MPoint  getTriangleCenter(const MPointArray& trianglePoints);
	static MVector getCamVector( int indexAxis = 2 );
	static MPoint  getCamPos();
	static double  getAngleWidthCam(const MPoint& pointSrc, const MVector& vector );
	static double  getManipSizeFromWorldPoint(const MPoint& worldPoint, const MMatrix& camMatrix);
	static MMatrix getWorldToViewMatrix( const MMatrix& camMatrix );
	static MMatrix getViewToWorldMatrix(const MMatrix& camMatrix);
	static MPoint  getViewPointFromWorld(MPoint worldPoint, const MMatrix& camMatrix, MMatrix* pMatrix = NULL);
	static MPoint  getWorldPointFromView(MPoint viewPoint, const MMatrix& camMatrix, MMatrix* pMatrix = NULL);
	static MMatrix getCamInverseMatrix(M3dView view);
	static MMatrix getProjectionMatrix(M3dView view);
	static double  getPointAndVectorDist(const MPoint& vectorSrc, const MPoint& vectorDest, const MPoint& point, MPoint* pointProjected, float* param, bool lockStartAndEnd = true);
	static MPoint  getLineIntersectPoint(MPoint lineSrc, MPoint lineDst, int mouseOffsetX, int mouseOffsetY, const MMatrix& camMatrix);
	static MPoint  getPlaneIntersectPoint(MPoint planeSrc, MVector normal, int mouseX, int mouseY, const MMatrix& camMatrix);
	static bool    isPointInPolygon2d(const MPoint& targetPoint, const MPointArray& polyPoints, MBoundingBox* pbb= NULL );
	static bool    isPointInPolygon3d(const MPoint& targetPoint, const MPointArray& polyPoints);
};