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
#include <GL/glew.h>
#include <QtOpenGL/QGLWidget>

using std::vector;

class SGGLWidget : public QGLWidget
{
public:
	SGGLWidget();
	~SGGLWidget();

	void initializeGL();
	void paintGL();
	void resizeGL( int width, int height );

	//bool winEvent(MSG* msg, long* result);
	/*
	virtual void	wheelEvent(QWheelEvent * event);
	virtual void	leaveEvent(QEvent * event);
	virtual void	inputMethodEvent(QInputMethodEvent * event);
	virtual void	hideEvent(QHideEvent * event);
	virtual void enterEvent(QEvent* evt);
	virtual void contextMenuEvent(QContextMenuEvent* evt );
	virtual void actionEvent(QActionEvent* evt);
	virtual void changeEvent(QEvent* evt);
	virtual void paintEvent(QPaintEvent* evt);
	virtual void showEvent(QShowEvent* evt);*/
	virtual void resizeEvent(QResizeEvent* evt);
	virtual void mouseMoveEvent(QMouseEvent* evt);
	virtual void mousePressEvent(QMouseEvent* evt);
	virtual void mouseReleaseEvent(QMouseEvent* evt);
	virtual void mouseDoubleClickEvent(QMouseEvent* evt);

	HDC   m_old_hdc;
	HDC   m_hDC;
	HGLRC m_old_hrc;
	HGLRC m_hRC;
	UINT   m_before;

	SGCam* m_cam;
	vector<SGMesh*> m_meshs;
/*
private:
	int m_vsid;
	int m_fsid;
	int m_prid;

	static const char* defaultVS_code;
	static const char* defaultFS_code;*/
};