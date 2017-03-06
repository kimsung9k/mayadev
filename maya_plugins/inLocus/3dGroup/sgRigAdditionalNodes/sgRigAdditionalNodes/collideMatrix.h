#ifndef _collideMatrix_h
#define _collideMatrix_h


#include <maya/MPxNode.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MTypeId.h>
#include <maya/MPlug.h>
#include <maya/MDataBlock.h>

#include <maya/MTransformationMatrix.h>

#include <maya/MVector.h>
#include <maya/MPoint.h>
#include <maya/MMatrix.h>
#include <maya/MMatrixArray.h>
#include <maya/MFloatArray.h>

#include <maya/MFnDependencyNode.h>
#include <maya/MPlugArray.h>
#include <maya/MDagPath.h>

#include <maya/MGlobal.h>


class collideMatrix : public MPxNode
{
public:
						collideMatrix();
	virtual				~collideMatrix();
	
	virtual MStatus     compute( const MPlug& plug, MDataBlock& data );
	MStatus getResult( MMatrixArray& mtxArrCollide, const MFloatArray valuesCollide );

	static  void*		creator();
	static  MStatus		initialize();

public:
	static  MObject  aEnvelop;
	static  MObject  aCollideList;
		static   MObject  aCollideMatrix;
		static   MObject  aCollideRate;
	static  MObject  aCollideBaseMatrix;

	static  MObject  aOutMatrix;

	static  MTypeId  id;
};


#endif