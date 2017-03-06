#include "SGDagNodeMesh.h"
#include <stdio.h>


SGDagNodeMeshBuffer::SGDagNodeMeshBuffer()
{
	m_numTriangles = 0;
	m_numQuads = 0;
	m_numOverQuads = 0;

	m_bufferTriangles = new SGVertexBuffer[0];
	m_bufferQuads = new SGVertexBuffer[0];
	m_bufferOverQuads = new SGVertexBuffer[0];
	m_vertexToBufferMap = new SGIntArray[0];
}



SGDagNodeMeshBuffer::~SGDagNodeMeshBuffer()
{
	delete[] m_bufferTriangles;
	delete[] m_bufferQuads;
	delete[] m_bufferOverQuads;
	delete[] m_vertexToBufferMap;
}



SGDagNodeMesh::SGDagNodeMesh() 
{
	for (int i = 0; i < 16; i++)
		m_matrix[i] = i % 5==0?1.0:0.0;

	m_numVertices = 0;
	m_numNormals = 0;
	m_numPolygons = 0;
	m_numUVs = 0;
	m_numIdArrayVertices = 0;

	m_points.resize(0);
	m_normals.resize(0);
	m_normalsPerPoints.resize(0);
	m_normalsPerPolygons.resize(0);
	m_uvArrays = new vector<vector2d>[0];
	m_numUVArrays.resize(0);
	m_countArrayVertices.resize(0);
	m_idArrayVertices.resize(0);

	m_vertexToPolygonsMap.resize(0);
	m_polygonToVerticesMap.resize(0);

	m_buffer = new SGDagNodeMeshBuffer;
}



SGDagNodeMesh::~SGDagNodeMesh()
{
	delete[] m_uvArrays;
	delete m_buffer;
}



void SGDagNodeMesh::updateBoundingBox()
{
	m_boundingBoxMin.x = 100000000.0;
	m_boundingBoxMin.y = 100000000.0;
	m_boundingBoxMin.z = 100000000.0;
	m_boundingBoxMax.x = -100000000.0;
	m_boundingBoxMax.y = -100000000.0;
	m_boundingBoxMax.z = -100000000.0;

	for (int i = 0; i < m_numVertices; i++)
	{
		if (m_boundingBoxMin.x > m_points[i].x)
			m_boundingBoxMin.x = m_points[i].x;
		if (m_boundingBoxMin.y > m_points[i].y)
			m_boundingBoxMin.y = m_points[i].y;
		if (m_boundingBoxMin.z > m_points[i].z)
			m_boundingBoxMin.z = m_points[i].z;

		if (m_boundingBoxMax.x < m_points[i].x)
			m_boundingBoxMax.x = m_points[i].x;
		if (m_boundingBoxMax.y < m_points[i].y)
			m_boundingBoxMax.y = m_points[i].y;
		if (m_boundingBoxMax.z < m_points[i].z)
			m_boundingBoxMax.z = m_points[i].z;
	}
}



void SGDagNodeMesh::updateBoundingBox(int index)
{
	if (m_boundingBoxMin.x > m_points[index].x)
		m_boundingBoxMin.x = m_points[index].x;
	if (m_boundingBoxMin.y > m_points[index].y)
		m_boundingBoxMin.y = m_points[index].y;
	if (m_boundingBoxMin.z > m_points[index].z)
		m_boundingBoxMin.z = m_points[index].z;

	if (m_boundingBoxMax.x < m_points[index].x)
		m_boundingBoxMax.x = m_points[index].x;
	if (m_boundingBoxMax.y < m_points[index].y)
		m_boundingBoxMax.y = m_points[index].y;
	if (m_boundingBoxMax.z < m_points[index].z)
		m_boundingBoxMax.z = m_points[index].z;
}



SGDagNodeMesh& SGDagNodeMesh::operator=(const SGDagNodeMesh& other)
{
	delete[] m_uvArrays;
	delete   m_buffer;


	this->m_numVertices = other.m_numVertices;
	this->m_numPolygons = other.m_numPolygons;
	this->m_numUVs = other.m_numUVs;
	this->m_numIdArrayVertices = other.m_numIdArrayVertices;

	m_points.resize(m_numVertices);
	m_normalsPerPoints.resize(m_numVertices);
	m_uvArrays = new vector<vector2d>[m_numUVs];
	m_numUVArrays.resize(m_numUVs);
	m_countArrayVertices.resize(m_numPolygons);
	m_idArrayVertices.resize(m_numIdArrayVertices);

	m_vertexToPolygonsMap.resize(m_numVertices);
	m_polygonToVerticesMap.resize(m_numPolygons);


	for (int i = 0; i < 16; i++)
		this->m_matrix[i] = other.m_matrix[i];

	for (int i = 0; i < m_numVertices; i++)
		this->m_points[i] = other.m_points[i];

	for (int i = 0; i < m_numVertices; i++)
		this->m_normalsPerPoints[i] = other.m_normalsPerPoints[i];

	for (int i = 0; i < m_numUVs; i++)
	{
		this->m_uvArrays[i].resize( other.m_numUVArrays[i] );
		for (int j = 0; j < other.m_numUVArrays[i]; j++)
			this->m_uvArrays[i][j] = other.m_uvArrays[i][j];
	}

	for (int i = 0; i < m_numUVs; i++ )
		this->m_numUVArrays[i] = other.m_numUVArrays[i];

	for (int i = 0; i < m_numPolygons; i++)
		this->m_countArrayVertices[i] = other.m_countArrayVertices[i];

	for (int i = 0; i < m_numIdArrayVertices; i++)
		this->m_idArrayVertices[i] = other.m_idArrayVertices[i];

	for (int i = 0; i < m_numVertices; i++)
		this->m_vertexToPolygonsMap[i] = other.m_vertexToPolygonsMap[i];

	for (int i = 0; i < m_numPolygons; i++)
		this->m_polygonToVerticesMap[i] = other.m_polygonToVerticesMap[i];

	m_boundingBoxMin = other.m_boundingBoxMin;
	m_boundingBoxMax = other.m_boundingBoxMax;

	setBuffer();

	return *this;
}



void SGDagNodeMesh::setDatasComopnentRelationship()
{
	m_vertexToPolygonsMap.resize(m_numVertices);
	m_polygonToVerticesMap.resize(m_numPolygons);

	for (int i = 0; i < m_numVertices; i++)
		m_vertexToPolygonsMap[i].clear();

	int idArrayVerticesPointer = 0;
	int targetVerticeIndex;
	for (int i = 0; i < m_numPolygons; i++)
	{
		m_polygonToVerticesMap[i].setLength(m_countArrayVertices[i]);
		for (int j = 0; j < m_countArrayVertices[i]; j++)
		{
			targetVerticeIndex = m_idArrayVertices[idArrayVerticesPointer + j];
			m_polygonToVerticesMap[i][j] = targetVerticeIndex;
			m_vertexToPolygonsMap[targetVerticeIndex].append(i);
		}
		idArrayVerticesPointer += m_countArrayVertices[i];
	}
}



void SGDagNodeMesh::setPolygonNormals()
{
	m_normalsPerPoints.resize(m_numVertices);

	for (int i = 0; i < m_numPolygons; i++)
		setPolygonNormal(i);
}



void SGDagNodeMesh::setPolygonNormal( int polygonIndex )
{
	SGIntArray indicesVertices = m_polygonToVerticesMap[polygonIndex];

	int indexVertex;
	for ( unsigned int i = 0; i < indicesVertices.length(); i++)
	{
		indexVertex = indicesVertices[i];
		vector3d& normals = m_normalsPerPoints[i];
		SGIntArray& indicesPolygon = m_vertexToPolygonsMap[indexVertex];
	}
}




SGVector SGDagNodeMesh::getPolygonVertexNormal(int polygonIndex, int vertexindex)
{
	SGIntArray& indicesVertex = m_polygonToVerticesMap[polygonIndex];
	int arrLength = indicesVertex.length();

	vector3d p1, p2, p3;
	SGVector v1, v2, normal;
	for (int i = 0; i < arrLength; i++)
	{
		if (indicesVertex[i] != vertexindex) continue;
		
		p1 = m_points[indicesVertex[(i + arrLength - 1) % arrLength]];
		p2 = m_points[i];
		p3 = m_points[indicesVertex[(i + arrLength + 1) % arrLength]];

		v1.x = p2.x - p1.x; v1.y = p2.y - p1.y; v1.z = p2.z - p1.z;
		v2.x = p3.x - p2.x; v2.y = p3.y - p2.y; v2.z = p3.z - p2.z;

		normal = v1^v2;
		normal.normalize();
		break;
	}
	return normal;
}




void SGDagNodeMesh::setVertexNormals()
{
	m_normalsPerPoints.resize(m_numVertices);

	for (int i = 0; i < m_numVertices; i++)
		setVertexNormal(i);
}




void SGDagNodeMesh::setVertexNormal(int vertexIndex)
{
	SGIntArray& vertexToPolygonIndices = m_vertexToPolygonsMap[vertexIndex];

	int polygonIndex;
	int vtxIndexFirst;
	int vtxIndexSecond;
	int vtxIndexThird;
	SGVector normalSum(0, 0, 0);

	for (unsigned int i = 0; i < vertexToPolygonIndices.length(); i++)
	{
		polygonIndex = vertexToPolygonIndices[i];
		SGIntArray& vertexIndices = m_polygonToVerticesMap[polygonIndex];
		for (unsigned int j = 0; j < vertexIndices.length(); j++)
		{
			if (vertexIndex != vertexIndices[j]) continue;

			vtxIndexFirst = vertexIndices[(j + vertexIndices.length() - 1) % vertexIndices.length()];
			vtxIndexSecond = vertexIndices[j];
			vtxIndexThird = vertexIndices[(j + vertexIndices.length() + 1) % vertexIndices.length()];

			SGVector p1(m_points[vtxIndexFirst].x, m_points[vtxIndexFirst].y, m_points[vtxIndexFirst].z);
			SGVector p2(m_points[vtxIndexSecond].x, m_points[vtxIndexSecond].y, m_points[vtxIndexSecond].z);
			SGVector p3(m_points[vtxIndexThird].x, m_points[vtxIndexThird].y, m_points[vtxIndexThird].z);

			SGVector v1 = p2 - p1;
			SGVector v2 = p3 - p2;
			SGVector normal = v1^v2;

			if(!normal.length()) continue;
			normalSum += normal;
			break;
		}
	}
	normalSum.normalize();
	if (normalSum.x != normalSum.x)
	{
		m_normalsPerPoints[vertexIndex] = m_normalsPerPoints[vertexIndex - 1];
	}
	else
	{
		m_normalsPerPoints[vertexIndex].x = normalSum.x;
		m_normalsPerPoints[vertexIndex].y = normalSum.y;
		m_normalsPerPoints[vertexIndex].z = normalSum.z;
	}
}




glm::mat4x4 SGDagNodeMesh::getMatrix()
{
	glm::mat4x4 mat;
	for (int i = 0; i < 16; i++)
		mat[i / 4][i % 4] = (float)m_matrix[i];
	return mat;
}




void SGDagNodeMesh::setBuffer()
{
	int countVtx;

	delete[] m_buffer->m_bufferTriangles;
	delete[] m_buffer->m_bufferQuads;
	delete[] m_buffer->m_bufferOverQuads;
	delete[] m_buffer->m_vertexToBufferMap;

	m_buffer->m_numTriangles = 0;
	m_buffer->m_numQuads = 0;
	m_buffer->m_numOverQuads = 0;

	m_buffer->m_sizeOverQuads = 0;

	for (int i = 0; i < m_numPolygons; i++)
	{
		countVtx = m_countArrayVertices[i];
		if (countVtx == 3)
			m_buffer->m_numTriangles++;
		else if (countVtx == 4)
			m_buffer->m_numQuads++;
		else
		{
			m_buffer->m_numOverQuads++;
			m_buffer->m_sizeOverQuads += countVtx;
		}
	}

	m_buffer->m_countArrayOverQuad.setLength(m_buffer->m_numOverQuads);

	m_buffer->m_bufferTriangles = new SGVertexBuffer[m_buffer->m_numTriangles * 3];
	m_buffer->m_bufferQuads = new SGVertexBuffer[m_buffer->m_numQuads * 4];
	m_buffer->m_bufferOverQuads = new SGVertexBuffer[m_buffer->m_sizeOverQuads];
	m_buffer->m_vertexToBufferMap = new SGIntArray[m_numVertices];

	int triangleIndex = 0;
	int quadIndex = 0;
	int overQuadIndex = 0;

	int idArrayOverQuadIndex = 0;

	for (int i = 0; i < m_numPolygons; i++)
	{
		countVtx = m_countArrayVertices[i];
		SGIntArray& vtxIds = m_polygonToVerticesMap[i];
		if (countVtx == 3)
		{
			for (int j = 0; j < countVtx; j++)
			{
				vector3d& cuPoint = m_points[vtxIds[j]];
				vector3d& cuNormal = m_normalsPerPoints[vtxIds[j]];
				m_buffer->m_bufferTriangles[triangleIndex].x = (float)cuPoint.x;
				m_buffer->m_bufferTriangles[triangleIndex].y= (float)cuPoint.y;
				m_buffer->m_bufferTriangles[triangleIndex].z= (float)cuPoint.z;
				m_buffer->m_bufferTriangles[triangleIndex].nx= (float)cuNormal.x;
				m_buffer->m_bufferTriangles[triangleIndex].ny= (float)cuNormal.y;
				m_buffer->m_bufferTriangles[triangleIndex].nz= (float)cuNormal.z;
				triangleIndex++;
			}
		}
		else if (countVtx == 4)
		{
			for (int j = 0; j < countVtx; j++)
			{
				vector3d& cuPoint = m_points[vtxIds[j]];
				vector3d& cuNormal = m_normalsPerPoints[vtxIds[j]];
				m_buffer->m_bufferQuads[quadIndex].x= (float)cuPoint.x;
				m_buffer->m_bufferQuads[quadIndex].y= (float)cuPoint.y;
				m_buffer->m_bufferQuads[quadIndex].z= (float)cuPoint.z;
				m_buffer->m_bufferQuads[quadIndex].nx= (float)cuNormal.x;
				m_buffer->m_bufferQuads[quadIndex].ny= (float)cuNormal.y;
				m_buffer->m_bufferQuads[quadIndex].nz= (float)cuNormal.z;
				quadIndex++;
			}
		}
		else
		{
			m_buffer->m_countArrayOverQuad[idArrayOverQuadIndex] = countVtx;
			for (int j = 0; j < countVtx; j++)
			{
				vector3d& cuPoint = m_points[vtxIds[j]];
				vector3d& cuNormal = m_normalsPerPoints[vtxIds[j]];
				m_buffer->m_bufferOverQuads[overQuadIndex].x= (float)cuPoint.x;
				m_buffer->m_bufferOverQuads[overQuadIndex].y= (float)cuPoint.y;
				m_buffer->m_bufferOverQuads[overQuadIndex].z= (float)cuPoint.z;
				m_buffer->m_bufferOverQuads[overQuadIndex].nx= (float)cuNormal.x;
				m_buffer->m_bufferOverQuads[overQuadIndex].ny= (float)cuNormal.y;
				m_buffer->m_bufferOverQuads[overQuadIndex].nz= (float)cuNormal.z;
				overQuadIndex++;
			}
			idArrayOverQuadIndex += 1;
		}
	}
}