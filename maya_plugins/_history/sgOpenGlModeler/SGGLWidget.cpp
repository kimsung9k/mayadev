#include "SGPrintf\SGPrintf.h"
#include "SGGLWidget.h"
#include <maya/MFnMesh.h>
#include "pixelformat.h"
#include <QT/qmatrix4x4.h>
#include <maya/MFloatMatrix.h>
#include "SGFunctions.h"


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
	aspect = 1.0f;
	m_cam = new SGCam();
	setMouseTracking(true);
}


SGGLWidget::~SGGLWidget() {
	delete m_cam;
	for (int i = 0; i < m_mesh.size(); i++) {
		delete m_mesh[i];
	}
	for (int i = 0; i < m_shader.size(); i++) {
		delete m_shader[i];
	}
	setMouseTracking(false);
}


void SGGLWidget::initializeGL() {
	glewInit();
	glFrontFace(GL_CCW);
	glEnable(GL_DEPTH_TEST);
	glClearColor(0.0f, 0.0f, 0.0f, 1.0f);

	SGFunctions::getShaders(m_shader);
	SGFunctions::getCamera(m_cam);
	SGFunctions::getMeshs(m_mesh);

	GLuint posLoc    = m_shader[0]->getAttribLocation("position");
	GLuint normalLoc = m_shader[0]->getAttribLocation("normal");

	GLuint projectionMatrix = m_shader[0]->getUniformLocation("projection");
	GLuint objectMatrix     = m_shader[0]->getUniformLocation("objectMatrix");
	GLuint camPosition      = m_shader[0]->getUniformLocation("camPosition");
	GLuint camVector        = m_shader[0]->getUniformLocation("camVector");

	for (int i = 0; i < m_mesh.size(); i++)
	{
		m_mesh[i]->locationBind( posLoc, normalLoc);
		m_mesh[i]->uniformBind( projectionMatrix, objectMatrix, camPosition, camVector );
	}
}



void SGGLWidget::paintGL() {
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	m_shader[0]->use();
	for (int i = 0; i < m_mesh.size(); i++)
	{
		m_mesh[i]->draw(m_cam);
	}
}


void SGGLWidget::resizeGL(int width, int height ) {
	glViewport(0, 0, (GLint)width, (GLint)height);
	aspect = (float)width / height;
	m_cam->m_width = width;
	m_cam->m_height = height;
	sgPrintf("resize");
}


void SGGLWidget::timerEvent(QTimerEvent* evt) {
	updateGL();
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