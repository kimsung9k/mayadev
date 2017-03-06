#include "clusterControledCurve.h"
#include "clusterControledCurve_def.h"

MTypeId   clusterControledCurve::id( 0xc8d303 );

MObject   clusterControledCurve::aInputCurve;
MObject   clusterControledCurve::aInputCurveMatrix;

MObject   clusterControledCurve::aDumyMatrix;
MObject   clusterControledCurve::aBindPreMatrix;
MObject   clusterControledCurve::aMatrix;

MObject   clusterControledCurve::aWeightList;
	MObject   clusterControledCurve::aWeights;

MObject   clusterControledCurve::aUpdate;

MObject   clusterControledCurve::aOutputCurve;

clusterControledCurve::clusterControledCurve(){
	bindPreMatrix = new MMatrix[1];
	setWeights = new float*[1];
	setWeights[0] = new float[1];
	beforeNumCV = 1;
	requireUpdate = true;
}
clusterControledCurve::~clusterControledCurve(){}

void* clusterControledCurve::creator()
{
	return new clusterControledCurve();
}

MStatus   clusterControledCurve::compute( const MPlug& plug, MDataBlock& data )
{
	//MFnDependencyNode thisNode( thisMObject() );
	//cout << thisNode.name() << ", start" << endl;

	MStatus status;

	MDataHandle hInputCurve = data.inputValue( aInputCurve, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hInputCurveMatrix = data.inputValue( aInputCurveMatrix, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hOutputCurve = data.outputValue( aOutputCurve, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MArrayDataHandle hArrBindPreMatrix = data.inputArrayValue( aBindPreMatrix, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MArrayDataHandle hArrMatrix = data.inputArrayValue( aMatrix, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MArrayDataHandle hArrWeightList = data.inputArrayValue( aWeightList, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MDataHandle hUpdate = data.inputValue( aUpdate, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MObject oInputCurve = hInputCurve.asNurbsCurve();

	int bindPreMatrixLength = hArrBindPreMatrix.elementCount();
	int matrixLength = hArrMatrix.elementCount();

	MFnNurbsCurve fnInputCurve = oInputCurve;
	int numCVs = fnInputCurve.numCVs();
	int weightListLength = hArrWeightList.elementCount();

	if( weightListLength > 100 )
	{
		cout << "WeightList Count Error : " << weightListLength << endl;
		return MS::kFailure;
	}

	MPointArray inputCvPoints;
	MPointArray outputCvPoints;

	fnInputCurve.getCVs( inputCvPoints );
	outputCvPoints.setLength( numCVs );

	MMatrix matrix;
	MMatrix inputCurveMatrix = hInputCurveMatrix.asMatrix();
	MMatrix inputCurveMatrixInverse = inputCurveMatrix.inverse();

	if( requireUpdate )
	CHECK_MSTATUS_AND_RETURN_IT( updateBindPreMatrix( oInputCurve, inputCurveMatrixInverse,
				                                      hArrMatrix, hArrBindPreMatrix, hUpdate.asBool() ) );

	for( int i=0; i< numCVs; i++ )
	{
		inputCvPoints[i] *= inputCurveMatrix;
	}

	for( int i=0; i< numCVs; i++ )
	{
		outputCvPoints[i] = MPoint( 0,0,0 );
		double weight;

		for( int j=0; j< matrixLength; j++ )
		{
			weight = setWeights[i][j];

			hArrMatrix.jumpToElement( j );
			matrix = hArrMatrix.inputValue().asMatrix();
			outputCvPoints[i] += inputCvPoints[i]*bindPreMatrix[j]*matrix*weight;
		}
	}

	for( int i=0; i< numCVs; i++ )
	{
		outputCvPoints[i] *= inputCurveMatrixInverse;
	}

	MFnNurbsCurveData outputCurveData;
	MObject oOutputCurve = outputCurveData.create();

	fnInputCurve.copy( oInputCurve, oOutputCurve );

	MFnNurbsCurve fnOutputCurve( oOutputCurve, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	fnOutputCurve.setCVs( outputCvPoints );

	hOutputCurve.set( oOutputCurve );

	data.setClean( plug );

	//cout << thisNode.name() << ", end" << endl;

	return status;
}

MStatus  clusterControledCurve::initialize()
{
	MStatus  status;

	MFnNumericAttribute  nAttr;
	MFnMatrixAttribute   mAttr;
	MFnTypedAttribute    tAttr;
	MFnCompoundAttribute cAttr;

	aInputCurve = tAttr.create( "inputCurve", "inputCurve", MFnData::kNurbsCurve );
	tAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aInputCurve ) );

	aInputCurveMatrix = mAttr.create( "inputCurveMatrix", "inputCurveMatrix" );
	mAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aInputCurveMatrix ) );

	aDumyMatrix = mAttr.create( "dumyMatrix", "dumyMatrix" );
	mAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aDumyMatrix ) );

	aBindPreMatrix = mAttr.create( "bindPreMatrix", "bindPreMatrix" );
	mAttr.setStorable( true );
	mAttr.setArray( true );
	nAttr.setUsesArrayDataBuilder( true );
	CHECK_MSTATUS( addAttribute( aBindPreMatrix ) );

	aMatrix = mAttr.create( "matrix", "matrix" );
	mAttr.setStorable( true );
	mAttr.setArray( true );
	CHECK_MSTATUS( addAttribute( aMatrix ) );

	aWeightList = cAttr.create( "weightList", "weightList" );
	aWeights = nAttr.create( "weights", "weights", MFnNumericData::kFloat, 0.0 );
	nAttr.setArray( true );
	nAttr.setUsesArrayDataBuilder( true );
	cAttr.addChild( aWeights );
	cAttr.setArray( true );
	cAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aWeightList ) );

	aUpdate = nAttr.create( "update", "update", MFnNumericData::kBoolean, false );
	nAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aUpdate ) );

	aOutputCurve = tAttr.create( "outputCurve", "outputCurve", MFnData::kNurbsCurve );
	CHECK_MSTATUS( addAttribute( aOutputCurve ) );

	CHECK_MSTATUS( attributeAffects( aInputCurve, aOutputCurve ) );
	CHECK_MSTATUS( attributeAffects( aInputCurveMatrix, aOutputCurve ) );
	CHECK_MSTATUS( attributeAffects( aDumyMatrix, aOutputCurve ) );
	CHECK_MSTATUS( attributeAffects( aBindPreMatrix, aOutputCurve ) );
	CHECK_MSTATUS( attributeAffects( aMatrix, aOutputCurve ) );
	CHECK_MSTATUS( attributeAffects( aWeightList, aOutputCurve ) );
	CHECK_MSTATUS( attributeAffects( aUpdate, aOutputCurve ) );

	return MS::kSuccess;
}