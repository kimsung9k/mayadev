#pragma once

#include "SGBase.h"
#include "SGMainWindowEvent.h"
#include <maya/MString.h>
#include <QtGui/qwidget.h>

class SGWidget
{
public:
	SGWidget( QWidget* widget );

	void startEvent();
	void releaseEvent();

	QWidget* m_widget;
	SGMainWindowEvent* m_event;
};