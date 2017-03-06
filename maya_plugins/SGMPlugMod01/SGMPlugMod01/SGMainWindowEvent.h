#pragma once

#include <SGBase.h>
#include "SGEvent.h"
#include "SGMainWindowEvent.h"
#include <QtCore/qobject.h>
#include <QtGui/qevent.h>


class SGMainWindowEvent : public QObject
{
public:
	SGMainWindowEvent();
	~SGMainWindowEvent();

	virtual bool eventFilter(QObject* object, QEvent* evt);
	QWidget* m_beforeWidget;
	MString m_focusWidgetName;
};