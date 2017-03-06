#ifndef _sgCurveEditBrush_h
#define _sgCurveEditBrush_h

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

#include <maya/MEulerRotation.h>
#include <maya/MTransformationMatrix.h>

#include <maya/MMeshIntersector.h>

#include <maya/MSelectionList.h>

#include <maya/MGlobal.h>

#include "sgCurveEditBrush_manip.h"


class sgCurveEditBrush_dArrs
{
public:
	sgCurveEditBrush_dArrs()
	{
		pDoubleArray = new MDoubleArray[0];
	}
	~sgCurveEditBrush_dArrs()
	{
		delete[] pDoubleArray;
	}
	
	void setLength( unsigned int length )
	{
		delete[] pDoubleArray;
		pDoubleArray = new MDoubleArray[ length ];
	}

	MDoubleArray& operator[]( unsigned int index )const
	{
		return pDoubleArray[ index ];
	}

	MDoubleArray* pDoubleArray;
};


class sgCurveEditBrush_pointArrs
{
public:
	sgCurveEditBrush_pointArrs()
	{
		pPointArray = new MPointArray[0];
	}
	~sgCurveEditBrush_pointArrs()
	{
		delete[] pPointArray;
	}
	
	void setLength( unsigned int length )
	{
		delete[] pPointArray;
		pPointArray = new MPointArray[ length ];
	}

	MPointArray& operator[]( unsigned int index )const
	{
		return pPointArray[ index ];
	}

	MPointArray* pPointArray;
};


class sgCurveEditBrush_ToolCommand : public MPxToolCommand
{
public:
	sgCurveEditBrush_ToolCommand();
	virtual ~sgCurveEditBrush_ToolCommand();
	static void* creator();

	virtual MStatus doIt( const MArgList& args );
	virtual MStatus redoIt();
	virtual MStatus undoIt();
	bool    isUndoable() const;
	virtual MStatus finalize();

	MDagPathArray m_dagPathCurves;
	sgCurveEditBrush_pointArrs m_pointArrsCurvesBefore;
	sgCurveEditBrush_pointArrs m_pointArrsCurvesAfter;
};



class sgCurveEditBrush_context : public MPxSelectionContext
{
public:
	sgCurveEditBrush_context();
	virtual ~sgCurveEditBrush_context();

	virtual void toolOnSetup( MEvent& evt );
	virtual void toolOffCleanup();
	virtual void getClassName( MString& name ) const;

	virtual MStatus doPress( MEvent& evt );
	virtual MStatus doDrag( MEvent& evt );
	virtual MStatus doRelease( MEvent& evt );

	MStatus getShapeNode( MDagPath& dagPath );

	MStatus editCurve( MDagPath dagPathCurve,
		int beforeX, int beforeY, int currentX, int currentY, float radius,
		const MDoubleArray& dArrLength, MPointArray& pointArr );

	M3dView       m_view;
	MDagPath      m_pathCamera;
	MDagPathArray m_geometry;

	bool  m_radiusEditOn;
	float m_radiusCurrent;

	sgCurveEditBrush_manip* m_manipulator;
	MObject m_oManip;

	short m_radiusEditX;

	short m_mouseBeforeX;
	short m_mouseBeforeY;
	float m_beforeRadius;

	MDagPathArray m_dagPathCurves;
	sgCurveEditBrush_dArrs m_dArrsCurvesLength;

	sgCurveEditBrush_ToolCommand* m_pToolCmd;
};

#endif