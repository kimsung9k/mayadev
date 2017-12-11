#include "sgSkinCluster.h"

MTypeId sgSkinCluster::id( 2015102000 );


MObject sgSkinCluster::aMatrix;
MObject sgSkinCluster::aBindPreMatrix;
MObject sgSkinCluster::aGeomMatrix;


sgSkinCluster::sgSkinCluster()
{
	m_fnThisNode.setObject( thisMObject() );
	m_plugMatrix = m_fnThisNode.findPlug( aMatrix );
	m_logicalLength = -1;
}

sgSkinCluster::~sgSkinCluster()
{
}


void* sgSkinCluster::creator()
{
	return new sgSkinCluster(); 
}



MStatus sgSkinCluster::deform( MDataBlock& data, MItGeometry& iter, const MMatrix& mat,
	            unsigned int mutiIndex )
{
	MStatus status;

	MDataHandle      hGeomMatrix = data.inputValue( aGeomMatrix );
	MArrayDataHandle hArrMatrix  = data.inputArrayValue( aMatrix );
	MArrayDataHandle hArrBindPre = data.inputArrayValue( aBindPreMatrix );

	MMatrix mtxGeom    = hGeomMatrix.asMatrix();
	MMatrix mtxInvGeom = mtxGeom.inverse();

	unsigned int numElements = m_plugMatrix.numElements();

	unsigned int logicalLength = m_plugMatrix[ numElements ].logicalIndex()+1;
	if( m_logicalLength != logicalLength )
	{
		m_mtxForMult.setLength( logicalLength );
		m_mtxMatrix.setLength( logicalLength );
		m_mtxBindPre.setLength( logicalLength );
		m_logicalLength = logicalLength;
	}
	for( int i=0; i< hArrMatrix.elementCount(); i++ )
	{
		unsigned int logicalMatrix = hArrMatrix.elementIndex();
		m_mtxMatrix[logicalMatrix] = hArrMatrix.inputValue().asMatrix();
	}
	for( int i=0; i< hArrBindPre.elementCount(); i++ )
	{
		unsigned int logicalMatrix = hArrBindPre.elementIndex();
		if( logicalMatrix >= numElements ) continue; 
		m_mtxBindPre[logicalMatrix] = hArrBindPre.inputValue().asMatrix();
	}

	for( int i=0; i< logicalLength; i++ )
	{
		m_mtxForMult[i] = mtxGeom * m_mtxBindPre[i] * m_mtxMatrix[i] * mtxInvGeom;
	}

	for( int i=0; i< iter.count(); i++ )
	{
		iter.position();
	}

	return MS::kSuccess;
}



MStatus sgSkinCluster::initialize()
{
	MStatus status;

	MFnCompoundAttribute cAttr;
	cAttr.setObject( weightList );
	cAttr.addChild( weights );

	MFnMatrixAttribute mAttr;

	aMatrix = mAttr.create( "matrix", "matrix" );
	mAttr.setArray( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aMatrix ) );

	aBindPreMatrix = mAttr.create( "bindPreMatrix", "bindPreMatrix" );
	mAttr.setArray( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aBindPreMatrix ) );

	aGeomMatrix = mAttr.create( "geomMatrix", "geomMatrix" );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aGeomMatrix ) );

	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aMatrix, outputGeom ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aBindPreMatrix, outputGeom ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aGeomMatrix, outputGeom ) );

	return MS::kSuccess;
}