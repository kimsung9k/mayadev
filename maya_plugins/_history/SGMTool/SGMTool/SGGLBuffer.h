#pragma once

#include <GL/glew.h>
#include "SGDagNodeMesh.h"
#include <vector>
#include "SGCam.h"


using namespace std;

class SGGLBuffer
{
public:
	SGGLBuffer();
	~SGGLBuffer();

	void installShader();

	void rebuildBuffer( int index );
	void deleteBuffer(int index);
	void appendMesh(SGDagNodeMesh* meshData);

	void drawIndex(int index);
	void drawAll();

	int m_numMeshs;

	vector<SGDagNodeMesh*> m_ptrMesh;
	GLuint* m_ptrBufferMeshVertex;
	GLuint* m_ptrBufferMeshVertexArrays;
	GLuint* m_ptrBufferMeshIndices;

	bool*   m_bVertexNormalBufferExists;
	GLuint* m_ptrBufferMeshVertexNormal;
	GLuint* m_ptrBufferMeshVertexNormalArrays;

	glm::mat4x4 matCamInvMatrix;
};