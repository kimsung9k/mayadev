#ifndef _sgCurveDraw_h
#define _sgCurveDraw_h

#include <maya/MStatus.h>
#include <maya/MArgList.h>
#include <maya/MEvent.h>
#include <maya/MPxToolCommand.h>
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

#include <maya/MPxGlBuffer.h>

#include <maya/MFnNurbsCurve.h>
#include <maya/MFnNurbsCurveData.h>

#include <maya/MEulerRotation.h>
#include <maya/MTransformationMatrix.h>

#include <maya/MMeshIntersector.h>

#include <maya/MSelectionList.h>

#include <maya/MGlobal.h>

#include <maya/MCursor.h>

class sgCurveDraw_ToolCommand : public MPxToolCommand
{
public:
	sgCurveDraw_ToolCommand();
	virtual ~sgCurveDraw_ToolCommand();
	static void* creator();

	virtual MStatus doIt( const MArgList& args );
	virtual MStatus redoIt();
	virtual MStatus undoIt();
	bool    isUndoable() const;
	virtual MStatus finalize();

	MDagPath m_dagPathOrigCurve;
	MPointArray m_curve_points;
	MObject m_oCurveTransform;

	bool m_editMode;

	double m_startParam;
	double m_endParam;
	bool   m_paramIsLocked;

	MPointArray m_pointsCVsOrig;
};



class sgCurveDraw_context : public MPxSelectionContext
{
public:
	sgCurveDraw_context();
	virtual ~sgCurveDraw_context();

	virtual void toolOnSetup( MEvent& evt );
	virtual void toolOffCleanup();
	virtual void getClassName( MString& name ) const;

	virtual MStatus doPress( MEvent& evt );
	virtual MStatus doDrag( MEvent& evt );
	virtual MStatus doRelease( MEvent& evt );

	MStatus getShapeNode( MDagPath& dagPath );
	MStatus drawCurve( int mouseX, int mouseY );
	MStatus createWorldCurve( const MDagPath& dagPathCurve );

	double getClosestParamFromCurveWidthRay( MPoint pointNear, MVector rayDir, MObject oCurve );
	MPoint getClosestPoint_of_rayAndCurve( MPoint pointCam, MVector vectorDir, MObject oCurve );

	MDagPath m_dagPathOrigCurve;
	MObject m_oWorldCurve;
	M3dView  m_view;
	MDagPath m_dagPathCam;
	MPointArray m_pointsDrawed;

	sgCurveDraw_ToolCommand* m_pContextCommand;

	bool   m_lockParam;
	double m_currentParam;
	double m_startParam;
	double m_paramLast;

	MObject m_oDisplayCurve;

	MStatus doPtrMoved(MEvent& evt);
	MStatus doPtrMoved(MEvent &, MHWRender::MUIDrawManager &, MHWRender::MFrameContext const &);

	bool   m_editMode;
};

#endif