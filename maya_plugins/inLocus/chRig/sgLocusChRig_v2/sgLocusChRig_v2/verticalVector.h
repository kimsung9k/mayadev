#ifndef _verticalVector_h
#define _verticalVector_h

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MTypeId.h>

class verticalVector : public MPxNode
{
public:
						verticalVector();
	virtual				~verticalVector(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

public:
	static  MObject     aBaseVector;
		static  MObject     aBaseVectorX;
		static  MObject     aBaseVectorY;
		static  MObject     aBaseVectorZ;
	static  MObject     aInputVector;
		static  MObject     aInputVectorX;
		static  MObject     aInputVectorY;
		static  MObject     aInputVectorZ;

	static  MObject     aOutputInverse;
	static  MObject     aOutputNormalize;
	static  MObject     aOutputVector;
		static  MObject     aOutputVectorX;
		static  MObject     aOutputVectorY;
		static  MObject     aOutputVectorZ;

	static  MObject     aCrossInverse;
	static  MObject     aCrossNormalize;
	static  MObject     aCrossVector;
		static  MObject     aCrossVectorX;
		static  MObject     aCrossVectorY;
		static  MObject     aCrossVectorZ;

	static	MTypeId		id;
};

#endif