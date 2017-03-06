#include "precompile.h"

#include "SGMouse.h"
#include <maya/M3dView.h>


int SGMouse::x;
int SGMouse::y;
int SGMouse::origX;
int SGMouse::origY;
int SGMouse::offsetX = -10;
int SGMouse::offsetY = 10;
vector<SGMouse> SGMouse::BUTTONS;

SGMouse::MouseEventType SGMouse::eventType;
SGMouse::MouseCondition SGMouse::condition;
Qt::MouseButton         SGMouse::button;


SGMouse::SGMouse(Qt::MouseButton button) {
	m_button = button;
}


void SGMouse::initializeButtons()
{
	SGMouse::BUTTONS.clear();
	SGMouse::BUTTONS.push_back(SGMouse(Qt::NoButton));
	SGMouse::BUTTONS.push_back(SGMouse(Qt::LeftButton));
	SGMouse::BUTTONS.push_back(SGMouse(Qt::MiddleButton));
	SGMouse::BUTTONS.push_back(SGMouse(Qt::RightButton));
}


SGMouse* SGMouse::btn(Qt::MouseButton button)
{
	for (int i = 0; i < BUTTONS.size(); i++){
		if (BUTTONS[i].m_button == button) return &BUTTONS[i];
	}
	return NULL;
}


bool SGMouse::translateEvent(QEvent* evt)
{
	QMouseEvent* mouseEvent;

	for (int i = 0; i < BUTTONS.size(); i++) {
		BUTTONS[i].m_eventType = SGMouse::kNone;
	}

	if (evt->type() == QEvent::MouseMove ||
		evt->type() == QEvent::MouseButtonPress ||
		evt->type() == QEvent::MouseButtonRelease ||
		evt->type() == QEvent::MouseButtonDblClick )
	{
		mouseEvent = (QMouseEvent*)evt;
		button = ((QMouseEvent*)evt)->button();
	}
	else return false;

	if (evt->type() == QEvent::MouseMove)
	{
		M3dView activeView = M3dView().active3dView();
		SGMouse::origX = mouseEvent->x();
		SGMouse::origY = activeView.portHeight() - mouseEvent->y();
		SGMouse::x = SGMouse::origX + SGMouse::offsetX;
		SGMouse::y = SGMouse::origY + SGMouse::offsetY;
		for (int i = 0; i < BUTTONS.size(); i++)
			BUTTONS[i].m_eventType = kMove;
		eventType = kMove;
		return true;
	}

	
	SGMouse* mouse = SGMouse::btn(button);
	if (mouse == NULL) {
		eventType = kNone;
		return false;
	}

	if (evt->type() == QEvent::MouseButtonPress) {
		mouse->m_condition = kPressed;
		mouse->m_eventType = kPress;
		condition = kPressed;
		eventType = kPress;
	}
	else if (evt->type() == QEvent::MouseButtonRelease) {
		mouse->m_condition = kReleased;
		mouse->m_eventType = kRelease;
		condition = kReleased;
		eventType = kRelease;
	}
	else if (evt->type() == QEvent::MouseButtonDblClick) {
		//sgPrintf("double click");
		mouse->m_eventType = kDbClick;
		eventType = kDbClick;
	}

	return true;
}