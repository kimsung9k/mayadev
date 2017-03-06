#ifndef _blendCurve_h
#define _blendCurve_h


#include <maya/MPxDeformerNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MTypeId.h>
#include <maya/MPlug.h>
#include <maya/MDataBlock.h>

#include <maya/MVector.h>
#include <maya/MPoint.h>
#include <maya/MPointArray.h>
#include <maya/MMatrix.h>

#include <maya/MFnNurbsCurve.h>
#include <maya/MItGeometry.h>

#include <maya/MFnDependencyNode.h>
#include <maya/MDagPath.h>

#include <maya/MGlobal.h>


class inputInfo
{
public:
	
	inputInfo()
	{
		points.setLength( 0 );
		weight  = 0.0f;
		blendPosition = 0.0f;
		blendArea = 0.0f;
	}

	bool        isCurveDirty;
	bool        isValuesDirty;

	MPointArray points;
	float       weight;
	float       blendPosition;
	float       blendArea;
};


class inputInfoArray
{
public:
	inputInfoArray()
	{
		pInputInfo = new inputInfo[0];
	}
	~inputInfoArray()
	{
		delete[] pInputInfo;
	}
	
	void setLength( unsigned int length )
	{
		inputInfo* tempP_inputInfo;
		tempP_inputInfo = new inputInfo[ length ];

		for( unsigned int i=0; i< length; i++ )
		{
			if( i + 1 < this->length ) break;
			tempP_inputInfo[i] = pInputInfo[i];
		}

		delete[] pInputInfo;
		pInputInfo = tempP_inputInfo;
		this->length = length;
	}

	inputInfo& operator[]( const unsigned int index )
	{
		return pInputInfo[ index ];
	}

	inputInfo*   pInputInfo;
	unsigned int length;
};


class blendCurve : public MPxDeformerNode
{
public:
						blendCurve();
	virtual				~blendCurve();
	
	virtual MStatus deform( MDataBlock& data, MItGeometry& iter, const MMatrix& mat, unsigned int multiIndex );
	virtual MStatus setDependentsDirty( const MPlug& plug, MPlugArray& plugArr );

	MStatus setCleanInputGeom( MItGeometry& iter );
	MStatus getInputsValues( MDataBlock& data );
	MStatus setClean( MItGeometry& iter );

	static  void*		creator();
	static  MStatus		initialize();

public:
	static  MObject  aInputs;
		static  MObject aInputCurve;
		static  MObject aWeight;
		static  MObject aBlendPosition;
		static  MObject aBlendArea;

	static  MTypeId  id;
public:
	inputInfoArray m_inputInfoArray;

	bool m_isInputGeomDirty;
	bool m_lengthDirty;
	MPointArray m_pointArr;
};


#endif