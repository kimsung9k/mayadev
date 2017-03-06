#ifndef _udAttrBlender_h
#define _udAttrBlender_h

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MObjectArray.h>
#include <maya/MTypeId.h> 

 
class udAttrBlender : public MPxNode
{
public:
						udAttrBlender();
	virtual				~udAttrBlender(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize(); 

public:

	static  MObject     aProcessMessage;

	static  MObject     aInput;
		static  MObject     aWeight;
		static  MObject     aUdAttr;

	static MObject     aOutput;

	static	MTypeId		id;
};

#endif
