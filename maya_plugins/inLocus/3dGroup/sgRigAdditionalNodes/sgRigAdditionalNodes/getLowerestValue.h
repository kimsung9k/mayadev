#ifndef _getLowerestValue_h
#define _getLowerestValue_h


#include <maya/MPxDeformerNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MTypeId.h>
#include <maya/MPlug.h>
#include <maya/MDataBlock.h>

#include <maya/MGlobal.h>


class getLowerestValue : public MPxNode
{
public:
						getLowerestValue();
	virtual				~getLowerestValue();
	
	virtual MStatus     compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

public:
	static  MObject  aInputValue;
	static  MObject  aOutputValue;

	static  MTypeId  id;
};


#endif