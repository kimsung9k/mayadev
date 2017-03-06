#pragma once

#include "SGVec3Array.h"
#include "SGIntArray.h"
#include <vector>
#include <maya/MDagPath.h>

#include "SGShaderProgram.h"

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

	vector<vector<int>> m_pointToPolysMap;
	vector<vector<int>> m_pointToEdgesMap;
	vector<vector<int>> m_pointToPointsMap;
	vector<vector<int>> m_edgeToPointsMap;
	vector<vector<int>> m_edgeToPolysMap;
	vector<vector<int>> m_polysToPointsMap;
	vector<vector<int>> m_polysToEdgesMap;

	SGShaderProgram* m_program;

	MDagPath m_dagPath;
	void setFromDagPath();
};