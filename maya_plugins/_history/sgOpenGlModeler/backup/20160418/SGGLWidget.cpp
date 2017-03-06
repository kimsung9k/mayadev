#include "SGPrintf\SGPrintf.h"
#include "SGGLWidget.h"
#include <maya/MFnMesh.h>
#include "pixelformat.h"
#include <QT/qmatrix4x4.h>


static const char *vertexShaderSource =
"#version 430\n"
"attribute vec2 position;\n"
"attribute vec3 color;\n"
"varying vec4 varyColor;\n"
"uniform mat4 matrix;\n"
"void main() {\n"
"   varyColor = vec4(color,1);\n"
"   gl_Position = matrix * vec4(position,0,1);\n"
"}\n";

static const char *fragmentShaderSource =
"#version 430\n"
"varying vec4 varyColor;\n"
"void main() {\n"
"   gl_FragColor = varyColor;\n"
"}\n";

bool checkShaderStatus2(unsigned int shaderID)
{
	GLint compileStatus[10];
	for (int i = 0; i < 10; i++) compileStatus[i] = -1;
	glGetShaderiv(shaderID, GL_COMPILE_STATUS, compileStatus);
	bool returnValue = true;
	for (int i = 0; i < 10; i++)
	{
		if (compileStatus[i] == -1) continue;
		if (compileStatus[i] != GL_TRUE)
		{
			GLint infoLogLength;
			glGetShaderiv(shaderID, GL_INFO_LOG_LENGTH, &infoLogLength);
			char* buffer = new char[infoLogLength];

			GLsizei bufferSize;
			glGetShaderInfoLog(shaderID, infoLogLength, &bufferSize, buffer);
			OutputDebugString(buffer);
			returnValue = false;
		}
	}
	return returnValue;
}

SGGLWidget::SGGLWidget() : QGLWidget(){
	m_cam = new SGCam();
	setMouseTracking(true);
}


SGGLWidget::~SGGLWidget() {
	delete m_cam;
	for (int i = 0; i < m_meshs.size(); i++) {
		delete m_meshs[i];
	}
	setMouseTracking(false);
}



void SGGLWidget::initializeGL() {
	glewInit();
	glFrontFace(GL_CCW);
	glEnable(GL_DEPTH_TEST);
	glClearColor(0.0f, 0.0f, 0.0f, 1.0f);

	//shader start//

	vsid = glCreateShader(GL_VERTEX_SHADER);
	fsid = glCreateShader(GL_FRAGMENT_SHADER);
	prid = glCreateProgram();

	char* adapter[1];
	adapter[0] = (char*)vertexShaderSource;
	glShaderSource(vsid, 1, adapter, 0);
	glCompileShader(vsid);
	adapter[0] = (char*)fragmentShaderSource;
	glShaderSource(fsid, 1, adapter, 0);
	glCompileShader(fsid);

	OutputDebugString("before vs");
	checkShaderStatus2(vsid);
	OutputDebugString("after vs");
	OutputDebugString("before fs");
	checkShaderStatus2(fsid);
	OutputDebugString("after fs");
	

	glAttachShader(prid, vsid);
	glAttachShader(prid, fsid);
	glLinkProgram(prid);
	glUseProgram(prid);
	//shader end//
}


void SGGLWidget::paintGL() {
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	glColor3f(1, 0, 0);

	QMatrix4x4 camInv;
	camInv.perspective(60.0f, 4.0f / 3.0f, 0.1f, 100.0f);
	camInv.translate(0, 0, -10);

	double points[] =
	{
		0, 1,   -1, -1,   1,-1
	};


	double color[] =
	{
		0, 1, 0,   
		1, 0, 0,
		0, 0, 1
	};

	float matrix[] = {
		1.516395, -1.135207, -0.624707, -0.624695,
		0.000000, 3.027220, -0.468531, -0.468522,
		-1.516395, -1.135207, -0.624707, -0.624695,
		0.000000, -0.000034, 44.622768, 44.821877
	};

	//vertex attribute start//
	GLuint vtxBufferId, uniformId;

	GLuint posLoc = glGetAttribLocation(prid, "position");
	GLuint colorLoc = glGetAttribLocation(prid, "color");
	glEnableVertexAttribArray(posLoc);
	glVertexAttribPointer(posLoc,   2, GL_DOUBLE, GL_FALSE, 0,  points);
	glEnableVertexAttribArray(colorLoc);
	glVertexAttribPointer(colorLoc, 3, GL_DOUBLE, GL_FALSE, 0,  color);

	uniformId = glGetUniformLocation(prid, "matrix");
	glUniformMatrix4fv(uniformId, 1, GL_FALSE, matrix );
	glDrawArrays(GL_TRIANGLES, 0, 3);
	
	
	/*
	glPushMatrix();
	glMultMatrixd(camInv.data());

	glDrawArrays(GL_TRIANGLES, 0, 3);
	glPopMatrix();
	/*
	glPushMatrix();
	glMultMatrixf(dMatrix);
	glBegin(GL_POLYGON);
	glVertex3f(-10.0f, -10.0f, 1.0f);
	glVertex3f(10.0f, -10.0f, 1.0f);
	glVertex3f(10.0f, 10.0f, 1.0f);
	glVertex3f(-10.0f, 10.0f, 1.0f);
	glEnd();

	glBegin(GL_POLYGON);
	glVertex3f(-10.0f, -10.0f, -1.0f);
	glVertex3f(-10.0f, 10.0f, -1.0f);
	glVertex3f(10.0f, 10.0f, -1.0f);
	glVertex3f(10.0f, -10.0f, -1.0f);
	glEnd();
	
	glPopMatrix();/**/
	
	sgPrintf("paint");
}


void SGGLWidget::resizeGL(int width, int height ) {
	glViewport(0, 0, (GLint)width, (GLint)height);
	/*
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();

	gluPerspective(45, 2, 0.01, 10000);

	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();
	*/
	sgPrintf("resize");
}


void SGGLWidget::resizeEvent(QResizeEvent* evt) {
	QSize size = evt->size();
	int width = size.width();
	int height = size.height();
	resizeGL(width, height);
}


void SGGLWidget::mouseMoveEvent(QMouseEvent* evt) {
	int poseX = evt->x();
	int poseY = evt->y();
	//sgPrintf("mouse move : %d, %d", poseX, poseY );	
}


void SGGLWidget::mousePressEvent(QMouseEvent* evt) {
	Qt::MouseButton button = evt->button();
	//sgPrintf("mouse press : %d", button);
}


void SGGLWidget::mouseReleaseEvent(QMouseEvent* evt) {
	Qt::MouseButton button = evt->button();
	//sgPrintf("mouse release : %d", button);
}


void SGGLWidget::mouseDoubleClickEvent(QMouseEvent* evt) {
	Qt::MouseButton button = evt->button();
	//sgPrintf("mouse double clicked : %d", button);
}