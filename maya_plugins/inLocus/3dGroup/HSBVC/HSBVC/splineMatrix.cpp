#include "splineMatrix.h"
#include "splineMatrix_def.h"

MTypeId   splineMatrix::id( 0xc8d304 );

MObject   splineMatrix::aInputCurve;
MObject   splineMatrix::aInputCurveMatrix;
MObject   splineMatrix::aTopMatrix;
MObject   splineMatrix::aParameter;
MObject   splineMatrix::aAngleByTangent;

MObject   splineMatrix::aOutputMatrix;

splineMatrix::splineMatrix(){
	angleByTangent = false;
}
splineMatrix::~splineMatrix(){}


void* splineMatrix::creator()
{
	return new splineMatrix();
}


MStatus   splineMatrix::compute( const MPlug& plug, MDataBlock& data )
{
	//MFnDependencyNode thisNode( thisMObject() );
	//cout << thisNode.name() << ", start" << endl;

	MStatus status;

	MDataHandle hInputCurve = data.inputValue( aInputCurve, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hInputCurveMatrix = data.inputValue( aInputCurveMatrix, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MDataHandle hTopMatrix = data.inputValue( aTopMatrix, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MArrayDataHandle hArrParameter = data.inputArrayValue( aParameter, &status );

	MDataHandle hAngleByTangent = data.inputValue( aAngleByTangent, &status );
	angleByTangent = hAngleByTangent.asBool();
	
	MDataHandle hOutputMatrix = data.outputValue( aOutputMatrix, &status );

	MObject  oInputCurve = hInputCurve.asNurbsCurve();
	MMatrix  inputCurveMatrix = hInputCurveMatrix.asMatrix();
	MMatrix  topMatrix   = hTopMatrix.asMatrix();

	CHECK_MSTATUS( updateCurveInfo( oInputCurve ) );

	int parameterLength = hArrParameter.elementCount();

	double* paramList = new double[parameterLength+1];

	for( int i=0; i<parameterLength; i++ )
	{
		double inputParamValue = hArrParameter.inputValue().asDouble();
		
		inputParamValue = ( inputParamValue < 0 ) ? 0.0 : inputParamValue;
		inputParamValue = ( inputParamValue > 0.999 ) ? 0.999 : inputParamValue;
		
		paramList[i] = inputParamValue;
		hArrParameter.next();
	}
	paramList[parameterLength] = 1.0;

	MMatrix* matrixPtr = getMatrixArrayFromParamList( topMatrix, paramList, inputCurveMatrix, &oInputCurve, parameterLength );

	MArrayDataHandle hArrOutputMatrix = data.outputArrayValue( aOutputMatrix );
	MArrayDataBuilder bArrOutputMatrix( aOutputMatrix, parameterLength );

	for( int i=0; i<parameterLength; i++ )
	{
		MDataHandle hOutputMatrix = bArrOutputMatrix.addElement( i );
		hOutputMatrix.set( matrixPtr[i] );
	}

	hArrOutputMatrix.set( bArrOutputMatrix );
	hArrOutputMatrix.setAllClean();

	data.setClean( plug );

	delete []matrixPtr;
	delete []paramList;

	//cout << thisNode.name() << ", end" << endl;

	return MS::kSuccess;
}