#pragma once

#include "SGIntArray.h"
#include "SGVectorArray.h"


class SGFnPolygon
{
public:
	SGFnPolygon();
	~SGFnPolygon();

	void create( int numVertices, int numPolygons, float* points,
		int* vertexCounts, int* vertexIds);

	void updateToScreen();

private:
	int           m_numVertices;
	int           m_numPolygons;
	float*        m_points;
	int*          m_vertexCounts;
	int*          m_vertexIds;
};