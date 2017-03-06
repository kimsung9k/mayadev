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

	unsigned int getAttribLocation(const char* str);
	unsigned int getUniformLocation(const char* str);

	unsigned int m_vsid;
	unsigned int m_fsid;
	unsigned int m_prid;

	static const char* defaultVS_code;
	static const char* defaultFS_code;
};