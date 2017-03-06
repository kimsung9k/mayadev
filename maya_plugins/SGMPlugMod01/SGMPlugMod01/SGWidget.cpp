#include "precompile.h"
#include "SGWidget.h"
#include <maya/M3dView.h>



SGWidget::SGWidget(QWidget* widget) {
	m_widget = widget;
}



void SGWidget::startEvent() {
	m_event = new SGMainWindowEvent();
	m_widget->installEventFilter(m_event);
}



void SGWidget::releaseEvent() {
	m_widget->removeEventFilter(m_event);
	delete m_event;
}