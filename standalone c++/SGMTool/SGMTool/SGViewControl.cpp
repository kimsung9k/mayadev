#include "SGViewControl.h"
#include "SGCam.h"
#include <math.h>
#include <stdio.h>


SGCam        g_camCurrent;
SGCam*       g_camList;
unsigned int g_indexCuCam;
unsigned int g_numCam;



SGViewControl::SGViewControl()
{
	m_bLButtonDown = false;
	m_bRButtonDown = false;
	m_bMButtonDown = false;
}



void SGViewControl::initializeCamera()
{
	g_camList = new SGCam[1];
	g_numCam = 1;
	g_indexCuCam = 0;
	g_camCurrent = g_camList[g_indexCuCam];
	g_camCurrent.moveToHome();
}


void SGViewControl::SetLButtonDown(bool value)
{
	m_bLButtonDown = value;
}

void SGViewControl::SetRButtonDown(bool value)
{
	m_bRButtonDown = value;
}

void SGViewControl::SetMButtonDown(bool value)
{
	m_bMButtonDown = value;
}


void SGViewControl::GetWindowWidthHeight(int& width, int& height) {
	width = m_windowWidth;
	height = m_windowHeight;
}


void SGViewControl::SetWindowWidthHeight(int width, int height) {
	m_windowWidth = width;
	m_windowHeight = height;
}


void SGViewControl::SetPMouseClient(int px, int py) {
	m_mousePx = px < 32768 ? px : px -65535;
	m_mousePy = py < 32768 ? m_windowHeight - py : m_windowHeight - py + 65535;
	//outputString("mousePos : %04d,   %04d", m_mousePx, m_mousePy);
}


MOUSE_EVT_RESULT SGViewControl::mouseEventControl() {
	static bool lButtonMode = false;
	static bool rButtonMode = false;
	static bool mButtonMode = false;
	static int  mousePx_standard;
	static int  mousePy_standard;

	if (!rButtonMode && !mButtonMode)
	{
		if (m_bLButtonDown && lButtonMode == false) {
			setView_standard(m_mousePx, m_mousePy);
			lButtonMode = true;
		}
		if (m_bLButtonDown) {
			setView_rotate(m_windowWidth, m_mousePx, m_mousePy );
			return MOUSE_EVT_UPDATE;
		}
		else{
			lButtonMode = false;
		}
	}

	if (!lButtonMode && !mButtonMode)
	{
		if (m_bRButtonDown && rButtonMode == false) {
			setView_standard(m_mousePx, m_mousePy);
			rButtonMode = true;
		}
		if (m_bRButtonDown) {
			setView_zoomInOut(m_windowWidth, m_mousePx );
			return MOUSE_EVT_UPDATE;
		}
		else{
			rButtonMode = false;
		}
	}

	if (!lButtonMode && !rButtonMode )
	{
		if (m_bMButtonDown && mButtonMode == false ) {
			setView_standard(m_mousePx, m_mousePy);
			mButtonMode = true;
		}
		if (m_bMButtonDown || m_bLButtonDown ) {
			setView_traverse(m_windowWidth, m_mousePx, m_mousePy );
			return MOUSE_EVT_UPDATE;
		}
		else{
			mButtonMode = false;
		}
	}
	
	return MOUSE_EVT_NOUPDATE;
}



void SGViewControl::setView_standard(int x, int y)
{
	m_mouseX_std = x;
	m_mouseY_std = y;
	g_camCurrent.getCamMatrix(m_mtxCam_std);
	m_dCam_distFocus_std = g_camCurrent.distFocus();
}



glm::mat4x4 SGViewControl::getCamMatrixInverse() {
	glm::mat4x4 matrix;
	g_camCurrent.getCamInverseMatrix(matrix);
	return matrix;
}


glm::mat4x4 SGViewControl::getPerspViewMatrix() {
	GLfloat aspect;
	float half_waov;
	float haov;

	aspect = (GLfloat)m_windowWidth / m_windowHeight;
	half_waov = (GLfloat)getAngleOfView() / 180.0f*SG_PI / 2.0f;
	haov = atan(tan(half_waov) / aspect) *2.0f;

	return glm::perspective(haov, aspect, (GLfloat)getCamNearClip(), (GLfloat)getCamFarClip());
}


glm::mat4x4 SGViewControl::getWorldToViewMatrix()
{
	return getPerspViewMatrix() * getCamMatrixInverse();
}


glm::vec3 SGViewControl::getCamPosition()
{
	double camPos[3];
	g_camCurrent.getTranslate(camPos);
	glm::vec3 vec3Pos;
	vec3Pos.x= (float)camPos[0];
	vec3Pos.y= (float)camPos[1];
	vec3Pos.z= (float)camPos[2];
	return vec3Pos;
}


glm::vec3 SGViewControl::getCamVector()
{
	double camMatrix[16];
	g_camCurrent.getCamMatrix(camMatrix);
	glm::vec3 vec3Vector;
	vec3Vector.x= (float)camMatrix[12];
	vec3Vector.y= (float)camMatrix[13];
	vec3Vector.z= (float)camMatrix[14];
	return vec3Vector;
}


float  SGViewControl::getAngleOfView() {
	return g_camCurrent.angleOfView();
}

float  SGViewControl::getCamNearClip() {
	return (float)g_camCurrent.nearClip();
}

float  SGViewControl::getCamFarClip() {
	return (float)g_camCurrent.farClip();
}


void  SGViewControl::setView_rotate(int winWidth, int x, int y)
{
	float dragValueWidth = (float)(x - m_mouseX_std) / winWidth;
	float dragValueHeight = (float)(y - m_mouseY_std) / winWidth;

	SGVector sgvCamZ = -SGVector(m_mtxCam_std[8], m_mtxCam_std[9], m_mtxCam_std[10]).normal() * m_dCam_distFocus_std;

	SGVector point(m_mtxCam_std[12], m_mtxCam_std[13], m_mtxCam_std[14]);
	SGVector pivot = point + sgvCamZ;

	SGMatrix defaultMatrix;
	defaultMatrix[12] = pivot.x;
	defaultMatrix[13] = pivot.y;
	defaultMatrix[14] = pivot.z;
	SGMatrix defaultMatrixInverse = defaultMatrix.inverseMatrix();

	SGVector horizonDirection = pivot - point;
	SGVector axis = horizonDirection ^ SGVector(0.0, 1.0, 0.0);

	float yaxis_yValue = (float)m_mtxCam_std[5];
	if (yaxis_yValue < 0) dragValueHeight *= -1;
	SGMatrix mtx_rotateVertical = getRotatationMatrix(dragValueHeight*SG_PI, axis) * defaultMatrix;
	SGMatrix mtx_rotateHorizon = defaultMatrix.getRotatedMatrix(0, SG_PI*dragValueWidth, 0);

	SGMatrix editMatrix = m_mtxCam_std;
	editMatrix *= defaultMatrixInverse * mtx_rotateVertical*defaultMatrixInverse * mtx_rotateHorizon;
	g_camCurrent.setCamMatrix(editMatrix);
}


void SGViewControl::setView_zoomInOut(int winWidth, int x)
{
	float dragValue = (float)(m_mouseX_std - x) / winWidth;

	SGVector sgvCamZ = -SGVector(m_mtxCam_std[8], m_mtxCam_std[9], m_mtxCam_std[10]).normal() * m_dCam_distFocus_std;

	SGVector point(m_mtxCam_std[12], m_mtxCam_std[13], m_mtxCam_std[14]);
	SGVector pivot = point + sgvCamZ;

	SGVector vDirection = pivot - point;

	if (dragValue < 0) {
		if (g_camCurrent.distFocus() < 0.1) return;
		dragValue = (float)pow(fabs(dragValue), 1) * 5;
		vDirection /= (1 + dragValue);
	}
	else {
		dragValue = (float)pow(fabs(dragValue), 1) * 5;
		vDirection *= (1 + dragValue);
	}

	SGVector pointEdit = pivot - vDirection;
	SGMatrix editMatrix;
	g_camCurrent.getCamMatrix(editMatrix);
	editMatrix[12] = pointEdit.x;
	editMatrix[13] = pointEdit.y;
	editMatrix[14] = pointEdit.z;
	g_camCurrent.setCamMatrix(editMatrix);
	g_camCurrent.setDistFocus((pivot - pointEdit).length());
}


void SGViewControl::setView_traverse(int winWidth, int x, int y)
{
	float C = (float)m_dCam_distFocus_std;
	float angle = (float)g_camCurrent.angleOfView() / 360.0f*SG_PI;
	float Y2d = C * (float)sin(angle) / (float)cos(angle);

	SGVector localP_std, localP;
	localP_std.x = (m_mouseX_std - winWidth / 2.0) / (winWidth / 2.0) *Y2d;
	localP_std.y = (m_mouseY_std - winWidth / 2.0) / (winWidth / 2.0) *Y2d;
	localP_std.z = -C;

	localP.x = (x - winWidth / 2.0) / (winWidth / 2.0) *Y2d;
	localP.y = (y - winWidth / 2.0) / (winWidth / 2.0) *Y2d;
	localP.z = -C;

	SGVector vMove = (localP_std - localP) * m_mtxCam_std;
	SGMatrix mtxResult = m_mtxCam_std;
	mtxResult[12] += vMove.x;
	mtxResult[13] += vMove.y;
	mtxResult[14] += vMove.z;
	g_camCurrent.setCamMatrix(mtxResult);
}