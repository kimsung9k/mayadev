#ifndef _CreateJointContext_h
#define _CreateJointContext_h

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

#include <maya/MEulerRotation.h>
#include <maya/MTransformationMatrix.h>

#include <maya/MMeshIntersector.h>

#include <maya/MSelectionList.h>

#include <maya/MGlobal.h>
#include <maya/MCursor.h>

class CreateJointToolCommand : public MPxToolCommand
{
public:
	CreateJointToolCommand();
	virtual ~CreateJointToolCommand();
	static void* creator();

	virtual MStatus doIt( const MArgList& args );
	virtual MStatus redoIt();
	virtual MStatus undoIt();
	bool    isUndoable() const;
	virtual MStatus finalize();

	MObject m_oJoint;
	MSelectionList m_beforeSelect;
};


class CreateJointContext : public MPxSelectionContext
{
public:
	CreateJointContext();
	virtual ~CreateJointContext();

	virtual void toolOnSetup( MEvent& evt );
	virtual void toolOffCleanup();
	virtual void getClassName( MString& name ) const;

	virtual MStatus doPress( MEvent& evt );
	virtual MStatus doDrag( MEvent& evt );
	virtual MStatus doRelease( MEvent& evt );

	MStatus getSelection( MDagPathArray& pathArr );
	MStatus getMeshIntersection( int x, int y, MPointArray& pointArr );
	MPoint  getCenterPoint( const MPointArray& pointArr );
	MStatus setUpdateCondition( const MSelectionList& beforeList,
		                        const MSelectionList& afterList,
								const MPoint worldPosition );

	M3dView       m_view;
	MDagPath      m_pathCamera;
	MDagPathArray m_geometry;
	MPointArray   m_pointsIntersect;
	int           m_closeGeoIndex;
	MSelectionList m_beforeSelect;
	MSelectionList m_afterSelect;
};

#endif