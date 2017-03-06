#include "SGDagNodeContrainer.h"
#include "SGViewControl.h"
#include "stdio.h"


GLuint  programID;
GLuint  vertexShaderID;
GLuint  fragmentShaderID;


extern SGViewControl ViewControl;
extern const char* vertexShaderCode;
extern const char* fragmentShaderCode;


SGDagNodeContrainer::SGDagNodeContrainer()
{
	m_ptrMesh.resize(0);
	m_ptrIDBufferTQ.resize(0);
	m_ptrIDBufferOQ.resize(0);
	m_ptrIDBufferTQVtxArr.resize(0);
	m_ptrIDBufferOQVtxArr.resize(0);
	m_numMeshs = 0;
}


SGDagNodeContrainer::~SGDagNodeContrainer()
{
	for ( unsigned int i = 0; i < m_numMeshs; i++)
		delete m_ptrMesh[i];
}


unsigned int SGDagNodeContrainer::numMesh() const
{
	return m_numMeshs;
}


void SGDagNodeContrainer::append( SGDagNodeMesh* element)
{
	m_ptrMesh.push_back(element);

	GLuint id;
	m_ptrIDBufferTQ.push_back(id);
	m_ptrIDBufferOQ.push_back(id);
	m_ptrIDBufferTQVtxArr.push_back(id);
	m_ptrIDBufferOQVtxArr.push_back(id);

	glGenBuffers(1, &m_ptrIDBufferTQ[m_numMeshs]);
	glGenBuffers(1, &m_ptrIDBufferOQ[m_numMeshs]);
	glGenVertexArrays(1, &m_ptrIDBufferTQVtxArr[m_numMeshs]);
	glGenVertexArrays(1, &m_ptrIDBufferOQVtxArr[m_numMeshs]);

	m_numMeshs += 1;
}



SGDagNodeMesh* SGDagNodeContrainer::getMeshElementPtr(unsigned int index)
{
	return (m_ptrMesh[index]);
}


void SGDagNodeContrainer::clear()
{
	for ( unsigned int i = 0; i < m_numMeshs; i++)
	{
		delete m_ptrMesh[i];
	}

	m_ptrMesh.resize(0);
	m_numMeshs = 0;
}


void SGDagNodeContrainer::remove(int index)
{
	delete m_ptrMesh[index];

	int cuIndex = 0;
	for (unsigned int i = index; i < m_numMeshs -1; i++)
	{
		m_ptrMesh[i] = m_ptrMesh[i + 1];
	}
	m_ptrMesh.pop_back();

	m_numMeshs -= 1;
}


bool checkShaderStatus(GLuint shaderID)
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



void SGDagNodeContrainer::updateBuffer(int index)
{
	SGDagNodeMesh& targetMesh = *m_ptrMesh[index];
	SGDagNodeMeshBuffer& targetBuffer = *targetMesh.m_buffer;
	int vtxBufferSize = sizeof(SGVertexBuffer);

	glDeleteBuffers(1, &m_ptrIDBufferTQ[index]);
	glDeleteBuffers(1, &m_ptrIDBufferOQ[index]);
	glDeleteVertexArrays(1, &m_ptrIDBufferTQVtxArr[index]);
	glDeleteVertexArrays(1, &m_ptrIDBufferOQVtxArr[index]);

	glGenBuffers(1, &m_ptrIDBufferTQ[index]);
	glGenBuffers(1, &m_ptrIDBufferOQ[index]);
	glGenVertexArrays(1, &m_ptrIDBufferTQVtxArr[index]);
	glGenVertexArrays(1, &m_ptrIDBufferOQVtxArr[index]);

	glBindBuffer(GL_ARRAY_BUFFER, m_ptrIDBufferTQ[index]);
	glBufferData(GL_ARRAY_BUFFER, (targetBuffer.m_numTriangles * 3 + targetBuffer.m_numQuads * 4)* vtxBufferSize, 0, GL_STATIC_DRAW);
	glBufferSubData(GL_ARRAY_BUFFER, 0, targetBuffer.m_numTriangles * 3 * vtxBufferSize, targetBuffer.m_bufferTriangles);
	glBufferSubData(GL_ARRAY_BUFFER, targetBuffer.m_numTriangles * 3 * vtxBufferSize, targetBuffer.m_numQuads * 4 * vtxBufferSize, targetBuffer.m_bufferQuads);
	glBindVertexArray(m_ptrIDBufferTQVtxArr[index]);
	glEnableVertexAttribArray(0);
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vtxBufferSize, 0);
	glEnableVertexAttribArray(1);
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, vtxBufferSize, (void*)(sizeof(float) * 3));

	glBindBuffer(GL_ARRAY_BUFFER, m_ptrIDBufferOQ[index]);
	glBufferData(GL_ARRAY_BUFFER, targetBuffer.m_sizeOverQuads * vtxBufferSize, targetBuffer.m_bufferOverQuads, GL_STATIC_DRAW);
	glBindVertexArray(m_ptrIDBufferOQVtxArr[index]);
	glEnableVertexAttribArray(0);
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vtxBufferSize, 0);
	glEnableVertexAttribArray(1);
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, vtxBufferSize, (void*)(sizeof(float) * 3));
}



void SGDagNodeContrainer::installShader()
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


void SGDagNodeContrainer::drawIndex(int index)
{
	SGDagNodeMesh& targetMesh = *m_ptrMesh[index];
	SGDagNodeMeshBuffer& targetBuffer = *targetMesh.m_buffer;
	int vtxBufferSize = sizeof(SGVertexBuffer);

	glBindVertexArray(m_ptrIDBufferTQVtxArr[index]);
	glDrawArrays(GL_TRIANGLES, 0, targetBuffer.m_numTriangles * 3);
	glDrawArrays(GL_QUADS, targetBuffer.m_numTriangles * 3, targetBuffer.m_numQuads * 4);
	
	glBindVertexArray(m_ptrIDBufferOQVtxArr[index]);
	int currentOffset = 0;
	for (int k = 0; k <targetBuffer.m_numOverQuads; k++)
	{
		glDrawArrays(GL_POLYGON, currentOffset, targetBuffer.m_countArrayOverQuad[k]);
		currentOffset += targetBuffer.m_countArrayOverQuad[k];
	}
}


void SGDagNodeContrainer::drawAll()
{
	GLuint idUf_camPosition = glGetUniformLocation(programID, "camPosition");
	glm::vec3   camPosition = ViewControl.getCamPosition();
	glUniform3fv(idUf_camPosition, 1, &camPosition[0]);
	GLuint idUf_camVector = glGetUniformLocation(programID, "camVector");
	glm::vec3   camVector = ViewControl.getCamVector();
	glUniform3fv(idUf_camVector, 1, &camVector[0]);

	GLuint idUf_worldToViewMatrix, idUf_viewToWorldMatrix, idUf_objectMatrix;
	glm::mat4x4 worldToViewMatrix = ViewControl.getWorldToViewMatrix();
	glm::mat4x4 viewToWorldMatrix = glm::inverse(worldToViewMatrix);

	idUf_worldToViewMatrix = glGetUniformLocation(programID, "worldToViewMatrix");
	glUniformMatrix4fv(idUf_worldToViewMatrix, 1, GL_FALSE, &worldToViewMatrix[0][0]);
	idUf_viewToWorldMatrix = glGetUniformLocation(programID, "viewToWorldMatrix");
	glUniformMatrix4fv(idUf_viewToWorldMatrix, 1, GL_FALSE, &viewToWorldMatrix[0][0]);

	glm::mat4x4 objectMatrix;
	for ( unsigned int i = 0; i < m_numMeshs; i++)
	{
		objectMatrix = m_ptrMesh[i]->getMatrix();
		idUf_objectMatrix = glGetUniformLocation(programID, "objectMatrix");
		glUniformMatrix4fv(idUf_objectMatrix, 1, GL_FALSE, &objectMatrix[0][0]);
		drawIndex(i);
	}
}