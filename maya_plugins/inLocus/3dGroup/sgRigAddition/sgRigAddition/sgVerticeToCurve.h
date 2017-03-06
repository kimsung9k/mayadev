#ifndef _sgVerticeToCurve
#define _sgVerticeToCurve


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



class VerticeIdsArray
{
public:
	VerticeIdsArray()
	{
		m_length = 0;
		m_pIds = new MIntArray[0];
	}
	~VerticeIdsArray()
	{
		delete[] m_pIds;
	}
	
	unsigned int length()
	{
		return m_length;
	}

	void setLength( unsigned int length )
	{
		if( this->m_length == length ) return;
		this->m_length = length;
		delete[] m_pIds;
		m_pIds = new MIntArray[ length ];
	}

	MIntArray& operator[]( unsigned int index ) const
	{
		return m_pIds[ index ];
	}
private:
	unsigned int m_length;
	MIntArray* m_pIds;
};


 
class sgVerticeToCurve : public MPxNode
{
public:
						sgVerticeToCurve();
	virtual				~sgVerticeToCurve();

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );
	virtual MStatus     setDependentsDirty( const MPlug& plug, MPlugArray& plugArr );

	static  void*		creator();
	static  MStatus		initialize();

public:
	static  MObject		aInputMesh;
	static  MObject		aInputMeshMatrix;
	static  MObject     aInput;
		static  MObject   aParentInverseMatrix;
		static  MObject   aDegree;
		static  MObject   aVerticeIds;
	static  MObject     aOutputCurve;

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

	MMatrixArray m_mtxArrParentInverse;
	MObjectArray m_oArrOutputCurve;

	VerticeIdsArray m_verticeIdsArray;
};

#endif