#include "SGPrintf\SGPrintf.h"
#include "SGGLWidget.h"
#include <maya/MFnMesh.h>
#include "pixelformat.h"
#include <GL/GLU.h>


static const char *vertexShaderSource =
"attribute highp vec4 posAttr;\n"
"attribute lowp vec4 colAttr;\n"
"varying lowp vec4 col;\n"
"uniform highp mat4 matrix;\n"
"void main() {\n"
"   col = colAttr;\n"
"   gl_Position = matrix * posAttr;\n"
"}\n";

static const char *fragmentShaderSource =
"varying lowp vec4 col;\n"
"void main() {\n"
"   gl_FragColor = col;\n"
"}\n";


SGGLWidget::SGGLWidget() : QGLWidget(){
	m_program=0;
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
	glFrontFace(GL_CCW);
	glEnable(GL_DEPTH_TEST);
	glClearColor(0.0f, 0.0f, 0.0f, 1.0f);

	m_program = new QGLShaderProgram(this);
	m_program->addShaderFromSourceCode(QGLShader::Vertex, vertexShaderSource);
	m_program->addShaderFromSourceCode(QGLShader::Fragment, fragmentShaderSource);
	m_program->link();
	m_posAttr = m_program->attributeLocation("posAttr");
	m_colAttr = m_program->attributeLocation("colAttr");
	m_matrixUniform = m_program->uniformLocation("matrix");

	sgPrintf("m_posAttr : %d", m_posAttr);
	sgPrintf("m_colAttr : %d", m_colAttr);
	sgPrintf("m_matrixUniform : %d", m_matrixUniform);
}


void SGGLWidget::paintGL() {
	glClear(GL_COLOR_BUFFER_BIT);
	

	m_program->bind();
	
	QMatrix4x4 matrix;
	matrix.perspective(60.0f, 4.0f / 3.0f, 0.1f, 100.0f);
	matrix.translate(0, 0, -2);

	m_program->setUniformValue(m_matrixUniform, matrix);

	GLfloat vertices[] = {
		0.0f, 0.707f,
		-0.5f, -0.5f,
		0.5f, -0.5f
	};

	GLfloat colors[] = {
		1.0f, 0.0f, 0.0f,
		0.0f, 1.0f, 0.0f,
		0.0f, 0.0f, 1.0f
	};
	
	glVertexAttribPointer(m_posAttr, 2, GL_FLOAT, GL_FALSE, 0, vertices);
	glVertexAttribPointer(m_colAttr, 3, GL_FLOAT, GL_FALSE, 0, colors);
	
	glEnableVertexAttribArray(0);
	glEnableVertexAttribArray(1);

	glDrawArrays(GL_TRIANGLES, 0, 3);

	glDisableVertexAttribArray(1);
	glDisableVertexAttribArray(0);
	/**/
	m_program->release();
}

/*
void SGGLWidget::appendMesh(SGMesh* ptrMesh) {
	m_meshs.push_back(ptrMesh);
}*/


void SGGLWidget::resizeGL(int width, int height ) {
	glViewport(0, 0, (GLint)width, (GLint)height);
	
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();

	gluPerspective(45, 2, 0.01, 10000);

	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();

	sgPrintf("resize gl");
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