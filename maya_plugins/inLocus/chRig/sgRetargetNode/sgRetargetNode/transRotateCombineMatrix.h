#ifndef _transRotateCombineMatrix_h
#define _transRotateCombineMatrix_h


#include <maya/MPxNode.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MTypeId.h> 

 
class transRotateCombineMatrix : public MPxNode
{
public:
						transRotateCombineMatrix();
	virtual				~transRotateCombineMatrix(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

public:
	static MStatus attributeAffectsArray( MObject& affectAttr, MObject** affectedAttrs );

public:

	static  MObject		aInputTransMatrix;
	static  MObject		aInputRotateMatrix;

	static  MObject     aOutputMatrix;
	static  MObject     aOutputInverseMatrix;

	static	MTypeId		id;
};

#endif
