#pragma once

#include "SGDefault.h"
#include "SGNode.h"
#include "SGShader.h"
#include "SGFile.h"
#include <GL/glew.h>


class SGShader : public SGNode
{
public:
	SGShader();
	virtual ~SGShader();

	bool checkShaderStatus(GLuint shaderID);
	void createDefaultShader();

	GLuint m_pr;
	GLuint m_vs;
	GLuint m_fs;
};