#ifndef _sgCurveFromPoints
#define _sgCurveFromPoints


#include <maya/MPxNode.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MArrayDataBuilder.h>
#include <maya/MTypeId.h>

#include <maya/MFnMesh.h>
#include <maya/MFnNurbsCurve.h>
#include <maya/MFnNurbsCurveData.h>
#include <maya/MFnMatrixData.h>

#include <maya/MPointArray.h>

#include <maya/MMatrix.h>
#include <maya/MMatrixArray.h>
#include <maya/MVector.h>


 
class sgCurveFromPoints : public MPxNode
{
public:
						sgCurveFromPoints();
	virtual				~sgCurveFromPoints();

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );
	virtual MStatus     setDependentsDirty( const MPlug& plug, MPlugArray& plugArr );

	static  void*		creator();
	static  MStatus		initialize();

public:
	static  MObject     aCreateType;
	static  MObject     aDegrees;
	static  MObject		aInput;
		static  MObject   aInputMatrix;
		static  MObject   aInputPoint;
			static  MObject  aInputPointX;
			static  MObject  aInputPointY;
			static  MObject  aInputPointZ;
	static  MObject     aOutputCurve;

	static	MTypeId		id;

private:
	bool  m_isDirtyCreate;
	bool  m_isDirtyDegrees;
	bool  m_isDirtyNumPoints;

	int   m_numPoints;
	int   m_createType;
	int   m_degree;

	MObject  m_oCurve;

	MPointArray   m_pointsWorld;
	MFnNurbsCurve m_fnCreateCurve;
};

#endif