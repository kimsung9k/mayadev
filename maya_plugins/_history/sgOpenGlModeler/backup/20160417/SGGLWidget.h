#pragma once

#include <Windows.h>
#include "SGMesh.h"
#include "SGCam.h"
#include <QtGui\qwidget.h>
#include <QtGui\qboxlayout.h>
#include <QtGui\qpushbutton.h>
#include <Qt\qmatrix4x4.h>
#include <QtGui\qevent.h>
#include <QT/qglfunctions.h>
#include <QT/qglshaderprogram.h>
#include <vector>
using std::vector;

class SGGLWidget : public QGLWidget, protected QGLFunctions
{
public:
	SGGLWidget();
	~SGGLWidget();

	void initializeGL();
	void paintGL();
	void resizeGL( int width, int height );

	void resizeEvent(QResizeEvent* evt);
	void mouseMoveEvent(QMouseEvent* evt);
	void mousePressEvent(QMouseEvent* evt);
	void mouseReleaseEvent(QMouseEvent* evt);
	void mouseDoubleClickEvent(QMouseEvent* evt);

	HDC   m_hDC;
	HGLRC m_hRC;

	SGCam* m_cam;
	vector<SGMesh*> m_meshs;
	QGLShaderProgram* m_program;

	GLuint m_posAttr;
	GLuint m_colAttr;
	GLuint m_matrixUniform;
/*
private:
	int m_vsid;
	int m_fsid;
	int m_prid;

	static const char* defaultVS_code;
	static const char* defaultFS_code;*/
};