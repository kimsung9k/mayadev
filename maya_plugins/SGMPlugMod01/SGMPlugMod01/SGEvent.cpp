#include "precompile.h"

#include "SGEvent.h"
#include <QtGui/qapplication.h>
#include <QtGui/qwidget.h>
#include <SGMesh.h>
#include <SGIntersectResult.h>
#include <SGMatrix.h>
#include <SGSelection.h>
#include <SGTimeCheck.h>
#include <SGPrintf.h>
#include "SGFunction.h"
#include <maya/MQtUtil.h>
#include "SGWidget.h"
#include "SGMarkingMenu.h"
#include "SGKey.h"
#include "SGMouse.h"
#include "SGToolCondition.h"
#include "SGGLWidget.h"


extern SGManip* manip;
extern SGWidget* toolWidget;

extern vector<SGGeneralManip> GeneralManips;
extern SGTransformManip       transManip;
extern SGNormalManip          normalManip;
extern SGPolygonManip         polygonManip;
extern SGSoftSelectionManip   softSelectionManip;
extern SGDragSelectionManip   dragSelectionManip;
extern SGMoveBrushManip       moveBrushManip;

extern vector<SGIntersectResult> generalResult;
extern vector<SGIntersectResult> edgeSplitIntersectResult;

extern vector<vector<SGSplitPoint>> spPointsArr;


SGEvent::SGEvent() {

	firstEvent = true;

	m_altPressed = false;
	m_controlJustPress = false;
	m_controlPressed = false;
	m_shiftPressed = false;
	m_mouseMove = false;
	m_mouseJustPress = false;
	m_mouseJustRelease = false;
	m_mousePressed = false;
	m_leftJustPress = false;
	m_leftJustRelease = false;
	m_leftPressed = false;
	m_rightJustPress = false;
	m_rightJustRelease = false;
	m_rightPressed = false;
	m_middleJustPress = false;
	m_middleJustRelease = false;
	m_middlePressed = false;

	edgeSplitPointPushed = false;

	smoothMode = false;

	updateCamMatrix();
}


SGEvent::~SGEvent() {
}


bool SGEvent::eventFilter(QObject* object, QEvent* evt)
{
	if ( SGMesh::pMesh->dagPath.node().isNull() ) {
		//MGlobal::displayWarning("Select mesh first before set tool");
		return QObject::eventFilter(object, evt);
	}
	if (isAutoRepeat(evt)) return true;

	if (!translateEvent(evt)) {
		return QObject::eventFilter(object, evt);
	}

	updateCamMatrix();

	if (m_altPressed && transManip.exists()) transManip.update();

	softSelectEvent();
	getIntersection();

	if (SGToolCondition::option.mode == SGToolCondition::kDefault) {
		selectEvent();
		vertexMoveEvent();
		edgeSplitEvent();
		edgeSplitRingEvent();
		edgeSlideEvent();
		deleteEvent();
	}
	else if (SGToolCondition::option.mode == SGToolCondition::kMoveMode) {
		if (m_leftJustPress || m_leftJustRelease || m_leftPressed) {}
		else
			selectEvent();
		moveBrushEvent();
	}
	
	markingMenuEvent();
	camFocusEvent();
	saveEvent();
	smoothDisplay();
	
	manipUpdate();
	M3dView().active3dView().refresh(false, true);

	if (!m_altPressed && m_leftJustPress ||
		!m_altPressed && m_middleJustPress ||
		SGKey::key("d")->m_eventType == SGKey::kPress ||
		SGKey::key("f")->m_eventType == SGKey::kPress ||
		SGKey::key("v")->m_eventType == SGKey::kPress ||
		SGKey::key("b")->m_eventType == SGKey::kPress ||
		SGKey::key("b")->m_eventType == SGKey::kRelease ||
		SGKey::key("b")->m_condition == SGKey::kPressed ||
		SGKey::key("delete")->m_eventType == SGKey::kPress ||
		(m_shiftPressed && SGKey::key(">")->m_eventType == SGKey::kPress) ||
		(m_shiftPressed && SGKey::key("<")->m_eventType == SGKey::kPress) ||
		(m_altPressed && m_controlPressed) ||
		(SGKey::key("s")->m_eventType == SGKey::kPress && !m_controlPressed) ){
		return true;
	}

	return QObject::eventFilter(object, evt);
}


bool SGEvent::translateEvent(QEvent* evt) {
	m_altPressed = false;
	m_controlJustPress = false;
	m_controlPressed = false;
	m_shiftPressed = false;
	m_mouseMove = false;
	m_mouseJustPress = false;
	m_mouseJustRelease = false;
	m_mousePressed = false;
	m_leftJustPress = false;
	m_leftJustRelease = false;
	m_leftPressed = false;
	m_rightJustPress = false;
	m_rightJustRelease = false;
	m_rightPressed = false;
	m_middleJustPress = false;
	m_middleJustRelease = false;
	m_middlePressed = false;

	m_isDragSelecting = false;

	m_isMouseEvent = SGMouse::translateEvent(evt);
	m_isKeyEvent   = SGKey::translateEvent(evt);

	m_altPressed = SGKey::key("alt")->m_condition == SGKey::kPressed;
	m_controlPressed = SGKey::key("ctrl")->m_condition == SGKey::kPressed;
	m_controlJustRelease = SGKey::key("ctrl")->m_eventType == SGKey::kRelease;
	m_shiftPressed = SGKey::key("shift")->m_condition == SGKey::kPressed;

	m_mouseMove = SGMouse::eventType == SGMouse::kMove;

	m_leftPressed = SGMouse::btn(Qt::LeftButton)->m_condition == SGMouse::kPressed;
	m_leftJustPress = SGMouse::btn(Qt::LeftButton)->m_eventType == SGMouse::kPress;
	m_leftJustRelease = SGMouse::btn(Qt::LeftButton)->m_eventType == SGMouse::kRelease;

	m_middlePressed = SGMouse::btn(Qt::MiddleButton)->m_condition == SGMouse::kPressed;
	m_middleJustPress = SGMouse::btn(Qt::MiddleButton)->m_eventType == SGMouse::kPress;
	m_middleJustRelease = SGMouse::btn(Qt::MiddleButton)->m_eventType == SGMouse::kRelease;

	m_rightPressed = SGMouse::btn(Qt::RightButton)->m_condition == SGMouse::kPressed;
	m_rightJustPress = SGMouse::btn(Qt::RightButton)->m_eventType == SGMouse::kPress;
	m_rightJustRelease = SGMouse::btn(Qt::RightButton)->m_eventType == SGMouse::kRelease;
	m_mousePressed = SGMouse::condition == SGMouse::kPressed;
	m_mousePressed = SGMouse::condition != SGMouse::kReleased;
	m_mouseJustPress = SGMouse::eventType == SGMouse::kPress;
	m_mouseJustRelease = SGMouse::eventType == SGMouse::kRelease;

	SGMouse::x = SGMouse::origX;
	SGMouse::y = SGMouse::origY;

	if (firstEvent) {
		SGMouse::btn(Qt::LeftButton)->m_condition = SGMouse::kReleased;
		SGMouse::condition = SGMouse::kReleased;

		m_mousePressed = false;
		firstEvent = false;
	}

	if (!m_isMouseEvent && !m_isKeyEvent) return false;
	return true;
}


void SGEvent::updateCamMatrix() {
	if (SGToolCondition::option.symInfo.isNoMirror()) {
		camMatrixList.setLength(1);
		camMatrixList[0] = SGMatrix::getCamMatrix();
		GeneralManips.resize(1);
		GeneralManips[0].camMatrix = camMatrixList[0];
	}
	else if (SGToolCondition::option.symInfo.isXMirror()) {
		MMatrix meshMatrix = SGMesh::pMesh->dagPath.inclusiveMatrix();
		MMatrix meshMatrixInverse = SGMesh::pMesh->dagPath.inclusiveMatrixInverse();
		camMatrixList.setLength(2);
		camMatrixList[0] = SGMatrix::getCamMatrix();
		camMatrixList[1] = camMatrixList[0] * meshMatrixInverse * SGToolCondition::option.symInfo.mirrorMatrix() * meshMatrix;
		GeneralManips.resize(2);
		GeneralManips[0].camMatrix = camMatrixList[0];
		GeneralManips[1].camMatrix = camMatrixList[1];
		GeneralManips[0].manipNum = 0;
		GeneralManips[1].manipNum = 1;
	}
}



bool SGEvent::isAutoRepeat(QEvent* evt) {
	if (evt->type() == QEvent::KeyPress ||
		evt->type() == QEvent::KeyRelease ||
		evt->type() == QEvent::ShortcutOverride ) {
		QKeyEvent* keyEvent = (QKeyEvent*)evt;
		if (keyEvent->isAutoRepeat()) return true;
	}
	return false;
}



void SGEvent::getGeneralIntersection() {

	if (SGMesh::pMesh->updateRequired()) {
		bool update = SGMesh::pMesh->update( SGToolCondition::option.symInfo );
		if (!update) {
			MGlobal::displayError("mesh update failed");
			MGlobal::executeCommand("setToolTo selectSuperContext;", false, true );
			return;
		}
	}

	for (int i = 0; i < generalResult.size(); i++) {
		generalResult[i] = SGIntersectResult::getIntersectionResult(SGMouse::x, SGMouse::y, camMatrixList[i] );
		SGIntersectResult* pResult = &generalResult[i];
		if (pResult->resultType == SGComponentType::kNone) {
			return;
		}
		if (!m_shiftPressed && !m_controlPressed && pResult->resultType != SGComponentType::kVertex) {
			pResult->resultType = SGComponentType::kVertex;
			pResult->resultIndex = pResult->vtxIndex;
		}
	}
}



void SGEvent::getIntersection()
{
	if ((!m_mouseJustPress&&m_mousePressed) || (m_altPressed&&!m_controlPressed) || m_mouseJustRelease ) return;

	transManip.getIntersectType();
	normalManip.getIntersectType();

	if (transManip.intersectType != SGTransformManipIntersector::kNone ||
		normalManip.intersectType != SGNormalManipIntersector::kNone) return;

	getGeneralIntersection();
	for (int i = 0; i < edgeSplitIntersectResult.size(); i++)
		edgeSplitIntersectResult[i] = SGIntersectResult::getIntersectionResult(SGMouse::x, SGMouse::y, camMatrixList[i]);
}



void SGEvent::vertexMoveEvent()
{
	static bool vertexPressed = false;
	static bool vertexMoved = false;
	static bool normalMode = false;

	if (SGKey::key("b")->m_condition == SGKey::kPressed) return;

	if (m_controlPressed)
		transManip.intersectType = SGTransformManipIntersector::kNone;

	if ( transManip.intersectType == SGTransformManipIntersector::kNone &&
		 normalManip.intersectType == SGNormalManipIntersector::kNone) {
		return;
	}


	if (  m_leftJustPress || m_middleJustPress  ) {
		MIntArray selVtxs = SGSelection::getIndices(SGSelection::sels.getSelVtxIndicesMap());
		if (selVtxs.length()) {
			if (m_controlPressed) {
				SGFunction::prepairVtxMoveNormal();
				normalMode = true;
			}
			else {
				SGFunction::prepairVtxMove();
			}
			vertexPressed = true;
		}
	}
	else if (vertexPressed && SGMouse::eventType == SGMouse::kMove) {
		if (!vertexMoved) {
			vertexMoved = true;
		}
		if (normalMode && m_leftPressed && normalManip.intersectType == SGNormalManipIntersector::kNormal) {
			SGFunction::vertexMove_normal();
		}
		else if(m_leftPressed){
			SGFunction::vertexMove_ing();
		}
		else if (m_middlePressed)SGFunction::vertexMove_slide();
		if (SGKey::key("v")->m_condition == SGKey::kPressed) {
			SGFunction::vertexMove_snap();
		}
	}

	if ((m_leftJustRelease || m_middleJustRelease) || (vertexPressed && m_altPressed)) {
		if (vertexMoved) {
			SGFunction::vertexMove_end(false);
			if (SGKey::key("v")->m_condition == SGKey::kPressed) {
				getIntersection();
				getIntersection();
			}
		}
		vertexMoved = false;
		vertexPressed = false;
		normalMode = false;
		transManip.build();
	}
}



void SGEvent::edgeSplitEvent()
{
	if (m_controlJustRelease)
	{
		SGFunction::splitEdge();
		edgeSplitPointPushed = false;
	}
	if (!m_controlPressed) return;
	if (m_shiftPressed) return;
	if (m_altPressed) return;


	SGIntersectResult* pResult = &edgeSplitIntersectResult[0];
	if ( pResult->resultType == SGComponentType::kNone ) return;
	if ( normalManip.intersectType == SGNormalManipIntersector::kNormal ) return;

	if ( pResult->resultType.isEdge() || pResult->resultType.isPolygon() ) {
		if (SGMouse::btn(Qt::LeftButton)->m_eventType == SGMouse::kPress) {
			SGFunction::pushSplitPoint();
			edgeSplitPointPushed = true;
		}
		else if (edgeSplitPointPushed && SGMouse::eventType == SGMouse::kMove) {
			SGFunction::editSplitPoint();
		}
		else if (SGMouse::btn(Qt::LeftButton)->m_eventType == SGMouse::kRelease) {
			edgeSplitPointPushed = false;
		}
	}
	else if ( pResult->resultType.isVertex() )
	{
		if ( SGMouse::btn(Qt::LeftButton)->m_eventType == SGMouse::kRelease )
		{
			SGFunction::pushSplitPoint();
		}
	}
}



void SGEvent::edgeSplitRingEvent()
{
	static bool edgeSplitRingPushed = false;

	if (!m_controlPressed || !m_altPressed) return;
	if (edgeSplitIntersectResult[0].resultType != SGComponentType::kEdge) return;

	if (SGMouse::btn(Qt::LeftButton)->m_eventType == SGMouse::kPress) {
		edgeSplitRingPushed = true;
	}
	else if (SGMouse::btn(Qt::LeftButton)->m_eventType == SGMouse::kMove && edgeSplitRingPushed) {
		SGFunction::editSplitRingPoint();
	}
	else if(SGMouse::btn(Qt::LeftButton)->m_eventType == SGMouse::kRelease && edgeSplitRingPushed){
		SGMesh* pMesh = SGMesh::pMesh;
		SGFunction::clearSplitPoint();
		SGFunction::polySplitRing();
		edgeSplitRingPushed = false;
	}
}



void SGEvent::edgeSlideEvent() {

	static bool edgeSlidePressed = false;
	static bool edgeSlideMoved = false;

	if (m_shiftPressed) return;

	if (edgeSplitIntersectResult[0].resultType != SGComponentType::kEdge) return;

	if (m_middleJustPress && m_controlPressed) {
		SGFunction::clearSplitPoint();
		SGFunction::prepairEdgeMove();
		edgeSlidePressed = true;
	}
	else if (m_mouseMove && edgeSlidePressed) {
		edgeSlideMoved = true;
		SGFunction::edgeMove_slide();
	}
	if ((m_middleJustRelease && edgeSlidePressed) || (edgeSlidePressed && m_altPressed) ) {
		if (edgeSlideMoved) {
			SGFunction::edgeMove_end(false);
			sgPrintf("edge move end");
		}
		edgeSlideMoved = false;
		edgeSlidePressed = false;
	}
}



void SGEvent::edgeBevelEvent() {

	static bool edgeBevelPressed = false;
	static bool edgeBevelMoved = false;

	if (m_shiftPressed) return;
	if (!m_controlPressed) return;
	SGIntersectResult* pResult = &edgeSplitIntersectResult[0];
	if (pResult->resultType != SGComponentType::kEdge) return;

	if (m_middleJustPress) {
		SGFunction::clearSplitPoint();
		edgeBevelPressed = true;
	}
	else if (m_mouseMove && edgeBevelPressed) {
		edgeBevelMoved = true;
		SGFunction::bevelEdge();
	}
	if ((m_middleJustRelease && edgeBevelPressed) || (edgeBevelPressed && m_altPressed)) {
		if (edgeBevelMoved) {
			SGFunction::bevelEdgeFinish();
		}
		edgeBevelMoved = false;
		edgeBevelPressed = false;
	}
}



void SGEvent::deleteEvent()
{
	SGIntersectResult* pResult = &generalResult[0];

	if (SGKey::key("d")->m_eventType == SGKey::kPress) {
		SGFunction::deleteComponent();
	}
}



void SGEvent::saveEvent() {
	if (m_controlPressed && SGKey::key("s")->m_eventType == SGKey::kPress) {
		sgPrintf("save event");
		//MGlobal::executeCommand("setToolTo moveSuperContext;");
	}
}



void SGEvent::selectEvent() {
	static bool mousePressed = false;
	static bool mouseDraged = false;
	if (m_altPressed) { mousePressed = false; mouseDraged = false; return; }
	if (SGKey::key("b")->m_condition == SGKey::kPressed) { mousePressed = false; mouseDraged = false; return; }

	if ((m_leftJustRelease || m_middleJustRelease) && !mouseDraged && !m_controlPressed ) {
		if (generalResult[0].resultType == SGComponentType::kNone &&
			normalManip.intersectType == SGNormalManipIntersector::kNone &&
			transManip.intersectType == SGTransformManipIntersector::kNone) {
			SGFunction::clearSelection(); 
			mousePressed = false; mouseDraged = false; return;
		}
	}

	if (m_shiftPressed && SGMouse::btn(Qt::LeftButton)->m_eventType == SGMouse::kDbClick) {
		SGFunction::addDbClickSelection();
		transManip.build();
		return;
	}


	if (m_shiftPressed && SGKey::key(">")->m_eventType == SGKey::kPress) {
		SGSelection::sels.growSelection();
		transManip.build();
		return;
	}
	if (m_shiftPressed && SGKey::key("<")->m_eventType == SGKey::kPress) {
		SGSelection::sels.reduceSelection();
		transManip.build();
		return;
	}


	if (generalResult[0].resultType != SGComponentType::kNone && 
		normalManip.intersectType == SGNormalManipIntersector::kNone &&
		transManip.intersectType == SGTransformManipIntersector::kNone&& 
		!mouseDraged && !m_controlPressed)
	{
		if ( m_leftJustPress || m_middleJustPress ) {
			if (!m_shiftPressed) {
				SGFunction::setSelection();
				transManip.build();
			}
		}else if (m_leftJustRelease && m_shiftPressed) {
			SGFunction::addSelection();
			transManip.build();
		}
		return;
	}


	if (m_leftJustPress|| m_middleJustPress) {
		if (generalResult[0].resultType == SGComponentType::kNone &&
			normalManip.intersectType == SGNormalManipIntersector::kNone &&
			transManip.intersectType == SGTransformManipIntersector::kNone) {
			SGIntersectResult result = SGIntersectResult::getIntersectionResult(SGMouse::x, SGMouse::y, SGMatrix::getCamMatrix());
			if (result.resultType == SGComponentType::kNone) {
				mousePressed = true;
				SGFunction::dragSelectionPress();
			}
		}
	}

	if (mousePressed && m_mouseMove) {
		SGFunction::dragSelectionDrag();
		m_isDragSelecting = true;
		mouseDraged = true;
	}

	if ( (m_leftJustRelease|| m_middleJustRelease) && mouseDraged) {
		mousePressed = false;
		mouseDraged = false;
		SGFunction::dragSelectionRelease(m_shiftPressed, m_controlPressed);
		transManip.build();
	}
}



void SGEvent::selectDragEvent() {
	
}


void SGEvent::camFocusEvent() {
	if (SGKey::key("f")->m_eventType == SGKey::kPress) {
		SGFunction::setCamFocus();
	}
}


void SGEvent::markingMenuEvent() {
	if (m_altPressed) return;
	if (!m_rightJustPress) return;

	if (SGSelection::sels.m_focusType.size()) {
		if (SGSelection::sels.m_focusType[0] == SGComponentType::kVertex) {
			SGMarkingMenu::menu.setVtxMenu();
		}
		else if (SGSelection::sels.m_focusType[0] == SGComponentType::kEdge) {
			SGMarkingMenu::menu.setEdgeMenu();
		}
		else if (SGSelection::sels.m_focusType[0] == SGComponentType::kPolygon) {
			SGMarkingMenu::menu.setPolyMenu();
		}
	}
	else {
		SGIntersectResult& closeResult = generalResult[0];
		if (closeResult.resultType == SGComponentType::kNone) {
			SGMarkingMenu::menu.setDefaultMenu();
			return;
		}

		if (closeResult.resultType == SGComponentType::kVertex ) {
			SGMarkingMenu::menu.setVtxMenu();
		}
		else if (closeResult.resultType == SGComponentType::kEdge ) {
			SGMarkingMenu::menu.setEdgeMenu();
		}
		else if (closeResult.resultType == SGComponentType::kPolygon ) {
			SGMarkingMenu::menu.setPolyMenu();
		}
	}
}


void SGEvent::manipUpdate() {
	manip->clearAll();

	if( SGKey::key("b")->m_condition == SGKey::kPressed && m_leftPressed  && m_mouseMove )
		softSelectionManip.draw(0);
	else if ( SGToolCondition::option.mode == SGToolCondition::kMoveMode && !m_altPressed && !m_isDragSelecting ) {
		moveBrushManip.draw(0);
	}

	if (m_isDragSelecting) {
		dragSelectionManip.draw(0);
	}
	
	if (m_controlPressed) {
		if (normalManip.exists()) normalManip.draw(0, m_leftPressed );
		if (!m_altPressed) {
			if (normalManip.intersectType == SGNormalManipIntersector::kNone) {
				for (int i = 0; i < GeneralManips.size(); i++) {
					GeneralManips[i].drawEdgeParamPoint(0);
					GeneralManips[i].drawSPoints(0);
				}
			}
		}
		else {
			for (int i = 0; i < GeneralManips.size(); i++) {
				GeneralManips[i].drawSplitRing(0);
			}
		}
	}
	else {
		if (transManip.exists() && SGToolCondition::option.mode == SGToolCondition::kDefault ) 
			transManip.draw(0, m_leftPressed || m_middlePressed );
	}
	if (transManip.intersectType == SGTransformManipIntersector::kNone) {
		if ( !m_altPressed && !m_mousePressed ) {
			for (int i = 0; i < GeneralManips.size(); i++) {
				GeneralManips[i].drawDefault(0);
			}
		}
	}
}


void SGEvent::smoothDisplay() {
	M3dView activeView = M3dView().active3dView();

	if (m_controlPressed) return;
	if (SGKey::key("s")->m_eventType != SGKey::kPress) return;

	MString pannelName;
	MGlobal::executeCommand("getPanel -wf;", pannelName, false, false);

	MFnMesh fnMesh = SGMesh::pMesh->dagPath;
	char buffer[128];
	sprintf(buffer, "displaySmoothness -q -po %s", fnMesh.partialPathName().asChar());
	MIntArray result;
	MGlobal::executeCommand(buffer, result, false, false);
	if (!result.length()) return;

	int mode = 1;
	if (result[0] == 1) mode = 3;

	MGlobal::executeCommand("select -cl;");
	SGExecuteCommand(false, "displaySmoothness -po %d %s;", mode, fnMesh.partialPathName().asChar());
	if (mode == 3) {
		SGExecuteCommand(false, "setWireframeOnShadedOption false %s;", pannelName.asChar());
	}
	else {
		SGExecuteCommand(false, "setWireframeOnShadedOption true %s;", pannelName.asChar());
	}
}


void SGEvent::softSelectEvent() {

	static bool softSelectPressed = false;
	static bool softSelectEdited = false;
	static bool softSelectMoved = false;

	if (m_middlePressed) {
		softSelectPressed = false;
		softSelectEdited = false;
		softSelectMoved = false;
	}

	if (SGKey::key("b")->m_eventType == SGKey::kPress) {
		softSelectPressed = true;
		softSelectEdited = false;
	}
	else if (SGKey::key("b")->m_eventType == SGKey::kRelease && softSelectPressed ) {
		if (!softSelectMoved && !softSelectEdited) SGFunction::toggleSoftSelection();
		softSelectPressed = false;
	}

	if ((softSelectPressed || softSelectMoved) && m_leftPressed && m_mouseMove) {
		if (!softSelectMoved) {
			SGFunction::prepairSoftSelection();
			softSelectMoved = true;
		}
		SGFunction::editSoftSelection();
	}

	if (softSelectMoved && m_leftJustRelease) {
		SGFunction::setSoftSelection();
		softSelectEdited = true;
		softSelectMoved = false;
	}
}



void SGEvent::moveBrushEvent() {
	
	if (m_middleJustPress) {
		SGFunction::prepairMoveBrushRadius();
	}

	if (!m_middlePressed) {
		SGFunction::updateMoveBrushCenter();
	}

	if (m_middlePressed && SGKey::key("b")->m_condition == SGKey::kPressed && m_mouseMove ) {
		SGFunction::editMoveBrushRadius();
	}
}