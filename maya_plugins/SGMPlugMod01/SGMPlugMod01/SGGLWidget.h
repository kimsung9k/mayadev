#pragma once

#include <Windows.h>
#include <QtOpenGL\qgl.h>
#include <QtCore/qobject.h>
#include <QtGui/qevent.h>
#include <QtGui/qwidget.h>
#include <Qt/qpointer.h>


class SGGLWidget : public QGLWidget {
public:
	SGGLWidget(QGLWidget * parent = 0);
protected:
	void initializeGL();
	void paintEvent(QPaintEvent *);
};