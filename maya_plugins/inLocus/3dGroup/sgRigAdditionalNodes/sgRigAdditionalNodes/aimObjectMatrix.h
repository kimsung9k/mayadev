#ifndef _aimObjectMatrix_h
#define _aimObjectMatrix_h


#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MTypeId.h>
#include <maya/MPlug.h>
#include <maya/MDataBlock.h>

#include <maya/MTransformationMatrix.h>
#include <maya/MEulerRotation.h>

#include <maya/MVector.h>
#include <maya/MPoint.h>
#include <maya/MMatrix.h>

#include <maya/MFnNurbsCurve.h>

#include <maya/MFnDependencyNode.h>
#include <maya/MPlugArray.h>
#include <maya/MDagPath.h>

#include <maya/MGlobal.h>


class aimObjectMatrix : public MPxNode
{
public:
						aimObjectMatrix();
	virtual				~aimObjectMatrix();
	
	virtual MStatus     compute( const MPlug& plug, MDataBlock& data );

	MStatus caculate();
	MStatus getMatrixByCurve();

	virtual MStatus setDependentsDirty( const MPlug& plug, MPlugArray& plugArr );

	static  void*		creator();
	static  MStatus		initialize();

public:
	static  MObject  aByCurve;
	static  MObject  aInputCurve;
	static  MObject  aCurveMatrix;

	static  MObject  aAimAxis;
	static  MObject  aBaseMatrix;
	static  MObject  aTargetMatrix;
	static  MObject  aParentInverseMatrix;
	static  MObject  aOffset;
		static  MObject  aOffsetX;
		static  MObject  aOffsetY;
		static  MObject  aOffsetZ;
	static  MObject  aOutMatrix;
	static  MObject  aOutRotate;
		static  MObject  aOutRotateX;
		static  MObject  aOutRotateY;
		static  MObject  aOutRotateZ;
	static  MObject  aOutTranslate;
		static  MObject  aOutTranslateX;
		static  MObject  aOutTranslateY;
		static  MObject  aOutTranslateZ;

	static  MObject  aInverseAim;
	static  MObject  aWorldSpaceOutput;
	
	static  MTypeId  id;

public:
	bool     m_bBaseCurveModified;
	bool     m_bCurveMatrixModified;

	MMatrix  m_mtxBase;
	MMatrix  m_mtxTarget;
	unsigned int m_aimIndex;
	unsigned int m_upIndex;
	bool     m_inverseAim;

	bool     m_isOffsetDirty;

	MMatrix  m_mtxOffset;
	MMatrix  m_mtxOutput;
	MMatrix  m_mtxTransform;

	MFnNurbsCurve m_fnCurve;
	MMatrix  m_mtxCurve;
};


#endif