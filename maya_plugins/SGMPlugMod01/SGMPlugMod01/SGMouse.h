#pragma once

#include <SGBase.h>
#include <QtGui/qevent.h>


class SGMouse
{
public:
	enum MouseCondition
	{
		kNoneCondition,
		kPressed,
		kReleased,
		kWheel
	};
	enum MouseEventType
	{
		kNone,
		kMove,
		kPress,
		kRelease,
		kDbClick
	};

	SGMouse(Qt::MouseButton button);
	static SGMouse* btn(Qt::MouseButton button);
	static bool translateEvent(QEvent* evt);
	static void initializeButtons();
	static vector<SGMouse> BUTTONS;

	static int x;
	static int y;
	static int origX;
	static int origY;
	static int offsetX;
	static int offsetY;
	

	Qt::MouseButton  m_button;
	MouseEventType   m_eventType;
	MouseCondition   m_condition;

	static Qt::MouseButton button;
	static MouseEventType eventType;
	static MouseCondition condition;
};