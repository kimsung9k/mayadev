#include "SGFnPolygon.h"



SGFnPolygon::SGFnPolygon()
{
	
}



SGFnPolygon::~SGFnPolygon()
{

}



void SGFnPolygon::create(int numVertices, int numPolygons,
	float* points, int* vertexCounts, int* vertexIds)
{
	m_numVertices  = numVertices;
	m_numPolygons  = numPolygons;
	for (int i = 0; i < m_numVertices*3; i++ )
		m_points[i] = points[i];
	m_vertexCounts = vertexCounts;
	m_vertexIds    = vertexIds;
}