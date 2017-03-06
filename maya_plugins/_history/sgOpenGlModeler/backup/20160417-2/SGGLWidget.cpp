#include "SGPrintf\SGPrintf.h"
#include "SGGLWidget.h"
#include <maya/MFnMesh.h>
#include "pixelformat.h"



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
	/*
	m_hDC = getDC();
	bSetupPixelFormat(m_hDC);
	m_hRC = wglGetCurrentContext();
	//m_hRC = wglCreateContext(m_hDC);

	wglMakeCurrent(m_hDC, m_hRC);*/

	glewInit();
	glFrontFace(GL_CCW);
	glEnable(GL_DEPTH_TEST);
	glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
}


void SGGLWidget::paintGL() {
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	float dMatrix[16];
	dMatrix[0] = 0.707107f;
	dMatrix[1] = -0.331295f;
	dMatrix[2] = 0.624695f;
	dMatrix[3] = 0.000000f;
	dMatrix[4] = 0.000000f;
	dMatrix[5] = 0.883452f;
	dMatrix[6] = 0.468521f;
	dMatrix[7] = 0.000000f;
	dMatrix[8] = -0.707107f;
	dMatrix[9] = -0.331295f;
	dMatrix[10] = 0.624695f;
	dMatrix[11] = 0.000000f;
	dMatrix[12] = -0.000000f;
	dMatrix[13] = 0.000000f;
	dMatrix[14] = -44.821870f;
	dMatrix[15] = 1.000000f;

	glColor3f(1, 0, 0);
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

	glPopMatrix();

	SwapBuffers(m_hDC);
	sgPrintf("paint");
}


void SGGLWidget::resizeGL(int width, int height ) {
	glViewport(0, 0, (GLint)width, (GLint)height);
	
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();

	gluPerspective(45, 2, 0.01, 10000);

	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();

	sgPrintf("resize");
}

/*
void SGGLWidget::showEvent(QShowEvent* evt) {
	initializeGL();
	sgPrintf("showEvent");
}

void SGGLWidget::paintEvent(QPaintEvent* evt) {
	QWidget::paintEvent(evt);
	sgPrintf("paintEvent");
	paintGL();
}

void SGGLWidget::changeEvent(QEvent* evt) {
	sgPrintf("changeEvent");
}

bool SGGLWidget::winEvent(MSG* msg, long* result) {
	//sgPrintf( "winEvent" );
	RECT rt;
	if(m_before != msg->message ) {
		sgPrintf("msg : %d", msg->message);
		m_before = msg->message;
		if(m_before == 15 || m_before == 71 || m_before ==  131 || m_before == 70){
			GetClientRect(winId(), &rt);
			resizeGL(rt.right, rt.bottom);
		}
	}

	return QWidget::winEvent(msg, result);
}

void SGGLWidget::wheelEvent(QWheelEvent * event) {
	sgPrintf("wheelEvent");
}


void SGGLWidget::leaveEvent(QEvent * event) {
	sgPrintf("leave event");
}


void SGGLWidget::inputMethodEvent(QInputMethodEvent * event) {
	sgPrintf("inputMethodEvent");
}

void SGGLWidget::hideEvent(QHideEvent * event) {
	sgPrintf("hideEvent");
}

void SGGLWidget::enterEvent(QEvent* evt) {
	sgPrintf("enterEvent");
}

void SGGLWidget::contextMenuEvent(QContextMenuEvent* evt) {
	sgPrintf("contextMenu event");
}

void SGGLWidget::actionEvent(QActionEvent* evt) {
	sgPrintf("action event");
}
*/

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