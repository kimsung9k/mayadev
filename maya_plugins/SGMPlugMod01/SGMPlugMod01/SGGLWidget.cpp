#include "precompile.h"
#include "SGPrintf.h"
#include "SGGLWidget.h"
#include <QtOpenGL\qgl.h>


SGGLWidget::SGGLWidget(QGLWidget * parent) : QGLWidget(QGLFormat(QGL::SampleBuffers), parent) {
	setAutoFillBackground(false);
	setMinimumSize(200, 200);
}


void SGGLWidget::initializeGL() {
}

void SGGLWidget::paintEvent(QPaintEvent*) {
}