#ifndef _fixCurvesPointOnMesh_h
#define _fixCurvesPointOnMesh_h

#include <maya/MPxNode.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnTypedAttribute.h>

#include <maya/MFnNurbsSurface.h>
#include <maya/MFnDependencyNode.h>

#include <maya/MTypeId.h> 

#include <maya/MIntArray.h>
#include <maya/MDoubleArray.h>
#include <maya/MPointArray.h>

#include <maya/MPlugArray.h>
#include <maya/MObject.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>

#include <maya/MMatrix.h>
#include <maya/MVector.h>

#include <maya/MFnMatrixData.h>

#include <maya/MObjectArray.h>
#include <maya/MFnMesh.h>
#include <maya/MFnNurbsCurve.h>
#include <maya/MFnNurbsCurveData.h>

#include <maya/MGlobal.h>

#include <maya/MThreadPool.h>


struct taskData
{
	int length;

	float startPosition;
	float blendArea;

	int         *pDegrees;
	MDoubleArray* pKnots;
	MPointArray* pStartCurvePoints;
	MPointArray* pVtxPoints;
	MPointArray* pMovedCurvePoints;

	MPointArray* pCurrentCurvePoints;

	MObject* pCurveObj;
};


struct  threadData
{
	int startNum;
	int endNum;
	int numThread;
	taskData* pTask;
};


class fixCurvesPointOnMesh : public MPxNode
{
public:
						fixCurvesPointOnMesh();
	virtual				~fixCurvesPointOnMesh(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

	MPointArray getVtxPoints( MFnMesh& fnMesh, int polygonIndex );
	MStatus     curveInfoToTesk( MArrayDataHandle& hArrCurveInfo, taskData* pTask, MFnMesh& fnMesh, bool refresh, MIntArray& curveInfoIndies );
	int         getClosestFaceIndex( MFnMesh& fnMesh, MPoint point );
	MMatrix     getMatrixByPolygonIndex( MFnMesh& fnMesh, int polygonIndex );
	MPointArray getCVPoints( MPointArray& movePoints, MMatrix& matrix );

	threadData*  createThread( taskData* pTask, int threadNum );
	static    void          parallelCompute( void* pData, MThreadRootTask* pRoot );
	static    MThreadRetVal threadCompute( void *pData );

public:
	static  MObject     aBaseMesh;

	static  MObject     aConstStart;
	static  MObject     aBlendArea;

	static  MObject     aCheckStart;

	static  MObject     aCurveInfo;
		static  MObject     aStartMatrix;
		static  MObject     aStartCV;
			static MObject     aStartCVx;
			static MObject     aStartCVy;
			static MObject     aStartCVz;
		static  MObject     aPolygonIndex;
		static  MObject     aMoveCurve;
	
	static  MObject     aRefresh;

	static  MObject     aOutputCurve;

	static	MTypeId		id;

public:
	int numCVsU, numCVsV;
	int degreeU, degreeV;
	int formU, formV;

	MDoubleArray centerCrvKnots;
};

#endif