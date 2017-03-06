#ifndef _multMatrixDecompose_h
#define _multMatrixDecompose_h

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MTypeId.h> 
#include <maya/MMatrix.h>

class multMatrixDecompose : public MPxNode
{
public:
						multMatrixDecompose();
	virtual				~multMatrixDecompose(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& block );
	virtual MStatus     setDependentsDirty( const MPlug& plug, MPlugArray& plugArr );

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

	static  MObject     aOutputMatrix;
	static  MObject     aOutputInverseMatrix;

	static  MObject     aOutputDistance;

	static	MTypeId		id;

private:
	bool m_isDirty;
	bool m_bInverseTrans;
	bool m_bInverseDist;

	MMatrix m_multMtx;
};

#endif