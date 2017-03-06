#ifndef _retargetBlender_h
#define _retargetBlender_h

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MObjectArray.h>
#include <maya/MTypeId.h> 

 
class retargetBlender : public MPxNode
{
public:
						retargetBlender();
	virtual				~retargetBlender(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize(); 

	static  MStatus  attributeAffectsArray( MObject &affectAttr, MObject** affectedAttrs );

public:

	static  MObject     aInput;
		static	MObject     aWeight;
		static  MObject     aTransMatrix;
		static  MObject     aOrientMatrix;
		static  MObject     aUdAttr;

	static	MObject     aOrient;
		static	MObject     aOrientX;
		static	MObject     aOrientY;
		static	MObject     aOrientZ;

	static MObject     aOutTrans;
		static MObject     aOutTransX;
		static MObject     aOutTransY;
		static MObject     aOutTransZ;
    static MObject     aOutOrient;
		static MObject     aOutOrientX;
		static MObject     aOutOrientY;
		static MObject     aOutOrientZ;
	static MObject     aOutUdAttr;

	static	MTypeId		id;
};

#endif
