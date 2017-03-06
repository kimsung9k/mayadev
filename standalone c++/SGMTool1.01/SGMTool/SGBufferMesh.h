#pragma once


#include "SGDefault.h"
#include "SGVector2f.h"
#include "SGVector3f.h"
#include <GL/glew.h>


struct SGBufferVtx
{
	SGVector3f pos;
	SGVector3f nor;
	SGVector2f uv;
};


struct SGBufferMesh
{
	SGBufferMesh::SGBufferMesh();
	SGBufferMesh::~SGBufferMesh();

	void update();
	void draw();

	int numTriangleVtxs;
	int numQuadsVtxs;
	vector<int> eachNumOverQuads;
	int numOverQuadsVtxs;

	vector<int> trianglePolyIds;
	vector<int> quadPolyIds;
	vector<int> overQuadPolyIds;

	vector<vector<int>> m_mapVtxToBuffers;
	SGBufferVtx* m_buffer;

	GLuint m_IdBuffer;
	GLuint m_IdBufferVtxArr;
};