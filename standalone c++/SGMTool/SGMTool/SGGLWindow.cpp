#include "SGGLWindow.h"
#include <math.h>
#include "SGFile.h"
#include "SGScene.h"



void SGGLWindow::initializeGL()
{
	glewInit();
	glFrontFace(GL_CCW);
	glEnable(GL_DEPTH_TEST);
	//glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
}

void SGGLWindow::resizeGL(GLsizei width, GLsizei height)
{
	glViewport(0,0,width, height);
}

void SGGLWindow::paintGL()
{
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	SGScene::dagNodeContainer.drawAll();
}