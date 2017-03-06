#pragma once

#include "SGVec3Array.h"
#include "SGIntArray.h"
#include <vector>
#include <maya/MDagPath.h>
#include "SGCam.h"

using std::vector;

class SGMesh
{
public:
	SGMesh();
	~SGMesh();

	int m_numPoints;
	int m_numEdges;
	int m_numPolys;

	SGVec3Array m_points;
	SGVec3Array m_normals;
	vector<SGIntArray> m_pointIdsPerPolys;

	void setBufferData();
	void locationBind(unsigned int posLoc, unsigned int colorLoc );
	void uniformBind(unsigned int projectionMatrix, unsigned int objectMatrix, unsigned int camPos, unsigned int camVector);
	void draw(SGCam* cam);

	unsigned int posLoc, normalLoc;
	unsigned int projectionMatrix, objectMatrix, camPosition, camVector;

	unsigned int buffer;

	vector<vector<int>> m_pointToPolysMap;
	vector<vector<int>> m_pointToEdgesMap;
	vector<vector<int>> m_pointToPointsMap;
	vector<vector<int>> m_edgeToPointsMap;
	vector<vector<int>> m_edgeToPolysMap;
	vector<vector<int>> m_polysToPointsMap;
	vector<vector<int>> m_polysToEdgesMap;

	MDagPath m_dagPath;
	void setFromDagPath();
};