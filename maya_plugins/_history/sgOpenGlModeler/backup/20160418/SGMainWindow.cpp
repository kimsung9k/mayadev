#include "SGMainWindow.h"
#include "SGPrintf\SGPrintf.h"

SGMainWindow::SGMainWindow(QWidget* parent) : QMainWindow( parent ) {
	m_ptrMesh.resize(0);
	sgPrintf("window id : %d", winId());
}


SGMainWindow::~SGMainWindow(){
	m_ptrMesh.clear();
	delete m_centralWidget;
}


void SGMainWindow::closeEvent(QCloseEvent* evt){
	this->~SGMainWindow();
}


void SGMainWindow::setCentralWidget(QWidget* widget){
	QMainWindow::setCentralWidget(widget);
	m_centralWidget = widget;
}


void SGMainWindow::appendMesh( SGMesh* mesh ) {
	m_ptrMesh.push_back(mesh);
}


void SGMainWindow::setCamera(SGCam* cam) {
	m_ptrCam = cam;
}