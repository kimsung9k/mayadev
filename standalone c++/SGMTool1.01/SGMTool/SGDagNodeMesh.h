#pragma once
#include <vector>
#include "SGIntArray.h"
#include "SGVectorArray.h"
#include "SGVector.h"
#include <glm/glm.hpp>


using namespace std;


struct vector3d
{
	double x, y, z;
};


struct vector2d
{
	double u, v;
};

struct SGVertexBuffer
{
	float x, y, z;
	float nx, ny, nz;
	float u, v;
};


class SGDagNodeMeshBuffer
{
public:
	SGDagNodeMeshBuffer();
	~SGDagNodeMeshBuffer();

	int m_numTriangles;
	int m_numQuads;
	int m_numOverQuads;
	int m_sizeOverQuads;
	SGIntArray m_countArrayOverQuad;

	SGVertexBuffer* m_bufferTriangles;
	SGVertexBuffer* m_bufferQuads;
	SGVertexBuffer* m_bufferOverQuads;

	SGIntArray*    m_vertexToBufferMap;
};


class SGDagNodeMesh
{
public:
	SGDagNodeMesh();
	~SGDagNodeMesh();

	SGDagNodeMesh& operator=( const SGDagNodeMesh&);
	void updateBoundingBox();
	void updateBoundingBox(int vertexIndex);

	void setDatasComopnentRelationship();
	void setVertexNormals();
	void setVertexNormal(int vertexIndex);
	void setPolygonNormals();
	void setPolygonNormal(int polygonIndex);
	SGVector getPolygonVertexNormal(int polygonIndex, int vertexindex);
	unsigned int m_objectIndex;
	glm::mat4x4 getMatrix();

	void setBuffer();

	double m_matrix[16];

	int  m_numVertices;
	int  m_numNormals;
	int  m_numPolygons;
	int  m_numUVs;
	int  m_numIdArrayVertices;

	string            m_name;
	vector<vector3d>  m_points;
	vector<vector3d>  m_normals;
	vector<vector3d>  m_normalsPerPoints;
	vector<vector3d>  m_normalsPerPolygons;
	vector<vector2d>* m_uvArrays;
	vector<int>       m_numUVArrays;
	vector<int>       m_countArrayVertices;
	vector<int>       m_idArrayVertices;

	vector<SGIntArray> m_vertexToPolygonsMap;
	vector<SGIntArray> m_polygonToVerticesMap;

	SGVector m_boundingBoxMin;
	SGVector m_boundingBoxMax;

	SGDagNodeMeshBuffer* m_buffer;
};