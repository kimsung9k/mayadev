#include "SGShaderContainer.h"

SGShaderContainer::SGShaderContainer()
{
	m_ptrShaders.resize(0);
	m_numShader = 0;
}

SGShaderContainer::~SGShaderContainer()
{
}



void SGShaderContainer::clear()
{
	for (int i = 1; i < m_numShader; i++)
	{
		glDeleteShader(m_ptrShaders[i]->m_VSID);
		glDeleteShader(m_ptrShaders[i]->m_FSID);
		glDeleteProgram(m_ptrShaders[i]->m_programId);
		delete m_ptrShaders[i];
	}
	m_ptrShaders.resize(1);
}


void SGShaderContainer::append( SGShaderStruct* ptrShader )
{
	m_ptrShaders.push_back(ptrShader);
	m_numShader++;
}

unsigned int SGShaderContainer::length()
{
	return m_numShader;
}


SGShaderStruct* SGShaderContainer::operator[](int index)
{
	return m_ptrShaders[index];
}