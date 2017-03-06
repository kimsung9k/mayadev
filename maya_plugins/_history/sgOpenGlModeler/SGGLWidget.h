#pragma once

#include <Windows.h>
#include "SGMesh.h"
#include "SGCam.h"
#include <QtGui\qwidget.h>
#include <QtGui\qboxlayout.h>
#include <QtGui\qpushbutton.h>
#include <Qt\qmatrix4x4.h>
#include <QtGui\qevent.h>
#include <vector>
#include "SGVec3.h"
#include "SGBase.h"
#include "SGShaderProgram.h"


using std::vector;

class SGGLWidget : public QGLWidget
{
public:
	SGGLWidget();
	~SGGLWidget();

	void initializeGL();
	void paintGL();
	void resizeGL( int width, int height );

	virtual void resizeEvent(QResizeEvent* evt);
	virtual void mouseMoveEvent(QMouseEvent* evt);
	virtual void mousePressEvent(QMouseEvent* evt);
	virtual void mouseReleaseEvent(QMouseEvent* evt);
	virtual void mouseDoubleClickEvent(QMouseEvent* evt);
	virtual void timerEvent(QTimerEvent* evt);

	SGCam* m_cam;
	vector<SGMesh*> m_mesh;
	vector<SGShaderProgram*> m_shader;

	GLuint posLoc, colorLoc, uniformProjection;
	GLuint vtxArrBufferId, elementBufferId;
	float aspect;

	int m_timerId;
};

 
