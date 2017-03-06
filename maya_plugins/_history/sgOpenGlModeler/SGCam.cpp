#include "SGCam.h"
#include <maya/MFnCamera.h>
#include <maya/MMatrix.h>
#include <maya/MFloatMatrix.h>
#include "SGPrintf\SGPrintf.h"
#include <maya/MPlug.h>

SGCam::SGCam() {

}

SGCam::~SGCam() {

}


void SGCam::getCamera(MDagPath dagPath) {
	m_dagPath = dagPath;
}


void SGCam::updateCamera() {
	MFnCamera cam(m_dagPath);
}


float* SGCam::getCamPosition() {
	MMatrix mtx = m_dagPath.inclusiveMatrix();
	m_position[0] = mtx(3,0);
	m_position[1] = mtx(3,1);
	m_position[2] = mtx(3,2);
	return m_position;
}

float* SGCam::getCamVector() {
	MMatrix mtx = m_dagPath.inclusiveMatrix();
	m_vector[0] = -mtx(2,0);
	m_vector[1] = -mtx(2,1);
	m_vector[2] = -mtx(2,2);
	return m_vector;
}


float* SGCam::getProjectionMatrix() {
	float aspect = m_width / m_height;
	sgPrintf("aspect : %f", aspect);
	MFnCamera cam = m_dagPath;
	
	MMatrix mtx = m_dagPath.inclusiveMatrix();
	QVector3D tr( -mtx(3,0), -mtx(3,1), -mtx(3,2));
	QVector3D dir(-mtx(2, 0), -mtx(2, 1), -mtx(2, 2));
	dir.normalize();
	dir *= cam.findPlug("centerOfInterest").asFloat();

	float focalLength = cam.findPlug("focalLength").asFloat();
	float hfa = cam.findPlug("horizontalFilmAperture").asFloat()*25.4 / 2;

	QMatrix4x4 mat4;

	float degToRad = 3.14159 / 180.0;
	float radToDeg = 180 / 3.14159;

	float waov = 54.43 / 2;
	float h = tan(waov*degToRad);
	float haov = atan(h / 2)*radToDeg;

	float aov = atan(hfa / aspect / focalLength) / 3.14159 * 180 * 2;
	mat4.perspective(aov, aspect, 0.1, 100000);
	mat4.lookAt(QVector3D(0, 0, 0), dir, QVector3D(0, 1, 0));
	mat4.translate(tr);

	qreal* data = mat4.data();
	float* fdata = *m_pMatrix;
	for (int i = 0; i < 16; i++){
		fdata[i] = data[i];
	}
	/*
	for (int i = 0; i < 4; i++) {
		sgPrintf("%f %f %f %f", fdata[i*4+0], fdata[i * 4 + 1], fdata[i * 4 + 2], fdata[i * 4 + 3]);
	}
	sgPrintf("");/**/
	return *m_pMatrix;
}