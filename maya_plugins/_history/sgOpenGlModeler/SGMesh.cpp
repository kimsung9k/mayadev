#include "SGBase.h"
#include "SGMesh.h"
#include "SGFunctions.h"

SGMesh::SGMesh() {
	m_numPoints = 0;
	m_numEdges = 0;
	m_numPolys = 0;
	glGenBuffers(1, &buffer );
}


SGMesh::~SGMesh() {
	glDeleteBuffers(1, &buffer);
}


void SGMesh::setBufferData() {
	glBindBuffer(GL_ARRAY_BUFFER, buffer);
	glBufferData(GL_ARRAY_BUFFER, sizeof(float)*3*m_numPoints * 2, m_points.getPointer(), GL_STATIC_DRAW);
	glBufferSubData(GL_ARRAY_BUFFER, sizeof(float) * 3 * m_numPoints, sizeof(float) * 3 * m_numPoints, m_normals.getPointer());
}

void SGMesh::locationBind( unsigned int posLoc, unsigned  int colorLoc ) {
	this->posLoc = posLoc;
	this->normalLoc = colorLoc;
}

void SGMesh::uniformBind(unsigned int projectionMatrix, unsigned int objectMatrix, unsigned int camPos, unsigned int camVector) {
	this->projectionMatrix = projectionMatrix;
	this->objectMatrix = objectMatrix;
	this->camPosition = camPos;
	this->camVector = camVector;
}


void SGMesh::draw( SGCam* cam ) {
	glBindBuffer(GL_ARRAY_BUFFER, buffer);

	glUniform3fv(this->camPosition, 1, cam->getCamPosition());
	glUniform3fv(this->camVector, 1, cam->getCamVector());
	glUniformMatrix4fv(this->projectionMatrix, 1, GL_FALSE, cam->getProjectionMatrix() );
	glVertexAttribPointer(posLoc, 3, GL_FLOAT, GL_FALSE, 0, 0);
	glVertexAttribPointer(normalLoc, 3, GL_FLOAT, GL_FALSE, 0, (char*)(sizeof(float)* 3 * m_numPoints));

	glEnableVertexAttribArray(posLoc);
	glEnableVertexAttribArray(normalLoc);
	
	for (int i = 0; i < m_pointIdsPerPolys.size(); i++) {
		glDrawElements(GL_POLYGON, m_pointIdsPerPolys[i].length(), GL_UNSIGNED_INT, m_pointIdsPerPolys[i].getPointer());
	}

	glDisableVertexAttribArray(posLoc);
	glDisableVertexAttribArray(normalLoc);

	glBindBuffer(GL_ARRAY_BUFFER, 0);
}


void SGMesh::setFromDagPath() {
	MFnMesh fnMesh = m_dagPath;
	MPointArray points;
	fnMesh.getPoints(points);

	m_numPoints = fnMesh.numVertices();
	m_numEdges = fnMesh.numEdges();
	m_numPolys = fnMesh.numPolygons();

	m_points.setLength(m_numPoints);
	m_normals.setLength(m_numPoints);

	MVector normal;
	for (int i = 0; i < m_numPoints; i++) {
		m_points.set(i, SGVec3((float)points[i].x, (float)points[i].y, (float)points[i].z));
		fnMesh.getVertexNormal(i, normal);
		m_normals.set(i, SGVec3((float)normal.x, (float)normal.y, (float)normal.z));
	}

	MIntArray vtxCount, vtxList;
	fnMesh.getVertices(vtxCount, vtxList);

	m_pointIdsPerPolys.resize(m_numPolys); // vtxCount.length() == m_numPolys

	int startIndex = 0;
	for (int i = 0; i < (int)vtxCount.length(); i++) {
		int count = vtxCount[i];
		m_pointIdsPerPolys[i].setLength(count);
		for (int j = 0; j < count; j++) {
			m_pointIdsPerPolys[i][j] = vtxList[startIndex + j];
		}
		startIndex += count;
	}
}