#include "precompile.h"

#include "SGToolContext.h"
#include <maya/MPx3dModelView.h>
#include <maya/MQtUtil.h>
#include <SGMesh.h>
#include <SGSelection.h>
#include "SGFile.h"
#include "SGWidget.h"
#include "SGMarkingMenu.h"
#include "SGToolCondition.h"
#include "SGPermit.h"
#include "SGMouse.h"
#include "SGKey.h"
#include "Names.h"


///////////////////////////////////////////////////////////////////////////////
//////////////////// SGToolContext ///////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

extern SGManip*  manip;
extern SGWidget* toolWidget;
extern SGEvent*  toolEvent;

extern vector<SGGeneralManip> GeneralManips;
extern SGTransformManip       transManip;
extern SGNormalManip          normalManip;
extern SGPolygonManip         polygonManip;
extern SGSoftSelectionManip   softSelectionManip;

extern vector<SGIntersectResult> generalResult;
extern vector<SGIntersectResult> edgeSplitIntersectResult;
extern vector<SGIntersectResult> edgeSplitRingIntersectResult;

extern vector<vector<SGSplitPoint>> spPointsArr;
extern vector<int>  snapIndexArr;



SGToolContext::SGToolContext()
{
}



SGToolContext::~SGToolContext()
{
}


#include <SGPrintf.h>
void SGToolContext::toolOnSetup(MEvent& evt)
{
	MStatus status;
	SGPermit permit;

	SGKey::initializeKeys();
	SGMouse::initializeButtons();

	SGMesh::getSelection(SGToolCondition::option.symInfo);
	SGSelection::sels.initialize(SGMesh::pMesh);

	M3dView activeView = M3dView().active3dView();
	manip = (SGManip*)SGManip::newManipulator(Names::manipName, m_oManip);
	if (!manip) sgPrintf("manip is null");
	this->addManipulator(m_oManip);

	toolWidget = new SGWidget(MQtUtil::mainWindow());
	toolWidget->startEvent();

	this->setCursor( MCursor::editCursor );

	if ( SGMesh::pMesh->dagPath.node().isNull() ) {
		//MGlobal::displayWarning("Select mesh first");
	}
	else {
		MFnMesh fnMesh = SGMesh::pMesh->dagPath;
		MFnDagNode dagNode = fnMesh.parent(0);
		char buffer[128];
		sprintf(buffer, "maintainActiveChangeSelectMode %s", dagNode.partialPathName().asChar() );
		MGlobal::executeCommand(buffer);
	}

	SGMarkingMenu::menu.setDefaultMenu();
	SGToolCondition::toolIsOn = true;
}



void SGToolContext::toolOffCleanup()
{
	delete SGMesh::pMesh;
	SGMesh::pMesh = NULL;

	toolWidget->releaseEvent();
	delete toolWidget;

	this->deleteManipulators();
	this->setCursor(MCursor::defaultCursor);

	SGMarkingMenu::menu.setMenu(SGMarkingMenu::origCommand);
	SGToolCondition::toolIsOn = false;
}



void SGToolContext::getClassName(MString& name) const
{
	name.set("SGMToolMod01Context");
}




MStatus SGToolContext::doPtrMoved(MEvent& evt) {
	sgPrintf("ptr moved");

	return MS::kSuccess;
}

MStatus SGToolContext::doPtrMoved(MEvent& evt, MHWRender::MUIDrawManager& drawManager, const MHWRender::MFrameContext& frameContext ) {
	sgPrintf( "context class name : %s", frameContext.className() );

	return MS::kSuccess;
}