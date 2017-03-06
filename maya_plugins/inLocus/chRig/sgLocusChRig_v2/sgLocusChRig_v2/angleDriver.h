#ifndef _angleDriver_h
#define _angleDriver_h

#include <maya/MPxNode.h>
#include <maya/MTypeId.h> 

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>

#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnEnumAttribute.h>

#include <maya/MVector.h>
#include <maya/MMatrix.h>

#include <maya/MGlobal.h>


class angleDriver : public MPxNode
{
public:
	angleDriver();
	virtual ~angleDriver();

	virtual MStatus  compute( const MPlug& plug, MDataBlock& data );

	virtual MStatus  setDependentsDirty( const MPlug& plug, MPlugArray& plugArray );
	void    getAngleMatrix( MMatrix& angleMatrix, int aimIndex );

	static  void* creator();
	static  MStatus  initialize();

public:
	static  MObject  aBaseMatrix;
	static  MObject  aUpVectorMatrix;
	static  MObject  aAngleMatrix;
	static  MObject  aAxis;

	static  MObject  aOutDriver;;
	static  MObject  aOutMatrix;

	static  MTypeId  id;

public:
	bool baseMatrixRequire;
	bool aimAxisRequire;

	MMatrix  baseMatrix;
	MMatrix  baseInvMatrix;
	MMatrix  upVectorMatrix;
	int  aimAxisNum;

	MMatrix buildMatrix;
	double firstValue;
	double secondValue;
	double thirdValue;
};


#endif