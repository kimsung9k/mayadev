#include "SGShaderProgram.h"
#include "SGBase.h"



bool checkShaderStatus(unsigned int shaderID)
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
			char* buffer = new char[infoLogLength];

			GLsizei bufferSize;
			glGetShaderInfoLog(shaderID, infoLogLength, &bufferSize, buffer);
			OutputDebugString(buffer);
			returnValue = false;
		}
	}
	return returnValue;
}

SGShaderProgram::SGShaderProgram() {
	m_vsid = glCreateShader(GL_VERTEX_SHADER);
	m_fsid = glCreateShader(GL_FRAGMENT_SHADER);
	m_prid = glCreateProgram();
}


void SGShaderProgram::setDefaultShader() {
	setVS(defaultVS_code);
	setFS(defaultFS_code);
}


void SGShaderProgram::setVS(const char* shaderCode) {
	const char* adapter[1];
	adapter[0] = (char*)shaderCode;
	glShaderSource(m_vsid, 1, adapter, 0);
	glCompileShader(m_vsid);
	checkShaderStatus(m_vsid);
}


void SGShaderProgram::setFS(const char* shaderCode) {
	const char* adapter[1];
	adapter[0] = (char*)shaderCode;
	glShaderSource(m_fsid, 1, adapter, 0);
	glCompileShader(m_fsid);
	checkShaderStatus(m_fsid);
}

void SGShaderProgram::link() {
	glAttachShader(m_prid, m_vsid);
	glAttachShader(m_prid, m_fsid);
	glLinkProgram(m_prid);
	glDetachShader(m_prid, m_vsid);
	glDetachShader(m_prid, m_fsid);
	glDeleteShader(m_vsid);
	glDeleteShader(m_fsid);
}

void SGShaderProgram::use(){
	glUseProgram(m_prid);
}

unsigned int SGShaderProgram::getAttribLocation(const char* str) {
	return glGetAttribLocation(m_prid, str);
}

unsigned int SGShaderProgram::getUniformLocation(const char* str) {
	return glGetUniformLocation(m_prid, str);
}