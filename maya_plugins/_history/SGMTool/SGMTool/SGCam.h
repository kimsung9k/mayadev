#pragma once
#include "SGMatrix.h"
#include "SGVector.h"
#include <glm/glm.hpp>


class SGCam
{
public:
	SGCam();
	
	void moveToHome();

	void getCamMatrix(SGMatrix& mtx);
	void getCamMatrix(float* fptMtx);
	void getCamMatrix(double* fptMtx);
	void getCamInverseMatrix(float* fptMtx);
	void getCamInverseMatrix(double* fptMtx);
	void getCamInverseMatrix(glm::mat4x4& invMtx );
	void getTranslate(double* fptTranslate);

	void setCamMatrix( const SGMatrix& mtx);
	void setDistFocus(double distFocus);
	void setFocalLength(int windowHeight);

	double nearClip();
	double farClip();
	double distFocus();
	float  angleOfView();
	double focalLength();

private:
	double    m_focalLength;
	float     m_fAngleOfView;
	double    m_dDistCamPivot;
	SGMatrix  m_SGMatrix;
	SGMatrix  m_SGMatrixInv;

	double    m_dNearClip;
	double    m_dFarClip;
};