#pragma once

#include <GL/glew.h>
#include "SGDagNodeMesh.h"
#include <vector>
#include "SGCam.h"


using namespace std;

class SGDagNodeContrainer
{
public:
	SGDagNodeContrainer();
	~SGDagNodeContrainer();

	void clear();
	unsigned int  numMesh() const;
	void append( SGDagNodeMesh* element);
	void remove(int index);
	SGDagNodeMesh* getMeshElementPtr(unsigned int index);

	void updateBuffer(int index);
	void installShader();
	void drawIndex(int index);
	void drawAll();
	
	unsigned int m_numMeshs;
	vector<SGDagNodeMesh*> m_ptrMesh;
	vector<GLuint> m_ptrIDBufferTQ;
	vector<GLuint> m_ptrIDBufferOQ;
	vector<GLuint> m_ptrIDBufferTQVtxArr;
	vector<GLuint> m_ptrIDBufferOQVtxArr;

	glm::mat4x4 matCamInvMatrix;
};