#include <maya/MIOStream.h>
#include <maya/MSimple.h>

#include <maya/MQtUtil.h>
#include "SGMainWindow.h"
#include "SGGLWidget.h"

#include "SGPrintf\SGPrintf.h"
#include "SGFunctions.h"

DeclareSimpleCommand( SGOpenGLModeler, PLUGIN_COMPANY, "4.5");

MStatus SGOpenGLModeler::doIt( const MArgList& args )
{
	SGMainWindow* mainWindow = new SGMainWindow( MQtUtil::mainWindow() );
	mainWindow->show();
	
	SGGLWidget* glWidget = new SGGLWidget();
	mainWindow->setCentralWidget(glWidget);

	SGFunctions::getCamera(glWidget->m_cam);
	SGFunctions::getMeshs(glWidget->m_meshs);
	
	/*
	QWidget* widget = new QWidget();
	QPushButton* button = new QPushButton();
	QVBoxLayout* layout = new QVBoxLayout();
	layout->addWidget(glWidget);
	layout->addWidget(button);
	widget->setLayout(layout);
	*/

	return MS::kSuccess;
}