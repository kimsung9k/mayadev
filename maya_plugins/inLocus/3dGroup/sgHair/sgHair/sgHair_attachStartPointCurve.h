#ifndef _sgHair_attachStartPointCurve_h
#define _sgHair_attachStartPointCurve_h


#include <maya/MPlug.h>
#include <maya/MPlugArray.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MMatrix.h>
#include <maya/MObject.h>
#include <maya/MPoint.h>
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

#include <maya/MFnNurbsCurve.h>
#include <maya/MFnNurbsCurveData.h>


class sgHair_attachStartPointCurve : public MPxNode
{
public:
	sgHair_attachStartPointCurve();
	virtual ~sgHair_attachStartPointCurve();

	virtual MStatus  compute( const MPlug& plug, MDataBlock& data );
	static  void*    creator();
	static  MStatus  initialize();

	MStatus checkAndCreateCurveAndGetPosition();
	MStatus editPositionByMatrix();

	virtual MStatus  setDependentsDirty( const MPlug& plug, MPlugArray& plugArr );

	static  MTypeId  id;

	static  MObject  aInputMatrix;
	static  MObject  aInputCurveMatrix;
	static  MObject  aInputCurve;
	static  MObject  aOutputCurve;

private:
	int      m_numCVs;


	MMatrix     m_mtxInput;
	MMatrix     m_mtxInputCurve;
	MObject     m_oInputCurve;
	MObject     m_oOutCurve;
	MPointArray m_outputPoints;

	MFnNurbsCurve m_fnCurve;

	bool     m_isDirtyInputMatrix;
	bool     m_isDirtyInputCurveMatrix;
	bool     m_isDirtyInputCurve;
};

#endif