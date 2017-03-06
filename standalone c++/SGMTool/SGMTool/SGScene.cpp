#include "SGScene.h"

SGShaderStruct     SGScene::defaultShader;
SGDagNodeContainer SGScene::dagNodeContainer;
SGShaderContainer  SGScene::shaderContainer;

extern const char* defaultVertexShaderCode;
extern const char* defaultFragmentShaderCode;

bool SGScene::checkShaderStatus(GLuint shaderID)
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


void SGScene::createBase()
{
	defaultShader.m_VSID = glCreateShader(GL_VERTEX_SHADER);
	defaultShader.m_FSID = glCreateShader(GL_FRAGMENT_SHADER);
	defaultShader.m_programId = glCreateProgram();

	defaultShader.m_VSID = glCreateShader(GL_VERTEX_SHADER);
	defaultShader.m_FSID = glCreateShader(GL_FRAGMENT_SHADER);

	const GLchar* adapter[1];
	adapter[0] = (GLchar*)defaultVertexShaderCode;
	glShaderSource(defaultShader.m_VSID, 1, adapter, 0);
	adapter[0] = (GLchar*)defaultFragmentShaderCode;
	glShaderSource(defaultShader.m_FSID, 1, adapter, 0);

	glCompileShader(defaultShader.m_VSID);
	checkShaderStatus(defaultShader.m_VSID);
	glCompileShader(defaultShader.m_FSID);
	checkShaderStatus(defaultShader.m_FSID);

	defaultShader.m_programId = glCreateProgram();
	glAttachShader(defaultShader.m_programId, defaultShader.m_VSID);
	glAttachShader(defaultShader.m_programId, defaultShader.m_FSID);
	glLinkProgram(defaultShader.m_programId);
	glUseProgram(defaultShader.m_programId);

	SGScene::shaderContainer.append(&SGScene::defaultShader);
}


void SGScene::newScene()
{
	dagNodeContainer.clear();
	shaderContainer.clear();
}