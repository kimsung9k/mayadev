#include "precompile.h"

#include "SGMMCommand.h"
#include "SGPolySplitManip.h"
#include "SGEvent.h"
#include <QtGui/qapplication.h>
#include <QtGui/qevent.h>


MString SGMMCommand::commandName = "SGMToolMod01MMCommand";

extern SGEvent* toolEvent;

SGMMCommand::SGMMCommand() {
}

SGMMCommand::~SGMMCommand() {
}


void* SGMMCommand::creator() {
	return new SGMMCommand();
}


MSyntax SGMMCommand::newSyntax() {
	MSyntax syntax;

	syntax.addFlag("-psm", "-polySplitMode", MSyntax::kNoArg);
	return syntax;
}


MStatus SGMMCommand::doIt(const MArgList& arg) {
	MStatus status;
	MString argStr = arg.asString(0);
	if (argStr == "-psm") m_psm = true;
	return redoIt();
}


MStatus SGMMCommand::redoIt() {
	if (m_psm) { 
		QWidget* activeWidget = M3dView::active3dView().widget();

		QMouseEvent mouseEvent((QEvent::MouseButtonRelease), QPoint(100, 100),
			Qt::RightButton,
			Qt::NoButton,
			Qt::NoModifier);

		QApplication::sendEvent((QObject*)activeWidget, &mouseEvent );
	}
	return MS::kSuccess;
}


MStatus SGMMCommand::undoIt() {
	if (m_psm) {
	}
	return MS::kSuccess;
}


bool SGMMCommand::isUndoable() const {
	return true;
}