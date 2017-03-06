#ifndef _sgLockAngleMatrix
#define _sgLockAngleMatrix


#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MTypeId.h>

#include <maya/MMatrix.h>
#include <maya/MVector.h>

 
class sgLockAngleMatrix : public MPxNode
{
public:
						sgLockAngleMatrix();
	virtual				~sgLockAngleMatrix();

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );
	virtual MStatus     setDependentsDirty( const MPlug& plug, MPlugArray& plugArr );

	static  void*		creator();
	static  MStatus		initialize();

	MMatrix  getsgLockAngleMatrix( const MMatrix& inputMatrix, unsigned char axis, double angle );

public:
	static  MObject		aBaseMatrix;
	static  MObject		aInputMatrix;
	static  MObject     aAngleAxis;
	static  MObject     aInputAngle;
	static  MObject     aOutputMatrix;

	static	MTypeId		id;

private:
	MMatrix  m_baseMatrix;
	MMatrix  m_inputMatrix;
	MMatrix  m_localMatrix;
	unsigned char m_angleAxis;
	double   m_inputAngle;
	MMatrix  m_mtxResult;
};

#endif