#include "SGMesh.h"
#include "SGPrintf\SGPrintf.h"
#include "SGFunctions.h"

SGMesh::SGMesh() {
}


SGMesh::~SGMesh() {
}


void SGMesh::setFromDagPath() {
	MFnMesh fnMesh = m_dagPath;

	MPointArray points;
	fnMesh.getPoints(points);

	m_numPoints = fnMesh.numVertices();
	m_numEdges = fnMesh.numEdges();
	m_numPolys = fnMesh.numPolygons();

	m_points.setLength(m_numPoints);
	m_normals.setLength(m_numPoints);

	MVector normal;
	for (int i = 0; i < m_numPoints; i++) {
		m_points.set(i, SGVec3((float)points[i].x, (float)points[i].y, (float)points[i].z));
		fnMesh.getVertexNormal(i, normal);
		m_normals.set(i, SGVec3((float)normal.x, (float)normal.y, (float)normal.z));
	}

	MIntArray vtxCount, vtxList;
	fnMesh.getVertices(vtxCount, vtxList);

	m_pointIdsPerPolys.resize(m_numPolys); // vtxCount.length() == m_numPolys

	int startIndex = 0;
	for (int i = 0; i < (int)vtxCount.length(); i++) {
		int count = vtxCount[i];
		m_pointIdsPerPolys[i].setLength(count);
		for (int j = 0; j < count; j++) {
			m_pointIdsPerPolys[i][j] = vtxList[startIndex + j];
		}
		startIndex += count;
	}
}