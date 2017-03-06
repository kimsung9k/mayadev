#include "SGBufferMesh.h"


SGBufferMesh::SGBufferMesh()
{
	numTriangleVtxs = 0;
	numQuadsVtxs = 0;
	eachNumOverQuads.clear();
	numOverQuadsVtxs = 0;

	m_mapVtxToBuffers.clear();
	m_buffer = new SGBufferVtx[0];

	glGenBuffers(1, &m_IdBuffer);
	glGenVertexArrays(1, &m_IdBufferVtxArr);
}



SGBufferMesh::~SGBufferMesh()
{
	glDeleteBuffers(1, &m_IdBuffer);
	glDeleteVertexArrays(1, &m_IdBufferVtxArr);

	delete[] m_buffer;
}


void SGBufferMesh::update()
{
	int vtxBufferSize = sizeof(SGBufferVtx);
	glBindBuffer(GL_ARRAY_BUFFER, m_IdBuffer);
	glBufferData(GL_ARRAY_BUFFER, (numTriangleVtxs + numQuadsVtxs + numOverQuadsVtxs)* vtxBufferSize, m_buffer, GL_STATIC_DRAW);
	glBindVertexArray(m_IdBufferVtxArr);
	glEnableVertexAttribArray(0);
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vtxBufferSize, 0);
	glEnableVertexAttribArray(1);
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, vtxBufferSize, (void*)(sizeof(float) * 3));
}


void SGBufferMesh::draw()
{
	glBindVertexArray(m_IdBufferVtxArr);
	glDrawArrays(GL_TRIANGLES, 0, numTriangleVtxs);
	glDrawArrays(GL_QUADS, numTriangleVtxs, numQuadsVtxs);

	int currentOffset = 0;
	for (int k = 0; k <eachNumOverQuads.size(); k++)
	{
		glDrawArrays(GL_POLYGON, currentOffset, eachNumOverQuads[k] );
		currentOffset += eachNumOverQuads[k];
	}
}