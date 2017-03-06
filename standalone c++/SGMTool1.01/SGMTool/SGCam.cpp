#include "SGCam.h"
#include <math.h>

SGCam::SGCam() :
	m_SGMatrix(SGMatrix()), m_SGMatrixInv(SGMatrix()), m_dDistCamPivot(5.0)
{
	m_dNearClip = 0.1;
	m_dFarClip  = 10000.0;
	m_fAngleOfView = 50.0f;
}


void SGCam::moveToHome() {
	m_SGMatrix[0] = 0.707107;
	m_SGMatrix[1] = 0.000000;
	m_SGMatrix[2] = -0.707107;
	m_SGMatrix[3] = 0.000000;
	m_SGMatrix[4] = -0.331295;
	m_SGMatrix[5] = 0.883452;
	m_SGMatrix[6] = -0.331295;
	m_SGMatrix[7] = 0.000000;
	m_SGMatrix[8] = 0.624695;
	m_SGMatrix[9] = 0.468521;
	m_SGMatrix[10] = 0.624695;
	m_SGMatrix[11] = 0.000000;
	m_SGMatrix[12] = 28.000000;
	m_SGMatrix[13] = 21.000000;
	m_SGMatrix[14] = 28.000000;
	m_SGMatrix[15] = 1.000000;

	m_dDistCamPivot = pow( pow(m_SGMatrix[12], 2) + pow(m_SGMatrix[13], 2) + pow(m_SGMatrix[14], 2), 0.5 );
	m_SGMatrixInv = m_SGMatrix.inverseMatrix();
}

void SGCam::getCamMatrix(SGMatrix& mtx) {
	for (int i = 0; i < 16; i++)
		mtx[i] = m_SGMatrix[i];
}


void SGCam::getCamMatrix(float* fptMtx) {
	for (int i = 0; i < 16; i++)
		fptMtx[i] = (float)m_SGMatrix[i];
}


void SGCam::getCamMatrix(double* fptMtx) {
	for (int i = 0; i < 16; i++)
		fptMtx[i] = m_SGMatrix[i];
}


void SGCam::getCamInverseMatrix(float* fptMtx) {
	for (int i = 0; i < 16; i++)
		fptMtx[i] = (float)m_SGMatrixInv[i];
}

void SGCam::getCamInverseMatrix(double* fptMtx) {
	for (int i = 0; i < 16; i++)
		fptMtx[i] = m_SGMatrixInv[i];
}


void SGCam::getCamInverseMatrix(glm::mat4x4& invMtx)
{
	for (int i = 0; i < 16; i++)
		invMtx[i/4][i%4] = (float)m_SGMatrixInv[i];
}


void SGCam::getTranslate(double* fptTranslate) {
	fptTranslate[0] = m_SGMatrix[12];
	fptTranslate[1] = m_SGMatrix[13];
	fptTranslate[2] = m_SGMatrix[14];
}


void SGCam::setCamMatrix(const SGMatrix& mtx)
{
	m_SGMatrix = mtx;
	m_SGMatrixInv = m_SGMatrix.inverseMatrix();
}

void SGCam::setDistFocus(double distFocus)
{
	m_dDistCamPivot = distFocus;
}


double SGCam::nearClip() {
	return m_dNearClip;
}


double SGCam::farClip() {
	return m_dFarClip;
}


double SGCam::distFocus() {
	return m_dDistCamPivot;
}


float SGCam::angleOfView() {
	return m_fAngleOfView;
}



void SGCam::setFocalLength(int windowHeight)
{
	double half_height = windowHeight/2.0;
	float  half_aov = m_fAngleOfView / 2.0f;

	m_focalLength = 1.0 / tan(half_aov) * half_height;
}


double SGCam::focalLength()
{
	return m_focalLength;
}