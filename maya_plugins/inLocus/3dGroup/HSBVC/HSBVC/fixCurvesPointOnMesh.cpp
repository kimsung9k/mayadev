#include "fixCurvesPointOnMesh.h"
#include "fixCurvesPointOnMesh_def.h"
#include "fixCurvesPointOnMesh_threadDef.h"


MTypeId    fixCurvesPointOnMesh::id( 0xc8d303 );

MObject    fixCurvesPointOnMesh::aBaseMesh;

MObject    fixCurvesPointOnMesh::aConstStart;
MObject    fixCurvesPointOnMesh::aBlendArea;

MObject    fixCurvesPointOnMesh::aCheckStart;

MObject    fixCurvesPointOnMesh::aCurveInfo;
	MObject    fixCurvesPointOnMesh::aStartMatrix;
	MObject    fixCurvesPointOnMesh::aStartCV;
		MObject    fixCurvesPointOnMesh::aStartCVx;
		MObject    fixCurvesPointOnMesh::aStartCVy;
		MObject    fixCurvesPointOnMesh::aStartCVz;
	MObject    fixCurvesPointOnMesh::aPolygonIndex;
	MObject    fixCurvesPointOnMesh::aMoveCurve;

MObject    fixCurvesPointOnMesh::aRefresh;

MObject    fixCurvesPointOnMesh::aOutputCurve;


fixCurvesPointOnMesh::fixCurvesPointOnMesh() 
{
	MThreadPool::init();
	centerCrvKnots.setLength( 0 );
}
fixCurvesPointOnMesh::~fixCurvesPointOnMesh() 
{
	MThreadPool::release();
}

void* fixCurvesPointOnMesh::creator()
{
	return new fixCurvesPointOnMesh();
}

MStatus fixCurvesPointOnMesh::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;
	//cout << "---------------------------------------------------" << endl;
	MDataHandle   hBaseMesh = data.inputValue( aBaseMesh, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle   hConstStart= data.inputValue( aConstStart, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle   hBlendArea = data.inputValue( aBlendArea, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	
	//MDataHandle   hCheckStart= data.inputValue( aCheckStart, &status );
	//CHECK_MSTATUS_AND_RETURN_IT( status );
	
	MArrayDataHandle hArrCurveInfo = data.inputArrayValue( aCurveInfo, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MDataHandle hRefresh = data.inputValue( aRefresh, &status );

	//cout <<"handle seted" << endl;

	int numThread = 8;

	MFnMesh baseMesh = hBaseMesh.asMesh();
	
	//bool    checkStart = hCheckStart.asBool();

	int     infoLength = hArrCurveInfo.elementCount();

	taskData task;
	task.length        = infoLength;
	task.startPosition = hConstStart.asFloat();
	task.blendArea     = hBlendArea.asFloat();
	task.pDegrees            = new int[ infoLength ];
	task.pKnots              = new MDoubleArray[ infoLength ];
	task.pStartCurvePoints   = new MPointArray[ infoLength ];
	task.pVtxPoints          = new MPointArray[ infoLength ];
	task.pMovedCurvePoints   = new MPointArray[ infoLength ];
	task.pCurrentCurvePoints = new MPointArray[ infoLength ];

	//cout << "setTask" << endl;

	MPointArray startCurvePoints;
	MPointArray moveCurvePoints;

	MIntArray curveInfoIndies;
	curveInfoIndies.setLength( infoLength );

	//cout << "----before create tesk-----" << endl;
	//cout << "element count : " << infoLength << endl;
	status = curveInfoToTesk( hArrCurveInfo, &task, baseMesh, hRefresh.asBool(), curveInfoIndies );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	//cout << "----after create tesk-----" << endl;

	threadData* pThread = createThread( &task, numThread );
	//cout << "----before parallel compute-----" << endl;
	MThreadPool::newParallelRegion( parallelCompute, ( void* )pThread );
	//cout << "----after parallel compute-----" << endl;
	
	//MFnNurbsCurveData fnDataCreateCurve;
	//MObject createCurveObj = fnDataCreateCurve.create();

	MArrayDataHandle  hArrOutputCurve = data.outputArrayValue( aOutputCurve );
	MArrayDataBuilder bOutputCurve( aOutputCurve, infoLength, &status );

	MPointArray curvePointArr;
	//cout << "before create" << endl;

	for( int i=0; i<infoLength; i++ )
	{
		MFnNurbsCurve fnCreateCurve( task.pCurveObj[i], &status );
		//fnCreateCurve.create( task.pCurrentCurvePoints[i], task.pKnots[i], task.pDegrees[i], MFnNurbsCurve::kOpen, 0,0,createCurveObj, &status );
		CHECK_MSTATUS_AND_RETURN_IT( status );
		fnCreateCurve.setCVs( task.pCurrentCurvePoints[i] );
		MDataHandle hOutputCurve = bOutputCurve.addElement( curveInfoIndies[i] );
		hOutputCurve.set( task.pCurveObj[i] );
	}
	//cout << "after create" << endl;
	//cout << curveInfoIndies << endl;
	//cout << "infoLength : " << infoLength << endl;
	//cout << "create curve done" << endl;
	hArrOutputCurve.set( bOutputCurve );
	hArrOutputCurve.setAllClean();

	data.setClean( plug );

	delete []task.pCurveObj;

	return MS::kSuccess;
}