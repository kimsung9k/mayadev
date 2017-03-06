#ifndef _splineMatrix_h
#define _splineMatrix_h

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
#include <maya/MMatrixArray.h>
#include <maya/MFnMatrixData.h>

#include <maya/MArrayDataBuilder.h>

#include <maya/MPointArray.h>

#include <maya/MGlobal.h>

class splineMatrix : public MPxNode
{
public:
						splineMatrix();
	virtual				~splineMatrix(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

	MStatus updateCurveInfo(MObject oInputCurve );
	MMatrix* getMatrixArrayFromParamList( MMatrix upMatrix, double* paramList, MMatrix mtxCurve, MObject* p_oCurve, int paramListLength );

public:

	static  MObject     aInputCurve;
	static  MObject     aInputCurveMatrix;

	static  MObject     aTopMatrix;

	static  MObject     aAngleByTangent;
	
	static  MObject     aParameter;

	static  MObject		aOutputMatrix;

	static	MTypeId		id;

public:
	double minParam;
	double maxParam;
	bool angleByTangent;
};

#endif
