#pragma once

#include <maya/MPointArray.h>
#include <maya/MFloatVectorArray.h>
#include <maya/MBoundingBox.h>
#include <maya/MStringArray.h>
#include <SGSplitPoint.h>
#include "SGTransformManip.h"
#include <SGIntersectResult.h>


class SGIntersectResult;
class SGComponentType;
class SGMesh;


class SGFunction
{
public:
	static int getSameIndex(const MIntArray& indices1, const MIntArray& indices2);
	static bool isIn(int index, const MIntArray& indices);

	static MIntArray getPolysMap(const SGSplitPoint& spPoint, SGMesh* pMesh);
	static MIntArray getEdgesMap(const SGSplitPoint& spPoint, SGMesh* pMesh);
	static double getVertexParamValue(int vtxIndex, int edgeIndex, SGMesh* pMesh);

	static void getPointOffset( MPoint center );
	static MPoint getWorldPointFromMousePoint( MPoint basePoint );
	static MPoint origCenter;
	static MVector origNormal;
	static MPoint origCenterIntersectPoint;
	static SGIntersectResult slidingIntersector;
	static int mouseXOrig, mouseYOrig;
	static MPoint pointOffset;
	static MPoint pointOffsetXY;
	static MPointArray points_before;
	static MFloatVectorArray normals_before;
	static MPointArray points_after;
	static MFloatArray vertexWeights;
	static void prepairVtxMove();
	static void prepairVtxMoveNormal();
	static void vertexMove_ing();
	static void vertexMove_slide();
	static void vertexMove_snap();
	static void vertexMove_direction(MVector direction = MVector(0, 0, 0));
	static void vertexMove_normal();
	static void vertexMove_end(bool clearSelection = false);
	static int getSnapPointIndex(int resultIndex, MPoint pointMove );

	static double slideParam;
	static vector<MIntArray> edgeGroups;
	static vector<vector<MPointArray>> edgesPoints;
	static MIntArray mergeVertexIndicesMap;
	static void  prepairEdgeMove();
	static void  repairEdgePoints(SGMesh* pMesh, vector<MPointArray>& edgePoints, const MIntArray& edgeGroup, int rootIndex, double dotValue);
	static void  edgeMove_slide();
	static void  edgeMove_end(bool clearSelection = false);

	static void clearSplitPoint();
	static void pushSplitPoint();
	static void editSplitPoint();
	static void splitEdge();

	static void deleteComponent();

	static void setSelection();
	static void addSelection();
	static void ifNewSetSelection();
	static void addDbClickSelection();
	static void clearSelection( bool excuteCommand = true );
	static void selectionGrow();
	static void selectionReduce();

	static double softSelectionRadiusOrig;
	static void prepairSoftSelection();
	static void editSoftSelection();
	static void setSoftSelection();
	static void toggleSoftSelection();

	static double moveBrushRadiusOrig;
	static void updateMoveBrushCenter();
	static void prepairMoveBrushRadius();
	static void editMoveBrushRadius();

	static void editSplitRingPoint();
	static void polySplitRing();

	static void setCamFocus();

	static MStringArray bevelNodes;
	static void bevelEdge();
	static void bevelEdgeFinish();

	static void dragSelectionPress();
	static void dragSelectionDrag();
	static void dragSelectionRelease( bool shift=false, bool ctrl= false);
};