#pragma once

#include <maya/MGlobal.h>
#include <maya/MObject.h>
#include <maya/MFloatArray.h>
#include <maya/MPointArray.h>
#include <maya/MMatrixArray.h>
#include <QtCore/qobject.h>
#include <QtGui/qevent.h>
#include "SGGeneralManip.h"
#include "SGTransformManip.h"
#include "SGNormalManip.h"
#include "SGPolySplitManip.h"
#include "SGPolygonManip.h"
#include "SGSoftSelectionManip.h"
#include "SGDragSelectionManip.h"
#include "SGMoveBrushManip.h"


class SGEvent : public QObject
{
public:
	SGEvent();
	~SGEvent();

	virtual bool eventFilter(QObject* object, QEvent* evt);

	bool isAutoRepeat(QEvent* evt);

	void camFocusEvent();
	void deleteEvent();

	bool firstEvent;

	void edgeSlideEvent();
	bool edgeSplitPointPushed;
	void edgeSplitEvent();
	void edgeSplitRingEvent();
	void edgeBevelEvent();

	void getIntersection();
	void getGeneralIntersection();

	void markingMenuEvent();
	void vertexMoveEvent();

	void saveEvent();

	void selectEvent();
	void selectDragEvent();
	bool smoothMode;
	void smoothDisplay();

	void softSelectEvent();

	void moveBrushEvent();

	void manipUpdate();

	MMatrixArray   camMatrixList;

	//translate
	bool translateEvent( QEvent* evt );
	void updateCamMatrix();

	bool m_isMouseEvent;
	bool m_isKeyEvent;

	bool m_altPressed;
	bool m_controlJustPress;
	bool m_controlJustRelease;
	bool m_controlPressed;
	bool m_shiftPressed;
	bool m_mouseMove;
	bool m_mouseJustPress;
	bool m_mouseJustRelease;
	bool m_mousePressed;
	bool m_leftJustPress;
	bool m_leftJustRelease;
	bool m_leftPressed;
	bool m_rightJustPress;
	bool m_rightJustRelease;
	bool m_rightPressed;
	bool m_middleJustPress;
	bool m_middleJustRelease;
	bool m_middlePressed;

	bool m_isDragSelecting;
};