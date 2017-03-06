#pragma once

#include "SGVec3.h"
#include "SGIntArray.h"
#include <vector>
using std::vector;

class SGShaderProgram
{
public:
	SGShaderProgram::SGShaderProgram();

	void setVS(const char* shaderCode);
	void setFS(const char* shaderCode);
	void setDefaultShader();
	void link();
	void use();

	unsigned int getAttribPointer(const char* str );
	void getBuffer();
	//void bindArrayBuffer();
	void bindVertexArray( float* ptrPoint, float* ptrNormal );
	void bindIndexBuffer(vector<SGIntArray> indexArr);

private:
	//unsigned int m_vtxBufferId;
	unsigned int m_vtxArrId;
	unsigned int m_indexBufferId;
	unsigned int m_vsid;
	unsigned int m_fsid;
	unsigned int m_prid;

	static const char* defaultVS_code;
	static const char* defaultFS_code;
};