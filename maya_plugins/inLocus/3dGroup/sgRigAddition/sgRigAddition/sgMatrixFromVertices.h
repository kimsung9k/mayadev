#ifndef _sgMatrixFromVertices
#define _sgMatrixFromVertices


#include <maya/MPxNode.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MArrayDataBuilder.h>
#include <maya/MFnGenericAttribute.h>
#include <maya/MTypeId.h>

#include <maya/MFnMesh.h>
#include <maya/MFnNurbsCurve.h>
#include <maya/MFnNurbsCurveData.h>
#include <maya/MFnMatrixData.h>

#include <maya/MPointArray.h>

#include <maya/MMatrix.h>
#include <maya/MMatrixArray.h>
#include <maya/MVector.h>


 
class sgMatrixFromVertices : public MPxNode
{
public:
						sgMatrixFromVertices();
	virtual				~sgMatrixFromVertices();

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );
	virtual MStatus     setDependentsDirty( const MPlug& plug, MPlugArray& plugArr );

	static  void*		creator();
	static  MStatus		initialize();

public:
	static  MObject		aInputMesh;
	static  MObject		aInputMeshMatrix;
	static  MObject     aVerticeId;
	static  MObject     aOutputMatrix;
	static  MObject     aOutputTranslate;
		static  MObject     aOutputTranslateX;
		static  MObject     aOutputTranslateY;
		static  MObject     aOutputTranslateZ;

	static	MTypeId		id;

private:
	bool   m_isDirtyMesh;
	bool   m_isDirtyMeshMatrix;
	bool   m_isDirtyInput;
	MIntArray m_inputIsDirty;

	MObject  m_oMesh;
	MMatrix  m_mtxMesh;

	unsigned int m_numPolygon;
	MPointArray m_pointsInputMesh;
};

#endif