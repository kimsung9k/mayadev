#include <maya/MIOStream.h>
#include <maya/MSimple.h>

#include <maya/MQtUtil.h>
#include "SGMainWindow.h"
#include "SGGLWidget.h"

#include "SGPrintf\SGPrintf.h"

DeclareSimpleCommand( SGOpenGLModeler, PLUGIN_COMPANY, "4.5");

MStatus SGOpenGLModeler::doIt( const MArgList& args )
{
	SGMainWindow* mainWindow = new SGMainWindow( MQtUtil::mainWindow() );
	mainWindow->show();
	
	SGGLWidget* glWidget = new SGGLWidget();
	mainWindow->setCentralWidget(glWidget);

	return MS::kSuccess;
}