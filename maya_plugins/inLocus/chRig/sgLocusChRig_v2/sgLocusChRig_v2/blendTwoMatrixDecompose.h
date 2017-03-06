#ifndef _blendTwoMatrixDecompose_h
#define _blendTwoMatrixDecompose_h

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MTypeId.h> 

class blendTwoMatrixDecompose : public MPxNode
{
public:
						blendTwoMatrixDecompose();
	virtual				~blendTwoMatrixDecompose(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& block );

	static  void*		creator();
	static  MStatus		initialize();

public:
	static  MObject     aMatrix1;
	static  MObject     aMatrix2;

	static  MObject     aBlender;

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