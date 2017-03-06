#include "SGGLBuffer.h"
#include "SGViewControl.h"
#include "SGFile.h"
#include <glm/glm.hpp>

GLuint  programID;
GLuint  vertexShaderID;
GLuint  fragmentShaderID;


extern SGViewControl ViewControl;
extern const char* vertexShaderCode;
extern const char* fragmentShaderCode;


SGGLBuffer::SGGLBuffer()
{
	m_ptrMesh.resize(0);
	m_ptrBufferMeshVertex = new GLuint[0];
	m_ptrBufferMeshVertexArrays = new GLuint[0];
	m_ptrBufferMeshIndices = new GLuint[0];
	m_numMeshs = 0;
}



SGGLBuffer::~SGGLBuffer()
{
	for (int i = 0; i < m_numMeshs; i++)
	{
		glDeleteBuffers(1, &m_ptrBufferMeshVertex[i]);
		glDeleteVertexArrays(1, &m_ptrBufferMeshVertexArrays[i]);
		glDeleteBuffers(1, &m_ptrBufferMeshIndices[i]);
	}
	m_ptrMesh.clear();
	delete[] m_ptrBufferMeshVertex;
	delete[] m_ptrBufferMeshVertexArrays;
	delete[] m_ptrBufferMeshIndices;
}


bool checkShaderStatus( GLuint shaderID )
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


void SGGLBuffer::installShader()
{
	vertexShaderID = glCreateShader(GL_VERTEX_SHADER);
	fragmentShaderID = glCreateShader(GL_FRAGMENT_SHADER);

	const GLchar* adapter[1];
	adapter[0] = (GLchar*)vertexShaderCode;
	glShaderSource(vertexShaderID, 1, adapter, 0);
	adapter[0] = (GLchar*)fragmentShaderCode;
	glShaderSource(fragmentShaderID, 1, adapter, 0);

	glCompileShader(vertexShaderID);
	checkShaderStatus(vertexShaderID);
	glCompileShader(fragmentShaderID);
	checkShaderStatus(fragmentShaderID);

	programID = glCreateProgram();
	glAttachShader(programID, vertexShaderID);
	glAttachShader(programID, fragmentShaderID);

	glLinkProgram(programID);
	glUseProgram(programID);
}



void SGGLBuffer::rebuildBuffer( int index )
{
	glDeleteBuffers(1, &m_ptrBufferMeshVertex[index]);
	glDeleteVertexArrays(1, &m_ptrBufferMeshVertexArrays[index]);
	glDeleteBuffers(1, &m_ptrBufferMeshIndices[index]);

	glGenBuffers(1, &m_ptrBufferMeshVertex[index]);
	glGenVertexArrays(1, &m_ptrBufferMeshVertexArrays[index]);
	glGenBuffers(1, &m_ptrBufferMeshIndices[index]);

	glBindBuffer(GL_ARRAY_BUFFER, m_ptrBufferMeshVertex[index]);
	glBindVertexArray(m_ptrBufferMeshVertexArrays[index]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(double)*m_ptrMesh[index]->m_numVertices * 6, m_ptrMesh[index]->m_pointAttributes, GL_DYNAMIC_DRAW);
	glEnableVertexAttribArray(0);
	glVertexAttribPointer(0, 3, GL_DOUBLE, GL_FALSE, sizeof(double) * 6, 0);
	glEnableVertexAttribArray(1);
	glVertexAttribPointer(1, 3, GL_DOUBLE, GL_FALSE, sizeof(double) * 6, (char*)(sizeof(double) * 3));

	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, m_ptrBufferMeshIndices[index]);
	int lenIndices = m_ptrMesh[index]->m_numTriangles*3 + m_ptrMesh[index]->m_numQuads*4;
	for (int k = 0; k < m_ptrMesh[index]->m_numOverQuads; k++)
		lenIndices += m_ptrMesh[index]->m_idArrayOverQuads[k].length();
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(int)*lenIndices, 0, GL_DYNAMIC_DRAW);
	glBufferSubData(GL_ELEMENT_ARRAY_BUFFER, 0, sizeof(int)*m_ptrMesh[index]->m_numTriangles*3, m_ptrMesh[index]->m_idArrayTriangles );
	glBufferSubData(GL_ELEMENT_ARRAY_BUFFER, sizeof(int)*m_ptrMesh[index]->m_numTriangles * 3, sizeof(int)*m_ptrMesh[index]->m_numQuads * 4, m_ptrMesh[index]->m_idArrayQuads );
		
	int currentOffset = sizeof(int)*(m_ptrMesh[index]->m_numTriangles*3+ m_ptrMesh[index]->m_numQuads*4);
	for (int k = 0; k < m_ptrMesh[index]->m_numOverQuads; k++)
	{
		glBufferSubData(GL_ELEMENT_ARRAY_BUFFER, currentOffset, sizeof(int)*m_ptrMesh[index]->m_idArrayOverQuads[k].length(), m_ptrMesh[index]->m_idArrayOverQuads[k].asIntPtr() );
		currentOffset += sizeof(int)*m_ptrMesh[index]->m_idArrayOverQuads[k].length();
	}
}


void SGGLBuffer::deleteBuffer(int index)
{
	vector<SGDagNodeMesh*> new_ptrMesh;
	GLuint* new_ptrBufferMeshVertex = new GLuint[m_numMeshs - 1];
	GLuint* new_ptrBufferMeshVertexArrays = new GLuint[m_numMeshs - 1];
	GLuint* new_ptrBufferMeshIndices = new GLuint[m_numMeshs - 1];

	for (int i = 0; i < m_numMeshs-1; i++)
	{
		if (i == index) {
			i--; continue;
		}
		new_ptrMesh[i] = m_ptrMesh[i];
		new_ptrBufferMeshVertex[i] = m_ptrBufferMeshVertex[i];
		new_ptrBufferMeshVertexArrays[i] = m_ptrBufferMeshVertexArrays[i];
		new_ptrBufferMeshIndices[i] = m_ptrBufferMeshIndices[i];
	}

	glDeleteBuffers(1, &m_ptrBufferMeshVertex[index]);
	glDeleteVertexArrays(1, &m_ptrBufferMeshVertexArrays[index]);
	glDeleteBuffers(1, &m_ptrBufferMeshIndices[index]);

	m_ptrMesh.clear();
	delete[] m_ptrBufferMeshVertex;
	delete[] m_ptrBufferMeshVertexArrays;
	delete[] m_ptrBufferMeshIndices;

	m_ptrMesh = new_ptrMesh;
	m_ptrBufferMeshVertex = new_ptrBufferMeshVertex;
	m_ptrBufferMeshVertexArrays = new_ptrBufferMeshVertexArrays;
	m_ptrBufferMeshIndices = new_ptrBufferMeshIndices;

	m_numMeshs -= 1;
}


void SGGLBuffer::drawIndex(int index)
{
	glBindVertexArray(m_ptrBufferMeshVertexArrays[index]);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, m_ptrBufferMeshIndices[index]);

	glDrawElements(GL_TRIANGLES, m_ptrMesh[index]->m_numTriangles*3, GL_UNSIGNED_INT, 0);
	int currentOffset = sizeof(int) * m_ptrMesh[index]->m_numTriangles * 3;
	glDrawElements(GL_QUADS, m_ptrMesh[index]->m_numQuads * 4, GL_UNSIGNED_INT, (void*)currentOffset);
	
	currentOffset += sizeof(int)*m_ptrMesh[index]->m_numQuads * 4;
	for (int k = 0; k <m_ptrMesh[index]->m_numOverQuads; k++)
	{
		glDrawElements(GL_POLYGON, m_ptrMesh[index]->m_idArrayOverQuads[k].length(), GL_UNSIGNED_INT, (void*)currentOffset );
		currentOffset += sizeof(int)*m_ptrMesh[index]->m_idArrayOverQuads[k].length();
	}
}


void SGGLBuffer::drawAll()
{
	GLuint idUf_camPosition = glGetUniformLocation(programID, "camPosition");
	glm::vec3   camPosition = ViewControl.getCamPosition();
	glUniform3fv(idUf_camPosition, 1, &camPosition[0]);

	GLuint idUf_worldToViewMatrix, idUf_viewToWorldMatrix, idUf_objectMatrix;
	glm::mat4x4 worldToViewMatrix = ViewControl.getWorldToViewMatrix();
	glm::mat4x4 viewToWorldMatrix = glm::inverse(worldToViewMatrix);

	idUf_worldToViewMatrix = glGetUniformLocation(programID, "worldToViewMatrix");
	glUniformMatrix4fv(idUf_worldToViewMatrix, 1, GL_FALSE, &worldToViewMatrix[0][0]);
	idUf_viewToWorldMatrix = glGetUniformLocation(programID, "viewToWorldMatrix");
	glUniformMatrix4fv(idUf_viewToWorldMatrix, 1, GL_FALSE, &viewToWorldMatrix[0][0]);

	glm::mat4x4 objectMatrix;
	for (int i = 0; i < m_numMeshs; i++)
	{
		objectMatrix = m_ptrMesh[i]->getMatrix();
		idUf_objectMatrix = glGetUniformLocation(programID, "objectMatrix");
		glUniformMatrix4fv(idUf_objectMatrix, 1, GL_FALSE, &objectMatrix[0][0]);
		drawIndex(i);
	}
}


void SGGLBuffer::appendMesh( SGDagNodeMesh* dataMesh )
{
	vector<SGDagNodeMesh*> new_ptrMesh;
	new_ptrMesh.resize(m_numMeshs + 1);
	GLuint* new_ptrBufferMeshVertex = new GLuint[m_numMeshs + 1];
	GLuint* new_ptrBufferMeshVertexArrays = new GLuint[m_numMeshs + 1];
	GLuint* new_ptrBufferMeshIndices = new GLuint[m_numMeshs + 1];

	for (int i = 0; i < m_numMeshs; i++)
	{
		new_ptrMesh[i] = m_ptrMesh[i];
		new_ptrBufferMeshVertex[i] = m_ptrBufferMeshVertex[i];
		new_ptrBufferMeshVertexArrays[i] = m_ptrBufferMeshVertexArrays[i];
		new_ptrBufferMeshIndices[i] = m_ptrBufferMeshIndices[i];
	}

	m_ptrMesh.clear();
	delete[] m_ptrBufferMeshVertex;
	delete[] m_ptrBufferMeshVertexArrays;
	delete[] m_ptrBufferMeshIndices;

	new_ptrMesh[m_numMeshs] = dataMesh;

	m_ptrMesh = new_ptrMesh;
	m_ptrBufferMeshVertex = new_ptrBufferMeshVertex;
	m_ptrBufferMeshVertexArrays = new_ptrBufferMeshVertexArrays;
	m_ptrBufferMeshIndices = new_ptrBufferMeshIndices;
	
	glGenBuffers(1, &m_ptrBufferMeshVertex[m_numMeshs]);
	glGenVertexArrays(1, &m_ptrBufferMeshVertexArrays[m_numMeshs]);
	glGenBuffers(1, &m_ptrBufferMeshIndices[m_numMeshs]);
	
	m_numMeshs += 1;
}