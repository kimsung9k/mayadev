#pragma once

#include <QT/qvector3d.h>
#include <QT/qmatrix4x4.h>
#include <maya/MDagPath.h>

class SGCam
{
public:
	SGCam();
	~SGCam();

	void getCamera( MDagPath dagPath );
	void updateCamera();
	float* getProjectionMatrix();
	float* getCamPosition();
	float* getCamVector();

	MDagPath m_dagPath;

	float m_pMatrix[4][4];
	float m_position[3];
	float m_vector[3];
	float m_width;
	float m_height;
};