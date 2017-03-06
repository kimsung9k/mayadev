#pragma once


#include <GL/glew.h>
#include <vector>

using namespace std;


struct SGShaderStruct
{
	GLuint m_programId;
	GLuint m_VSID;
	GLuint m_FSID;
	char   name[128];
};




class SGShaderContainer
{
public:
	SGShaderContainer();
	~SGShaderContainer();

	void clear();
	void append(SGShaderStruct* ptrShader);
	unsigned int length();
	SGShaderStruct* operator[](int index);

private:
	vector<SGShaderStruct*> m_ptrShaders;
	unsigned int m_numShader;
};