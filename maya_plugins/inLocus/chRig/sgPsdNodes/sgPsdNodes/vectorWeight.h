#ifndef _vectorWeight_h
#define _vectorWeight_h

#include <maya/MPxNode.h>
#include <maya/MPlug.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MDataBlock.h>
#include <maya/MObject.h>
#include <maya/MTypeId.h>
#include <maya/MGlobal.h>
#include <maya/MFloatArray.h>
#include <maya/MFloatVector.h>

#include <maya/MFnDoubleArrayData.h>


class vectorWeight : public MPxNode
{
public:
	         vectorWeight();
	virtual  ~vectorWeight();

	virtual MStatus compute( const MPlug& plug, MDataBlock& data );

	static void* creator();
	static MStatus initialize();

public:
	static MObject aInputVector;
	static MObject aBaseVector;
	static MObject aOutMinVector;
	static MObject aOutputWeight;

	static MTypeId  id;
};

float getFloatDist( MFloatArray& fArr );

MFloatArray normalizeArray( MFloatArray& fArr, float& dist );

float dotProductFloat( MFloatArray& fArr0, MFloatArray& fArr1 );

MFloatArray getMinVector( MFloatArray& base, MFloatArray& target, bool& success );

#endif