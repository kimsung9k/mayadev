#ifndef _sgKeyCurve_h
#define _sgKeyCurve_h

#include <maya/MPlugArray.h>
#include <maya/MPxDeformerNode.h>
#include <maya/MDataHandle.h>
#include <maya/MDataBlock.h>
#include <maya/MMatrix.h>
#include <maya/MItGeometry.h>
#include <maya/MStatus.h>
#include <maya/MTypeId.h>

#include <maya/MFnNumericAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnCompoundAttribute.h>

#include <maya/MTime.h>
#include <maya/MTimeArray.h>

#include <maya/MFnNurbsCurve.h>
#include <maya/MPointArray.h>
#include <maya/MVectorArray.h>
#include <maya/MMatrixArray.h>

#include <maya/MGlobal.h>

#include <maya/MCommandResult.h>
#include <maya/MTypeId.h>


class sgHair_keyCurve_keys
{
public:
	sgHair_keyCurve_keys()
	{
		m_pPointArr  = new MPointArray[0];
		m_pTime      = new MTime[0];
		m_pMatrix    = new MMatrix[0];
	}
	~sgHair_keyCurve_keys()
	{
		delete[] m_pPointArr;
		delete[] m_pTime;
		delete[] m_pMatrix;
	}
	void setLength( unsigned int length )
	{
		delete[] m_pPointArr;
		delete[] m_pTime;
		delete[] m_pMatrix;
		m_pPointArr  = new MPointArray[length];
		m_pTime      = new MTime[length];
		m_pMatrix    = new MMatrix[length];
		this->m_length = length;
	}
	unsigned int length() const
	{
		return m_length;
	}
	MTime& getTime( unsigned int index ) const
	{
		return m_pTime[index];
	}
	MPointArray& getPoints( unsigned int index ) const
	{
		return m_pPointArr[ index ];
	}
	MMatrix& getMatrix( unsigned int index ) const
	{
		return m_pMatrix[ index ];
	}

private:
	unsigned int  m_length;
	MTime*        m_pTime;
	MMatrix*      m_pMatrix;
	MPointArray*  m_pPointArr;
};



class sgHair_keyCurve : public MPxDeformerNode
{
public:
	sgHair_keyCurve();
	virtual ~sgHair_keyCurve();

	virtual MStatus deform( MDataBlock& data, MItGeometry& itGeo, const MMatrix& mtxGeo, unsigned int multIndex );
	virtual MStatus setDependentsDirty( const MPlug& plug, MPlugArray& plugArr );

	MStatus getOutputPoints( const MPointArray& inputPoints, MPointArray& outputPoints, const MMatrix& mtxBase,
		const MTime& time, const sgHair_keyCurve_keys& keys,
		const MTimeArray& timesSorted, const MIntArray& indicesSorted, float envValue );

	static void *creator();
	static MStatus initialize();

	static MTypeId id;

	static MObject aBaseLocalMatrix;
	static MObject aTime;
	static MObject aKeys;
		static MObject aKeyframe;
		static MObject aBaseMatrix;
		static MObject aInputCurve;

private:
	MPointArray  m_inputPoints;
	MMatrixArray m_matrixBases;
	MPointArray  m_outputPoints;

	bool m_isDirtyKeys;
	bool m_isDirtyInputGeom;
	bool m_isDirtyBaseMatrix;

	sgHair_keyCurve_keys m_keys;
	MIntArray m_indicesSorted;
	MTimeArray m_timesSorted;
};


#endif