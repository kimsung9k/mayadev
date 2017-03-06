#include "sgMatrixFromVertices.h"

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>

#include <maya/MGlobal.h>


MTypeId     sgMatrixFromVertices::id( 0x2015052100 );

MObject     sgMatrixFromVertices::aInputMesh;        
MObject     sgMatrixFromVertices::aInputMeshMatrix;     
MObject     sgMatrixFromVertices::aVerticeId;
MObject     sgMatrixFromVertices::aOutputMatrix; 
MObject     sgMatrixFromVertices::aOutputTranslate; 
	MObject     sgMatrixFromVertices::aOutputTranslateX; 
	MObject     sgMatrixFromVertices::aOutputTranslateY; 
	MObject     sgMatrixFromVertices::aOutputTranslateZ; 

sgMatrixFromVertices::sgMatrixFromVertices()
{
	m_isDirtyMesh = true;
	m_isDirtyMeshMatrix = true;
	m_isDirtyInput = true;
}
sgMatrixFromVertices::~sgMatrixFromVertices()
{
}

MStatus sgMatrixFromVertices::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	MFnDependencyNode fnNode( thisMObject() );
	MPlug plugVerticeId = fnNode.findPlug( aVerticeId );
	int numElement = plugVerticeId.numElements();

	int lastIndex = plugVerticeId[ numElement - 1 ].logicalIndex();

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

	if( plug == aOutputMatrix )
	{
		MArrayDataHandle  hArrVerticesIds = data.inputArrayValue( aVerticeId, &status );
		MArrayDataHandle  hArrOutput = data.outputArrayValue( aOutputMatrix, &status );
		CHECK_MSTATUS_AND_RETURN_IT( status );
		MArrayDataBuilder builder( aOutputMatrix, numElement );

		MMatrix mtxOutput;
		int numPoints = m_pointsInputMesh.length();
		for( int i=0; i< hArrVerticesIds.elementCount(); i++, hArrVerticesIds.next() )
		{
			int logicalIndex = hArrVerticesIds.elementIndex();

			MDataHandle hVertexId = hArrVerticesIds.inputValue( &status );
			CHECK_MSTATUS_AND_RETURN_IT( status );
			MDataHandle hOutput = builder.addElement( logicalIndex );

			int idVertex = hVertexId.asInt();
			if( idVertex >= numPoints )
				hOutput.setMMatrix( MMatrix() );
			else
			{
				MPoint& point = m_pointsInputMesh[ idVertex ] * m_mtxMesh;
				double dArrMtx[4][4] = { 1,0,0,0,
										 0,1,0,0,
										 0,0,0,1,
										 point.x, point.y, point.z, 1 };
				MMatrix mtxOutput( dArrMtx );
				hOutput.setMMatrix( mtxOutput );
			}
		}
		hArrOutput.set( builder );
		hArrOutput.setAllClean();
	}
	else if( plug == aOutputTranslate )
	{
		MArrayDataHandle  hArrVerticesIds = data.inputArrayValue( aVerticeId, &status );
		MArrayDataHandle  hArrOutput = data.outputArrayValue( aOutputTranslate, &status );
		CHECK_MSTATUS_AND_RETURN_IT( status );
		MArrayDataBuilder builder( aOutputTranslate, numElement );

		MMatrix mtxOutput;
		int numPoints = m_pointsInputMesh.length();
		for( int i=0; i< hArrVerticesIds.elementCount(); i++, hArrVerticesIds.next() )
		{
			int logicalIndex = hArrVerticesIds.elementIndex();

			MDataHandle hVertexId = hArrVerticesIds.inputValue( &status );
			CHECK_MSTATUS_AND_RETURN_IT( status );
			MDataHandle hOutput = builder.addElement( logicalIndex );

			int idVertex = hVertexId.asInt();
			idVertex = ( idVertex == -1 ) ? 0 : idVertex;
			if( idVertex >= numPoints )
				hOutput.setMMatrix( MMatrix() );
			else
			{
				MPoint& point = m_pointsInputMesh[ idVertex ] * m_mtxMesh;
				double dArrMtx[4][4] = { 1,0,0,0,
										 0,1,0,0,
										 0,0,0,1,
										 point.x, point.y, point.z, 1 };
				MMatrix mtxOutput( dArrMtx );
				hOutput.setMVector( point );
			}
		}
		hArrOutput.set( builder );
		hArrOutput.setAllClean();
	}

	m_isDirtyMesh = false;
	m_isDirtyMeshMatrix = false;
	m_isDirtyInput = false;

	return MS::kSuccess;
}


void* sgMatrixFromVertices::creator()
{
	return new sgMatrixFromVertices();
}

MStatus sgMatrixFromVertices::initialize()	
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

	aVerticeId = nAttr.create( "verticeId", "verticeId", MFnNumericData::kInt, 0 );
	nAttr.setArray( true );
	nAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aVerticeId ) );

	aOutputMatrix = mAttr.create( "outputMatrix", "outputMatrix" );
	mAttr.setArray( true );
	mAttr.setUsesArrayDataBuilder( true );
	mAttr.setStorable( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOutputMatrix ) );

	aOutputTranslateX = nAttr.create( "outputTranslateX", "outputTranslateX", MFnNumericData::kDouble, 0.0 );
	aOutputTranslateY = nAttr.create( "outputTranslateY", "outputTranslateY", MFnNumericData::kDouble, 0.0 );
	aOutputTranslateZ = nAttr.create( "outputTranslateZ", "outputTranslateZ", MFnNumericData::kDouble, 0.0 );
	aOutputTranslate = nAttr.create( "outputTranslate", "outputTranslate", aOutputTranslateX, aOutputTranslateY, aOutputTranslateZ );
	nAttr.setArray( true );
	nAttr.setUsesArrayDataBuilder( true );
	nAttr.setStorable( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOutputTranslate ) );

	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputMesh, aOutputMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputMeshMatrix, aOutputMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aVerticeId, aOutputMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputMesh, aOutputTranslate ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputMeshMatrix, aOutputTranslate ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aVerticeId, aOutputTranslate ) );

	return MS::kSuccess;
}


MStatus  sgMatrixFromVertices::setDependentsDirty( const MPlug& plug, MPlugArray& plugArr )
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