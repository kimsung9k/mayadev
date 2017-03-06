#pragma once

#include "SGBase.h"
#include <maya/MDagPath.h>
#include <maya/MIntArray.h>
#include <maya/MFloatArray.h>
#include <maya/MPointArray.h>
#include <maya/MFloatVectorArray.h>
#include <maya/MFnMeshData.h>
#include <maya/MMeshIntersector.h>
#include "SGSplitPoint.h"
#include "SGComponentType.h"
#include <maya/MItMeshVertex.h>
#include <maya/MItMeshEdge.h>
#include <maya/MItMeshPolygon.h>
#include <maya/MFnMesh.h>
#include "SGSymmetry.h"


class SGMesh
{
public:
	SGMesh();
	SGMesh( MDagPath dagPath, const SGSymmetry symInfo );
	~SGMesh();

	void setDagPath(MDagPath dagPath, const SGSymmetry symInfo );

	MMeshIntersector* intersector;
	MObject           oSlidingBaseMesh;

	MDagPath          dagPath;
	MPointArray       points;
	MFloatVectorArray normals;
	MFloatVectorArray polyNormals;
	MIntArray         mirrorIndices;

	int numVertices;
	int numEdges;
	int numPolygons;

	MIntArray getVtxToVtxs( int index ) const;
	MIntArray getVtxToEdges(int index) const;
	MIntArray getVtxToPolys(int index) const;

	MIntArray getEdgeToVtxs(int index) const;
	MIntArray getEdgeToEdges(int index) const;
	MIntArray getEdgeToPolys(int index) const;

	MIntArray getPolyToVtxs(int index) const;
	MIntArray getPolyToEdges(int index) const;
	MIntArray getPolyToPolys(int index) const;

	MIntArray& getVtxsMap(const SGSplitPoint& spPoint)const;
	MIntArray& getEdgesMap(const SGSplitPoint& spPoint)const;
	MIntArray& getPolysMap(const SGSplitPoint& spPoint)const;

	bool updateRequired();
	bool update(const SGSymmetry& symInfo, bool force=0 );
	bool updateVertexAndNormals();
	bool updateBaseMesh();
	bool updateMirror( const SGSymmetry& symInfo);

	bool      isCenter( int index, SGComponentType compType)const;
	bool      isTwoEdgeHasRelation(int index1, int index2)const;
	bool      isTwoSplitPointsHasRelation(const SGSplitPoint& spPoint1, const SGSplitPoint& spPoint2, int* indexPolygon = NULL )const;
	bool      isTwoSplitPointsHasSameEdge(const SGSplitPoint& spPoint1, const SGSplitPoint& spPoint2)const;
	bool      isTwoVertexHasSameEdge(int index1, int index2)const;
	void      getSplitEdgeAndParam(const SGSplitPoint& spPoint, int& edge, float& param, int indexPolygon )const;
	bool      getSplitEdgesAndParams(const SGSplitPoint& spPoint1, const SGSplitPoint& spPoint2,
		                             MIntArray& edges, MFloatArray& params)const;

	MPoint    getPoint(int indexPoint, MSpace::Space space)const;
	MPoint    getEdgeCenter(int indexEdge, MSpace::Space space)const;
	MIntArray getEdgeOpositIndices(int indexEdge, int otherOposit = -1)const;
	MIntArray getEdgeSideIndices(int indexEdge, int oterSide = -1)const;
	MIntArray getEdgeRing(int indexEdge, int beforeIndex = -1)const;
	MIntArray getEdgeLoop(int indexEdge, int beforeIndex = -1)const;
	MIntArray getVertexLoop(int indexVtx, int beforeIndex )const;
	MIntArray getPolygonLoop(int indexPoly, int beforeIndex)const;
	int       getPolygonFromTwoEdge(int edgeIndex1, int edgeIndex2)const;

	static SGMesh* pMesh;

	static MStatus getSelection(const SGSymmetry symInfo);

	MIntArray convertComponent(MIntArray compIndices, SGComponentType typeSrc, SGComponentType typeDest )const;

	MPointArray getEdgePoints(int edgeIndex, MSpace::Space space)const;
	MPointArray getPolyPoints(int polygonIndex, MSpace::Space space)const;
	MPoint      getPolygonCenter(int indexPoly, MSpace::Space space = MSpace::kObject)const;
	MVector     getPolygonNormal(int indexPoly, MSpace::Space space = MSpace::kObject)const;
	MVector     getEdgeVector(int edgeIndex, MSpace::Space space = MSpace::kObject)const;
	MIntArray   getInverseDirectionInfo( int indexEdge, const MIntArray& indicesEdge)const;
	MPoint      getPointFromEdgeParam(int indexEdge, float param, MSpace::Space space = MSpace::kObject)const;
	bool        isOppositeEdge(int baseEdge, int targetEdge)const;

	MIntArray getIndicesNewEdgeRing( int numNewEdges, bool oppositeExists, int offset = 0)const;
	MIntArray getSlideTargetIndices( int indexSlideRoot, int indexOppositeRoot, const MIntArray& indicesSlideMap, MIntArray& checkedMap, int beforeRoot=-1)const;

	MPointArray getIntersectedLinePoints(MPoint lineSrc, MPoint lineDst, const MMatrix& camMatrix, MIntArray* edges = NULL, MFloatArray* params = NULL)const;
};