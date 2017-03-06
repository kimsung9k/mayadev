#ifndef _sgMultMatrixDecompose_h
#define _sgMultMatrixDecompose_h

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MTypeId.h> 

class sgMultMatrixDecompose : public MPxNode
{
public:
						sgMultMatrixDecompose();
	virtual				~sgMultMatrixDecompose(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& block );

	static  void*		creator();
	static  MStatus		initialize();

public:
	static  MObject     aMatrixIn;

	static  MObject     aInverseTranslate;
	static  MObject     aInverseDistance;

	static  MObject     aOutputTranslate;
		static  MObject     aOutputTranslateX;
		static  MObject     aOutputTranslateY;
		static  MObject     aOutputTranslateZ;
	static  MObject     aOutputRotate;
		static  MObject     aOutputRotateX;
		static  MObject     aOutputRotateY;
		static  MObject     aOutputRotateZ;
	static  MObject     aOutputScale;
		static  MObject     aOutputScaleX;
		static  MObject     aOutputScaleY;
		static  MObject     aOutputScaleZ;
	static  MObject     aOutputShear;
		static  MObject     aOutputShearX;
		static  MObject     aOutputShearY;
		static  MObject     aOutputShearZ;

	static	MTypeId		id;
};

#endif