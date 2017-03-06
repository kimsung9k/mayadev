#ifndef _sgHair_cutInfo_h
#define _sgHair_cutInfo_h


#include <maya/MPlug.h>
#include <maya/MPlugArray.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MMatrix.h>
#include <maya/MObject.h>
#include <maya/MPoint.h>w
#include <maya/MPointArray.h>
#include <maya/MDoubleArray.h>
#include <maya/MStatus.h>
#include <maya/MItGeometry.h>
#include <maya/MFnIntArrayData.h>
#include <maya/MFnMesh.h>
#include <maya/MFnNurbsCurve.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MPxNode.h>
#include <maya/MTypeId.h>
#include <maya/MStatus.h>

#include <maya/MMeshIntersector.h>

#include <maya/MFnNurbsCurve.h>
#include <maya/MFnNurbsCurveData.h>


class sgHair_cutInfo : public MPxNode
{
public:
	sgHair_cutInfo();
	virtual ~sgHair_cutInfo();

	virtual MStatus  compute( const MPlug& plug, MDataBlock& data );
	static  void*    creator();
	static  MStatus  initialize();

	MStatus getOutput();
	virtual MStatus  setDependentsDirty( const MPlug& plug, MPlugArray& plugArr );

	static  MObject  aInputMeshMatrix;
	static  MObject  aInputMesh;
	static  MObject  aInputCurveMatrix;
	static  MObject  aInputCurve;
	static  MObject  aOutput;
		static  MObject  aOutU;
		static  MObject  aOutV;
		static  MObject  aOutParam;
		static  MObject  aOutPoint;
			static  MObject aOutPointX;
			static  MObject aOutPointY;
			static  MObject aOutPointZ;

	static  MTypeId  id;

private:
	MMatrix  m_mtxInputCurve;
	MMatrix  m_mtxInputMesh;
	MObject  m_oMeshBase;
	MObject  m_oCurveBase;

	MPoint   m_pointClose;

	double   m_outU;
	double   m_outV;
	double   m_outParam;
};


#endif