#pragma once

#include "SGBase.h"
#include <maya/MPoint.h>
#include <maya/MPointArray.h>
#include <maya/MDagPath.h>
#include <maya/M3dView.h>
#include <maya/MMatrix.h>
#include <maya/MFloatPoint.h>
#include <maya/MFloatPointArray.h>
#include <maya/MFnMesh.h>
#include <maya/MIntArray.h>
#include <maya/MPointArray.h>
#include <maya/MItMeshPolygon.h>
#include "SGComponentType.h"


class SGIntersectResult
{
public:
	enum intersectionType {
		kNoneResult,
		kVtxResult,
		kEdgeResult,
		kPolyResult
	};

	SGIntersectResult();
	~SGIntersectResult();

	void setObject( MObject oMesh );
	void setMeshMatrix(MDagPath dagPath);
	void setDagPath(MDagPath dagPath);
	void clearResult();
	bool   getInsideIntersectionResult(int x, int y);
	bool   getOutsideIntersectionResult(int x, int y);
	float  updateParameter(int mouseX, int mouseY, MPoint* pPointProjected );
	MPoint getVtxNormalIntersectPoint( int mouseX, int mouseY );

	MMatrix camMatrix;

	int     vtxIndex;
	double  vtxDist;
	MPoint  vtxPoint;
	MVector vtxNormal;

	int    edgeIndex;
	float  edgeParam;
	double edgeDist;
	MPointArray  edgePoints;

	MPoint       intersectPoint;
	int          polyIndex;
	MPointArray  polyPoints;

	MObject     oMesh;
	MMatrix     meshMatrix;

	SGComponentType gotType;
	SGComponentType resultType;
	bool isNone() const;
	bool isVertex() const;
	bool isEdge() const;
	bool isPolygon() const;

	int   resultIndex;

	static SGIntersectResult getIntersectionResult(int x, int y, const MMatrix& camMatrix );
	
	bool isResultHasNoProblem();
	bool itHasOppositNormal(int mouseX, int mouseY, const MMatrix& camMatrix);
};