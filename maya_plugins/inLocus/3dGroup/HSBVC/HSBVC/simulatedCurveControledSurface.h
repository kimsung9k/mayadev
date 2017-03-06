#ifndef simulatedCurveControledSurface_h
#define simulatedCurveControledSurface_h

#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnUnitAttribute.h>

#include <maya/MPxNode.h>

#include <maya/MGlobal.h>

#include <maya/MFnNurbsCurve.h>
#include <maya/MFnNurbsSurface.h>
#include <maya/MFnNurbsSurfaceData.h>

#include <maya/MTypeId.h>

#include  <maya/MIntArray.h>
#include  <maya/MFloatArray.h>
#include  <maya/MPointArray.h>
#include  <maya/MVectorArray.h>
#include  <maya/MMatrixArray.h>

#include <maya/MThreadPool.h>

#include <maya/MPlugArray.h>

#include <Windows.h>

#define NUM_THREAD  32;

#define CHECK_TIME_INIT __int64 freq, start_, end; BOOL condition;


struct getLocalPointsTask
{
	MPointArray*  p_surfaceWorldPoints;
	MPointArray*  p_surfacePivPoints;
	MMatrixArray* p_upMatrixArr;
	MIntArray*    p_paramIndies;
	MFloatArray*  p_paramWeights;

	MPointArray*  p_returnPoints;
	MDoubleArray* p_paramRanges;
};

struct getLocalPointsThread
{
	int numThread;
	int start;
	int end;
	getLocalPointsTask* p_task;
};


struct getResultPointsTask
{
	MMatrix*      p_surfaceMatrix;
	MPointArray*  p_localPoints;
	MPointArray*  p_localPivots;
	MMatrixArray* p_upMatrixList;
	MDoubleArray* p_paramList;
	MPointArray*  p_returnPoints;
};

struct getResultPointsThread
{
	int numThread;
	int start;
	int end;
	double minParam;
	double maxParam;
	getResultPointsTask* p_task;
};


class simulatedCurveControledSurface : public MPxNode
{
public:
	                 simulatedCurveControledSurface();
	virtual          ~simulatedCurveControledSurface();
	
	virtual MStatus  compute( const MPlug& plug, MDataBlock& data );
	virtual MStatus  setDependentsDirty (const MPlug &plug, MPlugArray &plugArray);
	
	static void parallel_getLocalPoints( void* data, MThreadRootTask* root );
	static void parallel_getResultPoints( void* data, MThreadRootTask* root );
	static  MThreadRetVal compute_getLocalPoints( void* data );
	static MThreadRetVal compute_getResultPoints( void* data );
	void getLocalPointsFromSurface( MFnNurbsSurface& fnSurface, MMatrix& baseSurfaceMatrix,
	                            MFnNurbsCurve& fnCurve, 
	                            MMatrixArray& upMatrixArr,
								MPointArray& returnPointArr,
								MDoubleArray& returnParamArr );
	void getSurfaceMovePoints( MMatrix& baseSurfaceMatrix,
	                       MPointArray& localPoints,  MPointArray& localPivs,
						   MDoubleArray& paramList,
						   MMatrixArray& upMatrixList,
						   double minParam, double maxParam,
						   MPointArray& returnPoints );

	static  void*    creator();
	static  MStatus  initialize();

public:

	static  MObject  aBaseUpMatrix;
	static  MObject  aMoveUpMatrix;

	static  MObject  aBaseSurfaceMatrix;
	static  MObject  aBaseSurface;
	static  MObject  aBaseCurve;
	static  MObject  aMoveCurve;

	static  MObject  aScaleMatrix;

	static  MObject  aCurrentTime;

	static  MObject  aOutputSurface;

	static  MTypeId  id;

public:
	MPointArray   baseLocalPoints;
	MDoubleArray  baseParamRanges;
	MMatrixArray  baseUpMatrixArr;
	MMatrixArray  moveUpMatrixArr;

	bool requireUpdateSurface;
	bool requireUpdateCurve;
};

#endif