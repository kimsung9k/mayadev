#ifndef _sgHair_controledCurve_h
#define _sgHair_controledCurve_h


#include <maya/MPlug.h>
#include <maya/MPlugArray.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MMatrix.h>
#include <maya/MMatrixArray.h>
#include <maya/MObject.h>
#include <maya/MPoint.h>
#include <maya/MPointArray.h>
#include <maya/MDoubleArray.h>
#include <maya/MStatus.h>
#include <maya/MFnTransform.h>
#include <maya/MItGeometry.h>
#include <maya/MFnIntArrayData.h>
#include <maya/MFnMesh.h>
#include <maya/MFnNurbsCurve.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnMessageAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MPxNode.h>
#include <maya/MTypeId.h>
#include <maya/MStatus.h>
#include <maya/MEulerRotation.h>
#include <maya/MDGContext.h>
#include <maya/MArrayDataBuilder.h>
#include <maya/MFnMatrixData.h>
#include <maya/MDagPath.h>

#include <maya/MItDag.h>
#include <maya/MFnNurbsCurve.h>
#include <maya/MFnNurbsCurveData.h>


class sgHair_controledCurve : public MPxNode
{
public:
	sgHair_controledCurve();
	virtual ~sgHair_controledCurve();

	virtual MStatus  compute( const MPlug& plug, MDataBlock& data );
	static  void*    creator();
	static  MStatus  initialize();

	virtual MStatus  setDependentsDirty( const MPlug& plug, MPlugArray& plugArr );
	MStatus updateObjectArray();
	MStatus updateJointPosition();

	static  MObject aTopJoint;
	static  MObject aEndJointMatrix;
	static  MObject aUpdateJoint;
	static  MObject aParentInverseMatrix;
	static  MObject aOutputCurve;

	static  MTypeId id;

private:
	bool    m_isDirtyJointMatrix;
	bool    m_isDirtyUpdate;

	MObjectArray m_oArrJoints;
	MObjectArray m_oArrTargets;
	MDoubleArray m_dArrKnots;
	MPointArray  m_pArrPosition;
	MPointArray  m_pArrPositionLocal;
	MObject      m_oDataCurve;
	MFnNurbsCurve m_fnCurve;
};

#endif