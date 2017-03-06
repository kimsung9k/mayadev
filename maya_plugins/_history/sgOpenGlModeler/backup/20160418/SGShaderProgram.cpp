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
	//glGenBuffers(1, &m_vtxBufferId);
	glGenVertexArrays(1, &m_vtxArrId);
	glGenBuffers(1, &m_indexBufferId);
}


void SGShaderProgram::setDefaultShader() {
	setVS(defaultVS_code);
	setFS(defaultFS_code);
}


void SGShaderProgram::getBuffer() {
	//glDeleteBuffers(1, &m_vtxBufferId);
	glDeleteVertexArrays(1, &m_vtxArrId);
	glDeleteBuffers(1, &m_indexBufferId);
	//glGenBuffers(1, &m_vtxBufferId);
	glGenVertexArrays(1, &m_vtxArrId);
	glGenBuffers(1, &m_indexBufferId);
}

/*
void SGShaderProgram::bindArrayBuffer() {
	glBindBuffer(GL_ARRAY_BUFFER, m_vtxBufferId);
}
*/

void SGShaderProgram::bindVertexArray( float* ptrPoint, float* ptrNormal ) {
	glBindVertexArray(m_vtxArrId);
	GLuint position = getAttribPointer("position");
	GLuint normal   = getAttribPointer("normal");
	glEnableVertexAttribArray(position);
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sizeof(float) * 3, ptrPoint );
	glEnableVertexAttribArray(normal);
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sizeof(float) * 3, ptrNormal );
}


void SGShaderProgram::bindIndexBuffer( vector<SGIntArray> indexArr ){
	GLuint allIndexLength = 0;

	for (int i = 0; i < indexArr.size(); i++) {
		allIndexLength += indexArr[i].length();
	}

	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,m_indexBufferId);
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, allIndexLength, 0, GL_STATIC_DRAW);

	allIndexLength = 0;
	int indexLength = 0;
	for (int i = 0; i < indexArr.size(); i++) {
		indexLength = indexArr[i].length();
		glBufferSubData(GL_ELEMENT_ARRAY_BUFFER, allIndexLength, indexLength, indexArr[i].getPointer());
		allIndexLength += indexLength;
	}
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
}

void SGShaderProgram::use() {
	glUseProgram(m_prid);
}

unsigned int SGShaderProgram::getAttribPointer(const char* str ) {
	glBindVertexArray(m_vtxArrId);
	GLuint location = glGetAttribLocation(m_prid, str);
	return location;
}