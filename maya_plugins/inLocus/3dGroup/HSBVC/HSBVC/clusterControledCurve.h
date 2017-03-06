#ifndef _clusterControledCurve_h
#define _clusterControledCurve_h

#include <maya/MPxNode.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MTypeId.h> 

#include <maya/MPlugArray.h>

#include  <maya/MFnDependencyNode.h>

#include  <maya/MFnNurbsCurveData.h>
#include  <maya/MFnNurbsCurve.h>

#include <maya/MMatrix.h>
#include <maya/MFnMatrixData.h>

#include <maya/MArrayDataBuilder.h>

#include <maya/MPointArray.h>
#include <maya/MFloatArray.h>

#include <maya/MGlobal.h>

class clusterControledCurve : public MPxNode
{
public:
						clusterControledCurve();
	virtual				~clusterControledCurve(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

	MStatus updateBindPreMatrix();
	MStatus updatePointWeights(  MObject oInputCurve,
		                         MMatrix mtxInputCurve,
								 MArrayDataHandle& hArrMatrix,
								 MArrayDataHandle& hArrBindPreMatrix );
	MStatus updateBindPreMatrix( MObject oInputCurve,
		                         MMatrix mtxInputCurve,
								 MArrayDataHandle& hArrMatrix,
								 MArrayDataHandle& hArrBindPreMatrix,
								 bool updateWeight );

	virtual  MStatus    setDependentsDirty( const MPlug &plug, MPlugArray& plugArray );

public:

	static  MObject     aInputCurve;
	static  MObject     aInputCurveMatrix;

	static  MObject     aDumyMatrix;

	static  MObject     aBindPreMatrix;
	static  MObject     aMatrix;

	static  MObject     aWeightList;
		static  MObject    aWeights;

	static  MObject     aUpdate;

	static  MObject		aOutputCurve;

	static	MTypeId		id;

public:
	MMatrix* bindPreMatrix;
	float** setWeights;
	int beforeNumCV;
	int beforeNumMatrix;

	bool requireUpdate;
};

#endif
