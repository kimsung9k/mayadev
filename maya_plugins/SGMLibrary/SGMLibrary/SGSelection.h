#pragma once

#include "SGBase.h"
#include <maya/MDagPath.h>
#include <maya/MIntArray.h>
#include <maya/MFloatArray.h>
#include "SGComponentType.h"
#include "SGIntersectResult.h"
#include "SGMesh.h"


class SGSelection
{
public:
	SGSelection();
	SGSelection(const SGMesh* pMesh);
	~SGSelection();

	void initialize(const SGMesh* pMesh);

	const SGMesh* pMesh;
	vector<SGComponentType> m_beforeType;
	vector<int>  m_beforeIndex;
	vector<SGComponentType> m_focusType;
	vector<int>  m_focusIndex;
	vector<SGComponentType> m_type;
	vector<int> m_index;

	void updateFocusInfo( const vector<SGIntersectResult>& intersectResults );

	MIntArray getSelVtxIndices();
	MIntArray getSelEdgeIndices();
	MIntArray getSelPolyIndices();

	MIntArray getSelVtxIndicesMap();
	MIntArray getSelEdgeIndicesMap();
	MIntArray getSelPolyIndicesMap();

	MIntArray getSelIndicesMap( SGComponentType compType );

	void select( const vector<SGIntersectResult>& intersectResults, int type = 0); // 0 : set, 1 : add, 2 : cross;
	void addDBClickSelection( const vector<SGIntersectResult>& intersectResults); // 0 : set, 1 : add, 2 : cross;
	void dragSelection(const vector<SGIntersectResult>& intersectResults,const MPointArray& mousePoints, const MMatrix& camMatrix, const SGSymmetry& symInfo, int type = 0 ); // 0 : set, 1 : add, 2 : remove, 3 : cross;
	void clearSelection();

	MFloatArray getVertexWeights();
	
	SGComponentType getBeforeType(int index);
	int getBeforeIndex(int index);

	MPoint getComponentCenter( SGComponentType compType, int index );
	MPoint getFocusCenter();
	MPoint getBeforeCenter();
	MPoint getSelectionCenter( const SGSymmetry& symInfo);

	bool selExists();
	bool selIsChanged(const MIntArray& map1, const MIntArray& map2);
	bool growSelection();
	bool reduceSelection();

	static vector<MIntArray> getEdgeLoopGroupByIndicesMap( const MIntArray& indicesMap);
	static MIntArray getMap(const MIntArray& indices, int maxLength, int defaultIndex = 0, int setIndex = 1);
	static void setMap( MIntArray& map, const MIntArray& indices, int setIndex = 1);
	static MIntArray getIndices(const MIntArray& map, int defaultIndex = 0);
	static MIntArray combineIndices(MIntArray indices1, MIntArray indices2, int maxNum );
	static SGSelection sels;

	
};