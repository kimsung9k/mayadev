#ifndef _volumeCurvesOnSurface_h
#define _volumeCurvesOnSurface_h

#include <maya/MPxNode.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnNurbsSurface.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MTypeId.h> 

#include <maya/MString.h>

#include <maya/MDoubleArray.h>
#include <maya/MPointArray.h>
#include <maya/MStringArray.h>
#include <maya/MGlobal.h>
#include <maya/MSelectionList.h>

#include <maya/MPlugArray.h>
#include <maya/MObject.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MFnDependencyNode.h>

#include <maya/MArrayDataBuilder.h>

#include <maya/MPointArray.h>
#include <maya/MBoundingBox.h>

#include <maya/MMatrix.h>

#include <maya/MFnMesh.h>
#include <maya/MItMeshPolygon.h>
#include <maya/MItMeshVertex.h>
#include <maya/MDagPath.h>
#include <maya/MFnNurbsCurve.h>
#include <maya/MFnNurbsCurveData.h>
#include <maya/MFnNurbsSurfaceData.h>

#include <maya/MMeshIntersector.h>

#include <maya/MGlobal.h>

//#include <maya/MThreadPool.h>

/*
struct  pointTaskData
{
	MPointArray  allPointArr;
	MDoubleArray centerParamArr;
	MDoubleArray paramUArr;
	MDoubleArray paramVArr;
	MDoubleArray centerRateArr;
	MFnNurbsSurface* pFnSurface[4];
	MFnNurbsCurve*   pFnCurve[4];
	MMatrix      matrix;
};

struct  pointThreadData
{
	int startNum;
	int endNum;
	int numThread;
	int threadNum;
	pointTaskData* pointTaskPtr;
};/**/
 
class volumeCurvesOnSurface : public MPxNode
{
public:
						volumeCurvesOnSurface();
	virtual				~volumeCurvesOnSurface(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();
	
	MDoubleArray buildKnots( int pointLength, int degree );
	MStatus     getSurfaceInfo( MFnNurbsSurface& fnSurface, MStatus &status );
	MFnNurbsCurve&  getCenterCurve( MFnNurbsSurface& fnSurface, MStatus& status );
	void     getCenterCurvePoints( MFnNurbsSurface& fnSurface, MPointArray& centerPoints, MStatus& status );

public:

	static  MObject     aInputSurface;
	static  MObject     aInputMatrix;
	static  MObject     aDirection;

	static  MObject     aByUV;
	
	static  MObject     aNumOfSample;

	static  MObject     aCutting;
		static  MObject     aCutAble;
		static  MObject     aInputMesh;
		static  MObject     aMeshMatrix;
		static  MObject     aConstStart;
		static  MObject     aConstEnd;
		static  MObject     aRefresh;

	static  MObject     aCurveInfo;
		static  MObject     aParamRate;
		static  MObject     aCenterRate;
		static  MObject		aStartEP;
			static MObject     aStartEPx;
			static MObject     aStartEPy;
			static MObject     aStartEPz;
		static  MObject     aStartIndex;
		static  MObject     aPolygonIndex;
		static  MObject     aUValue;
		static  MObject     aVValue;
		static  MObject     aCutParam;

	static  MObject		aOutputCurve;

	static	MTypeId		id;

public:
	int degreeU, degreeV;
	int formU, formV;
	int numCVsU, numCVsV;
	int numSpansU, numSpansV;
	double minRangeU, maxRangeU;
	double minRangeV, maxRangeV;
	MDoubleArray centerCrvKnots;

	bool byUV;

	MFnMesh* pFnMesh;
};

#endif
