#include "precompile.h"
#include "SGWidget.h"
#include "SGMainWindowEvent.h"
#include <QtGui/qwidget.h>
#include <QtGui/qapplication.h>
#include <SGPrintf.h>
#include "SGKey.h"
#include "SGMouse.h"


extern SGEvent* toolEvent;


SGMainWindowEvent::SGMainWindowEvent() {
	toolEvent = new SGEvent();
	m_beforeWidget = NULL;
}

SGMainWindowEvent::~SGMainWindowEvent() {
	if (m_beforeWidget != NULL) {
		m_beforeWidget->releaseKeyboard();
		m_beforeWidget->removeEventFilter(toolEvent);
	}
	delete toolEvent;
}


bool SGMainWindowEvent::eventFilter(QObject* object, QEvent* evt) {
	QWidget* focusWidget = QApplication::focusWidget();
	if (focusWidget == NULL) return true;
	if (m_focusWidgetName == focusWidget->objectName().toStdString().c_str()) return QObject::eventFilter(object, evt);

	QObjectList objList = focusWidget->children();
	bool glWidgetExists = false;
	for (int i = 0; i < objList.length(); i++) {
		QWidget* widget = (QWidget*)objList[i];
		QObjectList objList2 = widget->children();
		for (int j = 0; j < objList2.length(); j++) {
			QWidget* widget2 = (QWidget*)objList2[j];
			if (strcmp(widget2->metaObject()->className(), "QmayaGLWidget") == 0) {
				if (m_beforeWidget != NULL) {
					m_beforeWidget->releaseKeyboard();
					m_beforeWidget->removeEventFilter(toolEvent);
				}
				widget2->installEventFilter(toolEvent);
				widget2->grabKeyboard();

				m_beforeWidget = widget2;

				m_focusWidgetName = focusWidget->objectName().toStdString().c_str();
				glWidgetExists = true;

				SGKey::initializeKeys();
				SGMouse::initializeButtons();
				break;
			}
		}
		if (glWidgetExists)break;
	}

	if (!glWidgetExists) {
		if (m_beforeWidget != NULL) {
			m_beforeWidget->releaseKeyboard();
			m_beforeWidget->removeEventFilter(toolEvent);
		}
		m_focusWidgetName = focusWidget->objectName().toStdString().c_str();
	}

	return QObject::eventFilter(object, evt);
}