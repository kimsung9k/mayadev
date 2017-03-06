#pragma once

#include <GL/glew.h>
#include <GL/wglew.h>

class SGGLWindow
{
public:
	void initializeGL();
	void resizeGL(GLsizei width, GLsizei height);
	void paintGL();
};