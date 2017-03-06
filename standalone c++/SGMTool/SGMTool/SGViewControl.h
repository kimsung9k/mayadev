#pragma once
#include "SGMatrix.h"
#include <GL/glew.h>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>


#define MOUSE_EVT_RESULT int
#define MOUSE_EVT_UPDATE 1
#define MOUSE_EVT_NOUPDATE 0

#ifndef SG_PI
#define SG_PI 3.14159265359f
#endif


class SGViewControl
{
public:
	SGViewControl();

	static void initializeCamera();

	void SetLButtonDown(bool value);
	void SetRButtonDown(bool value);
	void SetMButtonDown(bool value);

	void GetWindowWidthHeight(int& width, int& height);
	void SetWindowWidthHeight(int width, int height);
	void SetPMouseClient(int px, int py);

	MOUSE_EVT_RESULT  mouseEventControl();

	glm::mat4x4 getCamMatrixInverse();
	glm::mat4x4 getPerspViewMatrix();
	glm::mat4x4 getWorldToViewMatrix();
	glm::vec3   getCamPosition();
	glm::vec3   getCamVector();

	float   getAngleOfView();
	float   getCamNearClip();
	float   getCamFarClip();

	void   setView_standard(int x, int y);
	void   setView_rotate(int winWidth, int x, int y);
	void   setView_zoomInOut(int winWidth, int x);
	void   setView_traverse(int winWidth, int x, int y);


private:
	bool   m_bLButtonDown;
	bool   m_bRButtonDown;
	bool   m_bMButtonDown;

	int  m_mousePx, m_mousePy;
	int  m_windowWidth, m_windowHeight;

	bool  m_onShift;
	bool  m_onCrrl;
	bool  m_onAlt;

	int      m_mouseX_std;
	int      m_mouseY_std;
	SGMatrix m_mtxCam_std;
	double   m_dCam_distFocus_std;
};






