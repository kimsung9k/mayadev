#ifndef _clusterControledSurface_h
#define _clusterControledSurface_h

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
#include  <maya/MFnNurbsSurfaceData.h>
#include  <maya/MFnNurbsSurface.h>

#include <maya/MMatrixArray.h>
#include <maya/MFnMatrixData.h>

#include <maya/MArrayDataBuilder.h>

#include <maya/MPointArray.h>
#include <maya/MItSurfaceCV.h>
#include <maya/MItCurveCV.h>

#include <maya/MDagPath.h>

#include <maya/MGlobal.h>

/*
#include <maya/MThreadPool.h>
#include <vector>

using namespace std;

struct TaskData
{
	MPointArray points;
	MDoubleArray paramPerPoints;
	MDoubleArray paramPerMatrix;
};

struct ThreadData
{
	unsigned int start;
	unsigned int end;
	unsigned int numTasks;
	TaskData*    pTaskData;
};/**/


class clusterControledSurface : public MPxNode
{
public:
						clusterControledSurface();
	virtual				~clusterControledSurface(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

	MStatus  updateBaseUpMatrix( MObject oInputOrigCurve, MMatrix& inputOrigCurveMatrix, MArrayDataHandle& hArrUpMatrix, MArrayDataHandle& hArrBaseUpMatrix, bool checkPoint  );
	MStatus  updateInputSurfaceInfo( MObject oInputOrigCurve, MObject oInputSurface, MMatrix mtxOrigCurve, MMatrix mtxSurface, bool checkPoint );

	MMatrix* getMatrixFromParameter( MObject* p_oCurve, MDoubleArray paramList );
	MStatus  moveSurfacePoints( MObject oOutputSurface, MObject oInputCurve, MMatrix mtxCurve, MMatrix mtxSurface, MArrayDataHandle& hArrUpMatrix );
	/*
	ThreadData*         createThreadData( int numTasks, TaskData* pTaskData );
    static void         createTasks( void* data, MThreadRootTask *pRoot );
    static MThreadRetVal threadCaculate( void* pParam );
	/**/

public:

	static  MObject     aInputOrigCurve;
	static  MObject     aInputOrigCurveMatrix;
	static  MObject     aInputCurve;
	static  MObject     aInputCurveMatrix;
	static  MObject     aInputSurface;
	static  MObject     aInputSurfaceMatrix;

	static  MObject     aBaseParameter;
	static  MObject     aBaseUpMatrix;
	static  MObject     aUpMatrix;

	static  MObject     aCheckPoint;

	static  MObject     aUpMatrixChangeAble;

	//static  MObject     aNumTasks;

	static  MObject		aOutputSurface;

	static	MTypeId		id;

public:
	MObject    inOrigCurve;
	MObject    inSurface;
	MPointArray  inPoints;
	MDoubleArray inParamPerPoints;
	MDoubleArray inParamPerMatrix;
	MMatrixArray inBaseUpMatrix;
	int numCVs;
	bool baseUpMatrixChanged;
	bool upMatrixChangeAble;
};

#endif
