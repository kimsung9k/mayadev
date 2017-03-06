#ifndef _SGMTool_h
#define _SGMTool_h

#include "SGBase.h"

#include <maya/MStatus.h>
#include <maya/MArgList.h>
#include <maya/MEvent.h>
#include <maya/MPxContext.h>
#include <maya/MPxSelectionContext.h>

#include <maya/M3dView.h>
#include <maya/MDagPath.h>
#include <maya/MDagPathArray.h>
#include <maya/MSelectionList.h>
#include <maya/MItSelectionList.h>
#include <maya/MFnDagNode.h>
#include <maya/MFnTransform.h>
#include <maya/MFnMesh.h>

#include <maya/MVector.h>
#include <maya/MPoint.h>
#include <maya/MMatrix.h>
#include <maya/MPointArray.h>
#include <maya/MFloatPointArray.h>
#include <maya/MFloatArray.h>
#include <maya/MDagModifier.h>

#include <maya/MEulerRotation.h>
#include <maya/MTransformationMatrix.h>

#include <maya/MMeshIntersector.h>

#include <maya/MSelectionList.h>

#include <maya/MPlug.h>
#include <maya/MGlobal.h>
#include <maya/MCursor.h>

#include <QtCore/qobject.h>
#include <QtGui/qevent.h>
#include <QtGui/qwidget.h>
#include <QtOpenGL/qgl.h>


class SGToolContext : public MPxSelectionContext
{
public:
	SGToolContext();
	virtual ~SGToolContext();

	virtual void toolOnSetup(MEvent& evt);
	virtual void toolOffCleanup();
	virtual void getClassName(MString& name) const;

	MStatus doPtrMoved(MEvent& evt);
	MStatus doPtrMoved(MEvent &,  MHWRender::MUIDrawManager &,  MHWRender::MFrameContext const &);

	MObject  m_oManip;
	QWidget* m_mainWindow;
};

#endif