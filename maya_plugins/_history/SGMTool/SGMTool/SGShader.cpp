#include "SGShader.h"



bool SGShader::checkShaderStatus(GLuint shaderID)
{
	GLint compileStatus[10];
	for (int i = 0; i < 10; i++) compileStatus[i] = -1;
	glGetShaderiv(shaderID, GL_COMPILE_STATUS, compileStatus);
	bool returnValue = true;
	for (int i = 0; i < 10; i++)
	{
		if (compileStatus[i] == -1) continue;
		if (compileStatus[i] != GL_TRUE)
		{
			GLint infoLogLength;
			glGetShaderiv(shaderID, GL_INFO_LOG_LENGTH, &infoLogLength);
			GLchar* buffer = new GLchar[infoLogLength];

			GLsizei bufferSize;
			glGetShaderInfoLog(shaderID, infoLogLength, &bufferSize, buffer);
			printf("%s\n", buffer);
			returnValue = false;
		}
	}
	return returnValue;
}



SGShader::SGShader()
{
	m_typeName = "shader";

	m_vs = glCreateShader(GL_VERTEX_SHADER);
	m_fs = glCreateShader(GL_FRAGMENT_SHADER);
	m_pr = glCreateProgram();
}


SGShader::~SGShader()
{
	glDeleteShader(m_vs);
	glDeleteShader(m_fs);
	glDeleteProgram(m_pr);
}




void SGShader::createDefaultShader()
{
	string stringVS = SGFile::readStringFromFile("defaultVertexShader.txt");
	string stringFS = SGFile::readStringFromFile("defaultFragmentShader.txt");

	const GLchar* adapter[1];
	adapter[0] = (GLchar*)stringVS.c_str();
	glShaderSource(m_vs, 1, adapter, 0);
	adapter[0] = (GLchar*)stringFS.c_str();
	glShaderSource(m_fs, 1, adapter, 0);

	glCompileShader(m_vs);
	checkShaderStatus(m_vs);
	glCompileShader(m_fs);
	checkShaderStatus(m_fs);

	glAttachShader(m_pr, m_vs);
	glAttachShader(m_pr, m_fs);
	glLinkProgram(m_pr);
	glUseProgram(m_pr);
}