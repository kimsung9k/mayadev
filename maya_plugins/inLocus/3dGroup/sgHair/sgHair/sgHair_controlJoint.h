#ifndef _sgHair_controlJoint_h
#define _sgHair_controlJoint_h


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

#include <maya/MItDag.h>
#include <maya/MFnNurbsCurve.h>
#include <maya/MFnNurbsCurveData.h>


class sgHair_controlJoint : public MPxNode
{
public:
	sgHair_controlJoint();
	virtual ~sgHair_controlJoint();

	virtual MStatus  compute( const MPlug& plug, MDataBlock& data );
	static  void*    creator();
	static  MStatus  initialize();

	virtual MStatus  setDependentsDirty( const MPlug& plug, MPlugArray& plugArr );

	MMatrix buildMatrix( MVector vX, MVector vY, MVector vZ, MPoint pPoins );
	MMatrix getAngleWeightedMatrix( const MMatrix& targetMtx, double weight );
	void normalizeMatrix( MMatrix& matrix );
	void cleanMatrix( MMatrix& matrix );
	MStatus getTopJointFromPlug( const MPlug& plug, MObject& oTopJoint );
	MStatus getJointPositionBaseWorld();
	MStatus setGravityJointPositionWorld();
	MStatus setOutput();

	static  MTypeId  id;
	static  MObject  aInputBaseCurve;
	static  MObject  aInputBaseCurveMatrix;
	static  MObject  aJointParentBaseMatrix;

	static  MObject  aGravityParam;
	static  MObject  aGravityRange;
	static  MObject  aGravityWeight;
	static  MObject  aGravityOffsetMatrix;
	static  MObject  aStaticRotation;
	static  MObject  aOutput;
		static  MObject  aOutTrans;
			static  MObject  aOutTransX;
			static  MObject  aOutTransY;
			static  MObject  aOutTransZ;
		static  MObject  aOutOrient;
			static  MObject  aOutOrientX;
			static  MObject  aOutOrientY;
			static  MObject  aOutOrientZ;

private:
	bool m_isDirtyMatrix;
	bool m_isDirtyCurve;
	bool m_isDirtyGravityOption;
	bool m_isDirtyOthers;
	bool m_isDirtyParentMatrixBase;

	bool m_bStaticRotation;

	MMatrix      m_mtxBaseCurve;
	MMatrix      m_mtxJointParentBase;
	MPointArray  m_cvs;
	MMatrixArray m_mtxArrBase;
	MMatrixArray m_mtxArrGravityAdd;
	MVectorArray m_vectorArrTransJoint;
	MVectorArray m_vectorArrRotateJoint;

	MMatrix      m_mtxGravityOffset;
	double       m_paramGravity;
	double       m_rangeGravity;
	double       m_weightGravity;
};

#endif