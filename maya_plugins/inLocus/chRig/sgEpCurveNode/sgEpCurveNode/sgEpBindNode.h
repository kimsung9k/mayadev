#ifndef _sgEpBindNode_h
#define _sgEpBindNode_h


#include <maya/MPxNode.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MArrayDataBuilder.h>
#include <maya/MTypeId.h> 


class sgEpBindNode : public MPxNode
{
public:
						sgEpBindNode();
	virtual				~sgEpBindNode(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

public:
	static  MObject     aEnvelope;
	static  MObject     aInputPoint;
		static  MObject     aInputPointX;
		static  MObject     aInputPointY;
		static  MObject     aInputPointZ;
	static  MObject		aMatrix;
	static  MObject     aOrigMatrix;  

	static  MObject     aOutputs;
		static  MObject		aOutputCurve;
		static  MObject     aOutputPoint;
			static  MObject     aOutputPointX;
			static  MObject     aOutputPointY;
			static  MObject     aOutputPointZ;

	static	MTypeId		id;
};

#endif
