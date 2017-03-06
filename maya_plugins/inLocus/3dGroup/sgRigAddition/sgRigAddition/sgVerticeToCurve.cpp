#include "sgVerticeToCurve.h"

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>

#include <maya/MGlobal.h>

#define  PI  3.14159265359


MTypeId     sgVerticeToCurve::id( 0x2015042900 );

MObject     sgVerticeToCurve::aInputMesh;        
MObject     sgVerticeToCurve::aInputMeshMatrix;     
MObject     sgVerticeToCurve::aInput;
	MObject     sgVerticeToCurve::aDegree;
	MObject     sgVerticeToCurve::aVerticeIds;
	MObject     sgVerticeToCurve::aParentInverseMatrix;
MObject     sgVerticeToCurve::aOutputCurve; 

sgVerticeToCurve::sgVerticeToCurve()
{
	m_isDirtyMesh = true;
	m_isDirtyMeshMatrix = true;
	m_isDirtyInput = true;
}
sgVerticeToCurve::~sgVerticeToCurve()
{
}

MStatus sgVerticeToCurve::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	MFnDependencyNode fnNode( thisMObject() );
	MPlug plugInput = fnNode.findPlug( aInput );
	int numElement = plugInput.numElements();

	int lastIndex = plugInput[ numElement - 1 ].logicalIndex();

	m_verticeIdsArray.setLength( lastIndex+1 );
	m_mtxArrParentInverse.setLength( lastIndex+1 );
	m_oArrOutputCurve.setLength( lastIndex+1 );

	if( m_isDirtyMesh )
	{
		//cout << "dirty mesh" << endl;
		MDataHandle hInputMesh = data.inputValue( aInputMesh, &status );
		CHECK_MSTATUS_AND_RETURN_IT( status );
		m_oMesh = hInputMesh.asMesh();

		if( m_oMesh.isNull() ) return MS::kFailure;
		MFnMesh fnMesh = m_oMesh;
		fnMesh.getPoints( m_pointsInputMesh );
		m_numPolygon = fnMesh.numPolygons();
	}

	if( m_isDirtyMeshMatrix )
	{
		//cout << "dirty matrix" << endl;
		MDataHandle hInputMeshMatrix = data.inputValue( aInputMeshMatrix, &status );
		CHECK_MSTATUS_AND_RETURN_IT( status );
		m_mtxMesh = hInputMeshMatrix.asMatrix();
	}

	MFnNurbsCurve fnCurveCreate;
	MFnNurbsCurveData curveData;

	MArrayDataHandle hArrInput = data.inputArrayValue( aInput, &status );
	MArrayDataHandle  hArrOutput = data.outputArrayValue( aOutputCurve, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MArrayDataBuilder builder( aOutputCurve, numElement );

	for( int i=0; i< hArrInput.elementCount(); i++, hArrInput.next() )
	{
		int logicalIndex = hArrInput.elementIndex();

		MDataHandle hInput = hArrInput.inputValue( &status );
		CHECK_MSTATUS_AND_RETURN_IT( status );

		MDataHandle hParentInvesreMatrix = hInput.child( aParentInverseMatrix );
		MDataHandle hDegree = hInput.child( aDegree );
		MArrayDataHandle hArrVerticeIds = hInput.child( aVerticeIds );

		m_verticeIdsArray[logicalIndex].setLength( hArrVerticeIds.elementCount() );

		for( int j=0; j< hArrVerticeIds.elementCount(); j++, hArrVerticeIds.next() )
		{
			MDataHandle hVerticeId = hArrVerticeIds.inputValue( &status );
			CHECK_MSTATUS_AND_RETURN_IT( status );
			m_verticeIdsArray[logicalIndex][j] = hVerticeId.asInt();
		}

		MDoubleArray knots;
		MPointArray pointArr;
		MIntArray& verticeIds = m_verticeIdsArray[logicalIndex];

		if( !verticeIds.length() ) continue;

		m_oArrOutputCurve[logicalIndex] = curveData.create( &status );
		CHECK_MSTATUS_AND_RETURN_IT( status );

		pointArr.setLength( verticeIds.length() );
		knots.setLength( verticeIds.length() + 2 );
		unsigned int length = verticeIds.length();

		for( int j=0; j< verticeIds.length(); j++ )
		{
			pointArr[j] = m_pointsInputMesh[ verticeIds[j] ];
		}

		MPlug plugPim = plugInput[i].child( aParentInverseMatrix );
		
		MFnMatrixData mtxData( plugPim.asMObject() );
		MMatrix mtxMult = m_mtxMesh * mtxData.matrix();

		pointArr.setLength( verticeIds.length() );
		for( int j=0; j< verticeIds.length(); j++ )
		{
			pointArr[j] = m_pointsInputMesh[ verticeIds[j] ] * mtxMult;
			//printf( "point[ %04d ]: %5.2f, %5.2f, %5.2f\n", verticeIds[j], pointArr[j].x, pointArr[j].y, pointArr[j].z ); 
		}
		fnCurveCreate.createWithEditPoints( pointArr, 3, MFnNurbsCurve::kOpen, false, false, false, m_oArrOutputCurve[logicalIndex] );
		fnCurveCreate.setObject( m_oArrOutputCurve[logicalIndex] );
		//cout << "vertice id length : " << verticeIds.length() << endl;
		//cout << "num cv : " << fnCurveModify.numCVs() << endl;

		MDataHandle hOutput = builder.addElement( logicalIndex );
		hOutput.setMObject( m_oArrOutputCurve[ logicalIndex ] );
	}

	hArrOutput.set( builder );
	hArrOutput.setAllClean();

	m_isDirtyMesh = false;
	m_isDirtyMeshMatrix = false;
	m_isDirtyInput = false;
	
	for( int i=0; i< m_inputIsDirty.length(); i++ )
	{
		m_inputIsDirty[i] = 0;
	}

	return MS::kSuccess;
}

void* sgVerticeToCurve::creator()
{
	return new sgVerticeToCurve();
}

MStatus sgVerticeToCurve::initialize()	
{
	MStatus status;

	MFnTypedAttribute   tAttr;
	MFnMatrixAttribute  mAttr;
	MFnNumericAttribute nAttr;
	MFnCompoundAttribute cAttr;
	MFnEnumAttribute eAttr;

	aInputMesh = tAttr.create( "inputMesh", "inputMesh", MFnData::kMesh );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputMesh ) );

	aInputMeshMatrix = mAttr.create( "inputMeshMatrix", "inputMeshMatrix" );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputMeshMatrix ) );

	aInput = cAttr.create( "input", "input" );

	aDegree = eAttr.create( "degree", "degree" );
	eAttr.addField( "1", 0 );
	eAttr.addField( "2", 1 );
	eAttr.addField( "3", 2 );
	eAttr.addField( "5", 3 );
	eAttr.addField( "7", 4 );
	eAttr.setDefault( 2 );
	aVerticeIds = nAttr.create( "verticeIds", "verticeIds", MFnNumericData::kInt, 0 );
	nAttr.setArray( true );
	aParentInverseMatrix = mAttr.create( "parentInverseMatrix", "pim" );

	cAttr.addChild( aDegree );
	cAttr.addChild( aVerticeIds );
	cAttr.addChild( aParentInverseMatrix );

	cAttr.setArray( true );
	cAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInput ) );

	aOutputCurve = tAttr.create( "outputCurve", "outputCurve", MFnData::kNurbsCurve );
	tAttr.setArray( true );
	tAttr.setUsesArrayDataBuilder( true );
	tAttr.setStorable( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOutputCurve ) );

	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputMesh, aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputMeshMatrix, aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aParentInverseMatrix, aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInput, aOutputCurve ) );

	return MS::kSuccess;
}


MStatus  sgVerticeToCurve::setDependentsDirty( const MPlug& plug, MPlugArray& plugArr )
{
	MStatus status;

	if( plug == aInputMesh )
	{
		m_isDirtyMesh = true;
	}
	else if( plug == aInputMeshMatrix )
	{
		m_isDirtyMeshMatrix = true;
	}

	return MS::kSuccess;
}